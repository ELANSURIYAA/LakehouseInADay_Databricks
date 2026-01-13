_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: Physical data model for Silver layer of DC Health Meter Reports in Medallion architecture with comprehensive DDL scripts
## *Version*: 2
## *Updated on*: 
_____________________________________________

# Databricks Silver Model Physical - DC Health Meter Reports

## 1. Overview

This document defines the comprehensive physical data model for the Silver layer of the Medallion architecture for DC Health Meter Reports. The Silver layer stores cleansed, validated, and conformed data with proper data types, partitioning strategies, and performance optimizations. All tables use Delta Lake format and are compatible with Databricks PySpark SQL.

## 2. Silver Layer DDL Scripts

### 2.1 Master/Reference Tables

#### 2.1.1 Organization Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_organization (
  org_id STRING,
  org_name STRING,
  org_type STRING,
  parent_org_id STRING,
  parent_org_name STRING,
  effective_start_dt DATE,
  effective_end_dt DATE,
  is_active BOOLEAN,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
PARTITIONED BY (org_type)
LOCATION '/mnt/silver/si_organization'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.1.2 Distribution Center Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_distribution_center (
  dc_id STRING,
  dc_name STRING,
  dc_code STRING,
  org_id STRING,
  org_name STRING,
  address_line1 STRING,
  address_line2 STRING,
  city STRING,
  state_prov STRING,
  postal_code STRING,
  country STRING,
  timezone STRING,
  is_active BOOLEAN,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
PARTITIONED BY (country, state_prov)
LOCATION '/mnt/silver/si_distribution_center'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.1.3 Shift Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_shift (
  shift_id STRING,
  dc_id STRING,
  dc_name STRING,
  shift_name STRING,
  shift_code STRING,
  start_time_local STRING,
  end_time_local STRING,
  crosses_midnight_flag BOOLEAN,
  is_active BOOLEAN,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
PARTITIONED BY (dc_name)
LOCATION '/mnt/silver/si_shift'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.1.4 Partner Type Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_partner_type (
  partner_type_id STRING,
  partner_type_name STRING,
  description STRING,
  is_active BOOLEAN,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/silver/si_partner_type'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.1.5 Partner Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_partner (
  partner_id STRING,
  partner_type_id STRING,
  partner_type_name STRING,
  partner_external_id STRING,
  first_name STRING,
  last_name STRING,
  hire_dt DATE,
  termination_dt DATE,
  home_dc_id STRING,
  home_dc_name STRING,
  status STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
PARTITIONED BY (home_dc_name, status)
LOCATION '/mnt/silver/si_partner'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.1.6 Item Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_item (
  item_id STRING,
  item_sku STRING,
  item_description STRING,
  item_category STRING,
  uom STRING,
  is_active BOOLEAN,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
PARTITIONED BY (item_category)
LOCATION '/mnt/silver/si_item'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.1.7 Equipment Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_equipment (
  equipment_id STRING,
  dc_id STRING,
  dc_name STRING,
  equipment_type STRING,
  equipment_code STRING,
  equipment_status STRING,
  effective_start_dt DATE,
  effective_end_dt DATE,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
PARTITIONED BY (dc_name, equipment_type)
LOCATION '/mnt/silver/si_equipment'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.1.8 Activity Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_activity (
  activity_id STRING,
  activity_code STRING,
  activity_name STRING,
  activity_group STRING,
  is_active BOOLEAN,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
PARTITIONED BY (activity_group)
LOCATION '/mnt/silver/si_activity'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.1.9 Exception Type Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_exception_type (
  exception_type_id STRING,
  exception_code STRING,
  exception_name STRING,
  severity STRING,
  description STRING,
  is_active BOOLEAN,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
PARTITIONED BY (severity)
LOCATION '/mnt/silver/si_exception_type'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

### 2.2 Transaction/Event Tables (Fact Sources)

#### 2.2.1 Activity Event Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_activity_event (
  event_id STRING,
  dc_id STRING,
  dc_name STRING,
  event_ts_utc TIMESTAMP,
  shift_id STRING,
  shift_name STRING,
  partner_id STRING,
  partner_external_id STRING,
  activity_id STRING,
  activity_name STRING,
  item_id STRING,
  item_sku STRING,
  equipment_id STRING,
  equipment_code STRING,
  source_system STRING,
  source_event_id STRING,
  location_code STRING,
  qty_handled DECIMAL(18,4),
  duration_seconds DECIMAL(18,4),
  labor_seconds DECIMAL(18,4),
  units_per_hour DECIMAL(18,4),
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP
) USING DELTA
PARTITIONED BY (dc_name, date(event_ts_utc))
LOCATION '/mnt/silver/si_activity_event'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.2.2 Inventory Balance Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_inventory_balance (
  inventory_balance_id STRING,
  dc_id STRING,
  dc_name STRING,
  item_id STRING,
  item_sku STRING,
  as_of_ts_utc TIMESTAMP,
  location_code STRING,
  on_hand_qty DECIMAL(18,4),
  allocated_qty DECIMAL(18,4),
  available_qty DECIMAL(18,4),
  in_transit_qty DECIMAL(18,4),
  damaged_qty DECIMAL(18,4),
  source_system STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP
) USING DELTA
PARTITIONED BY (dc_name, date(as_of_ts_utc))
LOCATION '/mnt/silver/si_inventory_balance'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.2.3 Pick Transaction Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_pick_transaction (
  pick_txn_id STRING,
  dc_id STRING,
  dc_name STRING,
  pick_ts_utc TIMESTAMP,
  shift_id STRING,
  shift_name STRING,
  partner_id STRING,
  partner_external_id STRING,
  item_id STRING,
  item_sku STRING,
  equipment_id STRING,
  equipment_code STRING,
  order_id STRING,
  order_line_id STRING,
  wave_id STRING,
  pick_location_code STRING,
  pick_qty DECIMAL(18,4),
  short_pick_qty DECIMAL(18,4),
  pick_status STRING,
  source_system STRING,
  source_pick_id STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP
) USING DELTA
PARTITIONED BY (dc_name, date(pick_ts_utc))
LOCATION '/mnt/silver/si_pick_transaction'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.2.4 Headcount Record Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_headcount_record (
  headcount_id STRING,
  dc_id STRING,
  dc_name STRING,
  as_of_ts_utc TIMESTAMP,
  shift_id STRING,
  shift_name STRING,
  partner_id STRING,
  partner_external_id STRING,
  activity_id STRING,
  activity_name STRING,
  headcount_type STRING,
  headcount_value DECIMAL(18,4),
  source_system STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP
) USING DELTA
PARTITIONED BY (dc_name, date(as_of_ts_utc))
LOCATION '/mnt/silver/si_headcount_record'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.2.5 Kronos Timecard Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_kronos_timecard (
  timecard_id STRING,
  kronos_timecard_id STRING,
  partner_id STRING,
  partner_external_id STRING,
  dc_id STRING,
  dc_name STRING,
  shift_id STRING,
  shift_name STRING,
  work_date DATE,
  clock_in_ts_local TIMESTAMP,
  clock_out_ts_local TIMESTAMP,
  regular_hours DECIMAL(18,4),
  overtime_hours DECIMAL(18,4),
  paid_hours DECIMAL(18,4),
  absence_code STRING,
  source_system STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP
) USING DELTA
PARTITIONED BY (dc_name, work_date)
LOCATION '/mnt/silver/si_kronos_timecard'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

#### 2.2.6 Exception Event Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_exception_event (
  exception_event_id STRING,
  exception_type_id STRING,
  exception_type_name STRING,
  dc_id STRING,
  dc_name STRING,
  exception_ts_utc TIMESTAMP,
  shift_id STRING,
  shift_name STRING,
  partner_id STRING,
  partner_external_id STRING,
  item_id STRING,
  item_sku STRING,
  activity_event_id STRING,
  activity_event_source_id STRING,
  exception_status STRING,
  severity_override STRING,
  notes STRING,
  source_system STRING,
  source_exception_id STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP
) USING DELTA
PARTITIONED BY (dc_name, date(exception_ts_utc))
LOCATION '/mnt/silver/si_exception_event'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

## 3. Error Data Table DDL Script

### 3.1 Data Quality Errors Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_data_quality_errors (
  error_id STRING,
  source_table STRING,
  source_record_id STRING,
  error_type STRING,
  error_category STRING,
  error_description STRING,
  error_field STRING,
  error_value STRING,
  expected_value STRING,
  severity STRING,
  error_timestamp TIMESTAMP,
  resolution_status STRING,
  resolution_notes STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP
) USING DELTA
PARTITIONED BY (source_table, date(error_timestamp))
LOCATION '/mnt/silver/si_data_quality_errors'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

## 4. Audit Table DDL Script

### 4.1 Pipeline Audit Table
```sql
CREATE TABLE IF NOT EXISTS silver.si_pipeline_audit (
  audit_id STRING,
  pipeline_name STRING,
  pipeline_run_id STRING,
  source_table STRING,
  target_table STRING,
  process_start_timestamp TIMESTAMP,
  process_end_timestamp TIMESTAMP,
  processing_duration_seconds BIGINT,
  records_read BIGINT,
  records_processed BIGINT,
  records_inserted BIGINT,
  records_updated BIGINT,
  records_failed BIGINT,
  error_count BIGINT,
  warning_count BIGINT,
  data_quality_score DECIMAL(5,2),
  pipeline_status STRING,
  error_message STRING,
  processed_by STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP
) USING DELTA
PARTITIONED BY (pipeline_name, date(process_start_timestamp))
LOCATION '/mnt/silver/si_pipeline_audit'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

## 5. Update DDL Scripts

### 5.1 Add Column Scripts
```sql
-- Add new columns to existing tables if needed
ALTER TABLE silver.si_organization ADD COLUMN region STRING;
ALTER TABLE silver.si_distribution_center ADD COLUMN region STRING;
ALTER TABLE silver.si_partner ADD COLUMN employee_type STRING;
ALTER TABLE silver.si_item ADD COLUMN weight_kg DECIMAL(10,3);
ALTER TABLE silver.si_equipment ADD COLUMN capacity_units DECIMAL(10,2);
```

### 5.2 Update Table Properties
```sql
-- Update table properties for performance optimization
ALTER TABLE silver.si_activity_event SET TBLPROPERTIES (
  'delta.tuneFileSizesForRewrites' = 'true',
  'delta.targetFileSize' = '134217728'
);

ALTER TABLE silver.si_inventory_balance SET TBLPROPERTIES (
  'delta.tuneFileSizesForRewrites' = 'true',
  'delta.targetFileSize' = '134217728'
);

ALTER TABLE silver.si_pick_transaction SET TBLPROPERTIES (
  'delta.tuneFileSizesForRewrites' = 'true',
  'delta.targetFileSize' = '134217728'
);
```

### 5.3 Create Indexes (Z-Ordering)
```sql
-- Optimize tables with Z-ordering for better query performance
OPTIMIZE silver.si_activity_event ZORDER BY (dc_name, partner_external_id, activity_name);
OPTIMIZE silver.si_inventory_balance ZORDER BY (dc_name, item_sku);
OPTIMIZE silver.si_pick_transaction ZORDER BY (dc_name, partner_external_id, item_sku);
OPTIMIZE silver.si_kronos_timecard ZORDER BY (dc_name, partner_external_id, work_date);
OPTIMIZE silver.si_exception_event ZORDER BY (dc_name, exception_type_name, exception_status);
```

## 6. Data Retention Policies

### 6.1 Retention Periods for Silver Layer

| Table Category | Retention Period | Rationale |
|----------------|------------------|----------|
| Master/Reference Tables | 7 years | Long-term reference data for historical analysis |
| Activity Events | 3 years | Operational history for trend analysis and compliance |
| Inventory Balances | 2 years | Inventory history for demand planning and analysis |
| Pick Transactions | 3 years | Pick performance history and audit requirements |
| Headcount Records | 2 years | Labor planning and historical workforce analysis |
| Kronos Timecards | 7 years | Legal and compliance requirements for payroll data |
| Exception Events | 5 years | Exception pattern analysis and compliance |
| Data Quality Errors | 1 year | Data quality monitoring and improvement |
| Pipeline Audit | 2 years | Pipeline monitoring and troubleshooting |

### 6.2 Archiving Strategies

#### 6.2.1 Automated Archiving Process
```sql
-- Create archival tables for long-term storage
CREATE TABLE IF NOT EXISTS archive.si_activity_event_archive
USING DELTA
LOCATION '/mnt/archive/si_activity_event_archive'
AS SELECT * FROM silver.si_activity_event WHERE 1=0;

-- Archive old data (example for activity events older than 3 years)
INSERT INTO archive.si_activity_event_archive
SELECT * FROM silver.si_activity_event 
WHERE event_ts_utc < date_sub(current_date(), 1095);

-- Delete archived data from silver layer
DELETE FROM silver.si_activity_event 
WHERE event_ts_utc < date_sub(current_date(), 1095);
```

#### 6.2.2 Vacuum Operations
```sql
-- Regular vacuum operations to remove old file versions
VACUUM silver.si_activity_event RETAIN 168 HOURS; -- 7 days
VACUUM silver.si_inventory_balance RETAIN 168 HOURS;
VACUUM silver.si_pick_transaction RETAIN 168 HOURS;
VACUUM silver.si_kronos_timecard RETAIN 168 HOURS;
VACUUM silver.si_exception_event RETAIN 168 HOURS;
```

## 7. Conceptual Data Model Diagram (Tabular Form)

| Source Table | Relationship Key Field | Target Table | Relationship Type |
|--------------|------------------------|--------------|-------------------|
| si_organization | org_name | si_distribution_center | One-to-Many |
| si_distribution_center | dc_name | si_shift | One-to-Many |
| si_partner_type | partner_type_name | si_partner | One-to-Many |
| si_distribution_center | dc_name | si_equipment | One-to-Many |
| si_distribution_center | dc_name | si_activity_event | One-to-Many |
| si_partner | partner_external_id | si_activity_event | Many-to-One |
| si_item | item_sku | si_activity_event | Many-to-One |
| si_equipment | equipment_code | si_activity_event | Many-to-One |
| si_shift | shift_name | si_activity_event | Many-to-One |
| si_activity | activity_name | si_activity_event | Many-to-One |
| si_distribution_center | dc_name | si_inventory_balance | One-to-Many |
| si_item | item_sku | si_inventory_balance | Many-to-One |
| si_distribution_center | dc_name | si_pick_transaction | One-to-Many |
| si_item | item_sku | si_pick_transaction | Many-to-One |
| si_partner | partner_external_id | si_pick_transaction | Many-to-One |
| si_shift | shift_name | si_pick_transaction | Many-to-One |
| si_equipment | equipment_code | si_pick_transaction | Many-to-One |
| si_distribution_center | dc_name | si_headcount_record | One-to-Many |
| si_partner | partner_external_id | si_headcount_record | Many-to-One |
| si_shift | shift_name | si_headcount_record | Many-to-One |
| si_activity | activity_name | si_headcount_record | Many-to-One |
| si_partner | partner_external_id | si_kronos_timecard | Many-to-One |
| si_distribution_center | dc_name | si_kronos_timecard | Many-to-One |
| si_shift | shift_name | si_kronos_timecard | Many-to-One |
| si_exception_type | exception_type_name | si_exception_event | One-to-Many |
| si_distribution_center | dc_name | si_exception_event | One-to-Many |
| si_partner | partner_external_id | si_exception_event | Many-to-One |
| si_item | item_sku | si_exception_event | Many-to-One |
| si_shift | shift_name | si_exception_event | Many-to-One |
| si_activity_event | source_event_id | si_exception_event | One-to-One |
| si_data_quality_errors | source_table | All Silver Tables | Many-to-One |
| si_pipeline_audit | source_table | All Silver Tables | Many-to-One |
| si_pipeline_audit | target_table | All Silver Tables | Many-to-One |

## 8. Design Decisions and Assumptions

### 8.1 Design Decisions

1. **Delta Lake Format**: All tables use Delta Lake format for ACID transactions, time travel, and schema evolution capabilities.

2. **ID Fields Addition**: Added ID fields (org_id, dc_id, partner_id, etc.) to all tables as required by the physical model specifications.

3. **Partitioning Strategy**: 
   - Master tables: Partitioned by business domain (org_type, country, dc_name, etc.)
   - Fact tables: Partitioned by dc_name and date for optimal query performance

4. **Data Types**: 
   - STRING for ID fields and text data
   - DECIMAL(18,4) for precise numeric calculations
   - TIMESTAMP for all datetime fields
   - BOOLEAN for flag fields

5. **Performance Optimization**:
   - Auto-optimize enabled for all tables
   - Z-ordering on frequently queried columns
   - Target file size optimization

6. **No Constraints**: Following Spark SQL limitations, no primary keys, foreign keys, or constraints are defined.

### 8.2 Key Assumptions

1. **Data Quality**: Silver layer assumes data has been validated and cleansed from Bronze layer.

2. **Business Keys**: Natural business keys (dc_name, item_sku, partner_external_id) are used for relationships.

3. **Time Zone Handling**: UTC timestamps are used consistently with local time conversions handled in application logic.

4. **Scalability**: Partitioning and optimization strategies support high-volume data processing.

5. **Compliance**: Retention policies align with business and regulatory requirements.

## 9. Implementation Guidelines

### 9.1 Data Processing

1. **ETL Pipeline**: Use Databricks notebooks with PySpark for data transformation from Bronze to Silver.

2. **Data Validation**: Implement comprehensive data quality checks before loading into Silver tables.

3. **Error Handling**: Capture all data quality issues in si_data_quality_errors table.

4. **Audit Trail**: Log all pipeline executions in si_pipeline_audit table.

### 9.2 Performance Optimization

1. **Regular Maintenance**: Schedule OPTIMIZE and VACUUM operations.

2. **Monitoring**: Monitor query performance and adjust Z-ordering as needed.

3. **Partitioning**: Review and adjust partitioning strategies based on query patterns.

### 9.3 Data Governance

1. **Access Control**: Implement proper access controls using Databricks Unity Catalog.

2. **Data Lineage**: Maintain data lineage through metadata columns and audit tables.

3. **Documentation**: Keep data dictionary and business rules documentation updated.

## 10. API Cost

**apiCost**: 0.000000

---

**Output URL**: https://github.com/ELANSURIYAA/LakehouseInADay_Databricks/tree/main/DI_Databricks_Silver_Model_Physical

**Pipeline ID**: 12357

---

**Note**: This Silver layer physical model provides a comprehensive foundation for cleansed and conformed data in the Medallion architecture, ensuring data quality, performance optimization, and scalability for analytics and data science workflows on the Databricks platform.