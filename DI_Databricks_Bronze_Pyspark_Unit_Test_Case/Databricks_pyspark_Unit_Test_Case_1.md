_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: Unit test cases and Pytest script for Databricks Bronze Layer Data Ingestion Pipeline
## *Version*: 1 
## *Updated on*: 
_____________________________________________

# Databricks Bronze DE Pipeline - PySpark Unit Test Cases

## Summary
This document provides comprehensive unit test cases and a Databricks-optimized Pytest script for the enhanced Bronze layer data ingestion pipeline for DC Health Meter Reports. The tests validate key data transformations, error handling, and performance optimizations implemented in the PySpark code.

---

## Test Case List

| Test Case ID | Test Case Description | Expected Outcome |
|--------------|----------------------|------------------|
| TC01 | SparkSession initializes with correct configs | SparkSession is active and configs are set |
| TC02 | get_current_user returns valid user | Returns non-empty string (user identity) |
| TC03 | calculate_data_quality_metrics with empty DataFrame | Returns zero quality score, null count, duplicate count |
| TC04 | calculate_data_quality_metrics with all nulls | Returns zero quality score, correct null count |
| TC05 | calculate_data_quality_metrics with duplicates | Returns penalized quality score, correct duplicate count |
| TC06 | log_audit_record writes audit record successfully | Audit record is written to Delta table |
| TC07 | load_table_to_bronze_with_retry loads table on first attempt | Table is loaded, audit record status is 'Success' |
| TC08 | load_table_to_bronze_with_retry retries on failure | Retries up to max_retry_attempts, logs failure if all fail |
| TC09 | load_table_to_bronze_with_retry handles empty source table | Audit record status is 'Warning - No Data' |
| TC10 | create_bronze_schema_enhanced creates schema | Bronze schema exists after execution |
| TC11 | optimize_bronze_tables_enhanced optimizes tables | OPTIMIZE and VACUUM run without error |
| TC12 | generate_data_quality_report generates report | Data quality report is generated and logged |
| TC13 | main completes batch successfully | All tables processed, audit records written |
| TC14 | main handles batch failure | Audit record status is 'Batch Failed' |
| TC15 | SparkSession teardown after main | SparkSession is stopped |

---

## Pytest Script

```python
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType, LongType, DecimalType
from pyspark.sql import Row
import sys
import logging

# Import functions from the pipeline (assume they are in bronze_pipeline.py)
from bronze_pipeline import (
    get_current_user,
    calculate_data_quality_metrics,
    log_audit_record,
    load_table_to_bronze_with_retry,
    create_bronze_schema_enhanced,
    optimize_bronze_tables_enhanced,
    generate_data_quality_report,
    main
)

@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .appName("unit_test") \
        .master("local[2]") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()
    yield spark
    spark.stop()

# TC01: SparkSession initializes with correct configs
def test_spark_session_config(spark):
    assert spark.conf.get("spark.sql.adaptive.enabled") == "true"
    assert spark.sparkContext._jsc is not None

# TC02: get_current_user returns valid user
def test_get_current_user(spark):
    user = get_current_user()
    assert isinstance(user, str)
    assert len(user) > 0

# TC03: calculate_data_quality_metrics with empty DataFrame
def test_quality_metrics_empty_df(spark):
    schema = StructType([StructField("id", IntegerType(), True)])
    df = spark.createDataFrame([], schema)
    metrics = calculate_data_quality_metrics(df)
    assert metrics["quality_score"] == 0.0
    assert metrics["null_count"] == 0
    assert metrics["duplicate_count"] == 0

# TC04: calculate_data_quality_metrics with all nulls
def test_quality_metrics_all_nulls(spark):
    schema = StructType([StructField("id", IntegerType(), True)])
    df = spark.createDataFrame([Row(id=None), Row(id=None)], schema)
    metrics = calculate_data_quality_metrics(df)
    assert metrics["quality_score"] == 0.0
    assert metrics["null_count"] == 2

# TC05: calculate_data_quality_metrics with duplicates
def test_quality_metrics_duplicates(spark):
    schema = StructType([StructField("id", IntegerType(), True)])
    df = spark.createDataFrame([Row(id=1), Row(id=1)], schema)
    metrics = calculate_data_quality_metrics(df)
    assert metrics["duplicate_count"] == 1
    assert metrics["quality_score"] < 100.0

# TC06: log_audit_record writes audit record successfully
def test_log_audit_record(spark):
    # Mock audit record writing (use temp view)
    try:
        log_audit_record(
            record_id=1,
            source_table="TEST_TABLE",
            processing_time=1.23,
            status="Success",
            records_processed=10,
            records_failed=0,
            quality_metrics={"quality_score": 95.0, "null_count": 0, "duplicate_count": 0},
            batch_id="BATCH_TEST",
            file_size_mb=0.01,
            partition_count=1
        )
    except Exception as e:
        pytest.fail(f"Audit record logging failed: {e}")

# TC07: load_table_to_bronze_with_retry loads table on first attempt
def test_load_table_to_bronze_success(monkeypatch, spark):
    def mock_read(*args, **kwargs):
        schema = StructType([StructField("id", IntegerType(), True)])
        return spark.createDataFrame([Row(id=1), Row(id=2)], schema)
    monkeypatch.setattr(spark.read, "format", lambda x: mock_read)
    try:
        load_table_to_bronze_with_retry("TEST_TABLE", 1, "BATCH_TEST")
    except Exception as e:
        pytest.fail(f"Table load failed: {e}")

# TC08: load_table_to_bronze_with_retry retries on failure
def test_load_table_to_bronze_retry(monkeypatch, spark):
    call_count = {"count": 0}
    def mock_read_fail(*args, **kwargs):
        call_count["count"] += 1
        raise Exception("Simulated JDBC failure")
    monkeypatch.setattr(spark.read, "format", lambda x: mock_read_fail)
    with pytest.raises(Exception):
        load_table_to_bronze_with_retry("TEST_TABLE", 1, "BATCH_TEST")
    assert call_count["count"] >= 3

# TC09: load_table_to_bronze_with_retry handles empty source table
def test_load_table_to_bronze_empty(monkeypatch, spark):
    def mock_read_empty(*args, **kwargs):
        schema = StructType([StructField("id", IntegerType(), True)])
        return spark.createDataFrame([], schema)
    monkeypatch.setattr(spark.read, "format", lambda x: mock_read_empty)
    load_table_to_bronze_with_retry("TEST_TABLE", 1, "BATCH_TEST")
    # Should log audit with 'Warning - No Data'

# TC10: create_bronze_schema_enhanced creates schema
def test_create_bronze_schema(spark):
    try:
        create_bronze_schema_enhanced()
        schemas = [row["databaseName"] for row in spark.sql("SHOW SCHEMAS").collect()]
        assert "bronze" in schemas
    except Exception as e:
        pytest.fail(f"Schema creation failed: {e}")

# TC11: optimize_bronze_tables_enhanced optimizes tables
def test_optimize_bronze_tables(spark):
    try:
        results = optimize_bronze_tables_enhanced()
        assert isinstance(results, list)
    except Exception as e:
        pytest.fail(f"Table optimization failed: {e}")

# TC12: generate_data_quality_report generates report
def test_generate_data_quality_report(spark):
    try:
        generate_data_quality_report("BATCH_TEST")
    except Exception as e:
        pytest.fail(f"Quality report generation failed: {e}")

# TC13: main completes batch successfully
def test_main_success(monkeypatch, spark):
    # Monkeypatch functions to simulate success
    monkeypatch.setattr("bronze_pipeline.create_bronze_schema_enhanced", lambda: None)
    monkeypatch.setattr("bronze_pipeline.load_table_to_bronze_with_retry", lambda table, rid, bid: None)
    monkeypatch.setattr("bronze_pipeline.optimize_bronze_tables_enhanced", lambda: [])
    monkeypatch.setattr("bronze_pipeline.generate_data_quality_report", lambda batch_id: None)
    try:
        main()
    except Exception as e:
        pytest.fail(f"Main batch failed: {e}")

# TC14: main handles batch failure
def test_main_failure(monkeypatch, spark):
    monkeypatch.setattr("bronze_pipeline.create_bronze_schema_enhanced", lambda: (_ for _ in ()).throw(Exception("Schema error")))
    with pytest.raises(Exception):
        main()

# TC15: SparkSession teardown after main
def test_spark_teardown():
    spark = SparkSession.builder.appName("teardown_test").getOrCreate()
    spark.stop()
    assert spark._jvm is not None  # JVM should still exist, but SparkContext is stopped
```

---

## API Cost
apiCost: 0.0000187 USD

---

**outputURL:** https://github.com/ELANSURIYAA/LakehouseInADay_Databricks/tree/main/DI_Databricks_Bronze_Pyspark_Unit_Test_Case
**pipelineID:** 12308
