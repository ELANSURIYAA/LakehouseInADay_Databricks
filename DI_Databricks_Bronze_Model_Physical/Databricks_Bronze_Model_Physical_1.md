_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: Physical data model for Bronze layer of DC Health Meter Reports in Databricks Medallion architecture
## *Version*: 1
## *Updated on*: 
_____________________________________________

# Databricks Bronze Model Physical - DC Health Meter Reports

## 1. Overview

This document defines the physical data model for the Bronze layer of the DC Health Meter Reports system using the Medallion architecture in Databricks. The Bronze layer stores raw data as-is with minimal transformations, using Delta Lake format for ACID transactions and time travel capabilities.

## 2. Design Principles

- **Raw Data Preservation**: Store data exactly as received from source systems
- **Delta Lake Format**: All tables use Delta Lake for ACID compliance and versioning
- **Metadata Enrichment**: Add load timestamps and source system information
- **No Constraints**: Bronze layer does not enforce primary keys, foreign keys, or constraints
- **Naming Convention**: Tables prefixed with `bz_` within `bronze` schema
- **Audit Trail**: Comprehensive audit table for data lineage and governance

## 3. Bronze Layer DDL Scripts

### 3.1 Dimension Tables

#### 3.1.1 Bronze Organization Dimension
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dim_organization (
  org_id INT,
  org_name STRING,
  org_level STRING,
  parent_org_id INT,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/dim_organization';
```

#### 3.1.2 Bronze Distribution Center Dimension
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dim_distribution_center (
  dc_id INT,
  dc_name STRING,
  org_id INT,
  dc_status STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/dim_distribution_center';
```

#### 3.1.3 Bronze Date Dimension
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dim_date (
  date_key INT,
  calendar_date DATE,
  week_start_date DATE,
  fiscal_period STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/dim_date';
```

#### 3.1.4 Bronze Shift Dimension
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dim_shift (
  shift_id INT,
  shift_name STRING,
  shift_start_time STRING,
  shift_end_time STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/dim_shift';
```

#### 3.1.5 Bronze Partner Type Dimension
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dim_partner_type (
  partner_type_id INT,
  partner_type_name STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/dim_partner_type';
```

#### 3.1.6 Bronze Partner Dimension
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dim_partner (
  partner_id INT,
  partner_name STRING,
  partner_type_id INT,
  partner_status STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/dim_partner';
```

#### 3.1.7 Bronze Item Dimension
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dim_item (
  item_id INT,
  item_name STRING,
  item_category STRING,
  item_status STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/dim_item';
```

#### 3.1.8 Bronze Activity Dimension
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dim_activity (
  activity_id INT,
  activity_name STRING,
  activity_group STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/dim_activity';
```

#### 3.1.9 Bronze Equipment Dimension
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dim_equipment (
  equipment_id INT,
  equipment_type STRING,
  equipment_status STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/dim_equipment';
```

#### 3.1.10 Bronze Employee Dimension
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dim_employee (
  employee_id STRING,
  home_dc_id INT,
  partner_id INT,
  role_name STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/dim_employee';
```

#### 3.1.11 Bronze Exception Type Dimension
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_dim_exception_type (
  exception_type_id INT,
  exception_type STRING,
  exception_subtype STRING,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/dim_exception_type';
```

### 3.2 Fact Tables

#### 3.2.1 Bronze DC Operations Fact
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_fact_dc_operations (
  operations_fact_id BIGINT,
  dc_id INT,
  date_key INT,
  shift_id INT,
  activity_id INT,
  partner_id INT,
  equipment_id INT,
  throughput_units INT,
  throughput_lines INT,
  labor_hours DECIMAL(10,2),
  cycle_time_minutes DECIMAL(10,2),
  ontime_completion_pct DECIMAL(5,2),
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/fact_dc_operations';
```

#### 3.2.2 Bronze Inventory Fact
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_fact_inventory (
  inventory_fact_id BIGINT,
  dc_id INT,
  date_key INT,
  item_id INT,
  onhand_qty INT,
  available_qty INT,
  allocated_qty INT,
  damaged_qty INT,
  onorder_qty INT,
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/fact_inventory';
```

#### 3.2.3 Bronze Headcount Fact
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_fact_headcount (
  headcount_fact_id BIGINT,
  dc_id INT,
  date_key INT,
  shift_id INT,
  partner_type_id INT,
  partner_id INT,
  role_name STRING,
  planned_headcount INT,
  actual_headcount INT,
  planned_hours DECIMAL(10,2),
  worked_hours DECIMAL(10,2),
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/fact_headcount';
```

#### 3.2.4 Bronze Picks Fact
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_fact_picks (
  picks_fact_id BIGINT,
  dc_id INT,
  date_key INT,
  shift_id INT,
  activity_id INT,
  partner_id INT,
  item_id INT,
  pick_units INT,
  pick_lines INT,
  pick_errors INT,
  rework_count INT,
  labor_hours DECIMAL(10,2),
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/fact_picks';
```

#### 3.2.5 Bronze Kronos Fact
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_fact_kronos (
  kronos_fact_id BIGINT,
  employee_id STRING,
  dc_id INT,
  date_key INT,
  shift_id INT,
  scheduled_hours DECIMAL(10,2),
  worked_hours DECIMAL(10,2),
  overtime_hours DECIMAL(10,2),
  absence_flag STRING,
  adherence_pct DECIMAL(5,2),
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/fact_kronos';
```

#### 3.2.6 Bronze Exceptions Fact
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_fact_exceptions (
  exception_event_id STRING,
  exception_type_id INT,
  dc_id INT,
  date_key INT,
  shift_id INT,
  activity_id INT,
  partner_id INT,
  item_id INT,
  equipment_id INT,
  severity STRING,
  status STRING,
  opened_timestamp TIMESTAMP,
  closed_timestamp TIMESTAMP,
  impact_units INT,
  impact_minutes DECIMAL(10,2),
  load_timestamp TIMESTAMP,
  update_timestamp TIMESTAMP,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/fact_exceptions';
```

### 3.3 Audit Table

#### 3.3.1 Bronze Audit Table
```sql
CREATE TABLE IF NOT EXISTS bronze.bz_audit_log (
  record_id BIGINT,
  source_table STRING,
  load_timestamp TIMESTAMP,
  processed_by STRING,
  processing_time DECIMAL(10,3),
  status STRING,
  records_processed BIGINT,
  records_failed BIGINT,
  error_message STRING,
  batch_id STRING,
  source_file_path STRING,
  source_system STRING
) USING DELTA
LOCATION '/mnt/bronze/audit_log';
```

## 4. Conceptual Data Model Diagram (Tabular Form)

| Source Table | Relationship Key Field | Target Table | Relationship Type |
|--------------|------------------------|--------------|-------------------|
| bz_dim_organization | org_id | bz_dim_distribution_center | One-to-Many |
| bz_dim_distribution_center | dc_id | bz_fact_dc_operations | One-to-Many |
| bz_dim_distribution_center | dc_id | bz_fact_inventory | One-to-Many |
| bz_dim_distribution_center | dc_id | bz_fact_headcount | One-to-Many |
| bz_dim_distribution_center | dc_id | bz_fact_picks | One-to-Many |
| bz_dim_distribution_center | dc_id | bz_fact_kronos | One-to-Many |
| bz_dim_distribution_center | dc_id | bz_fact_exceptions | One-to-Many |
| bz_dim_date | date_key | bz_fact_dc_operations | One-to-Many |
| bz_dim_date | date_key | bz_fact_inventory | One-to-Many |
| bz_dim_date | date_key | bz_fact_headcount | One-to-Many |
| bz_dim_date | date_key | bz_fact_picks | One-to-Many |
| bz_dim_date | date_key | bz_fact_kronos | One-to-Many |
| bz_dim_date | date_key | bz_fact_exceptions | One-to-Many |
| bz_dim_shift | shift_id | bz_fact_dc_operations | One-to-Many |
| bz_dim_shift | shift_id | bz_fact_headcount | One-to-Many |
| bz_dim_shift | shift_id | bz_fact_picks | One-to-Many |
| bz_dim_shift | shift_id | bz_fact_kronos | One-to-Many |
| bz_dim_shift | shift_id | bz_fact_exceptions | One-to-Many |
| bz_dim_partner_type | partner_type_id | bz_dim_partner | One-to-Many |
| bz_dim_partner_type | partner_type_id | bz_fact_headcount | One-to-Many |
| bz_dim_partner | partner_id | bz_fact_dc_operations | One-to-Many |
| bz_dim_partner | partner_id | bz_fact_headcount | One-to-Many |
| bz_dim_partner | partner_id | bz_fact_picks | One-to-Many |
| bz_dim_partner | partner_id | bz_fact_exceptions | One-to-Many |
| bz_dim_partner | partner_id | bz_dim_employee | One-to-Many |
| bz_dim_item | item_id | bz_fact_inventory | One-to-Many |
| bz_dim_item | item_id | bz_fact_picks | One-to-Many |
| bz_dim_item | item_id | bz_fact_exceptions | One-to-Many |
| bz_dim_activity | activity_id | bz_fact_dc_operations | One-to-Many |
| bz_dim_activity | activity_id | bz_fact_picks | One-to-Many |
| bz_dim_activity | activity_id | bz_fact_exceptions | One-to-Many |
| bz_dim_equipment | equipment_id | bz_fact_dc_operations | One-to-Many |
| bz_dim_equipment | equipment_id | bz_fact_exceptions | One-to-Many |
| bz_dim_employee | employee_id | bz_fact_kronos | One-to-Many |
| bz_dim_exception_type | exception_type_id | bz_fact_exceptions | One-to-Many |

## 5. Design Decisions and Assumptions

### 5.1 Design Decisions

1. **Data Types**: 
   - Used INT for ID fields to optimize storage and performance
   - Used STRING instead of VARCHAR for flexibility in Databricks
   - Used DECIMAL(10,2) for monetary and percentage values
   - Used TIMESTAMP for all datetime fields

2. **Storage Format**: 
   - Delta Lake chosen for ACID compliance, time travel, and schema evolution
   - External locations specified for better data organization

3. **Naming Convention**: 
   - All Bronze tables prefixed with `bz_` for clear identification
   - Snake_case naming for consistency with Databricks best practices

4. **Metadata Columns**: 
   - Added load_timestamp, update_timestamp, and source_system to all tables
   - Enables data lineage tracking and audit capabilities

5. **No Constraints**: 
   - Primary keys, foreign keys, and constraints not enforced at Bronze layer
   - Data quality validation deferred to Silver layer

### 5.2 Assumptions

1. **Source Systems**: 
   - Data arrives from multiple source systems (WMS, ERP, Kronos, etc.)
   - Source system identification required for data lineage

2. **Data Volume**: 
   - High-volume transactional data expected
   - Partitioning strategy to be implemented based on date_key

3. **Data Freshness**: 
   - Near real-time data ingestion expected
   - Incremental loading patterns to be implemented

4. **Security**: 
   - Employee data requires PII protection
   - Role-based access controls to be implemented

5. **Performance**: 
   - Query patterns primarily time-based
   - Date partitioning recommended for optimal performance

## 6. Implementation Guidelines

### 6.1 Table Creation Order
1. Create all dimension tables first
2. Create fact tables after dimensions
3. Create audit table last

### 6.2 Data Loading Strategy
1. Use MERGE operations for upserts
2. Implement change data capture where possible
3. Maintain data lineage through audit table

### 6.3 Performance Optimization
1. Partition large tables by date_key
2. Use Z-ordering for frequently queried columns
3. Implement table maintenance procedures (OPTIMIZE, VACUUM)

### 6.4 Monitoring and Governance
1. Track data quality metrics through audit table
2. Implement data freshness monitoring
3. Set up alerting for failed loads

## 7. API Cost

apiCost: 0.000000

---

**Note**: This Bronze layer physical model serves as the foundation for the Medallion architecture, providing raw data storage with minimal transformation while maintaining data lineage and audit capabilities. The Silver layer will implement data quality rules, transformations, and business logic based on this Bronze foundation.