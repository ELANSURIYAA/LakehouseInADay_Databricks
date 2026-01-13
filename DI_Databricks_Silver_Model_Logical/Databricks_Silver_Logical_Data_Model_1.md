_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: Silver Layer Logical Data Model for DC Health Meter Reports in Medallion architecture
## *Version*: 1
## *Updated on*: 
_____________________________________________

# Databricks Silver Layer Logical Data Model - DC Health Meter Reports

## 1. Silver Layer Logical Model

### 1.1 Master/Reference Tables

#### 1.1.1 Si_Organization
**Description**: Silver layer table for organizational hierarchy and structure information with cleansed and standardized data

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| org_name | Name of the organizational unit | String |
| org_type | Type of organization (Region/BusinessUnit/CostCenter/Other) | String |
| parent_org_name | Name of parent organizational unit | String |
| effective_start_dt | Start date when organization became effective | Date |
| effective_end_dt | End date when organization became ineffective | Date |
| is_active | Flag indicating if organization is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |
| source_system | Source system from which data originated | String |

#### 1.1.2 Si_Distribution_Center
**Description**: Silver layer table for distribution center master data with validated and cleansed information

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
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |
| source_system | Source system from which data originated | String |

#### 1.1.3 Si_Shift
**Description**: Silver layer table for shift definitions per distribution center with standardized time formats

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| dc_name | Name of the distribution center | String |
| shift_name | Name identifier for the shift period | String |
| shift_code | Code identifier for the shift | String |
| start_time_local | Local start time for the shift (HH:MM format) | String |
| end_time_local | Local end time for the shift (HH:MM format) | String |
| crosses_midnight_flag | Flag indicating if shift crosses midnight | Boolean |
| is_active | Flag indicating if shift is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |
| source_system | Source system from which data originated | String |

#### 1.1.4 Si_Partner_Type
**Description**: Silver layer table for partner classification types with standardized categories

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| partner_type_name | Name of the partner type classification | String |
| description | Detailed description of partner type characteristics | String |
| is_active | Flag indicating if partner type is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |
| source_system | Source system from which data originated | String |

#### 1.1.5 Si_Partner
**Description**: Silver layer table for worker/associate/vendor partner entities with cleansed personal information

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
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |
| source_system | Source system from which data originated | String |

#### 1.1.6 Si_Item
**Description**: Silver layer table for item/SKU master data with standardized product information

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| item_sku | Stock keeping unit identifier | String |
| item_description | Description of the item/product | String |
| item_category | Product category classification | String |
| uom | Unit of measure for the item | String |
| is_active | Flag indicating if item is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |
| source_system | Source system from which data originated | String |

#### 1.1.7 Si_Equipment
**Description**: Silver layer table for equipment/assets used in distribution center activities with validated status information

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| dc_name | Name of the distribution center | String |
| equipment_type | Classification of equipment type | String |
| equipment_code | Tag/asset code for the equipment | String |
| equipment_status | Current operational status (InService/OutOfService/Maintenance) | String |
| effective_start_dt | Date when equipment became effective | Date |
| effective_end_dt | Date when equipment became ineffective | Date |
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |
| source_system | Source system from which data originated | String |

#### 1.1.8 Si_Activity
**Description**: Silver layer table for activity reference data with standardized activity classifications

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| activity_code | Code identifier for the activity | String |
| activity_name | Name of the operational activity | String |
| activity_group | Group classification (Inbound/Outbound/Inventory) | String |
| is_active | Flag indicating if activity is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |
| source_system | Source system from which data originated | String |

#### 1.1.9 Si_Exception_Type
**Description**: Silver layer table for exception taxonomy with standardized severity levels

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| exception_code | Code identifier for the exception type | String |
| exception_name | Name of the exception type | String |
| severity | Impact level (Low/Medium/High/Critical) | String |
| description | Detailed description of the exception type | String |
| is_active | Flag indicating if exception type is currently active | Boolean |
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |
| source_system | Source system from which data originated | String |

### 1.2 Transaction/Event Tables (Fact Sources)

#### 1.2.1 Si_Activity_Event
**Description**: Silver layer table for atomic operational events with validated and cleansed operational data

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
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |

#### 1.2.2 Si_Inventory_Balance
**Description**: Silver layer table for inventory position snapshots with validated quantity data

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
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |

#### 1.2.3 Si_Pick_Transaction
**Description**: Silver layer table for picking transactions with validated pick data and standardized status codes

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
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |

#### 1.2.4 Si_Headcount_Record
**Description**: Silver layer table for headcount readings with validated headcount data

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
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |

#### 1.2.5 Si_Kronos_Timecard
**Description**: Silver layer table for timecard/punch data from Kronos with validated time calculations

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
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |

#### 1.2.6 Si_Exception_Event
**Description**: Silver layer table for operational exceptions with validated exception data and standardized status codes

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
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated in Silver layer | Timestamp |

### 1.3 Data Quality and Error Management Tables

#### 1.3.1 Si_Data_Quality_Errors
**Description**: Silver layer table to store data validation errors and quality issues identified during data processing

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| error_id | Unique identifier for the error record | String |
| source_table | Name of the source table where error was detected | String |
| source_record_id | Identifier of the source record with error | String |
| error_type | Type of data quality error (Missing/Invalid/Duplicate/Constraint) | String |
| error_category | Category of error (Data_Type/Business_Rule/Referential_Integrity) | String |
| error_description | Detailed description of the data quality issue | String |
| error_field | Field name where error was detected | String |
| error_value | Value that caused the error | String |
| expected_value | Expected value or format | String |
| severity | Severity level of the error (Low/Medium/High/Critical) | String |
| error_timestamp | Timestamp when error was detected | Timestamp |
| resolution_status | Status of error resolution (Open/InProgress/Resolved/Ignored) | String |
| resolution_notes | Notes about error resolution | String |
| load_timestamp | Timestamp when record was loaded into Silver layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |

#### 1.3.2 Si_Pipeline_Audit
**Description**: Silver layer table to store audit details from pipeline execution and data processing activities

| Column Name | Description | Data Type |
|-------------|-------------|----------|
| audit_id | Unique identifier for the audit record | String |
| pipeline_name | Name of the data pipeline | String |
| pipeline_run_id | Unique identifier for the pipeline run | String |
| source_table | Name of the source table being processed | String |
| target_table | Name of the target table being loaded | String |
| process_start_timestamp | Timestamp when processing started | Timestamp |
| process_end_timestamp | Timestamp when processing completed | Timestamp |
| processing_duration_seconds | Duration of processing in seconds | Integer |
| records_read | Number of records read from source | Integer |
| records_processed | Number of records successfully processed | Integer |
| records_inserted | Number of records inserted into target | Integer |
| records_updated | Number of records updated in target | Integer |
| records_failed | Number of records that failed processing | Integer |
| error_count | Total number of errors encountered | Integer |
| warning_count | Total number of warnings generated | Integer |
| data_quality_score | Overall data quality score for the batch | Decimal |
| pipeline_status | Status of pipeline execution (Success/Failed/Warning/Partial) | String |
| error_message | Error message if pipeline failed | String |
| processed_by | System or user that executed the pipeline | String |
| load_timestamp | Timestamp when audit record was created | Timestamp |
| update_timestamp | Timestamp when audit record was last updated | Timestamp |

## 2. Conceptual Data Model Diagram (Tabular Form)

| Source Table | Relationship Key Field | Target Table | Relationship Type |
|--------------|------------------------|--------------|-------------------|
| Si_Organization | org_name | Si_Distribution_Center | One-to-Many |
| Si_Distribution_Center | dc_name | Si_Shift | One-to-Many |
| Si_Partner_Type | partner_type_name | Si_Partner | One-to-Many |
| Si_Distribution_Center | dc_name | Si_Equipment | One-to-Many |
| Si_Distribution_Center | dc_name | Si_Activity_Event | One-to-Many |
| Si_Partner | partner_external_id | Si_Activity_Event | Many-to-One |
| Si_Item | item_sku | Si_Activity_Event | Many-to-One |
| Si_Equipment | equipment_code | Si_Activity_Event | Many-to-One |
| Si_Shift | shift_name | Si_Activity_Event | Many-to-One |
| Si_Activity | activity_name | Si_Activity_Event | Many-to-One |
| Si_Distribution_Center | dc_name | Si_Inventory_Balance | One-to-Many |
| Si_Item | item_sku | Si_Inventory_Balance | Many-to-One |
| Si_Distribution_Center | dc_name | Si_Pick_Transaction | One-to-Many |
| Si_Item | item_sku | Si_Pick_Transaction | Many-to-One |
| Si_Partner | partner_external_id | Si_Pick_Transaction | Many-to-One |
| Si_Shift | shift_name | Si_Pick_Transaction | Many-to-One |
| Si_Equipment | equipment_code | Si_Pick_Transaction | Many-to-One |
| Si_Distribution_Center | dc_name | Si_Headcount_Record | One-to-Many |
| Si_Partner | partner_external_id | Si_Headcount_Record | Many-to-One |
| Si_Shift | shift_name | Si_Headcount_Record | Many-to-One |
| Si_Activity | activity_name | Si_Headcount_Record | Many-to-One |
| Si_Partner | partner_external_id | Si_Kronos_Timecard | Many-to-One |
| Si_Distribution_Center | dc_name | Si_Kronos_Timecard | Many-to-One |
| Si_Shift | shift_name | Si_Kronos_Timecard | Many-to-One |
| Si_Exception_Type | exception_type_name | Si_Exception_Event | One-to-Many |
| Si_Distribution_Center | dc_name | Si_Exception_Event | One-to-Many |
| Si_Partner | partner_external_id | Si_Exception_Event | Many-to-One |
| Si_Item | item_sku | Si_Exception_Event | Many-to-One |
| Si_Shift | shift_name | Si_Exception_Event | Many-to-One |
| Si_Activity_Event | source_event_id | Si_Exception_Event | One-to-One |
| Si_Data_Quality_Errors | source_table | All Silver Tables | Many-to-One |
| Si_Pipeline_Audit | source_table | All Silver Tables | Many-to-One |
| Si_Pipeline_Audit | target_table | All Silver Tables | Many-to-One |

## 3. Design Rationale and Key Assumptions

### 3.1 Design Decisions

1. **Naming Convention**: All Silver layer tables use the "Si_" prefix to clearly identify them as Silver layer entities, following the requirement for the first 3 characters to be 'Si_'.

2. **Key Field Exclusion**: Primary key and foreign key fields from the Bronze layer are excluded, focusing on business attributes and natural keys for relationships.

3. **Data Quality Integration**: Dedicated tables (Si_Data_Quality_Errors and Si_Pipeline_Audit) are included to capture data validation errors and pipeline execution audit details.

4. **Data Type Standardization**: Consistent data types are applied across all tables with proper precision for decimal fields and standardized string lengths.

5. **Metadata Preservation**: Standard metadata columns (load_timestamp, update_timestamp, source_system) are maintained from Bronze layer for lineage tracking.

6. **Natural Key Relationships**: Business natural keys (dc_name, item_sku, partner_external_id, etc.) are used for establishing relationships between tables.

### 3.2 Key Assumptions

1. **Data Cleansing**: Silver layer assumes data has been validated, cleansed, and standardized from Bronze layer raw data.

2. **Business Rule Application**: Business rules and constraints from the constraints document are applied during Silver layer processing.

3. **Error Handling**: All data quality issues are captured in the Si_Data_Quality_Errors table rather than rejecting records.

4. **Audit Trail**: Complete audit trail is maintained through Si_Pipeline_Audit table for compliance and monitoring.

5. **Time Zone Consistency**: UTC timestamps are standardized for all event data with local time conversions handled appropriately.

6. **Referential Integrity**: Natural key relationships are maintained through business logic rather than database constraints.

### 3.3 Data Quality and Validation

1. **Completeness Validation**: Mandatory fields are validated according to constraints document requirements.

2. **Accuracy Validation**: Data accuracy rules are applied including health score calculations and throughput validations.

3. **Format Standardization**: All data formats are standardized including timestamps, percentages, and enumerated values.

4. **Consistency Checks**: Cross-table consistency is validated for DC names, partner relationships, and organizational hierarchy.

5. **Business Rule Enforcement**: All business rules from the constraints document are implemented in Silver layer processing.

## 4. API Cost

**apiCost**: 0.000000