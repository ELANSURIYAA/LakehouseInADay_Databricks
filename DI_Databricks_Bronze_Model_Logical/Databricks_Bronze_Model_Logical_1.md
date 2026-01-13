_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: Comprehensive logical data model for Databricks Bronze layer in medallion architecture for DC Health Meter Reports
## *Version*: 1
## *Updated on*: 
_____________________________________________

# Databricks Bronze Layer Logical Data Model

## 1. PII Classification

| Column Names | Reason why it is classified as PII |
|--------------|------------------------------------|
| Employee_ID | Contains unique employee identifier that can be used to identify individual workers |
| Employee.Employee_Identifier | Direct personal identifier linking to specific individuals in the workforce |
| Employee.Labor_Role | Job role information that when combined with other data can identify individuals |
| Exception_Event.Opened_Timestamp | When combined with employee data, can reveal individual work patterns and performance |
| Exception_Event.Closed_Timestamp | When combined with employee data, can reveal individual work patterns and performance |
| Fact_Kronos.Scheduled_Hours | Individual employee scheduling data that reveals personal work patterns |
| Fact_Kronos.Worked_Hours | Individual employee time tracking data |
| Fact_Kronos.Overtime_Hours | Personal overtime information |
| Fact_Kronos.Absence_Flag | Individual absence records |
| Fact_Kronos.Adherence_Pct | Individual performance metrics |

## 2. Bronze Layer Logical Model

### 2.1 Dimension Tables

#### Bz_Organization
**Description**: Organizational hierarchy structure containing regions, areas, and network divisions for distribution center operations

| Column Name | Business Description | Data Type | 
|-------------|---------------------|----------|
| Org_Name | Name of organizational node (region, area, network) | String |
| Org_Level | Hierarchy level within organizational structure | String |
| Parent_Org_Name | Parent organizational node name | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_DistributionCenter
**Description**: Physical distribution center locations that handle inventory and fulfillment operations

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| DC_Name | Distribution center name identifier | String |
| Org_Name | Owning organizational node name | String |
| DC_Status | Active status of the distribution center | String |
| Region | Geographic or operational region of the distribution center | String |
| Status | Active/inactive operational status | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_Date
**Description**: Calendar date dimension for temporal reporting and analysis across all operational metrics

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| Calendar_Date | Calendar date for reporting | Date |
| Week_Start_Date | Start date of the week period | Date |
| Fiscal_Period | Fiscal period identifier for financial reporting | String |
| Date | Calendar date | Date |
| Week | Week period for weekly reporting | String |
| Month | Month period for monthly reporting | String |
| Pay_Period | Payroll period for labor reporting | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_Shift
**Description**: Work shift periods within distribution centers representing daily operational periods

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| Shift_Name | Identifier for the shift period | String |
| Shift_Start_Time | Scheduled shift start time | Time |
| Shift_End_Time | Scheduled shift end time | Time |
| Start_Time | Shift start time | Time |
| End_Time | Shift end time | Time |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_PartnerType
**Description**: Classification of partners including internal teams, external contractors, and third-party logistics providers

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| PartnerType_Name | Partner type category classification | String |
| Type_Name | Name of the partner type classification | String |
| Type_Description | Description of the partner type | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_Partner
**Description**: Third-party partners or internal teams operating within distribution centers

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| Partner_Name | Name of the partner organization or team | String |
| PartnerType_Name | Partner type classification | String |
| Partner_Status | Active status of the partner | String |
| Partner_Type | Classification of partner | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_Item
**Description**: Products, SKUs, and inventory items processed through distribution centers

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| Item_Name | Item description and name | String |
| Item_Category | Product category classification | String |
| Item_Status | Active/discontinued status of the item | String |
| Item_Identifier | Unique identifier for the item/SKU | String |
| Category | Product category classification | String |
| Status | Active/discontinued status | String |
| Safety_Stock | Safety stock parameters | Integer |
| Reorder_Parameters | Replenishment parameters | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_Activity
**Description**: Operational activities performed in distribution centers including receiving, putaway, picking, packing, shipping, and cycle count

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| Activity_Name | Name of the operational activity | String |
| Activity_Group | Activity grouping classification | String |
| Activity_Type | Type classification of the activity | String |
| Sub_activity | Optional sub-activity classification | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_Equipment
**Description**: Operational equipment used in distribution center activities including forklifts, conveyors, scanners, and automated systems

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| Equipment_Type | Type classification of equipment | String |
| Equipment_Status | Operational status of equipment | String |
| Equipment_Identifier | Unique identifier for equipment | String |
| Status | Operational status | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_Employee
**Description**: Workforce members working in distribution centers (PII data - requires special handling)

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| Employee_Identifier | Unique identifier for employee (hashed for privacy) | String |
| Home_DC_Name | Primary distribution center assignment | String |
| Partner_Name | Employing partner name | String |
| Role_Name | Labor role and job position | String |
| Labor_Role | Job role of the employee | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_ExceptionType
**Description**: Classification of operational exceptions and issues that impact distribution center performance

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| Exception_Type | High-level exception domain classification | String |
| Exception_Subtype | Detailed subtype of exception | String |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

### 2.2 Fact Tables

#### Bz_Fact_DC_Operations
**Description**: Operational performance metrics aggregated by distribution center, date, shift, activity, partner, and equipment

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| DC_Name | Distribution center name | String |
| Calendar_Date | Date of operations | Date |
| Shift_Name | Shift identifier | String |
| Activity_Name | Activity name | String |
| Partner_Name | Partner name | String |
| Equipment_Type | Equipment type used | String |
| Throughput_Units | Units processed during operations | Integer |
| Throughput_Lines | Lines processed during operations | Integer |
| Labor_Hours | Labor hours consumed | Decimal |
| Cycle_Time_Minutes | Average cycle time in minutes | Decimal |
| OnTime_Completion_Pct | Percentage completed on time | Decimal |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_Fact_Inventory
**Description**: Inventory levels and availability metrics by distribution center, date, and item

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| DC_Name | Distribution center name | String |
| Calendar_Date | Date of inventory snapshot | Date |
| Item_Name | Item description | String |
| OnHand_Qty | On-hand quantity available | Integer |
| Available_Qty | Available quantity for allocation | Integer |
| Allocated_Qty | Allocated quantity | Integer |
| Damaged_Qty | Damaged or hold quantity | Integer |
| OnOrder_Qty | On-order quantity | Integer |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_Fact_Headcount
**Description**: Workforce planning and actual headcount by distribution center, date, shift, partner type, partner, and role

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| DC_Name | Distribution center name | String |
| Calendar_Date | Date of headcount record | Date |
| Shift_Name | Shift identifier | String |
| PartnerType_Name | Partner type classification | String |
| Partner_Name | Partner name | String |
| Role_Name | Labor role | String |
| Planned_Headcount | Planned headcount | Integer |
| Actual_Headcount | Actual headcount | Integer |
| Planned_Hours | Planned hours | Decimal |
| Worked_Hours | Worked hours | Decimal |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_Fact_Picks
**Description**: Picking operations performance metrics by distribution center, date, shift, activity, partner, and item

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| DC_Name | Distribution center name | String |
| Calendar_Date | Date of picking operations | Date |
| Shift_Name | Shift identifier | String |
| Activity_Name | Activity name (typically Picking) | String |
| Partner_Name | Partner name | String |
| Item_Name | Item description | String |
| Pick_Units | Units picked | Integer |
| Pick_Lines | Lines picked | Integer |
| Pick_Errors | Errors or mis-picks | Integer |
| Rework_Count | Rework occurrences | Integer |
| Labor_Hours | Labor hours for picks | Decimal |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_Fact_Kronos
**Description**: Employee time and attendance data from Kronos system (PII data - requires special handling)

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| Employee_Identifier | Employee identifier (hashed for privacy) | String |
| DC_Name | Distribution center at time of work | String |
| Calendar_Date | Date of timecard | Date |
| Shift_Name | Shift identifier | String |
| Scheduled_Hours | Scheduled hours | Decimal |
| Worked_Hours | Worked hours | Decimal |
| Overtime_Hours | Overtime hours | Decimal |
| Absence_Flag | Absent indicator | String |
| Adherence_Pct | Worked within schedule window percentage | Decimal |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

#### Bz_Fact_Exceptions
**Description**: Operational exceptions and issues tracking with impact metrics

| Column Name | Business Description | Data Type |
|-------------|---------------------|----------|
| Exception_Event_Name | Unique identifier for exception event | String |
| Exception_Type | Exception type classification | String |
| DC_Name | Distribution center name | String |
| Calendar_Date | Date of exception event | Date |
| Shift_Name | Shift identifier | String |
| Activity_Name | Activity impacted | String |
| Partner_Name | Partner involved | String |
| Item_Name | Item impacted | String |
| Equipment_Type | Equipment impacted | String |
| Severity | Severity level | String |
| Status | Current status | String |
| Opened_Timestamp | When exception opened | Timestamp |
| Closed_Timestamp | When exception closed | Timestamp |
| Impact_Units | Units impacted | Integer |
| Impact_Minutes | Minutes of impact | Decimal |
| load_timestamp | Timestamp when record was loaded into Bronze layer | Timestamp |
| update_timestamp | Timestamp when record was last updated | Timestamp |
| source_system | Source system from which data originated | String |

## 3. Audit Table Design

#### Bz_Audit_Log
**Description**: Comprehensive audit trail for all Bronze layer data processing activities

| Field Name | Business Description | Data Type |
|------------|---------------------|----------|
| record_id | Unique identifier for audit record | String |
| source_table | Name of the source table being processed | String |
| load_timestamp | Timestamp when data was loaded | Timestamp |
| processed_by | System or user that processed the data | String |
| processing_time | Time taken to process the data | Decimal |
| status | Processing status (Success, Failed, Warning) | String |
| record_count | Number of records processed | Integer |
| error_message | Error message if processing failed | String |
| source_file_path | Path to source file | String |
| target_table_name | Target Bronze table name | String |

## 4. Conceptual Data Model Diagram (Tabular Form)

| Source Entity | Relationship Key Field | Target Entity | Relationship Type |
|---------------|------------------------|---------------|-------------------|
| Bz_Organization | Org_Name | Bz_DistributionCenter | One-to-Many |
| Bz_DistributionCenter | DC_Name | Bz_Shift | One-to-Many |
| Bz_PartnerType | PartnerType_Name | Bz_Partner | One-to-Many |
| Bz_DistributionCenter | DC_Name | Bz_Partner | Many-to-Many |
| Bz_Item | Item_Name | Bz_Activity | Many-to-Many |
| Bz_Equipment | Equipment_Type | Bz_Activity | Many-to-Many |
| Bz_Employee | Partner_Name | Bz_Partner | Many-to-One |
| Bz_Employee | Home_DC_Name | Bz_DistributionCenter | Many-to-One |
| Bz_Date | Calendar_Date | Bz_Fact_DC_Operations | One-to-Many |
| Bz_Date | Calendar_Date | Bz_Fact_Inventory | One-to-Many |
| Bz_Date | Calendar_Date | Bz_Fact_Headcount | One-to-Many |
| Bz_Date | Calendar_Date | Bz_Fact_Picks | One-to-Many |
| Bz_Date | Calendar_Date | Bz_Fact_Kronos | One-to-Many |
| Bz_Date | Calendar_Date | Bz_Fact_Exceptions | One-to-Many |
| Bz_Shift | Shift_Name | Bz_Fact_DC_Operations | One-to-Many |
| Bz_ExceptionType | Exception_Type | Bz_Fact_Exceptions | One-to-Many |
| Bz_DistributionCenter | DC_Name | Bz_Fact_DC_Operations | One-to-Many |
| Bz_DistributionCenter | DC_Name | Bz_Fact_Inventory | One-to-Many |
| Bz_DistributionCenter | DC_Name | Bz_Fact_Headcount | One-to-Many |
| Bz_DistributionCenter | DC_Name | Bz_Fact_Picks | One-to-Many |
| Bz_DistributionCenter | DC_Name | Bz_Fact_Kronos | One-to-Many |
| Bz_DistributionCenter | DC_Name | Bz_Fact_Exceptions | One-to-Many |
| Bz_Activity | Activity_Name | Bz_Fact_DC_Operations | One-to-Many |
| Bz_Activity | Activity_Name | Bz_Fact_Picks | One-to-Many |
| Bz_Partner | Partner_Name | Bz_Fact_DC_Operations | One-to-Many |
| Bz_Partner | Partner_Name | Bz_Fact_Headcount | One-to-Many |
| Bz_Partner | Partner_Name | Bz_Fact_Picks | One-to-Many |
| Bz_Equipment | Equipment_Type | Bz_Fact_DC_Operations | One-to-Many |
| Bz_Item | Item_Name | Bz_Fact_Inventory | One-to-Many |
| Bz_Item | Item_Name | Bz_Fact_Picks | One-to-Many |
| Bz_Employee | Employee_Identifier | Bz_Fact_Kronos | One-to-Many |

## 5. Design Rationale and Key Decisions

### 5.1 Naming Convention
- **Bz_ Prefix**: All Bronze layer tables use the "Bz_" prefix to clearly identify them as Bronze layer entities in the medallion architecture
- **Descriptive Names**: Table and column names are descriptive and business-friendly to enhance understanding

### 5.2 Data Structure Decisions
- **Source Mirroring**: Bronze layer exactly mirrors source data structure while excluding primary/foreign key fields
- **Metadata Columns**: All tables include load_timestamp, update_timestamp, and source_system for data lineage and auditing
- **Business Descriptions**: Every column includes business context to facilitate understanding and usage

### 5.3 PII Handling
- **Employee Data**: Employee identifiers are hashed to protect individual privacy while maintaining analytical capability
- **Access Controls**: PII fields are clearly identified for implementing appropriate access controls and data governance

### 5.4 Audit Strategy
- **Comprehensive Logging**: Audit table captures all processing activities with detailed status and error information
- **Data Lineage**: Source file paths and processing metadata enable complete data lineage tracking

### 5.5 Relationship Design
- **Business Key Relationships**: Relationships are established using business keys (names) rather than technical IDs
- **Flexible Associations**: Many-to-many relationships support complex operational scenarios

## 6. Data Quality Considerations

### 6.1 Constraints
- **Referential Integrity**: All relationships maintain referential integrity through business key matching
- **Data Validation**: Source data validation rules are preserved in Bronze layer
- **Duplicate Prevention**: Unique constraints on business keys prevent duplicate entries

### 6.2 Standardization
- **Domain Values**: Standardized domain values for status fields, categories, and classifications
- **Timestamp Consistency**: Consistent timestamp formats across all tables
- **Naming Standards**: Consistent naming conventions for similar attributes across tables

## apiCost

apiCost: 0.000000