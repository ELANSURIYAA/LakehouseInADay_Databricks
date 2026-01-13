_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: Comprehensive data quality checks for DC Health Meter Reports Silver layer
## *Version*: 1
## *Updated on*: 
_____________________________________________

# Databricks Silver DQ Recommender - DC Health Meter Reports

## Overview

This document provides comprehensive data quality recommendations for the DC Health Meter Reports system based on the analysis of DDL statements, conceptual model, business rules, and constraints. The recommendations are designed to ensure data integrity, accuracy, and consistency across the Silver layer of the Medallion architecture.

## Recommended Data Quality Checks

### 1. Master/Reference Data Quality Checks

#### 1.1 Organization Data Quality

**1.1.1 Organization Hierarchy Integrity Check**
- **Description**: Validate that parent-child relationships in organizational hierarchy are consistent and do not create circular references
- **Rationale**: Prevents infinite loops in hierarchy traversal and ensures proper organizational reporting structure
- **SQL Example**:
```sql
-- Check for circular references in organization hierarchy
WITH RECURSIVE org_hierarchy AS (
  SELECT org_id, parent_org_id, org_name, 1 as level
  FROM silver.sv_org_organization
  WHERE parent_org_id IS NOT NULL
  UNION ALL
  SELECT o.org_id, o.parent_org_id, o.org_name, oh.level + 1
  FROM silver.sv_org_organization o
  JOIN org_hierarchy oh ON o.parent_org_id = oh.org_id
  WHERE oh.level < 10
)
SELECT org_id, org_name
FROM org_hierarchy
WHERE level > 5  -- Flag potential circular references
```

**1.1.2 Organization Type Validation**
- **Description**: Ensure org_type values conform to predefined enumerated values
- **Rationale**: Maintains consistency in organizational classification and enables proper filtering and grouping
- **SQL Example**:
```sql
SELECT org_id, org_name, org_type
FROM silver.sv_org_organization
WHERE org_type NOT IN ('Region', 'BusinessUnit', 'CostCenter', 'Other')
```

**1.1.3 Effective Date Range Validation**
- **Description**: Validate that effective_end_dt >= effective_start_dt for all organization records
- **Rationale**: Ensures logical date ranges for organizational validity periods
- **SQL Example**:
```sql
SELECT org_id, org_name, effective_start_dt, effective_end_dt
FROM silver.sv_org_organization
WHERE effective_end_dt IS NOT NULL 
  AND effective_end_dt < effective_start_dt
```

#### 1.2 Distribution Center Data Quality

**1.2.1 DC Code Uniqueness Check**
- **Description**: Ensure dc_code values are unique across all distribution centers
- **Rationale**: DC codes serve as external identifiers and must be unique for proper system integration
- **SQL Example**:
```sql
SELECT dc_code, COUNT(*) as duplicate_count
FROM silver.sv_dc_distribution_center
WHERE dc_code IS NOT NULL
GROUP BY dc_code
HAVING COUNT(*) > 1
```

**1.2.2 Timezone Validation**
- **Description**: Validate that timezone values are valid IANA timezone identifiers
- **Rationale**: Ensures proper time zone handling for cross-DC analysis and reporting
- **SQL Example**:
```sql
SELECT dc_id, dc_name, timezone
FROM silver.sv_dc_distribution_center
WHERE timezone IS NULL 
   OR timezone NOT RLIKE '^[A-Za-z_]+/[A-Za-z_]+$'
```

**1.2.3 Organizational Reference Integrity**
- **Description**: Ensure all distribution centers reference valid organization records
- **Rationale**: Maintains referential integrity for organizational hierarchy reporting
- **SQL Example**:
```sql
SELECT dc.dc_id, dc.dc_name, dc.org_id
FROM silver.sv_dc_distribution_center dc
LEFT JOIN silver.sv_org_organization org ON dc.org_id = org.org_id
WHERE org.org_id IS NULL
```

#### 1.3 Partner Data Quality

**1.3.1 Partner External ID Uniqueness**
- **Description**: Validate uniqueness of partner_external_id across all partners
- **Rationale**: External IDs serve as unique identifiers from source systems and must remain unique
- **SQL Example**:
```sql
SELECT partner_external_id, COUNT(*) as duplicate_count
FROM silver.sv_partner
WHERE partner_external_id IS NOT NULL
GROUP BY partner_external_id
HAVING COUNT(*) > 1
```

**1.3.2 Partner Status Validation**
- **Description**: Ensure partner status values conform to predefined enumerated values
- **Rationale**: Maintains consistency in partner status classification for accurate workforce reporting
- **SQL Example**:
```sql
SELECT partner_id, first_name, last_name, status
FROM silver.sv_partner
WHERE status NOT IN ('Active', 'Inactive', 'Leave')
```

**1.3.3 Employment Date Logic Validation**
- **Description**: Validate that termination_dt >= hire_dt when both dates are present
- **Rationale**: Ensures logical employment date ranges for accurate tenure calculations
- **SQL Example**:
```sql
SELECT partner_id, first_name, last_name, hire_dt, termination_dt
FROM silver.sv_partner
WHERE termination_dt IS NOT NULL 
  AND termination_dt < hire_dt
```

#### 1.4 Item Data Quality

**1.4.1 Item SKU Uniqueness**
- **Description**: Ensure item_sku values are unique across all items
- **Rationale**: SKUs serve as unique product identifiers and must be unique for proper inventory management
- **SQL Example**:
```sql
SELECT item_sku, COUNT(*) as duplicate_count
FROM silver.sv_item
WHERE item_sku IS NOT NULL
GROUP BY item_sku
HAVING COUNT(*) > 1
```

**1.4.2 Item Description Completeness**
- **Description**: Validate that all active items have non-null, non-empty descriptions
- **Rationale**: Item descriptions are essential for reporting and user interface display
- **SQL Example**:
```sql
SELECT item_id, item_sku, item_description
FROM silver.sv_item
WHERE is_active = true 
  AND (item_description IS NULL OR TRIM(item_description) = '')
```

### 2. Transaction Data Quality Checks

#### 2.1 Activity Event Data Quality

**2.1.1 Quantity Non-Negative Validation**
- **Description**: Ensure qty_handled values are non-negative when present
- **Rationale**: Negative quantities would indicate data corruption or incorrect processing
- **SQL Example**:
```sql
SELECT event_id, dc_id, activity_id, qty_handled
FROM silver.sv_activity_event
WHERE qty_handled IS NOT NULL AND qty_handled < 0
```

**2.1.2 Duration Consistency Check**
- **Description**: Validate that duration_seconds and labor_seconds are logical and consistent
- **Rationale**: Ensures accurate productivity calculations and identifies potential data quality issues
- **SQL Example**:
```sql
SELECT event_id, dc_id, duration_seconds, labor_seconds
FROM silver.sv_activity_event
WHERE duration_seconds IS NOT NULL 
  AND labor_seconds IS NOT NULL
  AND labor_seconds > duration_seconds * 1.5  -- Flag if labor exceeds duration by 50%
```

**2.1.3 Units Per Hour Calculation Validation**
- **Description**: Validate that units_per_hour calculations are consistent with qty_handled and labor_seconds
- **Rationale**: Ensures accuracy of productivity metrics and identifies calculation errors
- **SQL Example**:
```sql
SELECT event_id, dc_id, qty_handled, labor_seconds, units_per_hour,
       CASE WHEN labor_seconds > 0 THEN (qty_handled * 3600.0 / labor_seconds) ELSE NULL END as calculated_uph
FROM silver.sv_activity_event
WHERE qty_handled IS NOT NULL 
  AND labor_seconds IS NOT NULL 
  AND labor_seconds > 0
  AND units_per_hour IS NOT NULL
  AND ABS(units_per_hour - (qty_handled * 3600.0 / labor_seconds)) > 0.1
```

**2.1.4 Source System Consistency**
- **Description**: Validate uniqueness of (source_system, source_event_id) combinations
- **Rationale**: Prevents duplicate processing of events from source systems
- **SQL Example**:
```sql
SELECT source_system, source_event_id, COUNT(*) as duplicate_count
FROM silver.sv_activity_event
WHERE source_system IS NOT NULL AND source_event_id IS NOT NULL
GROUP BY source_system, source_event_id
HAVING COUNT(*) > 1
```

#### 2.2 Inventory Balance Data Quality

**2.2.1 Quantity Non-Negative Validation**
- **Description**: Ensure all quantity fields are non-negative when present
- **Rationale**: Negative inventory quantities indicate data corruption or processing errors
- **SQL Example**:
```sql
SELECT inventory_balance_id, dc_id, item_id, on_hand_qty, allocated_qty, available_qty
FROM silver.sv_inventory_balance
WHERE on_hand_qty < 0 
   OR (allocated_qty IS NOT NULL AND allocated_qty < 0)
   OR (available_qty IS NOT NULL AND available_qty < 0)
   OR (in_transit_qty IS NOT NULL AND in_transit_qty < 0)
   OR (damaged_qty IS NOT NULL AND damaged_qty < 0)
```

**2.2.2 Available Quantity Logic Check**
- **Description**: Validate that available_qty <= on_hand_qty when both are present
- **Rationale**: Available quantity cannot exceed on-hand quantity per business rules
- **SQL Example**:
```sql
SELECT inventory_balance_id, dc_id, item_id, on_hand_qty, available_qty
FROM silver.sv_inventory_balance
WHERE available_qty IS NOT NULL 
  AND on_hand_qty IS NOT NULL
  AND available_qty > on_hand_qty
```

**2.2.3 Inventory Balance Completeness**
- **Description**: Ensure daily inventory snapshots exist for all active items in each DC
- **Rationale**: Complete inventory data is required for accurate availability calculations
- **SQL Example**:
```sql
WITH expected_combinations AS (
  SELECT dc.dc_id, i.item_id, CURRENT_DATE() as expected_date
  FROM silver.sv_dc_distribution_center dc
  CROSS JOIN silver.sv_item i
  WHERE dc.is_active = true AND i.is_active = true
)
SELECT ec.dc_id, ec.item_id, ec.expected_date
FROM expected_combinations ec
LEFT JOIN silver.sv_inventory_balance ib 
  ON ec.dc_id = ib.dc_id 
  AND ec.item_id = ib.item_id 
  AND DATE(ib.as_of_ts_utc) = ec.expected_date
WHERE ib.inventory_balance_id IS NULL
```

#### 2.3 Pick Transaction Data Quality

**2.3.1 Pick Quantity Validation**
- **Description**: Ensure pick_qty is positive and short_pick_qty is non-negative
- **Rationale**: Pick quantities must be positive, short picks can be zero but not negative
- **SQL Example**:
```sql
SELECT pick_txn_id, dc_id, item_id, pick_qty, short_pick_qty
FROM silver.sv_pick_transaction
WHERE pick_qty <= 0 
   OR (short_pick_qty IS NOT NULL AND short_pick_qty < 0)
```

**2.3.2 Pick Status Validation**
- **Description**: Ensure pick_status values conform to predefined enumerated values
- **Rationale**: Maintains consistency in pick status classification for accurate performance reporting
- **SQL Example**:
```sql
SELECT pick_txn_id, dc_id, pick_status
FROM silver.sv_pick_transaction
WHERE pick_status NOT IN ('Picked', 'Short', 'Cancelled')
```

**2.3.3 Short Pick Logic Validation**
- **Description**: Validate that short_pick_qty is only present when pick_status = 'Short'
- **Rationale**: Short pick quantities should only exist for transactions with short pick status
- **SQL Example**:
```sql
SELECT pick_txn_id, dc_id, pick_status, short_pick_qty
FROM silver.sv_pick_transaction
WHERE (pick_status = 'Short' AND (short_pick_qty IS NULL OR short_pick_qty = 0))
   OR (pick_status != 'Short' AND short_pick_qty IS NOT NULL AND short_pick_qty > 0)
```

#### 2.4 Kronos Timecard Data Quality

**2.4.1 Hours Non-Negative Validation**
- **Description**: Ensure all hour fields are non-negative
- **Rationale**: Negative hours indicate data corruption or processing errors
- **SQL Example**:
```sql
SELECT timecard_id, partner_id, regular_hours, overtime_hours, paid_hours
FROM silver.sv_kronos_timecard
WHERE regular_hours < 0 
   OR (overtime_hours IS NOT NULL AND overtime_hours < 0)
   OR paid_hours < 0
```

**2.4.2 Paid Hours Logic Validation**
- **Description**: Validate that paid_hours >= regular_hours + overtime_hours
- **Rationale**: Paid hours should equal or exceed the sum of regular and overtime hours
- **SQL Example**:
```sql
SELECT timecard_id, partner_id, regular_hours, overtime_hours, paid_hours
FROM silver.sv_kronos_timecard
WHERE paid_hours < (regular_hours + COALESCE(overtime_hours, 0))
```

**2.4.3 Clock Time Logic Validation**
- **Description**: Validate that clock_out_ts_local > clock_in_ts_local when both are present
- **Rationale**: Clock out time must be after clock in time for logical work periods
- **SQL Example**:
```sql
SELECT timecard_id, partner_id, work_date, clock_in_ts_local, clock_out_ts_local
FROM silver.sv_kronos_timecard
WHERE clock_in_ts_local IS NOT NULL 
  AND clock_out_ts_local IS NOT NULL
  AND clock_out_ts_local <= clock_in_ts_local
```

#### 2.5 Exception Event Data Quality

**2.5.1 Exception Status Validation**
- **Description**: Ensure exception_status values conform to predefined enumerated values
- **Rationale**: Maintains consistency in exception status classification for proper workflow management
- **SQL Example**:
```sql
SELECT exception_event_id, dc_id, exception_status
FROM silver.sv_exception_event
WHERE exception_status NOT IN ('Open', 'InProgress', 'Resolved', 'Closed')
```

**2.5.2 Severity Consistency Check**
- **Description**: Validate that severity_override values are consistent with exception type severity when present
- **Rationale**: Severity overrides should be logical and within acceptable ranges
- **SQL Example**:
```sql
SELECT ee.exception_event_id, ee.dc_id, et.severity as type_severity, ee.severity_override
FROM silver.sv_exception_event ee
JOIN silver.sv_exception_type et ON ee.exception_type_id = et.exception_type_id
WHERE ee.severity_override IS NOT NULL 
  AND ee.severity_override NOT IN ('Low', 'Medium', 'High', 'Critical')
```

### 3. Cross-Table Referential Integrity Checks

#### 3.1 Foreign Key Validation

**3.1.1 Activity Event Foreign Key Validation**
- **Description**: Validate that all foreign key references in activity events point to valid records
- **Rationale**: Ensures referential integrity for proper join operations and reporting
- **SQL Example**:
```sql
-- Check DC reference
SELECT ae.event_id, ae.dc_id
FROM silver.sv_activity_event ae
LEFT JOIN silver.sv_dc_distribution_center dc ON ae.dc_id = dc.dc_id
WHERE dc.dc_id IS NULL

UNION ALL

-- Check Activity reference
SELECT ae.event_id, ae.activity_id
FROM silver.sv_activity_event ae
LEFT JOIN silver.sv_activity a ON ae.activity_id = a.activity_id
WHERE ae.activity_id IS NOT NULL AND a.activity_id IS NULL
```

**3.1.2 Partner Assignment Validation**
- **Description**: Validate that partners are assigned to appropriate distribution centers
- **Rationale**: Ensures partners are working in their assigned locations for accurate reporting
- **SQL Example**:
```sql
SELECT ae.event_id, ae.dc_id, ae.partner_id, p.home_dc_id
FROM silver.sv_activity_event ae
JOIN silver.sv_partner p ON ae.partner_id = p.partner_id
WHERE ae.partner_id IS NOT NULL 
  AND p.home_dc_id IS NOT NULL
  AND ae.dc_id != p.home_dc_id
```

### 4. Business Rule Validation Checks

#### 4.1 Health Score Component Validation

**4.1.1 Health Score Range Validation**
- **Description**: Validate that all health scores are between 0 and 100
- **Rationale**: Health scores must be within the defined 0-100 range per business rules
- **SQL Example**:
```sql
SELECT dc_id, date_key, health_score_overall, ops_score, inv_score, picks_score, labor_score, kronos_score, exceptions_score
FROM silver.sv_health_scorecard
WHERE health_score_overall < 0 OR health_score_overall > 100
   OR ops_score < 0 OR ops_score > 100
   OR inv_score < 0 OR inv_score > 100
   OR picks_score < 0 OR picks_score > 100
   OR labor_score < 0 OR labor_score > 100
   OR kronos_score < 0 OR kronos_score > 100
   OR exceptions_score < 0 OR exceptions_score > 100
```

#### 4.2 Percentage Field Validation

**4.2.1 Percentage Range Validation**
- **Description**: Validate that all percentage fields are between 0 and 100 (or 0 and 1 depending on format)
- **Rationale**: Percentage values must be within logical ranges per business rules
- **SQL Example**:
```sql
SELECT dc_id, date_key, on_time_shipping_pct, pick_accuracy_pct, inventory_availability_pct
FROM silver.sv_operations_summary
WHERE on_time_shipping_pct < 0 OR on_time_shipping_pct > 100
   OR pick_accuracy_pct < 0 OR pick_accuracy_pct > 100
   OR inventory_availability_pct < 0 OR inventory_availability_pct > 100
```

#### 4.3 Variance Calculation Validation

**4.3.1 Staffing Variance Logic Check**
- **Description**: Validate staffing variance calculations when planned values are available
- **Rationale**: Ensures accurate variance calculations for workforce management reporting
- **SQL Example**:
```sql
SELECT dc_id, date_key, shift_id, planned_headcount, actual_headcount, staffing_variance_pct,
       CASE WHEN planned_headcount > 0 
            THEN ((actual_headcount - planned_headcount) / planned_headcount) * 100 
            ELSE NULL END as calculated_variance
FROM silver.sv_labor_summary
WHERE planned_headcount IS NOT NULL 
  AND actual_headcount IS NOT NULL
  AND planned_headcount > 0
  AND ABS(staffing_variance_pct - ((actual_headcount - planned_headcount) / planned_headcount) * 100) > 0.1
```

### 5. Data Completeness Checks

#### 5.1 Mandatory Field Completeness

**5.1.1 Critical Field Null Check**
- **Description**: Validate that mandatory fields are not null across all tables
- **Rationale**: Critical fields must be populated for proper system functionality
- **SQL Example**:
```sql
-- Activity Events
SELECT 'activity_event' as table_name, event_id, 'dc_id' as missing_field
FROM silver.sv_activity_event WHERE dc_id IS NULL
UNION ALL
SELECT 'activity_event' as table_name, event_id, 'activity_id' as missing_field
FROM silver.sv_activity_event WHERE activity_id IS NULL
UNION ALL
-- Pick Transactions
SELECT 'pick_transaction' as table_name, pick_txn_id, 'dc_id' as missing_field
FROM silver.sv_pick_transaction WHERE dc_id IS NULL
UNION ALL
SELECT 'pick_transaction' as table_name, pick_txn_id, 'item_id' as missing_field
FROM silver.sv_pick_transaction WHERE item_id IS NULL
```

#### 5.2 Daily Data Completeness

**5.2.1 Daily Health Score Completeness**
- **Description**: Validate that health score data exists for all active DCs for each business day
- **Rationale**: Complete daily health scores are required for trending and performance monitoring
- **SQL Example**:
```sql
WITH business_dates AS (
  SELECT date_key
  FROM silver.sv_date_dimension
  WHERE date_key >= CURRENT_DATE() - INTERVAL 7 DAYS
    AND is_business_day = true
),
active_dcs AS (
  SELECT dc_id
  FROM silver.sv_dc_distribution_center
  WHERE is_active = true
)
SELECT bd.date_key, adc.dc_id
FROM business_dates bd
CROSS JOIN active_dcs adc
LEFT JOIN silver.sv_health_scorecard hs 
  ON bd.date_key = hs.date_key AND adc.dc_id = hs.dc_id
WHERE hs.dc_id IS NULL
```

### 6. Data Quality Monitoring Framework

#### 6.1 Data Quality Score Calculation

**6.1.1 Overall Data Quality Score**
- **Description**: Calculate comprehensive data quality score based on all validation checks
- **Rationale**: Provides single metric for monitoring overall data quality health
- **SQL Example**:
```sql
WITH quality_metrics AS (
  SELECT 
    'completeness' as metric_type,
    COUNT(CASE WHEN dc_id IS NULL THEN 1 END) as failed_checks,
    COUNT(*) as total_checks
  FROM silver.sv_activity_event
  
  UNION ALL
  
  SELECT 
    'accuracy' as metric_type,
    COUNT(CASE WHEN qty_handled < 0 THEN 1 END) as failed_checks,
    COUNT(*) as total_checks
  FROM silver.sv_activity_event
  WHERE qty_handled IS NOT NULL
)
SELECT 
  metric_type,
  (1.0 - CAST(failed_checks AS DOUBLE) / total_checks) * 100 as quality_score_pct
FROM quality_metrics
```

### 7. Implementation Guidelines

#### 7.1 Automated Data Quality Pipeline

1. **Batch Processing**: Implement data quality checks as part of Silver layer ETL pipeline
2. **Real-time Monitoring**: Set up streaming quality checks for critical data flows
3. **Alert Thresholds**: Configure alerts when quality scores fall below acceptable thresholds
4. **Quarantine Process**: Implement data quarantine for records failing critical quality checks

#### 7.2 Data Quality Reporting

1. **Daily Quality Dashboard**: Create automated dashboard showing quality metrics by table and check type
2. **Trend Analysis**: Track quality score trends over time to identify degradation patterns
3. **Root Cause Analysis**: Implement drill-down capabilities to identify specific quality issues
4. **SLA Monitoring**: Track data quality SLAs and generate compliance reports

#### 7.3 Data Remediation Process

1. **Automated Fixes**: Implement automated remediation for common data quality issues
2. **Manual Review Queue**: Create workflow for manual review of complex quality issues
3. **Source System Feedback**: Establish process to provide feedback to source systems on quality issues
4. **Historical Correction**: Implement process for correcting historical data quality issues

## API Cost

**apiCost**: 0.00 USD

---

**Note**: This comprehensive data quality framework ensures the integrity and reliability of the DC Health Meter Reports system by implementing robust validation processes across all data layers and business domains.