_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: Physical data model for Bronze layer of DC Health Meter Reports in Medallion architecture
## *Version*: 1
## *Updated on*: 
_____________________________________________

# Databricks Bronze Model Physical - DC Health Meter Reports

## 1. Overview

This document defines the physical data model for the Bronze layer of the Medallion architecture for DC Health Meter Reports. The Bronze layer stores raw data as-is from source systems with added metadata for governance and lineage tracking. All tables use Delta Lake format and follow Databricks SQL/PySpark standards.

## 2. Bronze Layer DDL Scripts

### 2.1 Master/Reference Tables

#### 2.1.1 Organization Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_org_organization (
  org_id STRING,
  org_name STRING,
  org_type STRING,
  parent_org_id STRING,
  effective_start_dt DATE,
  effective_end_dt DATE,
  is_active BOOLEAN,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_org_organization';
```

#### 2.1.2 Distribution Center Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dc_distribution_center (
  dc_id STRING,
  dc_name STRING,
  dc_code STRING,
  org_id STRING,
  address_line1 STRING,
  address_line2 STRING,
  city STRING,
  state_prov STRING,
  postal_code STRING,
  country STRING,
  timezone STRING,
  is_active BOOLEAN,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_dc_distribution_center';
```

#### 2.1.3 DC Shift Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dc_shift (
  shift_id STRING,
  dc_id STRING,
  shift_name STRING,
  shift_code STRING,
  start_time_local STRING,
  end_time_local STRING,
  crosses_midnight_flag BOOLEAN,
  is_active BOOLEAN,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_dc_shift';
```

#### 2.1.4 Partner Type Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_partner_type (
  partner_type_id STRING,
  partner_type_name STRING,
  description STRING,
  is_active BOOLEAN,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_partner_type';
```

#### 2.1.5 Partner Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_partner (
  partner_id STRING,
  partner_type_id STRING,
  partner_external_id STRING,
  first_name STRING,
  last_name STRING,
  hire_dt DATE,
  termination_dt DATE,
  home_dc_id STRING,
  status STRING,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_partner';
```

#### 2.1.6 Item Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_item (
  item_id STRING,
  item_sku STRING,
  item_description STRING,
  item_category STRING,
  uom STRING,
  is_active BOOLEAN,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_item';
```

#### 2.1.7 Equipment Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_equipment (
  equipment_id STRING,
  dc_id STRING,
  equipment_type STRING,
  equipment_code STRING,
  equipment_status STRING,
  effective_start_dt DATE,
  effective_end_dt DATE,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_equipment';
```

#### 2.1.8 Activity Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_activity (
  activity_id STRING,
  activity_code STRING,
  activity_name STRING,
  activity_group STRING,
  is_active BOOLEAN,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_activity';
```

#### 2.1.9 Exception Type Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_exception_type (
  exception_type_id STRING,
  exception_code STRING,
  exception_name STRING,
  severity STRING,
  description STRING,
  is_active BOOLEAN,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_exception_type';
```

### 2.2 Transaction/Event Tables (Fact Sources)

#### 2.2.1 Activity Event Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_activity_event (
  event_id STRING,
  dc_id STRING,
  event_ts_utc TIMESTAMP,
  shift_id STRING,
  partner_id STRING,
  activity_id STRING,
  item_id STRING,
  equipment_id STRING,
  source_system STRING,
  source_event_id STRING,
  location_code STRING,
  qty_handled DECIMAL(18,4),
  duration_seconds DECIMAL(18,4),
  labor_seconds DECIMAL(18,4),
  units_per_hour DECIMAL(18,4),
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system_meta STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_activity_event';
```

#### 2.2.2 Inventory Balance Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_inventory_balance (
  inventory_balance_id STRING,
  dc_id STRING,
  item_id STRING,
  as_of_ts_utc TIMESTAMP,
  location_code STRING,
  on_hand_qty DECIMAL(18,4),
  allocated_qty DECIMAL(18,4),
  available_qty DECIMAL(18,4),
  in_transit_qty DECIMAL(18,4),
  damaged_qty DECIMAL(18,4),
  source_system STRING,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system_meta STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_inventory_balance';
```

#### 2.2.3 Pick Transaction Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_pick_transaction (
  pick_txn_id STRING,
  dc_id STRING,
  pick_ts_utc TIMESTAMP,
  shift_id STRING,
  partner_id STRING,
  item_id STRING,
  equipment_id STRING,
  order_id STRING,
  order_line_id STRING,
  wave_id STRING,
  pick_location_code STRING,
  pick_qty DECIMAL(18,4),
  short_pick_qty DECIMAL(18,4),
  pick_status STRING,
  source_system STRING,
  source_pick_id STRING,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system_meta STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_pick_transaction';
```

#### 2.2.4 Headcount Record Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_headcount_record (
  headcount_id STRING,
  dc_id STRING,
  as_of_ts_utc TIMESTAMP,
  shift_id STRING,
  partner_id STRING,
  activity_id STRING,
  headcount_type STRING,
  headcount_value DECIMAL(18,4),
  source_system STRING,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system_meta STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_headcount_record';
```

#### 2.2.5 Kronos Timecard Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_kronos_timecard (
  timecard_id STRING,
  kronos_timecard_id STRING,
  partner_id STRING,
  dc_id STRING,
  shift_id STRING,
  work_date DATE,
  clock_in_ts_local TIMESTAMP,
  clock_out_ts_local TIMESTAMP,
  regular_hours DECIMAL(18,4),
  overtime_hours DECIMAL(18,4),
  paid_hours DECIMAL(18,4),
  absence_code STRING,
  source_system STRING,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system_meta STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_kronos_timecard';
```

#### 2.2.6 Exception Event Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_exception_event (
  exception_event_id STRING,
  exception_type_id STRING,
  dc_id STRING,
  exception_ts_utc TIMESTAMP,
  shift_id STRING,
  partner_id STRING,
  item_id STRING,
  activity_event_id STRING,
  exception_status STRING,
  severity_override STRING,
  notes STRING,
  source_system STRING,
  source_exception_id STRING,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system_meta STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_exception_event';
```

### 2.3 Audit Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_audit_log (
  record_id STRING,
  source_table STRING,
  load_timestamp TIMESTAMP,
  processed_by STRING,
  processing_time DECIMAL(18,4),
  status STRING,
  error_message STRING,
  records_processed BIGINT,
  records_failed BIGINT,
  batch_id STRING,
  created_ts TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/bz_audit_log';
```

## 3. Conceptual Data Model Diagram (Tabular Form)

| Source Table | Relationship Key Field | Target Table | Relationship Type |
|--------------|------------------------|--------------|-------------------|
| bz_org_organization | org_id | bz_dc_distribution_center | One-to-Many |
| bz_dc_distribution_center | dc_id | bz_dc_shift | One-to-Many |
| bz_partner_type | partner_type_id | bz_partner | One-to-Many |
| bz_dc_distribution_center | dc_id | bz_equipment | One-to-Many |
| bz_dc_distribution_center | dc_id | bz_activity_event | One-to-Many |
| bz_partner | partner_id | bz_activity_event | Many-to-One |
| bz_activity | activity_id | bz_activity_event | Many-to-One |
| bz_item | item_id | bz_activity_event | Many-to-One |
| bz_equipment | equipment_id | bz_activity_event | Many-to-One |
| bz_dc_shift | shift_id | bz_activity_event | Many-to-One |
| bz_dc_distribution_center | dc_id | bz_inventory_balance | One-to-Many |
| bz_item | item_id | bz_inventory_balance | Many-to-One |
| bz_dc_distribution_center | dc_id | bz_pick_transaction | One-to-Many |
| bz_item | item_id | bz_pick_transaction | Many-to-One |
| bz_partner | partner_id | bz_pick_transaction | Many-to-One |
| bz_dc_shift | shift_id | bz_pick_transaction | Many-to-One |
| bz_equipment | equipment_id | bz_pick_transaction | Many-to-One |
| bz_dc_distribution_center | dc_id | bz_headcount_record | One-to-Many |
| bz_partner | partner_id | bz_headcount_record | Many-to-One |
| bz_dc_shift | shift_id | bz_headcount_record | Many-to-One |
| bz_activity | activity_id | bz_headcount_record | Many-to-One |
| bz_partner | partner_id | bz_kronos_timecard | Many-to-One |
| bz_dc_distribution_center | dc_id | bz_kronos_timecard | Many-to-One |
| bz_dc_shift | shift_id | bz_kronos_timecard | Many-to-One |
| bz_exception_type | exception_type_id | bz_exception_event | One-to-Many |
| bz_dc_distribution_center | dc_id | bz_exception_event | One-to-Many |
| bz_partner | partner_id | bz_exception_event | Many-to-One |
| bz_item | item_id | bz_exception_event | Many-to-One |
| bz_activity_event | event_id | bz_exception_event | One-to-One |

## 4. Design Decisions and Assumptions

### 4.1 Design Decisions

1. **Delta Lake Format**: All tables use Delta Lake format for ACID transactions, time travel, and schema evolution capabilities.

2. **No Constraints**: Following Bronze layer principles, no primary keys, foreign keys, or constraints are enforced at the table level.

3. **Metadata Columns**: All tables include standard metadata columns:
   - `load_timestamp`: When the record was loaded into Bronze layer
   - `update_timestamp`: When the record was last updated
   - `source_system`: Identifies the source system

4. **String Data Types**: Most ID fields use STRING data type to accommodate various source system formats.

5. **Decimal Precision**: Numeric fields use DECIMAL(18,4) for precision in quantity and time calculations.

6. **Naming Convention**: All Bronze tables follow the pattern `bronze.bz_<tablename>`.

### 4.2 Assumptions

1. **Source System Integration**: Assumes multiple source systems (WMS, LMS, Kronos, Custom) will feed data into Bronze layer.

2. **Time Zone Handling**: UTC timestamps are used for consistency, with local time conversions handled in Silver/Gold layers.

3. **Data Governance**: Audit trail is maintained through the dedicated audit table and metadata columns.

4. **Scalability**: Delta Lake partitioning strategies will be implemented based on data volume and query patterns.

5. **Schema Evolution**: Delta Lake's schema evolution capabilities will handle source system changes.

## 5. Implementation Guidelines

### 5.1 Data Ingestion

1. Use Databricks Auto Loader for streaming ingestion from cloud storage.
2. Implement idempotent loading using source system keys.
3. Capture all source columns as-is without transformation.
4. Add metadata columns during ingestion process.

### 5.2 Data Quality

1. Implement data quality checks in Silver layer, not Bronze.
2. Store all data in Bronze, including invalid records.
3. Use audit table to track processing statistics and errors.

### 5.3 Performance Optimization

1. Partition large tables by date columns (e.g., event_ts_utc, as_of_ts_utc).
2. Use Z-ordering on frequently queried columns.
3. Implement table maintenance procedures (OPTIMIZE, VACUUM).

## 6. API Cost

**apiCost**: 0.000000

---

**Note**: This Bronze layer physical model provides the foundation for the Medallion architecture, ensuring raw data preservation while enabling efficient downstream processing in Silver and Gold layers.