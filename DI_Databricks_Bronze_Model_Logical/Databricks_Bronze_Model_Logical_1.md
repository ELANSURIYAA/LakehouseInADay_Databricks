_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: Databricks Bronze Model Logical for DC Health Meter Reports
## *Version*: 1
## *Updated on*: 
_____________________________________________

# Databricks Bronze Model Logical for DC Health Meter Reports

## 1. PII Classification

| Column Names | Reason why it is classified as PII |
|--------------|------------------------------------|
| first_name | Contains personal identifying information - individual's first name |
| last_name | Contains personal identifying information - individual's last name |
| partner_external_id | Contains employee badge ID/HR ID which can identify specific individuals |
| hire_dt | Contains employment start date which is personal employment information |
| termination_dt | Contains employment termination date which is sensitive personal employment information |
| address_line1 | Contains physical address information for distribution centers which could be sensitive location data |
| address_line2 | Contains physical address information for distribution centers which could be sensitive location data |
| city | Contains location information that could be used for identification purposes |
| state_prov | Contains location information that could be used for identification purposes |
| postal_code | Contains specific location identifier that could be used for identification purposes |
| clock_in_ts_local | Contains specific work timing information that could identify individual work patterns |
| clock_out_ts_local | Contains specific work timing information that could identify individual work patterns |
| absence_code | Contains personal absence information which is sensitive employee data |

## 2. Bronze Layer Logical Model

### 2.1 Bz_Organization
**Description**: Bronze layer table for organizational hierarchy and structure information

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| org_name | Name of the organizational unit | String |
| org_type | Type of organization (Region/BusinessUnit/CostCenter/Other) | String |
| parent_org_name | Name of parent organizational unit | String |
| effective_start_dt | Start date when organization became effective | Date |
| effective_end_dt | End date when organization became ineffective | Date |
| is_active | Flag indicating if organization is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |
| source_system | Source system from which data originated | String |

### 2.2 Bz_Distribution_Center
**Description**: Bronze layer table for distribution center master data

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| dc_name | Business name identifier for the distribution center | String |
| dc_code | External/site code for the distribution center | String |
| org_name | Name of the organization this DC belongs to | String |
| address_line1 | First line of physical address | String |
| address_line2 | Second line of physical address | String |
| city | City where distribution center is located | String |
| state_prov | State or province of distribution center location | String |
| postal_code | Postal code of distribution center location | String |
| country | Country where distribution center is located | String |
| timezone | IANA timezone identifier for the distribution center | String |
| is_active | Flag indicating if distribution center is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |
| source_system | Source system from which data originated | String |

### 2.3 Bz_Shift
**Description**: Bronze layer table for shift definitions per distribution center

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| dc_name | Name of the distribution center | String |
| shift_name | Name identifier for the shift period | String |
| shift_code | Code identifier for the shift | String |
| start_time_local | Local start time for the shift (HH:MM format) | String |
| end_time_local | Local end time for the shift (HH:MM format) | String |
| crosses_midnight_flag | Flag indicating if shift crosses midnight | Boolean |
| is_active | Flag indicating if shift is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |
| source_system | Source system from which data originated | String |

### 2.4 Bz_Partner_Type
**Description**: Bronze layer table for partner classification types

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| partner_type_name | Name of the partner type classification | String |
| description | Detailed description of partner type characteristics | String |
| is_active | Flag indicating if partner type is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |
| source_system | Source system from which data originated | String |

### 2.5 Bz_Partner
**Description**: Bronze layer table for worker/associate/vendor partner entities

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| partner_type_name | Name of the partner type classification | String |
| partner_external_id | Badge ID/HR ID/vendor worker identifier | String |
| first_name | First name of the partner | String |
| last_name | Last name of the partner | String |
| hire_dt | Date when partner was hired | Date |
| termination_dt | Date when partner was terminated (if applicable) | Date |
| home_dc_name | Name of home distribution center | String |
| status | Current status of partner (Active/Inactive/Leave) | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |
| source_system | Source system from which data originated | String |

### 2.6 Bz_Item
**Description**: Bronze layer table for item/SKU master data

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| item_sku | Stock keeping unit identifier | String |
| item_description | Description of the item/product | String |
| item_category | Product category classification | String |
| uom | Unit of measure for the item | String |
| is_active | Flag indicating if item is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |
| source_system | Source system from which data originated | String |

### 2.7 Bz_Equipment
**Description**: Bronze layer table for equipment/assets used in distribution center activities

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| dc_name | Name of the distribution center | String |
| equipment_type | Classification of equipment type | String |
| equipment_code | Tag/asset code for the equipment | String |
| equipment_status | Current operational status (InService/OutOfService/Maintenance) | String |
| effective_start_dt | Date when equipment became effective | Date |
| effective_end_dt | Date when equipment became ineffective | Date |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |
| source_system | Source system from which data originated | String |

### 2.8 Bz_Activity
**Description**: Bronze layer table for activity reference data

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| activity_code | Code identifier for the activity | String |
| activity_name | Name of the operational activity | String |
| activity_group | Group classification (Inbound/Outbound/Inventory) | String |
| is_active | Flag indicating if activity is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |
| source_system | Source system from which data originated | String |

### 2.9 Bz_Exception_Type
**Description**: Bronze layer table for exception taxonomy

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| exception_code | Code identifier for the exception type | String |
| exception_name | Name of the exception type | String |
| severity | Impact level (Low/Medium/High/Critical) | String |
| description | Detailed description of the exception type | String |
| is_active | Flag indicating if exception type is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |
| source_system | Source system from which data originated | String |

### 2.10 Bz_Activity_Event
**Description**: Bronze layer table for atomic operational events (Operations Fact Source)

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| dc_name | Name of the distribution center | String |
| event_ts_utc | UTC timestamp when event occurred | Timestamp |
| shift_name | Name of the shift during which event occurred | String |
| partner_external_id | External identifier of partner who performed activity | String |
| activity_name | Name of the activity performed | String |
| item_sku | SKU of item involved in the activity | String |
| equipment_code | Code of equipment used in the activity | String |
| source_system | Source system that generated the event | String |
| source_event_id | Identifier in the source system | String |
| location_code | Aisle/bin/door location if available | String |
| qty_handled | Quantity handled during the activity | Decimal |
| duration_seconds | Duration of activity in seconds | Integer |
| labor_seconds | Labor time spent in seconds | Integer |
| units_per_hour | Productivity measure in units per hour | Decimal |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |

### 2.11 Bz_Inventory_Balance
**Description**: Bronze layer table for inventory position snapshots (Inventory Fact Source)

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| dc_name | Name of the distribution center | String |
| item_sku | SKU of the inventory item | String |
| as_of_ts_utc | UTC timestamp of inventory snapshot | Timestamp |
| location_code | Location code where inventory is stored | String |
| on_hand_qty | Quantity physically on hand | Decimal |
| allocated_qty | Quantity allocated for orders | Decimal |
| available_qty | Quantity available for allocation | Decimal |
| in_transit_qty | Quantity in transit | Decimal |
| damaged_qty | Quantity that is damaged | Decimal |
| source_system | Source system that provided inventory data | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |

### 2.12 Bz_Pick_Transaction
**Description**: Bronze layer table for picking transactions (Picks Fact Source)

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| dc_name | Name of the distribution center | String |
| pick_ts_utc | UTC timestamp when pick occurred | Timestamp |
| shift_name | Name of the shift during which pick occurred | String |
| partner_external_id | External identifier of partner who performed pick | String |
| item_sku | SKU of item being picked | String |
| equipment_code | Code of equipment used for picking | String |
| order_id | Order identifier | String |
| order_line_id | Order line identifier | String |
| wave_id | Wave identifier | String |
| pick_location_code | Location code where item was picked | String |
| pick_qty | Quantity picked | Decimal |
| short_pick_qty | Quantity short picked | Decimal |
| pick_status | Status of pick (Picked/Short/Cancelled) | String |
| source_system | Source system that generated pick transaction | String |
| source_pick_id | Identifier in the source system | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |

### 2.13 Bz_Headcount_Record
**Description**: Bronze layer table for headcount readings (Headcount Fact Source)

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| dc_name | Name of the distribution center | String |
| as_of_ts_utc | UTC timestamp of headcount reading | Timestamp |
| shift_name | Name of the shift | String |
| partner_external_id | External identifier of partner (for individual records) | String |
| activity_name | Name of activity for which headcount is recorded | String |
| headcount_type | Type of headcount (Actual/Planned/OnFloor) | String |
| headcount_value | Numeric value of headcount | Integer |
| source_system | Source system that provided headcount data | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |

### 2.14 Bz_Kronos_Timecard
**Description**: Bronze layer table for timecard/punch data from Kronos (Kronos Fact Source)

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| kronos_timecard_id | Source key from Kronos system | String |
| partner_external_id | External identifier of partner | String |
| dc_name | Name of the distribution center | String |
| shift_name | Name of the shift | String |
| work_date | Local date at DC when work was performed | Date |
| clock_in_ts_local | Local timestamp when partner clocked in | Timestamp |
| clock_out_ts_local | Local timestamp when partner clocked out | Timestamp |
| regular_hours | Number of regular hours worked | Decimal |
| overtime_hours | Number of overtime hours worked | Decimal |
| paid_hours | Total paid hours | Decimal |
| absence_code | Code indicating type of absence if applicable | String |
| source_system | Source system (typically Kronos) | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |

### 2.15 Bz_Exception_Event
**Description**: Bronze layer table for operational exceptions (Exceptions Fact Source)

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| exception_type_name | Name of the exception type | String |
| dc_name | Name of the distribution center | String |
| exception_ts_utc | UTC timestamp when exception occurred | Timestamp |
| shift_name | Name of the shift during which exception occurred | String |
| partner_external_id | External identifier of partner involved in exception | String |
| item_sku | SKU of item involved in exception | String |
| activity_event_source_id | Source identifier of related activity event | String |
| exception_status | Current status (Open/InProgress/Resolved/Closed) | String |
| severity_override | Override severity if different from type default | String |
| notes | Additional notes about the exception | String |
| source_system | Source system that generated exception | String |
| source_exception_id | Identifier in the source system | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Bronze layer | Timestamp |

## 3. Audit Table Design

### 3.1 Bz_Audit_Log
**Description**: Audit table to track data processing activities across all Bronze layer tables

| Field Name | Description | Data Type |
|------------|-------------|----------|
| record_id | Unique identifier for audit record | String |
| source_table | Name of the Bronze layer table being audited | String |
| load_timestamp | Timestamp when data was loaded | Timestamp |
| processed_by | System or process that loaded the data | String |
| processing_time | Time taken to process the data (in seconds) | Decimal |
| status | Status of the processing (Success/Failed/Warning) | String |

## 4. Conceptual Data Model Diagram (Tabular Form)

| Source Table | Connected to Target Table | Key Field |
|--------------|----------------------------|----------|
| Bz_Organization | Bz_Distribution_Center | org_name |
| Bz_Distribution_Center | Bz_Shift | dc_name |
| Bz_Partner_Type | Bz_Partner | partner_type_name |
| Bz_Distribution_Center | Bz_Equipment | dc_name |
| Bz_Distribution_Center | Bz_Activity_Event | dc_name |
| Bz_Partner | Bz_Activity_Event | partner_external_id |
| Bz_Item | Bz_Activity_Event | item_sku |
| Bz_Equipment | Bz_Activity_Event | equipment_code |
| Bz_Shift | Bz_Activity_Event | shift_name |
| Bz_Activity | Bz_Activity_Event | activity_name |
| Bz_Distribution_Center | Bz_Inventory_Balance | dc_name |
| Bz_Item | Bz_Inventory_Balance | item_sku |
| Bz_Distribution_Center | Bz_Pick_Transaction | dc_name |
| Bz_Item | Bz_Pick_Transaction | item_sku |
| Bz_Partner | Bz_Pick_Transaction | partner_external_id |
| Bz_Shift | Bz_Pick_Transaction | shift_name |
| Bz_Equipment | Bz_Pick_Transaction | equipment_code |
| Bz_Distribution_Center | Bz_Headcount_Record | dc_name |
| Bz_Partner | Bz_Headcount_Record | partner_external_id |
| Bz_Shift | Bz_Headcount_Record | shift_name |
| Bz_Activity | Bz_Headcount_Record | activity_name |
| Bz_Partner | Bz_Kronos_Timecard | partner_external_id |
| Bz_Distribution_Center | Bz_Kronos_Timecard | dc_name |
| Bz_Shift | Bz_Kronos_Timecard | shift_name |
| Bz_Exception_Type | Bz_Exception_Event | exception_type_name |
| Bz_Distribution_Center | Bz_Exception_Event | dc_name |
| Bz_Partner | Bz_Exception_Event | partner_external_id |
| Bz_Item | Bz_Exception_Event | item_sku |
| Bz_Shift | Bz_Exception_Event | shift_name |

## 5. Design Rationale and Key Assumptions

### 5.1 Design Decisions
1. **Naming Convention**: All Bronze layer tables use the "Bz_" prefix to clearly identify them as Bronze layer entities
2. **Key Field Exclusion**: Primary key and foreign key fields from source systems are excluded, focusing on business attributes
3. **Metadata Columns**: Standard metadata columns (load_timestamp, update_timestamp, source_system) are added to all tables for audit and lineage tracking
4. **Natural Keys**: Business natural keys (like dc_name, item_sku, partner_external_id) are used for relationships instead of surrogate keys
5. **Data Types**: Logical data types are used (String, Integer, Decimal, Date, Timestamp, Boolean) rather than physical storage types

### 5.2 Key Assumptions
1. **Source Data Quality**: Assumes source systems provide consistent and valid data for natural key relationships
2. **Time Zone Handling**: UTC timestamps are used for all event data, with local times preserved where business-relevant
3. **PII Handling**: PII fields are identified but retained in Bronze layer for complete source data preservation
4. **Incremental Loading**: Design supports both full and incremental data loading patterns
5. **Data Retention**: No specific retention policies applied at Bronze layer - raw data preservation is prioritized

### 5.3 Compliance Considerations
1. **GDPR Compliance**: PII fields are clearly identified and can be masked or encrypted in downstream layers
2. **Data Lineage**: Source system tracking enables full data lineage from source to Bronze layer
3. **Audit Trail**: Comprehensive audit logging supports compliance reporting and data governance

## 6. API Cost

apiCost: 0.000000