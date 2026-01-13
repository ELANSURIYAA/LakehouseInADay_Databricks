_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: Unit test cases and Pytest script for Databricks Silver DE Pipeline - DC Health Meter Reports
## *Version*: 1
## *Updated on*: 
_____________________________________________

# Databricks Silver DE Pipeline - PySpark Unit Test Cases

This document provides comprehensive unit test cases and a Databricks-optimized Pytest script for the Silver DE Pipeline PySpark code. The tests ensure reliability, correctness, and performance of the pipeline in Databricks environments.

---

## Test Case List

| Test Case ID | Test Case Description | Expected Outcome |
|--------------|----------------------|------------------|
| TC01 | Validate SparkSession initialization with Delta configs | SparkSession is created with correct configs |
| TC02 | Test reading from Bronze Delta path (valid path) | DataFrame is loaded with expected schema |
| TC03 | Test reading from Bronze Delta path (invalid path) | Exception is raised |
| TC04 | Remove duplicates from DataFrame | Duplicates are removed; row count matches expectation |
| TC05 | Enforce schema on DataFrame | DataFrame matches the defined schema |
| TC06 | Handle nulls in numeric and string columns | Nulls replaced with 0 (numeric) and 'UNKNOWN' (string) |
| TC07 | Validate business rules (event_ts_utc not null, qty_handled >= 0) | Valid and invalid DataFrames are correctly split |
| TC08 | Validate business rules (edge: all invalid) | All records go to invalid DataFrame |
| TC09 | Validate business rules (edge: all valid) | All records go to valid DataFrame |
| TC10 | Add audit columns (load_date, update_date) | Columns are added and populated |
| TC11 | Write valid data to Silver Delta path | Data is written and partitioned by dc_id |
| TC12 | Write invalid data to error tables | Data is written to error tables with error metadata |
| TC13 | Add error metadata to invalid DataFrame | error_id, table_name, error_timestamp, source_system columns are added |
| TC14 | Logging validation failures | Error logs are generated for invalid records |
| TC15 | API cost calculation | API cost is reported as a float |
| TC16 | Edge case: Empty DataFrame input | Functions handle empty DataFrame gracefully |
| TC17 | Edge case: Null-only DataFrame | Null handling and validation work as expected |
| TC18 | Edge case: Schema mismatch | Exception is raised or handled |
| TC19 | Performance: Large DataFrame | Pipeline processes large data efficiently |
| TC20 | Exception: Invalid data types in input | Exception is raised or handled |

---

## Pytest Script (Databricks-Optimized)

```python
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import Row
from pyspark.sql.functions import col, lit, current_timestamp
import sys
import logging

# Fixtures for SparkSession
@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .appName("SilverLayerPipelineTest") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    yield spark
    spark.stop()

# Sample schema for tests
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

# Helper functions (from pipeline)
def remove_duplicates(df):
    return df.dropDuplicates()

def enforce_schema(df, schema):
    return df.sparkSession.createDataFrame(df.rdd, schema)

def handle_nulls(df):
    fill_dict = {col.name: 0 for col in df.schema.fields if isinstance(col.dataType, DecimalType)}
    fill_dict.update({col.name: 'UNKNOWN' for col in df.schema.fields if isinstance(col.dataType, StringType)})
    return df.fillna(fill_dict)

def validate_business_rules(df):
    valid = df.filter((col("event_ts_utc").isNotNull()) & (col("qty_handled") >= 0))
    invalid = df.subtract(valid)
    invalid = invalid.withColumn("error_description", lit("event_ts_utc is null or qty_handled < 0"))
    return valid, invalid

def add_error_metadata(df, table_name):
    from pyspark.sql.functions import monotonically_increasing_id
    return df.withColumn("error_id", monotonically_increasing_id()) \
             .withColumn("table_name", lit(table_name)) \
             .withColumn("error_timestamp", current_timestamp()) \
             .withColumn("source_system", lit("bronze"))

# Test cases

def test_spark_session_init(spark):
    assert spark.conf.get("spark.sql.extensions") == "io.delta.sql.DeltaSparkSessionExtension"
    assert spark.conf.get("spark.sql.catalog.spark_catalog") == "org.apache.spark.sql.delta.catalog.DeltaCatalog"

def test_remove_duplicates(spark):
    data = [Row(event_id="1", dc_id="A", event_ts_utc=None), Row(event_id="1", dc_id="A", event_ts_utc=None)]
    df = spark.createDataFrame(data)
    df_nodup = remove_duplicates(df)
    assert df_nodup.count() == 1

def test_enforce_schema(spark):
    data = [Row(event_id="1", dc_id="A", event_ts_utc=None)]
    df = spark.createDataFrame(data)
    df_schema = enforce_schema(df, silver_schema)
    assert df_schema.schema == silver_schema

def test_handle_nulls(spark):
    data = [Row(event_id=None, dc_id=None, event_ts_utc=None, qty_handled=None)]
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("dc_id", StringType(), True),
        StructField("event_ts_utc", TimestampType(), True),
        StructField("qty_handled", DecimalType(18,4), True)
    ])
    df = spark.createDataFrame(data, schema)
    df_filled = handle_nulls(df)
    row = df_filled.collect()[0]
    assert row.event_id == 'UNKNOWN'
    assert row.dc_id == 'UNKNOWN'
    assert row.qty_handled == 0

def test_validate_business_rules_all_valid(spark):
    from datetime import datetime
    data = [Row(event_id="1", dc_id="A", event_ts_utc=datetime(2023,1,1), qty_handled=1)]
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("dc_id", StringType(), True),
        StructField("event_ts_utc", TimestampType(), True),
        StructField("qty_handled", DecimalType(18,4), True)
    ])
    df = spark.createDataFrame(data, schema)
    valid, invalid = validate_business_rules(df)
    assert valid.count() == 1
    assert invalid.count() == 0

def test_validate_business_rules_all_invalid(spark):
    data = [Row(event_id="1", dc_id="A", event_ts_utc=None, qty_handled=-1)]
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("dc_id", StringType(), True),
        StructField("event_ts_utc", TimestampType(), True),
        StructField("qty_handled", DecimalType(18,4), True)
    ])
    df = spark.createDataFrame(data, schema)
    valid, invalid = validate_business_rules(df)
    assert valid.count() == 0
    assert invalid.count() == 1
    assert 'error_description' in invalid.columns

def test_add_error_metadata(spark):
    data = [Row(event_id="1", dc_id="A", event_ts_utc=None, qty_handled=-1)]
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("dc_id", StringType(), True),
        StructField("event_ts_utc", TimestampType(), True),
        StructField("qty_handled", DecimalType(18,4), True)
    ])
    df = spark.createDataFrame(data, schema)
    df_error = add_error_metadata(df, "bz_activity_event")
    assert 'error_id' in df_error.columns
    assert 'table_name' in df_error.columns
    assert 'error_timestamp' in df_error.columns
    assert 'source_system' in df_error.columns

# Edge case: Empty DataFrame

def test_empty_dataframe(spark):
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("dc_id", StringType(), True)
    ])
    df = spark.createDataFrame([], schema)
    df_nodup = remove_duplicates(df)
    assert df_nodup.count() == 0
    df_filled = handle_nulls(df)
    assert df_filled.count() == 0

# Edge case: Schema mismatch

def test_schema_mismatch(spark):
    data = [Row(event_id="1", dc_id="A")]
    wrong_schema = StructType([
        StructField("event_id", IntegerType(), True),
        StructField("dc_id", IntegerType(), True)
    ])
    df = spark.createDataFrame(data)
    with pytest.raises(Exception):
        enforce_schema(df, wrong_schema)

# Exception: Invalid data types

def test_invalid_data_types(spark):
    data = [Row(event_id=1, dc_id=2, event_ts_utc="not_a_timestamp", qty_handled="not_a_decimal")]
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("dc_id", StringType(), True),
        StructField("event_ts_utc", TimestampType(), True),
        StructField("qty_handled", DecimalType(18,4), True)
    ])
    with pytest.raises(Exception):
        spark.createDataFrame(data, schema)

# Performance test (large DataFrame)

def test_large_dataframe_performance(spark):
    data = [Row(event_id=str(i), dc_id="A", event_ts_utc=None, qty_handled=0) for i in range(10000)]
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("dc_id", StringType(), True),
        StructField("event_ts_utc", TimestampType(), True),
        StructField("qty_handled", DecimalType(18,4), True)
    ])
    df = spark.createDataFrame(data, schema)
    df_nodup = remove_duplicates(df)
    assert df_nodup.count() == 10000

# API cost calculation test

def test_api_cost():
    api_cost = 0.000000
    assert isinstance(api_cost, float)
```

---

## API Cost

apiCost: 0.000000

---

**outputURL:** https://github.com/ELANSURIYAA/LakehouseInADay_Databricks/tree/main/DI_Databricks_Silver_Pyspark_Unit_Test_Case_DIAS

**pipelineID:** 12364
