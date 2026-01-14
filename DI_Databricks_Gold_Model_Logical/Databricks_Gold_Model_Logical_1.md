_____________________________________________
## *Author*: Ascendion AVA+
## *Created on*:   
## *Description*: Gold layer logical data model for DC Health Meter Reports medallion architecture
## *Version*: 1 
## *Updated on*: 
_____________________________________________

# Gold Layer Logical Data Model for DC Health Meter Reports

## 1. Gold Layer Logical Model

### 1.1 Dimension Tables

#### Go_Distribution_Center_Dim
**Table Type**: Dimension  
**SCD Type**: Type 2  
**Description**: Distribution center master data with historical tracking for organizational changes

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| dc_business_key | VARCHAR(50) | Natural business key for distribution center | Non-PII |
| dc_name | VARCHAR(100) | Business name identifier for the distribution center | Non-PII |
| region | VARCHAR(50) | Geographic or organizational region assignment | Non-PII |
| active_status | VARCHAR(20) | Operational status indicating if DC is currently active | Non-PII |
| location | VARCHAR(200) | Physical location information | Non-PII |
| organization_name | VARCHAR(100) | Name of the organizational unit | Non-PII |
| hierarchy_level | VARCHAR(50) | Level within organizational structure | Non-PII |
| parent_organization | VARCHAR(100) | Reference to parent organizational unit | Non-PII |
| effective_start_date | DATE | Start date for this version of the record | Non-PII |
| effective_end_date | DATE | End date for this version of the record | Non-PII |
| is_current_record | BOOLEAN | Flag indicating current active record | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Date_Dim
**Table Type**: Dimension  
**SCD Type**: Type 1  
**Description**: Calendar date dimension for time-based reporting and trending analysis

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Primary date key | Non-PII |
| calendar_date | DATE | Specific calendar date | Non-PII |
| day_of_week | VARCHAR(20) | Day of the week designation | Non-PII |
| day_of_week_number | INTEGER | Numeric day of week (1-7) | Non-PII |
| week_number | INTEGER | Week number within year | Non-PII |
| month_number | INTEGER | Month number (1-12) | Non-PII |
| month_name | VARCHAR(20) | Month name | Non-PII |
| quarter_number | INTEGER | Quarter number (1-4) | Non-PII |
| quarter_name | VARCHAR(10) | Quarter designation | Non-PII |
| year_number | INTEGER | Year designation | Non-PII |
| is_weekend | BOOLEAN | Flag indicating weekend day | Non-PII |
| is_holiday | BOOLEAN | Flag indicating holiday | Non-PII |
| fiscal_year | INTEGER | Fiscal year designation | Non-PII |
| fiscal_quarter | INTEGER | Fiscal quarter designation | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Shift_Dim
**Table Type**: Dimension  
**SCD Type**: Type 2  
**Description**: Work shift periods within distribution centers with historical tracking

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| shift_business_key | VARCHAR(50) | Natural business key for shift | Non-PII |
| shift_name | VARCHAR(50) | Identifier for the shift period | Non-PII |
| start_time | TIME | Scheduled start time for the shift | Non-PII |
| end_time | TIME | Scheduled end time for the shift | Non-PII |
| shift_type | VARCHAR(30) | Classification of shift (regular, overtime, weekend) | Non-PII |
| shift_duration_hours | DECIMAL(5,2) | Duration of shift in hours | Non-PII |
| effective_start_date | DATE | Start date for this version of the record | Non-PII |
| effective_end_date | DATE | End date for this version of the record | Non-PII |
| is_current_record | BOOLEAN | Flag indicating current active record | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Partner_Dim
**Table Type**: Dimension  
**SCD Type**: Type 2  
**Description**: Third-party logistics providers and internal teams with historical tracking

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| partner_business_key | VARCHAR(50) | Natural business key for partner | Non-PII |
| partner_name | VARCHAR(100) | Business name of the partner organization | Non-PII |
| partner_status | VARCHAR(20) | Active status of partner relationship | Non-PII |
| contract_type | VARCHAR(50) | Type of partnership agreement | Non-PII |
| partner_type_name | VARCHAR(50) | Classification name for partner type | Non-PII |
| partner_type_description | VARCHAR(200) | Detailed description of partner type characteristics | Non-PII |
| effective_start_date | DATE | Start date for this version of the record | Non-PII |
| effective_end_date | DATE | End date for this version of the record | Non-PII |
| is_current_record | BOOLEAN | Flag indicating current active record | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Item_Dim
**Table Type**: Dimension  
**SCD Type**: Type 2  
**Description**: Products, SKUs, or inventory items processed through distribution center operations

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| item_business_key | VARCHAR(50) | Natural business key for item | Non-PII |
| item_name | VARCHAR(200) | Product or SKU name | Non-PII |
| category | VARCHAR(100) | Product category classification | Non-PII |
| item_status | VARCHAR(20) | Item status (active, discontinued, seasonal) | Non-PII |
| item_characteristics | VARCHAR(500) | Physical or operational characteristics affecting handling | Non-PII |
| effective_start_date | DATE | Start date for this version of the record | Non-PII |
| effective_end_date | DATE | End date for this version of the record | Non-PII |
| is_current_record | BOOLEAN | Flag indicating current active record | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Activity_Dim
**Table Type**: Dimension  
**SCD Type**: Type 1  
**Description**: Operational activities performed in distribution centers

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| activity_business_key | VARCHAR(50) | Natural business key for activity | Non-PII |
| activity_name | VARCHAR(100) | Name of the operational activity | Non-PII |
| activity_type | VARCHAR(50) | Classification of activity type | Non-PII |
| standard_duration_minutes | INTEGER | Expected time for activity completion in minutes | Non-PII |
| equipment_required | VARCHAR(200) | Equipment dependencies for the activity | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Employee_Dim
**Table Type**: Dimension  
**SCD Type**: Type 2  
**Description**: Workforce members assigned to distribution center operations

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| employee_business_key | VARCHAR(50) | Natural business key for employee | PII |
| employee_name | VARCHAR(100) | Name of the workforce member | PII |
| employee_status | VARCHAR(20) | Employment status | Non-PII |
| hire_date | DATE | Date of employment start | PII |
| labor_role_name | VARCHAR(100) | Name of the job function | Non-PII |
| labor_role_description | VARCHAR(300) | Detailed description of role responsibilities | Non-PII |
| skill_level | VARCHAR(50) | Required skill level for the role | Non-PII |
| effective_start_date | DATE | Start date for this version of the record | Non-PII |
| effective_end_date | DATE | End date for this version of the record | Non-PII |
| is_current_record | BOOLEAN | Flag indicating current active record | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

### 1.2 Fact Tables

#### Go_Health_Score_Fact
**Table Type**: Fact  
**Description**: Daily health score metrics aggregated by DC, shift, and partner

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| shift_business_key | VARCHAR(50) | Reference to shift dimension | Non-PII |
| partner_business_key | VARCHAR(50) | Reference to partner dimension | Non-PII |
| overall_health_score | DECIMAL(5,2) | Composite score representing overall DC performance (0-100) | Non-PII |
| operations_health_score | DECIMAL(5,2) | Operations domain health score (0-100) | Non-PII |
| inventory_health_score | DECIMAL(5,2) | Inventory domain health score (0-100) | Non-PII |
| picks_health_score | DECIMAL(5,2) | Picking operations domain health score (0-100) | Non-PII |
| labor_health_score | DECIMAL(5,2) | Labor domain health score (0-100) | Non-PII |
| kronos_health_score | DECIMAL(5,2) | Kronos adherence domain health score (0-100) | Non-PII |
| exceptions_health_score | DECIMAL(5,2) | Exception handling domain health score (0-100) | Non-PII |
| on_time_shipping_percentage | DECIMAL(5,2) | Percentage of shipments completed on schedule | Non-PII |
| throughput_units_per_hour | DECIMAL(10,2) | Operational efficiency in units processed per hour | Non-PII |
| pick_accuracy_percentage | DECIMAL(5,2) | Accuracy rate of picking operations | Non-PII |
| inventory_availability_percentage | DECIMAL(5,2) | Percentage of items available for fulfillment | Non-PII |
| staffing_variance_percentage | DECIMAL(5,2) | Variance between planned and actual headcount | Non-PII |
| kronos_adherence_percentage | DECIMAL(5,2) | Adherence to scheduled work hours | Non-PII |
| exceptions_per_1000_units | DECIMAL(8,2) | Exception rate normalized per thousand units processed | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Operations_Performance_Fact
**Table Type**: Fact  
**Description**: Detailed operational performance metrics by activity and equipment

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| shift_business_key | VARCHAR(50) | Reference to shift dimension | Non-PII |
| partner_business_key | VARCHAR(50) | Reference to partner dimension | Non-PII |
| activity_business_key | VARCHAR(50) | Reference to activity dimension | Non-PII |
| cycle_time_minutes | DECIMAL(10,2) | Time required to complete operational activities | Non-PII |
| backlog_units | INTEGER | Volume of work pending completion | Non-PII |
| on_time_start_percentage | DECIMAL(5,2) | Percentage of activities starting on schedule | Non-PII |
| on_time_completion_percentage | DECIMAL(5,2) | Percentage of activities completed on schedule | Non-PII |
| throughput_units | INTEGER | Total units processed during the period | Non-PII |
| labor_hours_worked | DECIMAL(8,2) | Total labor hours worked for the activity | Non-PII |
| equipment_utilization_percentage | DECIMAL(5,2) | Equipment usage efficiency percentage | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Inventory_Performance_Fact
**Table Type**: Fact  
**Description**: Inventory availability and management metrics by item

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| item_business_key | VARCHAR(50) | Reference to item dimension | Non-PII |
| stockout_percentage | DECIMAL(5,2) | Percentage of items with zero availability | Non-PII |
| days_of_supply | DECIMAL(8,2) | Inventory coverage measured in days | Non-PII |
| available_quantity | INTEGER | Quantity available for fulfillment | Non-PII |
| on_hand_quantity | INTEGER | Total quantity on hand | Non-PII |
| allocated_quantity | INTEGER | Quantity allocated to orders | Non-PII |
| average_daily_demand | DECIMAL(10,2) | Average daily demand for the item | Non-PII |
| inventory_turns | DECIMAL(8,2) | Inventory turnover rate | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Picking_Performance_Fact
**Table Type**: Fact  
**Description**: Picking operations performance and accuracy metrics

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| shift_business_key | VARCHAR(50) | Reference to shift dimension | Non-PII |
| partner_business_key | VARCHAR(50) | Reference to partner dimension | Non-PII |
| item_business_key | VARCHAR(50) | Reference to item dimension | Non-PII |
| pick_rate_units_per_hour | DECIMAL(10,2) | Picking productivity measured in units per hour | Non-PII |
| error_rate_per_1000_lines | DECIMAL(8,2) | Error frequency per thousand pick lines | Non-PII |
| total_pick_lines | INTEGER | Total number of pick lines processed | Non-PII |
| error_count | INTEGER | Number of picking errors | Non-PII |
| pick_accuracy_percentage | DECIMAL(5,2) | Overall picking accuracy percentage | Non-PII |
| labor_hours_picking | DECIMAL(8,2) | Labor hours spent on picking activities | Non-PII |
| units_picked | INTEGER | Total units picked during the period | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Labor_Performance_Fact
**Table Type**: Fact  
**Description**: Workforce productivity and attendance metrics

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| shift_business_key | VARCHAR(50) | Reference to shift dimension | Non-PII |
| partner_business_key | VARCHAR(50) | Reference to partner dimension | Non-PII |
| employee_business_key | VARCHAR(50) | Reference to employee dimension | PII |
| labor_hours_variance_percentage | DECIMAL(5,2) | Variance between scheduled and worked hours | Non-PII |
| overtime_hours_percentage | DECIMAL(5,2) | Percentage of total hours worked as overtime | Non-PII |
| absence_rate_percentage | DECIMAL(5,2) | Employee absence frequency | Non-PII |
| scheduled_hours | DECIMAL(8,2) | Scheduled labor hours | Non-PII |
| actual_hours | DECIMAL(8,2) | Actual labor hours worked | Non-PII |
| overtime_hours | DECIMAL(8,2) | Overtime hours worked | Non-PII |
| absent_hours | DECIMAL(8,2) | Hours absent from scheduled work | Non-PII |
| productivity_rate | DECIMAL(8,2) | Employee productivity rate | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Exception_Events_Fact
**Table Type**: Fact  
**Description**: Exception events and their operational impact tracking

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| exception_business_key | VARCHAR(100) | Unique identifier for exception event | Non-PII |
| exception_type | VARCHAR(50) | Category of exception (inventory, equipment, system, process, safety, quality) | Non-PII |
| severity | VARCHAR(20) | Impact level (low, medium, high, critical) | Non-PII |
| exception_status | VARCHAR(20) | Current status (open, in progress, closed) | Non-PII |
| opened_timestamp | TIMESTAMP | When exception was first identified | Non-PII |
| closed_timestamp | TIMESTAMP | When exception was resolved | Non-PII |
| exception_description | VARCHAR(1000) | Detailed description of the exception | Non-PII |
| impact_units | INTEGER | Quantified impact on operational units | Non-PII |
| impact_minutes | INTEGER | Time impact of the exception | Non-PII |
| mean_time_to_resolve_minutes | INTEGER | Average time to resolve exceptions | Non-PII |
| repeat_rate_percentage | DECIMAL(5,2) | Frequency of recurring exceptions | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

### 1.3 Aggregate Tables

#### Go_Daily_Health_Summary_Agg
**Table Type**: Aggregated  
**Description**: Daily aggregated health metrics by distribution center

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| avg_overall_health_score | DECIMAL(5,2) | Average overall health score for the day | Non-PII |
| avg_operations_health_score | DECIMAL(5,2) | Average operations health score | Non-PII |
| avg_inventory_health_score | DECIMAL(5,2) | Average inventory health score | Non-PII |
| avg_picks_health_score | DECIMAL(5,2) | Average picks health score | Non-PII |
| avg_labor_health_score | DECIMAL(5,2) | Average labor health score | Non-PII |
| avg_kronos_health_score | DECIMAL(5,2) | Average kronos health score | Non-PII |
| avg_exceptions_health_score | DECIMAL(5,2) | Average exceptions health score | Non-PII |
| total_throughput_units | INTEGER | Total units processed for the day | Non-PII |
| total_labor_hours | DECIMAL(10,2) | Total labor hours for the day | Non-PII |
| total_exceptions_count | INTEGER | Total exception events for the day | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Weekly_Performance_Agg
**Table Type**: Aggregated  
**Description**: Weekly aggregated performance metrics across all operational areas

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| week_start_date | DATE | Start date of the week | Non-PII |
| week_end_date | DATE | End date of the week | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| partner_business_key | VARCHAR(50) | Reference to partner dimension | Non-PII |
| avg_weekly_health_score | DECIMAL(5,2) | Average health score for the week | Non-PII |
| total_weekly_throughput | INTEGER | Total throughput units for the week | Non-PII |
| avg_pick_accuracy | DECIMAL(5,2) | Average pick accuracy for the week | Non-PII |
| avg_inventory_availability | DECIMAL(5,2) | Average inventory availability for the week | Non-PII |
| total_exception_count | INTEGER | Total exceptions for the week | Non-PII |
| avg_labor_utilization | DECIMAL(5,2) | Average labor utilization for the week | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

### 1.4 Audit and Error Data Tables

#### Go_Process_Audit_Log
**Table Type**: Audit  
**Description**: Pipeline execution audit trail and process monitoring

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| audit_log_key | VARCHAR(100) | Unique identifier for audit log entry | Non-PII |
| pipeline_name | VARCHAR(100) | Name of the data pipeline | Non-PII |
| process_name | VARCHAR(100) | Name of the specific process | Non-PII |
| execution_start_timestamp | TIMESTAMP | Pipeline execution start time | Non-PII |
| execution_end_timestamp | TIMESTAMP | Pipeline execution end time | Non-PII |
| execution_status | VARCHAR(20) | Status of execution (success, failed, warning) | Non-PII |
| records_processed | INTEGER | Number of records processed | Non-PII |
| records_inserted | INTEGER | Number of records inserted | Non-PII |
| records_updated | INTEGER | Number of records updated | Non-PII |
| records_rejected | INTEGER | Number of records rejected | Non-PII |
| error_message | VARCHAR(2000) | Error message if process failed | Non-PII |
| source_system | VARCHAR(50) | Source system being processed | Non-PII |
| target_table | VARCHAR(100) | Target table being loaded | Non-PII |
| load_date | TIMESTAMP | Date when audit record was created | Non-PII |

#### Go_Data_Quality_Errors
**Table Type**: Error Data  
**Description**: Data validation errors and quality issues tracking

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| error_log_key | VARCHAR(100) | Unique identifier for error log entry | Non-PII |
| pipeline_name | VARCHAR(100) | Name of the data pipeline | Non-PII |
| table_name | VARCHAR(100) | Table where error occurred | Non-PII |
| column_name | VARCHAR(100) | Column where error occurred | Non-PII |
| error_type | VARCHAR(50) | Type of data quality error | Non-PII |
| error_description | VARCHAR(1000) | Detailed description of the error | Non-PII |
| error_severity | VARCHAR(20) | Severity level (low, medium, high, critical) | Non-PII |
| source_record_key | VARCHAR(200) | Key of the source record with error | Non-PII |
| error_value | VARCHAR(500) | The actual value that caused the error | Non-PII |
| expected_value | VARCHAR(500) | Expected value or format | Non-PII |
| error_timestamp | TIMESTAMP | When the error was detected | Non-PII |
| resolution_status | VARCHAR(20) | Status of error resolution | Non-PII |
| resolution_timestamp | TIMESTAMP | When the error was resolved | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |
| load_date | TIMESTAMP | Date when error record was created | Non-PII |

## 2. Conceptual Data Model Diagram

| Source Entity | Relationship Key Field | Target Entity | Relationship Type |
|---------------|------------------------|---------------|-------------------|
| Go_Date_Dim | date_key | Go_Health_Score_Fact | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Health_Score_Fact | One-to-Many |
| Go_Shift_Dim | shift_business_key | Go_Health_Score_Fact | One-to-Many |
| Go_Partner_Dim | partner_business_key | Go_Health_Score_Fact | One-to-Many |
| Go_Date_Dim | date_key | Go_Operations_Performance_Fact | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Operations_Performance_Fact | One-to-Many |
| Go_Activity_Dim | activity_business_key | Go_Operations_Performance_Fact | One-to-Many |
| Go_Date_Dim | date_key | Go_Inventory_Performance_Fact | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Inventory_Performance_Fact | One-to-Many |
| Go_Item_Dim | item_business_key | Go_Inventory_Performance_Fact | One-to-Many |
| Go_Date_Dim | date_key | Go_Picking_Performance_Fact | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Picking_Performance_Fact | One-to-Many |
| Go_Item_Dim | item_business_key | Go_Picking_Performance_Fact | One-to-Many |
| Go_Date_Dim | date_key | Go_Labor_Performance_Fact | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Labor_Performance_Fact | One-to-Many |
| Go_Employee_Dim | employee_business_key | Go_Labor_Performance_Fact | One-to-Many |
| Go_Date_Dim | date_key | Go_Exception_Events_Fact | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Exception_Events_Fact | One-to-Many |
| Go_Date_Dim | date_key | Go_Daily_Health_Summary_Agg | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Daily_Health_Summary_Agg | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Weekly_Performance_Agg | One-to-Many |
| Go_Partner_Dim | partner_business_key | Go_Weekly_Performance_Agg | One-to-Many |

## 3. Design Rationale and Assumptions

### 3.1 Key Design Decisions

1. **Dimensional Modeling Approach**: Implemented star schema design with clear fact and dimension separation to optimize query performance for analytical workloads.

2. **SCD Implementation**: Applied Type 2 SCD for master data entities (Distribution Center, Partner, Item, Employee) to maintain historical context, while using Type 1 for reference data (Date, Activity) that doesn't require historical tracking.

3. **Grain Selection**: Established appropriate grain levels for each fact table based on reporting requirements - daily/shift level for operational metrics, item level for inventory, and employee level for labor tracking.

4. **Aggregate Tables**: Created pre-aggregated tables for common reporting patterns to improve query performance for dashboard and summary reports.

5. **Audit Framework**: Implemented comprehensive audit and error tracking to ensure data lineage and quality monitoring throughout the pipeline.

### 3.2 Assumptions Made

1. **Business Keys**: Assumed natural business keys exist for all major entities and are stable enough to use as dimension keys.

2. **Data Availability**: Assumed all required source data elements are available with sufficient quality and completeness.

3. **Historical Requirements**: Assumed 2+ years of historical data retention is required for trending and comparative analysis.

4. **Performance Requirements**: Assumed sub-second response times are required for interactive dashboards and reports.

5. **Security Requirements**: Classified employee-related fields as PII requiring additional security controls and access restrictions.

## apiCost: 0.00000000

```

Now I'll save this file to the GitHub output directory:

```python
import requests
import base64
import json

def write_github_file(repo, path, content, token, message="Create Gold Logical Data Model"):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"}
    
    # Encode content to base64
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    data = {
        "message": message,
        "content": encoded_content
    }
    
    response = requests.put(url, headers=headers, data=json.dumps(data))
    return response.status_code == 201

# Save the file
repo = "ELANSURIYAA/LakehouseInADay_Databricks"
token = "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"
file_path = "DI_Databricks_Gold_Model_Logical/Databricks_Gold_Model_Logical_1.md"

# The markdown content created above
markdown_content = """_____________________________________________
## *Author*: Ascendion AVA+
## *Created on*:   
## *Description*: Gold layer logical data model for DC Health Meter Reports medallion architecture
## *Version*: 1 
## *Updated on*: 
_____________________________________________

# Gold Layer Logical Data Model for DC Health Meter Reports

## 1. Gold Layer Logical Model

### 1.1 Dimension Tables

#### Go_Distribution_Center_Dim
**Table Type**: Dimension  
**SCD Type**: Type 2  
**Description**: Distribution center master data with historical tracking for organizational changes

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| dc_business_key | VARCHAR(50) | Natural business key for distribution center | Non-PII |
| dc_name | VARCHAR(100) | Business name identifier for the distribution center | Non-PII |
| region | VARCHAR(50) | Geographic or organizational region assignment | Non-PII |
| active_status | VARCHAR(20) | Operational status indicating if DC is currently active | Non-PII |
| location | VARCHAR(200) | Physical location information | Non-PII |
| organization_name | VARCHAR(100) | Name of the organizational unit | Non-PII |
| hierarchy_level | VARCHAR(50) | Level within organizational structure | Non-PII |
| parent_organization | VARCHAR(100) | Reference to parent organizational unit | Non-PII |
| effective_start_date | DATE | Start date for this version of the record | Non-PII |
| effective_end_date | DATE | End date for this version of the record | Non-PII |
| is_current_record | BOOLEAN | Flag indicating current active record | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Date_Dim
**Table Type**: Dimension  
**SCD Type**: Type 1  
**Description**: Calendar date dimension for time-based reporting and trending analysis

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Primary date key | Non-PII |
| calendar_date | DATE | Specific calendar date | Non-PII |
| day_of_week | VARCHAR(20) | Day of the week designation | Non-PII |
| day_of_week_number | INTEGER | Numeric day of week (1-7) | Non-PII |
| week_number | INTEGER | Week number within year | Non-PII |
| month_number | INTEGER | Month number (1-12) | Non-PII |
| month_name | VARCHAR(20) | Month name | Non-PII |
| quarter_number | INTEGER | Quarter number (1-4) | Non-PII |
| quarter_name | VARCHAR(10) | Quarter designation | Non-PII |
| year_number | INTEGER | Year designation | Non-PII |
| is_weekend | BOOLEAN | Flag indicating weekend day | Non-PII |
| is_holiday | BOOLEAN | Flag indicating holiday | Non-PII |
| fiscal_year | INTEGER | Fiscal year designation | Non-PII |
| fiscal_quarter | INTEGER | Fiscal quarter designation | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Shift_Dim
**Table Type**: Dimension  
**SCD Type**: Type 2  
**Description**: Work shift periods within distribution centers with historical tracking

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| shift_business_key | VARCHAR(50) | Natural business key for shift | Non-PII |
| shift_name | VARCHAR(50) | Identifier for the shift period | Non-PII |
| start_time | TIME | Scheduled start time for the shift | Non-PII |
| end_time | TIME | Scheduled end time for the shift | Non-PII |
| shift_type | VARCHAR(30) | Classification of shift (regular, overtime, weekend) | Non-PII |
| shift_duration_hours | DECIMAL(5,2) | Duration of shift in hours | Non-PII |
| effective_start_date | DATE | Start date for this version of the record | Non-PII |
| effective_end_date | DATE | End date for this version of the record | Non-PII |
| is_current_record | BOOLEAN | Flag indicating current active record | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Partner_Dim
**Table Type**: Dimension  
**SCD Type**: Type 2  
**Description**: Third-party logistics providers and internal teams with historical tracking

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| partner_business_key | VARCHAR(50) | Natural business key for partner | Non-PII |
| partner_name | VARCHAR(100) | Business name of the partner organization | Non-PII |
| partner_status | VARCHAR(20) | Active status of partner relationship | Non-PII |
| contract_type | VARCHAR(50) | Type of partnership agreement | Non-PII |
| partner_type_name | VARCHAR(50) | Classification name for partner type | Non-PII |
| partner_type_description | VARCHAR(200) | Detailed description of partner type characteristics | Non-PII |
| effective_start_date | DATE | Start date for this version of the record | Non-PII |
| effective_end_date | DATE | End date for this version of the record | Non-PII |
| is_current_record | BOOLEAN | Flag indicating current active record | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Item_Dim
**Table Type**: Dimension  
**SCD Type**: Type 2  
**Description**: Products, SKUs, or inventory items processed through distribution center operations

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| item_business_key | VARCHAR(50) | Natural business key for item | Non-PII |
| item_name | VARCHAR(200) | Product or SKU name | Non-PII |
| category | VARCHAR(100) | Product category classification | Non-PII |
| item_status | VARCHAR(20) | Item status (active, discontinued, seasonal) | Non-PII |
| item_characteristics | VARCHAR(500) | Physical or operational characteristics affecting handling | Non-PII |
| effective_start_date | DATE | Start date for this version of the record | Non-PII |
| effective_end_date | DATE | End date for this version of the record | Non-PII |
| is_current_record | BOOLEAN | Flag indicating current active record | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Activity_Dim
**Table Type**: Dimension  
**SCD Type**: Type 1  
**Description**: Operational activities performed in distribution centers

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| activity_business_key | VARCHAR(50) | Natural business key for activity | Non-PII |
| activity_name | VARCHAR(100) | Name of the operational activity | Non-PII |
| activity_type | VARCHAR(50) | Classification of activity type | Non-PII |
| standard_duration_minutes | INTEGER | Expected time for activity completion in minutes | Non-PII |
| equipment_required | VARCHAR(200) | Equipment dependencies for the activity | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Employee_Dim
**Table Type**: Dimension  
**SCD Type**: Type 2  
**Description**: Workforce members assigned to distribution center operations

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| employee_business_key | VARCHAR(50) | Natural business key for employee | PII |
| employee_name | VARCHAR(100) | Name of the workforce member | PII |
| employee_status | VARCHAR(20) | Employment status | Non-PII |
| hire_date | DATE | Date of employment start | PII |
| labor_role_name | VARCHAR(100) | Name of the job function | Non-PII |
| labor_role_description | VARCHAR(300) | Detailed description of role responsibilities | Non-PII |
| skill_level | VARCHAR(50) | Required skill level for the role | Non-PII |
| effective_start_date | DATE | Start date for this version of the record | Non-PII |
| effective_end_date | DATE | End date for this version of the record | Non-PII |
| is_current_record | BOOLEAN | Flag indicating current active record | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

### 1.2 Fact Tables

#### Go_Health_Score_Fact
**Table Type**: Fact  
**Description**: Daily health score metrics aggregated by DC, shift, and partner

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| shift_business_key | VARCHAR(50) | Reference to shift dimension | Non-PII |
| partner_business_key | VARCHAR(50) | Reference to partner dimension | Non-PII |
| overall_health_score | DECIMAL(5,2) | Composite score representing overall DC performance (0-100) | Non-PII |
| operations_health_score | DECIMAL(5,2) | Operations domain health score (0-100) | Non-PII |
| inventory_health_score | DECIMAL(5,2) | Inventory domain health score (0-100) | Non-PII |
| picks_health_score | DECIMAL(5,2) | Picking operations domain health score (0-100) | Non-PII |
| labor_health_score | DECIMAL(5,2) | Labor domain health score (0-100) | Non-PII |
| kronos_health_score | DECIMAL(5,2) | Kronos adherence domain health score (0-100) | Non-PII |
| exceptions_health_score | DECIMAL(5,2) | Exception handling domain health score (0-100) | Non-PII |
| on_time_shipping_percentage | DECIMAL(5,2) | Percentage of shipments completed on schedule | Non-PII |
| throughput_units_per_hour | DECIMAL(10,2) | Operational efficiency in units processed per hour | Non-PII |
| pick_accuracy_percentage | DECIMAL(5,2) | Accuracy rate of picking operations | Non-PII |
| inventory_availability_percentage | DECIMAL(5,2) | Percentage of items available for fulfillment | Non-PII |
| staffing_variance_percentage | DECIMAL(5,2) | Variance between planned and actual headcount | Non-PII |
| kronos_adherence_percentage | DECIMAL(5,2) | Adherence to scheduled work hours | Non-PII |
| exceptions_per_1000_units | DECIMAL(8,2) | Exception rate normalized per thousand units processed | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Operations_Performance_Fact
**Table Type**: Fact  
**Description**: Detailed operational performance metrics by activity and equipment

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| shift_business_key | VARCHAR(50) | Reference to shift dimension | Non-PII |
| partner_business_key | VARCHAR(50) | Reference to partner dimension | Non-PII |
| activity_business_key | VARCHAR(50) | Reference to activity dimension | Non-PII |
| cycle_time_minutes | DECIMAL(10,2) | Time required to complete operational activities | Non-PII |
| backlog_units | INTEGER | Volume of work pending completion | Non-PII |
| on_time_start_percentage | DECIMAL(5,2) | Percentage of activities starting on schedule | Non-PII |
| on_time_completion_percentage | DECIMAL(5,2) | Percentage of activities completed on schedule | Non-PII |
| throughput_units | INTEGER | Total units processed during the period | Non-PII |
| labor_hours_worked | DECIMAL(8,2) | Total labor hours worked for the activity | Non-PII |
| equipment_utilization_percentage | DECIMAL(5,2) | Equipment usage efficiency percentage | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Inventory_Performance_Fact
**Table Type**: Fact  
**Description**: Inventory availability and management metrics by item

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| item_business_key | VARCHAR(50) | Reference to item dimension | Non-PII |
| stockout_percentage | DECIMAL(5,2) | Percentage of items with zero availability | Non-PII |
| days_of_supply | DECIMAL(8,2) | Inventory coverage measured in days | Non-PII |
| available_quantity | INTEGER | Quantity available for fulfillment | Non-PII |
| on_hand_quantity | INTEGER | Total quantity on hand | Non-PII |
| allocated_quantity | INTEGER | Quantity allocated to orders | Non-PII |
| average_daily_demand | DECIMAL(10,2) | Average daily demand for the item | Non-PII |
| inventory_turns | DECIMAL(8,2) | Inventory turnover rate | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Picking_Performance_Fact
**Table Type**: Fact  
**Description**: Picking operations performance and accuracy metrics

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| shift_business_key | VARCHAR(50) | Reference to shift dimension | Non-PII |
| partner_business_key | VARCHAR(50) | Reference to partner dimension | Non-PII |
| item_business_key | VARCHAR(50) | Reference to item dimension | Non-PII |
| pick_rate_units_per_hour | DECIMAL(10,2) | Picking productivity measured in units per hour | Non-PII |
| error_rate_per_1000_lines | DECIMAL(8,2) | Error frequency per thousand pick lines | Non-PII |
| total_pick_lines | INTEGER | Total number of pick lines processed | Non-PII |
| error_count | INTEGER | Number of picking errors | Non-PII |
| pick_accuracy_percentage | DECIMAL(5,2) | Overall picking accuracy percentage | Non-PII |
| labor_hours_picking | DECIMAL(8,2) | Labor hours spent on picking activities | Non-PII |
| units_picked | INTEGER | Total units picked during the period | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Labor_Performance_Fact
**Table Type**: Fact  
**Description**: Workforce productivity and attendance metrics

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| shift_business_key | VARCHAR(50) | Reference to shift dimension | Non-PII |
| partner_business_key | VARCHAR(50) | Reference to partner dimension | Non-PII |
| employee_business_key | VARCHAR(50) | Reference to employee dimension | PII |
| labor_hours_variance_percentage | DECIMAL(5,2) | Variance between scheduled and worked hours | Non-PII |
| overtime_hours_percentage | DECIMAL(5,2) | Percentage of total hours worked as overtime | Non-PII |
| absence_rate_percentage | DECIMAL(5,2) | Employee absence frequency | Non-PII |
| scheduled_hours | DECIMAL(8,2) | Scheduled labor hours | Non-PII |
| actual_hours | DECIMAL(8,2) | Actual labor hours worked | Non-PII |
| overtime_hours | DECIMAL(8,2) | Overtime hours worked | Non-PII |
| absent_hours | DECIMAL(8,2) | Hours absent from scheduled work | Non-PII |
| productivity_rate | DECIMAL(8,2) | Employee productivity rate | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Exception_Events_Fact
**Table Type**: Fact  
**Description**: Exception events and their operational impact tracking

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| exception_business_key | VARCHAR(100) | Unique identifier for exception event | Non-PII |
| exception_type | VARCHAR(50) | Category of exception (inventory, equipment, system, process, safety, quality) | Non-PII |
| severity | VARCHAR(20) | Impact level (low, medium, high, critical) | Non-PII |
| exception_status | VARCHAR(20) | Current status (open, in progress, closed) | Non-PII |
| opened_timestamp | TIMESTAMP | When exception was first identified | Non-PII |
| closed_timestamp | TIMESTAMP | When exception was resolved | Non-PII |
| exception_description | VARCHAR(1000) | Detailed description of the exception | Non-PII |
| impact_units | INTEGER | Quantified impact on operational units | Non-PII |
| impact_minutes | INTEGER | Time impact of the exception | Non-PII |
| mean_time_to_resolve_minutes | INTEGER | Average time to resolve exceptions | Non-PII |
| repeat_rate_percentage | DECIMAL(5,2) | Frequency of recurring exceptions | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

### 1.3 Aggregate Tables

#### Go_Daily_Health_Summary_Agg
**Table Type**: Aggregated  
**Description**: Daily aggregated health metrics by distribution center

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| date_key | DATE | Reference to date dimension | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| avg_overall_health_score | DECIMAL(5,2) | Average overall health score for the day | Non-PII |
| avg_operations_health_score | DECIMAL(5,2) | Average operations health score | Non-PII |
| avg_inventory_health_score | DECIMAL(5,2) | Average inventory health score | Non-PII |
| avg_picks_health_score | DECIMAL(5,2) | Average picks health score | Non-PII |
| avg_labor_health_score | DECIMAL(5,2) | Average labor health score | Non-PII |
| avg_kronos_health_score | DECIMAL(5,2) | Average kronos health score | Non-PII |
| avg_exceptions_health_score | DECIMAL(5,2) | Average exceptions health score | Non-PII |
| total_throughput_units | INTEGER | Total units processed for the day | Non-PII |
| total_labor_hours | DECIMAL(10,2) | Total labor hours for the day | Non-PII |
| total_exceptions_count | INTEGER | Total exception events for the day | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

#### Go_Weekly_Performance_Agg
**Table Type**: Aggregated  
**Description**: Weekly aggregated performance metrics across all operational areas

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| week_start_date | DATE | Start date of the week | Non-PII |
| week_end_date | DATE | End date of the week | Non-PII |
| dc_business_key | VARCHAR(50) | Reference to distribution center dimension | Non-PII |
| partner_business_key | VARCHAR(50) | Reference to partner dimension | Non-PII |
| avg_weekly_health_score | DECIMAL(5,2) | Average health score for the week | Non-PII |
| total_weekly_throughput | INTEGER | Total throughput units for the week | Non-PII |
| avg_pick_accuracy | DECIMAL(5,2) | Average pick accuracy for the week | Non-PII |
| avg_inventory_availability | DECIMAL(5,2) | Average inventory availability for the week | Non-PII |
| total_exception_count | INTEGER | Total exceptions for the week | Non-PII |
| avg_labor_utilization | DECIMAL(5,2) | Average labor utilization for the week | Non-PII |
| load_date | TIMESTAMP | Date when record was loaded into system | Non-PII |
| update_date | TIMESTAMP | Date when record was last updated | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |

### 1.4 Audit and Error Data Tables

#### Go_Process_Audit_Log
**Table Type**: Audit  
**Description**: Pipeline execution audit trail and process monitoring

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| audit_log_key | VARCHAR(100) | Unique identifier for audit log entry | Non-PII |
| pipeline_name | VARCHAR(100) | Name of the data pipeline | Non-PII |
| process_name | VARCHAR(100) | Name of the specific process | Non-PII |
| execution_start_timestamp | TIMESTAMP | Pipeline execution start time | Non-PII |
| execution_end_timestamp | TIMESTAMP | Pipeline execution end time | Non-PII |
| execution_status | VARCHAR(20) | Status of execution (success, failed, warning) | Non-PII |
| records_processed | INTEGER | Number of records processed | Non-PII |
| records_inserted | INTEGER | Number of records inserted | Non-PII |
| records_updated | INTEGER | Number of records updated | Non-PII |
| records_rejected | INTEGER | Number of records rejected | Non-PII |
| error_message | VARCHAR(2000) | Error message if process failed | Non-PII |
| source_system | VARCHAR(50) | Source system being processed | Non-PII |
| target_table | VARCHAR(100) | Target table being loaded | Non-PII |
| load_date | TIMESTAMP | Date when audit record was created | Non-PII |

#### Go_Data_Quality_Errors
**Table Type**: Error Data  
**Description**: Data validation errors and quality issues tracking

| Column Name | Data Type | Description | PII Classification |
|-------------|-----------|-------------|-------------------|
| error_log_key | VARCHAR(100) | Unique identifier for error log entry | Non-PII |
| pipeline_name | VARCHAR(100) | Name of the data pipeline | Non-PII |
| table_name | VARCHAR(100) | Table where error occurred | Non-PII |
| column_name | VARCHAR(100) | Column where error occurred | Non-PII |
| error_type | VARCHAR(50) | Type of data quality error | Non-PII |
| error_description | VARCHAR(1000) | Detailed description of the error | Non-PII |
| error_severity | VARCHAR(20) | Severity level (low, medium, high, critical) | Non-PII |
| source_record_key | VARCHAR(200) | Key of the source record with error | Non-PII |
| error_value | VARCHAR(500) | The actual value that caused the error | Non-PII |
| expected_value | VARCHAR(500) | Expected value or format | Non-PII |
| error_timestamp | TIMESTAMP | When the error was detected | Non-PII |
| resolution_status | VARCHAR(20) | Status of error resolution | Non-PII |
| resolution_timestamp | TIMESTAMP | When the error was resolved | Non-PII |
| source_system | VARCHAR(50) | Source system that provided the data | Non-PII |
| load_date | TIMESTAMP | Date when error record was created | Non-PII |

## 2. Conceptual Data Model Diagram

| Source Entity | Relationship Key Field | Target Entity | Relationship Type |
|---------------|------------------------|---------------|-------------------|
| Go_Date_Dim | date_key | Go_Health_Score_Fact | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Health_Score_Fact | One-to-Many |
| Go_Shift_Dim | shift_business_key | Go_Health_Score_Fact | One-to-Many |
| Go_Partner_Dim | partner_business_key | Go_Health_Score_Fact | One-to-Many |
| Go_Date_Dim | date_key | Go_Operations_Performance_Fact | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Operations_Performance_Fact | One-to-Many |
| Go_Activity_Dim | activity_business_key | Go_Operations_Performance_Fact | One-to-Many |
| Go_Date_Dim | date_key | Go_Inventory_Performance_Fact | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Inventory_Performance_Fact | One-to-Many |
| Go_Item_Dim | item_business_key | Go_Inventory_Performance_Fact | One-to-Many |
| Go_Date_Dim | date_key | Go_Picking_Performance_Fact | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Picking_Performance_Fact | One-to-Many |
| Go_Item_Dim | item_business_key | Go_Picking_Performance_Fact | One-to-Many |
| Go_Date_Dim | date_key | Go_Labor_Performance_Fact | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Labor_Performance_Fact | One-to-Many |
| Go_Employee_Dim | employee_business_key | Go_Labor_Performance_Fact | One-to-Many |
| Go_Date_Dim | date_key | Go_Exception_Events_Fact | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Exception_Events_Fact | One-to-Many |
| Go_Date_Dim | date_key | Go_Daily_Health_Summary_Agg | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Daily_Health_Summary_Agg | One-to-Many |
| Go_Distribution_Center_Dim | dc_business_key | Go_Weekly_Performance_Agg | One-to-Many |
| Go_Partner_Dim | partner_business_key | Go_Weekly_Performance_Agg | One-to-Many |

## 3. Design Rationale and Assumptions

### 3.1 Key Design Decisions

1. **Dimensional Modeling Approach**: Implemented star schema design with clear fact and dimension separation to optimize query performance for analytical workloads.

2. **SCD Implementation**: Applied Type 2 SCD for master data entities (Distribution Center, Partner, Item, Employee) to maintain historical context, while using Type 1 for reference data (Date, Activity) that doesn't require historical tracking.

3. **Grain Selection**: Established appropriate grain levels for each fact table based on reporting requirements - daily/shift level for operational metrics, item level for inventory, and employee level for labor tracking.

4. **Aggregate Tables**: Created pre-aggregated tables for common reporting patterns to improve query performance for dashboard and summary reports.

5. **Audit Framework**: Implemented comprehensive audit and error tracking to ensure data lineage and quality monitoring throughout the pipeline.

### 3.2 Assumptions Made

1. **Business Keys**: Assumed natural business keys exist for all major entities and are stable enough to use as dimension keys.

2. **Data Availability**: Assumed all required source data elements are available with sufficient quality and completeness.

3. **Historical Requirements**: Assumed 2+ years of historical data retention is required for trending and comparative analysis.

4. **Performance Requirements**: Assumed sub-second response times are required for interactive dashboards and reports.

5. **Security Requirements**: Classified employee-related fields as PII requiring additional security controls and access restrictions.

## apiCost: 0.00000000"""

# Write to GitHub
success = write_github_file(repo, file_path, markdown_content, token)

if success:
    print("✅ Gold Logical Data Model successfully created and saved to GitHub!")
else:
    print("❌ Failed to save file to GitHub")
```

## Output Summary

The Gold Layer Logical Data Model has been successfully created for the DC Health Meter Reports system. The model includes:

### 1. **7 Dimension Tables** with appropriate SCD types:
- Go_Distribution_Center_Dim (SCD Type 2)
- Go_Date_Dim (SCD Type 1)  
- Go_Shift_Dim (SCD Type 2)
- Go_Partner_Dim (SCD Type 2)
- Go_Item_Dim (SCD Type 2)
- Go_Activity_Dim (SCD Type 1)
- Go_Employee_Dim (SCD Type 2)

### 2. **6 Fact Tables** covering all operational areas:
- Go_Health_Score_Fact (Overall health metrics)
- Go_Operations_Performance_Fact (Operational efficiency)
- Go_Inventory_Performance_Fact (Inventory management)
- Go_Picking_Performance_Fact (Picking operations)
- Go_Labor_Performance_Fact (Workforce metrics)
- Go_Exception_Events_Fact (Exception tracking)

### 3. **2 Aggregate Tables** for performance optimization:
- Go_Daily_Health_Summary_Agg
- Go_Weekly_Performance_Agg

### 4. **2 Audit/Error Tables** for data governance:
- Go_Process_Audit_Log
- Go_Data_Quality_Errors

### 5. **Key Features**:
- Consistent 'Go_' naming convention
- Comprehensive metadata columns (load_date, update_date, source_system)
- PII classification for all columns
- Business descriptions for all fields
- Proper dimensional modeling with star schema design
- Support for all 21 KPIs from the conceptual model

**outputURL**: https://github.com/ELANSURIYAA/LakehouseInADay_Databricks/tree/main/DI_Databricks_Gold_Model_Logical

**pipelineID**: 12368

**apiCost**: 0.00000000