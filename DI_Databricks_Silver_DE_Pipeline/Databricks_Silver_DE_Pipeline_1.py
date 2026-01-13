_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: PySpark pipeline for cleansing, validating, and standardizing Bronze layer data into the Silver layer for DC Health Meter Reports
## *Version*: 1
## *Updated on*: 
_____________________________________________

# Databricks Silver DE Pipeline - DC Health Meter Reports

"""
This PySpark pipeline reads raw data from the Bronze layer, applies data cleansing, validation, and standardization, and writes the processed data to the Silver layer in Delta Lake format. It enforces schema, deduplication, null handling, business rule validation, and redirects invalid records to an error table with detailed logs. The pipeline is optimized for analytical processing and auditability.
"""

# 1. Initialize Spark Session with Delta Configurations
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_timestamp, monotonically_increasing_id
from pyspark.sql.types import *
import logging

spark = SparkSession.builder \
    .appName("SilverLayerPipeline") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# 2. Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SilverLayerPipeline")

# 3. Define Schema for Silver Layer (example for bz_activity_event)
silver_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("dc_id", StringType(), False),
    StructField("event_ts_utc", TimestampType(), False),
    StructField("shift_id", StringType(), True),
    StructField("partner_id", StringType(), True),
    StructField("activity_id", StringType(), True),
    StructField("item_id", StringType(), True),
    StructField("equipment_id", StringType(), True),
    StructField("source_system", StringType(), True),
    StructField("source_event_id", StringType(), True),
    StructField("location_code", StringType(), True),
    StructField("qty_handled", DecimalType(18,4), True),
    StructField("duration_seconds", DecimalType(18,4), True),
    StructField("labor_seconds", DecimalType(18,4), True),
    StructField("units_per_hour", DecimalType(18,4), True),
    StructField("created_ts", TimestampType(), True),
    StructField("updated_ts", TimestampType(), True),
    StructField("load_timestamp", TimestampType(), True),
    StructField("update_timestamp", TimestampType(), True),
    StructField("source_system_meta", StringType(), True)
])

# 4. Read Data from Bronze Layer
bronze_path = "/mnt/bronze/bz_activity_event"
df_bronze = spark.read.format("delta").load(bronze_path)

# 5. Data Cleansing and Validation Functions
from typing import List, Tuple

def remove_duplicates(df):
    return df.dropDuplicates()

def enforce_schema(df, schema):
    return spark.createDataFrame(df.rdd, schema)

def handle_nulls(df):
    # Example: Fill nulls for numeric columns with 0, string columns with 'UNKNOWN'
    fill_dict = {col.name: 0 for col in df.schema.fields if isinstance(col.dataType, DecimalType)}
    fill_dict.update({col.name: 'UNKNOWN' for col in df.schema.fields if isinstance(col.dataType, StringType)})
    return df.fillna(fill_dict)

def validate_business_rules(df) -> Tuple['DataFrame', 'DataFrame']:
    # Example: event_ts_utc must not be null and qty_handled >= 0
    valid = df.filter((col("event_ts_utc").isNotNull()) & (col("qty_handled") >= 0))
    invalid = df.subtract(valid)
    invalid = invalid.withColumn("error_description", lit("event_ts_utc is null or qty_handled < 0"))
    return valid, invalid

# 6. Apply Cleansing and Validation
logger.info("Removing duplicates...")
df_clean = remove_duplicates(df_bronze)
logger.info("Enforcing schema...")
df_clean = enforce_schema(df_clean, silver_schema)
logger.info("Handling nulls...")
df_clean = handle_nulls(df_clean)
logger.info("Applying business rule validation...")
df_valid, df_invalid = validate_business_rules(df_clean)

# 7. Add Audit Columns
load_date = current_timestamp()
df_valid = df_valid.withColumn("load_date", load_date).withColumn("update_date", load_date)
df_invalid = df_invalid.withColumn("load_date", load_date).withColumn("update_date", load_date)

# 8. Write Valid Data to Silver Layer (Delta Lake, partitioned by dc_id)
silver_path = "/mnt/silver/sv_activity_event"
df_valid.write.format("delta").mode("overwrite").partitionBy("dc_id").save(silver_path)
logger.info(f"Written valid records to Silver layer at {silver_path}")

# 9. Write Invalid Data to Error Table (with error metadata)
error_schema = StructType([
    StructField("error_id", LongType(), False),
    StructField("table_name", StringType(), False),
    StructField("error_description", StringType(), False),
    StructField("load_date", TimestampType(), False),
    StructField("update_date", TimestampType(), False),
    StructField("error_timestamp", TimestampType(), False),
    StructField("source_system", StringType(), False)
])

def add_error_metadata(df, table_name):
    return df.withColumn("error_id", monotonically_increasing_id()) \
             .withColumn("table_name", lit(table_name)) \
             .withColumn("error_timestamp", current_timestamp()) \
             .withColumn("source_system", lit("bronze"))

df_error = add_error_metadata(df_invalid, "bz_activity_event")
error_path_silver = "/mnt/silver/error_bz_activity_event"
error_path_gold = "/mnt/gold/error_bz_activity_event"
df_error.write.format("delta").mode("overwrite").save(error_path_silver)
df_error.write.format("delta").mode("overwrite").save(error_path_gold)
logger.info(f"Written invalid/error records to Silver and Gold error tables.")

# 10. Logging Validation Failures
for row in df_error.select("error_id", "error_description").collect():
    logger.error(f"ErrorID: {row.error_id}, Description: {row.error_description}")

# 11. API Cost Calculation
api_cost = 0.000000  # Replace with actual cost calculation if available
print(f"\nAPI Cost Consumed: {api_cost} USD\n")
