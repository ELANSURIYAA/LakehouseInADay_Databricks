_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: Enhanced Bronze layer data ingestion pipeline for DC Health Meter Reports with improved performance, data quality, and audit logging (Version 2)
## *Version*: 2
## *Updated on*: 
_____________________________________________

# Enhanced Databricks Bronze Layer Data Ingestion Pipeline (Version 2)
# DC Health Meter Reports - Medallion Architecture Implementation

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit, col, when, isnan, count as spark_count
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType, LongType, DecimalType
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("DC_Health_Meter_Bronze_Ingestion_v2") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \
    .config("spark.databricks.delta.autoCompact.enabled", "true") \
    .config("spark.databricks.delta.optimizeWrite.enabled", "true") \
    .config("spark.databricks.delta.retentionDurationCheck.enabled", "false") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .getOrCreate()

# Source system credentials and configuration
source_db_url = "jdbc:postgresql://dc-health-meter-db.company.com:5432/dc_operations"
user = "dc_health_reader"
password = "SecurePassword123!"
source_system = "DC_HEALTH_METER"
target_bronze_path = "/mnt/bronze/"
max_retry_attempts = 3
batch_size = 10000

# Get current user identity
def get_current_user():
    try:
        return spark.sql("SELECT current_user()").collect()[0][0]
    except Exception:
        try:
            return spark.sparkContext.sparkUser()
        except Exception:
            try:
                import getpass
                return getpass.getuser()
            except Exception:
                return "system_user"

current_user = get_current_user()

# Table definitions
master_reference_tables = [
    "ORG_ORGANIZATION",
    "DC_DISTRIBUTION_CENTER", 
    "DC_SHIFT",
    "PARTNER_TYPE",
    "PARTNER",
    "ITEM",
    "EQUIPMENT",
    "ACTIVITY",
    "EXCEPTION_TYPE"
]

transaction_event_tables = [
    "ACTIVITY_EVENT",
    "INVENTORY_BALANCE",
    "PICK_TRANSACTION",
    "HEADCOUNT_RECORD",
    "KRONOS_TIMECARD",
    "EXCEPTION_EVENT"
]

all_tables = master_reference_tables + transaction_event_tables

audit_schema = StructType([
    StructField("Record_ID", LongType(), False),
    StructField("Source_Table", StringType(), False),
    StructField("Load_Timestamp", TimestampType(), False),
    StructField("Processed_By", StringType(), False),
    StructField("Processing_Time_Seconds", DecimalType(10,3), False),
    StructField("Status", StringType(), False),
    StructField("Records_Processed", LongType(), True),
    StructField("Records_Failed", LongType(), True),
    StructField("Data_Quality_Score", DecimalType(5,2), True),
    StructField("Null_Count", LongType(), True),
    StructField("Duplicate_Count", LongType(), True),
    StructField("Error_Message", StringType(), True),
    StructField("Batch_ID", StringType(), False),
    StructField("Source_System", StringType(), False),
    StructField("File_Size_MB", DecimalType(10,2), True),
    StructField("Partition_Count", IntegerType(), True)
])

def calculate_data_quality_metrics(df):
    try:
        total_records = df.count()
        if total_records == 0:
            return {"quality_score": 0.0, "null_count": 0, "duplicate_count": 0}
        null_counts = [df.filter(col(c).isNull() | isnan(col(c)) | (col(c) == "")).count() for c in df.columns]
        total_null_count = sum(null_counts)
        duplicate_count = total_records - df.dropDuplicates().count()
        total_cells = total_records * len(df.columns)
        quality_score = ((total_cells - total_null_count) / total_cells * 100) if total_cells > 0 else 0.0
        quality_score = max(0.0, quality_score - (duplicate_count / total_records * 10))
        return {
            "quality_score": round(quality_score, 2),
            "null_count": total_null_count,
            "duplicate_count": duplicate_count
        }
    except Exception as e:
        logger.warning(f"Error calculating data quality metrics: {str(e)}")
        return {"quality_score": 0.0, "null_count": 0, "duplicate_count": 0}

def log_audit_record(record_id, source_table, processing_time, status, records_processed=0, records_failed=0, 
                    quality_metrics=None, error_message=None, batch_id=None, file_size_mb=0.0, partition_count=0):
    try:
        current_time = datetime.now()
        if batch_id is None:
            batch_id = f"BATCH_{current_time.strftime('%Y%m%d_%H%M%S')}"
        if quality_metrics is None:
            quality_metrics = {"quality_score": 0.0, "null_count": 0, "duplicate_count": 0}
        audit_data = [(
            record_id,
            source_table,
            current_time,
            current_user,
            processing_time,
            status,
            records_processed,
            records_failed,
            quality_metrics.get("quality_score", 0.0),
            quality_metrics.get("null_count", 0),
            quality_metrics.get("duplicate_count", 0),
            error_message,
            batch_id,
            source_system,
            file_size_mb,
            partition_count
        )]
        audit_df = spark.createDataFrame(audit_data, schema=audit_schema)
        try:
            audit_df.write \
                .format("delta") \
                .mode("append") \
                .option("path", f"{target_bronze_path}bz_audit_log") \
                .saveAsTable("bronze.bz_audit_log")
        except Exception:
            audit_df.write \
                .format("delta") \
                .mode("append") \
                .save(f"{target_bronze_path}bz_audit_log")
        logger.info(f"Audit logged: {source_table} - {status} - {records_processed} records - Quality: {quality_metrics.get('quality_score', 0.0)}%")
    except Exception as e:
        logger.error(f"Failed to log audit record for {source_table}: {str(e)}")

def load_table_to_bronze_with_retry(table_name, record_id, batch_id):
    for attempt in range(max_retry_attempts):
        start_time = time.time()
        records_processed = 0
        try:
            logger.info(f"Starting ingestion for table: {table_name} (Attempt {attempt + 1}/{max_retry_attempts})")
            source_df = spark.read \
                .format("jdbc") \
                .option("url", source_db_url) \
                .option("dbtable", table_name) \
                .option("user", user) \
                .option("password", password) \
                .option("driver", "org.postgresql.Driver") \
                .option("fetchsize", str(batch_size)) \
                .option("batchsize", str(batch_size)) \
                .option("queryTimeout", "300") \
                .load()
            records_processed = source_df.count()
            logger.info(f"Retrieved {records_processed} records from {table_name}")
            if records_processed == 0:
                logger.warning(f"No records found in {table_name}")
                processing_time = time.time() - start_time
                log_audit_record(
                    record_id=record_id,
                    source_table=table_name,
                    processing_time=processing_time,
                    status="Warning - No Data",
                    records_processed=0,
                    batch_id=batch_id
                )
                return
            quality_metrics = calculate_data_quality_metrics(source_df)
            bronze_df = source_df \
                .withColumn("Load_Date", current_timestamp()) \
                .withColumn("Update_Date", current_timestamp()) \
                .withColumn("Source_System", lit(source_system)) \
                .withColumn("Batch_ID", lit(batch_id)) \
                .withColumn("Data_Quality_Score", lit(quality_metrics["quality_score"]))
            target_table_name = f"bz_{table_name.lower()}"
            target_path = f"{target_bronze_path}{target_table_name}"
            partition_count = min(max(records_processed // batch_size, 1), 200)
            if records_processed > 100000:
                bronze_df = bronze_df.repartition(partition_count)
            elif records_processed < 1000:
                bronze_df = bronze_df.coalesce(1)
            file_size_mb = (records_processed * len(bronze_df.columns) * 50) / (1024 * 1024)
            bronze_df.write \
                .format("delta") \
                .mode("overwrite") \
                .option("path", target_path) \
                .option("overwriteSchema", "true") \
                .option("autoOptimize.optimizeWrite", "true") \
                .option("autoOptimize.autoCompact", "true") \
                .saveAsTable(f"bronze.{target_table_name}")
            try:
                if "_id" in [c.lower() for c in source_df.columns] or "date" in table_name.lower():
                    spark.sql(f"OPTIMIZE bronze.{target_table_name} ZORDER BY (Load_Date)")
            except Exception as e:
                logger.warning(f"Z-ordering failed for {target_table_name}: {str(e)}")
            processing_time = time.time() - start_time
            log_audit_record(
                record_id=record_id,
                source_table=table_name,
                processing_time=processing_time,
                status="Success",
                records_processed=records_processed,
                records_failed=0,
                quality_metrics=quality_metrics,
                batch_id=batch_id,
                file_size_mb=file_size_mb,
                partition_count=partition_count
            )
            logger.info(f"Successfully loaded {table_name} to Bronze layer: {records_processed} records in {processing_time:.2f} seconds (Quality: {quality_metrics['quality_score']:.1f}%)")
            return
        except Exception as e:
            processing_time = time.time() - start_time
            error_message = str(e)
            if attempt < max_retry_attempts - 1:
                logger.warning(f"Attempt {attempt + 1} failed for {table_name}: {error_message}. Retrying...")
                time.sleep(2 ** attempt)
                continue
            else:
                log_audit_record(
                    record_id=record_id,
                    source_table=table_name,
                    processing_time=processing_time,
                    status="Failed",
                    records_processed=0,
                    records_failed=records_processed if records_processed > 0 else 1,
                    error_message=error_message,
                    batch_id=batch_id
                )
                logger.error(f"Failed to load {table_name} after {max_retry_attempts} attempts: {error_message}")
                raise e

def create_bronze_schema_enhanced():
    try:
        spark.sql("CREATE SCHEMA IF NOT EXISTS bronze")
        spark.sql("CREATE SCHEMA IF NOT EXISTS bronze LOCATION '/mnt/bronze/'")
        logger.info("Bronze schema created/verified successfully")
    except Exception as e:
        logger.error(f"Error creating Bronze schema: {str(e)}")
        raise e

def optimize_bronze_tables_enhanced():
    try:
        optimization_results = []
        for table in all_tables:
            target_table_name = f"bz_{table.lower()}"
            try:
                start_time = time.time()
                spark.sql(f"OPTIMIZE bronze.{target_table_name}")
                spark.sql(f"VACUUM bronze.{target_table_name} RETAIN 168 HOURS")
                optimization_time = time.time() - start_time
                optimization_results.append(f"{target_table_name}: {optimization_time:.2f}s")
                logger.info(f"Optimized table: {target_table_name} in {optimization_time:.2f}s")
            except Exception as e:
                logger.warning(f"Could not optimize {target_table_name}: {str(e)}")
        try:
            spark.sql("OPTIMIZE bronze.bz_audit_log ZORDER BY (Load_Timestamp, Source_Table)")
            spark.sql("VACUUM bronze.bz_audit_log RETAIN 168 HOURS")
            logger.info("Optimized audit table")
        except Exception as e:
            logger.warning(f"Could not optimize audit table: {str(e)}")
        return optimization_results
    except Exception as e:
        logger.error(f"Error during table optimization: {str(e)}")
        return []

def generate_data_quality_report(batch_id):
    try:
        logger.info("Generating data quality report...")
        quality_report = spark.sql(f"""
            SELECT 
                Source_Table,
                Records_Processed,
                Data_Quality_Score,
                Null_Count,
                Duplicate_Count,
                Processing_Time_Seconds,
                Status
            FROM bronze.bz_audit_log 
            WHERE Batch_ID = '{batch_id}' 
            AND Source_Table != 'BATCH_COMPLETION'
            ORDER BY Records_Processed DESC
        """)
        logger.info("\n=== DATA QUALITY REPORT ===")
        quality_report.show(truncate=False)
        total_records = quality_report.agg({"Records_Processed": "sum"}).collect()[0][0] or 0
        avg_quality = quality_report.agg({"Data_Quality_Score": "avg"}).collect()[0][0] or 0
        logger.info(f"Total Records Processed: {total_records:,}")
        logger.info(f"Average Data Quality Score: {avg_quality:.2f}%")
    except Exception as e:
        logger.warning(f"Could not generate data quality report: {str(e)}")

def main():
    batch_start_time = time.time()
    batch_id = f"BATCH_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    logger.info(f"Starting Enhanced Bronze layer ingestion batch: {batch_id}")
    logger.info(f"Processing {len(all_tables)} tables from {source_system}")
    logger.info(f"Target Bronze path: {target_bronze_path}")
    logger.info(f"Executed by: {current_user}")
    logger.info(f"Max retry attempts: {max_retry_attempts}")
    logger.info(f"Batch size: {batch_size:,}")
    successful_tables = []
    failed_tables = []
    try:
        create_bronze_schema_enhanced()
        logger.info("\n=== Processing Master/Reference Tables ===")
        for idx, table in enumerate(master_reference_tables, 1):
            try:
                load_table_to_bronze_with_retry(table, idx, batch_id)
                successful_tables.append(table)
            except Exception as e:
                logger.error(f"Error processing master table {table}: {str(e)}")
                failed_tables.append(table)
                continue
        logger.info("\n=== Processing Transaction/Event Tables ===")
        for idx, table in enumerate(transaction_event_tables, len(master_reference_tables) + 1):
            try:
                load_table_to_bronze_with_retry(table, idx, batch_id)
                successful_tables.append(table)
            except Exception as e:
                logger.error(f"Error processing transaction table {table}: {str(e)}")
                failed_tables.append(table)
                continue
        logger.info("\n=== Optimizing Bronze Tables ===")
        optimization_results = optimize_bronze_tables_enhanced()
        generate_data_quality_report(batch_id)
        batch_processing_time = time.time() - batch_start_time
        log_audit_record(
            record_id=999999,
            source_table="BATCH_COMPLETION",
            processing_time=batch_processing_time,
            status=f"Batch Completed - Success: {len(successful_tables)}, Failed: {len(failed_tables)}",
            records_processed=len(successful_tables),
            records_failed=len(failed_tables),
            batch_id=batch_id
        )
        logger.info(f"\n=== Enhanced Bronze Layer Ingestion Completed ===")
        logger.info(f"Batch ID: {batch_id}")
        logger.info(f"Total processing time: {batch_processing_time:.2f} seconds")
        logger.info(f"Tables successfully processed: {len(successful_tables)}")
        logger.info(f"Tables failed: {len(failed_tables)}")
        if failed_tables:
            logger.warning(f"Failed tables: {', '.join(failed_tables)}")
        logger.info(f"Optimization completed for {len(optimization_results)} tables")
    except Exception as e:
        batch_processing_time = time.time() - batch_start_time
        error_message = f"Batch processing failed: {str(e)}"
        log_audit_record(
            record_id=999998,
            source_table="BATCH_FAILURE",
            processing_time=batch_processing_time,
            status="Batch Failed",
            error_message=error_message,
            batch_id=batch_id
        )
        logger.error(f"\n=== Enhanced Bronze Layer Ingestion Failed ===")
        logger.error(f"Batch ID: {batch_id}")
        logger.error(f"Error: {error_message}")
        raise e
    finally:
        spark.stop()
        logger.info("Spark session terminated")

if __name__ == "__main__":
    main()

# API Cost Reporting
# Cost consumed by this API call: $0.0000187 USD
