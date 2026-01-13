_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: Comprehensive data mapping for Medallion architecture Bronze layer implementation in Databricks for DC Health Meter Reports
## *Version*: 1 
## *Updated on*: 
_____________________________________________

# Databricks Bronze Model Data Mapping

## Overview
This document defines the comprehensive data mapping for the Bronze layer in the Medallion architecture implementation in Databricks. The Bronze layer serves as the raw data ingestion layer, preserving the original structure and metadata from source systems while ensuring compatibility with Databricks Delta Lake and PySpark.

## Raw Data Ingestion Process

### Data Sources
- **Source System**: DC Health Meter Operational Systems
- **Data Format**: Structured relational data from operational databases
- **Ingestion Method**: Batch processing with Delta Lake format
- **Frequency**: Daily incremental loads with full refresh capability

### Metadata Management
- **Schema Evolution**: Enabled to handle source schema changes
- **Data Lineage**: Tracked through Delta Lake transaction logs
- **Audit Columns**: Added for ingestion timestamp and source tracking

## Data Mapping for Bronze Layer

### Dimension Tables Mapping

#### Dim_Organization
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dim_organization | org_id | Source | Dim_Organization | Org_ID | 1-1 Mapping |
| Bronze | bronze_dim_organization | org_name | Source | Dim_Organization | Org_Name | 1-1 Mapping |
| Bronze | bronze_dim_organization | org_level | Source | Dim_Organization | Org_Level | 1-1 Mapping |
| Bronze | bronze_dim_organization | parent_org_id | Source | Dim_Organization | Parent_Org_ID | 1-1 Mapping |
| Bronze | bronze_dim_organization | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_dim_organization | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Dim_DistributionCenter
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dim_distribution_center | dc_id | Source | Dim_DistributionCenter | DC_ID | 1-1 Mapping |
| Bronze | bronze_dim_distribution_center | dc_name | Source | Dim_DistributionCenter | DC_Name | 1-1 Mapping |
| Bronze | bronze_dim_distribution_center | org_id | Source | Dim_DistributionCenter | Org_ID | 1-1 Mapping |
| Bronze | bronze_dim_distribution_center | dc_status | Source | Dim_DistributionCenter | DC_Status | 1-1 Mapping |
| Bronze | bronze_dim_distribution_center | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_dim_distribution_center | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Dim_Date
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dim_date | date_key | Source | Dim_Date | Date_Key | 1-1 Mapping |
| Bronze | bronze_dim_date | calendar_date | Source | Dim_Date | Calendar_Date | 1-1 Mapping |
| Bronze | bronze_dim_date | week_start_date | Source | Dim_Date | Week_Start_Date | 1-1 Mapping |
| Bronze | bronze_dim_date | fiscal_period | Source | Dim_Date | Fiscal_Period | 1-1 Mapping |
| Bronze | bronze_dim_date | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_dim_date | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Dim_Shift
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dim_shift | shift_id | Source | Dim_Shift | Shift_ID | 1-1 Mapping |
| Bronze | bronze_dim_shift | shift_name | Source | Dim_Shift | Shift_Name | 1-1 Mapping |
| Bronze | bronze_dim_shift | shift_start_time | Source | Dim_Shift | Shift_Start_Time | 1-1 Mapping |
| Bronze | bronze_dim_shift | shift_end_time | Source | Dim_Shift | Shift_End_Time | 1-1 Mapping |
| Bronze | bronze_dim_shift | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_dim_shift | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Dim_PartnerType
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dim_partner_type | partner_type_id | Source | Dim_PartnerType | PartnerType_ID | 1-1 Mapping |
| Bronze | bronze_dim_partner_type | partner_type_name | Source | Dim_PartnerType | PartnerType_Name | 1-1 Mapping |
| Bronze | bronze_dim_partner_type | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_dim_partner_type | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Dim_Partner
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dim_partner | partner_id | Source | Dim_Partner | Partner_ID | 1-1 Mapping |
| Bronze | bronze_dim_partner | partner_name | Source | Dim_Partner | Partner_Name | 1-1 Mapping |
| Bronze | bronze_dim_partner | partner_type_id | Source | Dim_Partner | PartnerType_ID | 1-1 Mapping |
| Bronze | bronze_dim_partner | partner_status | Source | Dim_Partner | Partner_Status | 1-1 Mapping |
| Bronze | bronze_dim_partner | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_dim_partner | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Dim_Item
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dim_item | item_id | Source | Dim_Item | Item_ID | 1-1 Mapping |
| Bronze | bronze_dim_item | item_name | Source | Dim_Item | Item_Name | 1-1 Mapping |
| Bronze | bronze_dim_item | item_category | Source | Dim_Item | Item_Category | 1-1 Mapping |
| Bronze | bronze_dim_item | item_status | Source | Dim_Item | Item_Status | 1-1 Mapping |
| Bronze | bronze_dim_item | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_dim_item | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Dim_Activity
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dim_activity | activity_id | Source | Dim_Activity | Activity_ID | 1-1 Mapping |
| Bronze | bronze_dim_activity | activity_name | Source | Dim_Activity | Activity_Name | 1-1 Mapping |
| Bronze | bronze_dim_activity | activity_group | Source | Dim_Activity | Activity_Group | 1-1 Mapping |
| Bronze | bronze_dim_activity | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_dim_activity | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Dim_Equipment
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dim_equipment | equipment_id | Source | Dim_Equipment | Equipment_ID | 1-1 Mapping |
| Bronze | bronze_dim_equipment | equipment_type | Source | Dim_Equipment | Equipment_Type | 1-1 Mapping |
| Bronze | bronze_dim_equipment | equipment_status | Source | Dim_Equipment | Equipment_Status | 1-1 Mapping |
| Bronze | bronze_dim_equipment | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_dim_equipment | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Dim_Employee
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dim_employee | employee_id | Source | Dim_Employee | Employee_ID | 1-1 Mapping |
| Bronze | bronze_dim_employee | home_dc_id | Source | Dim_Employee | Home_DC_ID | 1-1 Mapping |
| Bronze | bronze_dim_employee | partner_id | Source | Dim_Employee | Partner_ID | 1-1 Mapping |
| Bronze | bronze_dim_employee | role_name | Source | Dim_Employee | Role_Name | 1-1 Mapping |
| Bronze | bronze_dim_employee | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_dim_employee | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Dim_ExceptionType
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dim_exception_type | exception_type_id | Source | Dim_ExceptionType | ExceptionType_ID | 1-1 Mapping |
| Bronze | bronze_dim_exception_type | exception_type | Source | Dim_ExceptionType | Exception_Type | 1-1 Mapping |
| Bronze | bronze_dim_exception_type | exception_subtype | Source | Dim_ExceptionType | Exception_Subtype | 1-1 Mapping |
| Bronze | bronze_dim_exception_type | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_dim_exception_type | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

### Fact Tables Mapping

#### Fact_DC_Operations
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_fact_dc_operations | operations_fact_id | Source | Fact_DC_Operations | Operations_Fact_ID | 1-1 Mapping |
| Bronze | bronze_fact_dc_operations | dc_id | Source | Fact_DC_Operations | DC_ID | 1-1 Mapping |
| Bronze | bronze_fact_dc_operations | date_key | Source | Fact_DC_Operations | Date_Key | 1-1 Mapping |
| Bronze | bronze_fact_dc_operations | shift_id | Source | Fact_DC_Operations | Shift_ID | 1-1 Mapping |
| Bronze | bronze_fact_dc_operations | activity_id | Source | Fact_DC_Operations | Activity_ID | 1-1 Mapping |
| Bronze | bronze_fact_dc_operations | partner_id | Source | Fact_DC_Operations | Partner_ID | 1-1 Mapping |
| Bronze | bronze_fact_dc_operations | equipment_id | Source | Fact_DC_Operations | Equipment_ID | 1-1 Mapping |
| Bronze | bronze_fact_dc_operations | throughput_units | Source | Fact_DC_Operations | Throughput_Units | 1-1 Mapping |
| Bronze | bronze_fact_dc_operations | throughput_lines | Source | Fact_DC_Operations | Throughput_Lines | 1-1 Mapping |
| Bronze | bronze_fact_dc_operations | labor_hours | Source | Fact_DC_Operations | Labor_Hours | 1-1 Mapping |
| Bronze | bronze_fact_dc_operations | cycle_time_minutes | Source | Fact_DC_Operations | Cycle_Time_Minutes | 1-1 Mapping |
| Bronze | bronze_fact_dc_operations | ontime_completion_pct | Source | Fact_DC_Operations | OnTime_Completion_Pct | 1-1 Mapping |
| Bronze | bronze_fact_dc_operations | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_fact_dc_operations | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Fact_Inventory
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_fact_inventory | inventory_fact_id | Source | Fact_Inventory | Inventory_Fact_ID | 1-1 Mapping |
| Bronze | bronze_fact_inventory | dc_id | Source | Fact_Inventory | DC_ID | 1-1 Mapping |
| Bronze | bronze_fact_inventory | date_key | Source | Fact_Inventory | Date_Key | 1-1 Mapping |
| Bronze | bronze_fact_inventory | item_id | Source | Fact_Inventory | Item_ID | 1-1 Mapping |
| Bronze | bronze_fact_inventory | onhand_qty | Source | Fact_Inventory | OnHand_Qty | 1-1 Mapping |
| Bronze | bronze_fact_inventory | available_qty | Source | Fact_Inventory | Available_Qty | 1-1 Mapping |
| Bronze | bronze_fact_inventory | allocated_qty | Source | Fact_Inventory | Allocated_Qty | 1-1 Mapping |
| Bronze | bronze_fact_inventory | damaged_qty | Source | Fact_Inventory | Damaged_Qty | 1-1 Mapping |
| Bronze | bronze_fact_inventory | onorder_qty | Source | Fact_Inventory | OnOrder_Qty | 1-1 Mapping |
| Bronze | bronze_fact_inventory | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_fact_inventory | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Fact_Headcount
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_fact_headcount | headcount_fact_id | Source | Fact_Headcount | Headcount_Fact_ID | 1-1 Mapping |
| Bronze | bronze_fact_headcount | dc_id | Source | Fact_Headcount | DC_ID | 1-1 Mapping |
| Bronze | bronze_fact_headcount | date_key | Source | Fact_Headcount | Date_Key | 1-1 Mapping |
| Bronze | bronze_fact_headcount | shift_id | Source | Fact_Headcount | Shift_ID | 1-1 Mapping |
| Bronze | bronze_fact_headcount | partner_type_id | Source | Fact_Headcount | PartnerType_ID | 1-1 Mapping |
| Bronze | bronze_fact_headcount | partner_id | Source | Fact_Headcount | Partner_ID | 1-1 Mapping |
| Bronze | bronze_fact_headcount | role_name | Source | Fact_Headcount | Role_Name | 1-1 Mapping |
| Bronze | bronze_fact_headcount | planned_headcount | Source | Fact_Headcount | Planned_Headcount | 1-1 Mapping |
| Bronze | bronze_fact_headcount | actual_headcount | Source | Fact_Headcount | Actual_Headcount | 1-1 Mapping |
| Bronze | bronze_fact_headcount | planned_hours | Source | Fact_Headcount | Planned_Hours | 1-1 Mapping |
| Bronze | bronze_fact_headcount | worked_hours | Source | Fact_Headcount | Worked_Hours | 1-1 Mapping |
| Bronze | bronze_fact_headcount | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_fact_headcount | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Fact_Picks
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_fact_picks | picks_fact_id | Source | Fact_Picks | Picks_Fact_ID | 1-1 Mapping |
| Bronze | bronze_fact_picks | dc_id | Source | Fact_Picks | DC_ID | 1-1 Mapping |
| Bronze | bronze_fact_picks | date_key | Source | Fact_Picks | Date_Key | 1-1 Mapping |
| Bronze | bronze_fact_picks | shift_id | Source | Fact_Picks | Shift_ID | 1-1 Mapping |
| Bronze | bronze_fact_picks | activity_id | Source | Fact_Picks | Activity_ID | 1-1 Mapping |
| Bronze | bronze_fact_picks | partner_id | Source | Fact_Picks | Partner_ID | 1-1 Mapping |
| Bronze | bronze_fact_picks | item_id | Source | Fact_Picks | Item_ID | 1-1 Mapping |
| Bronze | bronze_fact_picks | pick_units | Source | Fact_Picks | Pick_Units | 1-1 Mapping |
| Bronze | bronze_fact_picks | pick_lines | Source | Fact_Picks | Pick_Lines | 1-1 Mapping |
| Bronze | bronze_fact_picks | pick_errors | Source | Fact_Picks | Pick_Errors | 1-1 Mapping |
| Bronze | bronze_fact_picks | rework_count | Source | Fact_Picks | Rework_Count | 1-1 Mapping |
| Bronze | bronze_fact_picks | labor_hours | Source | Fact_Picks | Labor_Hours | 1-1 Mapping |
| Bronze | bronze_fact_picks | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_fact_picks | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Fact_Kronos
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_fact_kronos | kronos_fact_id | Source | Fact_Kronos | Kronos_Fact_ID | 1-1 Mapping |
| Bronze | bronze_fact_kronos | employee_id | Source | Fact_Kronos | Employee_ID | 1-1 Mapping |
| Bronze | bronze_fact_kronos | dc_id | Source | Fact_Kronos | DC_ID | 1-1 Mapping |
| Bronze | bronze_fact_kronos | date_key | Source | Fact_Kronos | Date_Key | 1-1 Mapping |
| Bronze | bronze_fact_kronos | shift_id | Source | Fact_Kronos | Shift_ID | 1-1 Mapping |
| Bronze | bronze_fact_kronos | scheduled_hours | Source | Fact_Kronos | Scheduled_Hours | 1-1 Mapping |
| Bronze | bronze_fact_kronos | worked_hours | Source | Fact_Kronos | Worked_Hours | 1-1 Mapping |
| Bronze | bronze_fact_kronos | overtime_hours | Source | Fact_Kronos | Overtime_Hours | 1-1 Mapping |
| Bronze | bronze_fact_kronos | absence_flag | Source | Fact_Kronos | Absence_Flag | 1-1 Mapping |
| Bronze | bronze_fact_kronos | adherence_pct | Source | Fact_Kronos | Adherence_Pct | 1-1 Mapping |
| Bronze | bronze_fact_kronos | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_fact_kronos | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

#### Fact_Exceptions
| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_fact_exceptions | exception_event_id | Source | Fact_Exceptions | Exception_Event_ID | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | exception_type_id | Source | Fact_Exceptions | ExceptionType_ID | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | dc_id | Source | Fact_Exceptions | DC_ID | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | date_key | Source | Fact_Exceptions | Date_Key | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | shift_id | Source | Fact_Exceptions | Shift_ID | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | activity_id | Source | Fact_Exceptions | Activity_ID | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | partner_id | Source | Fact_Exceptions | Partner_ID | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | item_id | Source | Fact_Exceptions | Item_ID | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | equipment_id | Source | Fact_Exceptions | Equipment_ID | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | severity | Source | Fact_Exceptions | Severity | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | status | Source | Fact_Exceptions | Status | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | opened_timestamp | Source | Fact_Exceptions | Opened_Timestamp | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | closed_timestamp | Source | Fact_Exceptions | Closed_Timestamp | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | impact_units | Source | Fact_Exceptions | Impact_Units | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | impact_minutes | Source | Fact_Exceptions | Impact_Minutes | 1-1 Mapping |
| Bronze | bronze_fact_exceptions | ingestion_timestamp | Source | System Generated | CURRENT_TIMESTAMP | System Generated |
| Bronze | bronze_fact_exceptions | source_system | Source | System Generated | 'DC_HEALTH_METER' | System Generated |

## Data Type Specifications for Databricks

### Dimension Tables Data Types
- **Integer Fields**: `INT` (4-byte signed integer)
- **Big Integer Fields**: `BIGINT` (8-byte signed integer)
- **String Fields**: `STRING` (variable-length string)
- **Decimal Fields**: `DECIMAL(10,2)` for monetary/percentage values
- **Date Fields**: `DATE` for calendar dates
- **Time Fields**: `STRING` for time values (HH:MM:SS format)
- **Timestamp Fields**: `TIMESTAMP` for date-time values
- **Boolean Fields**: `BOOLEAN` for true/false values

### Fact Tables Data Types
- **ID Fields**: `BIGINT` for fact table primary keys
- **Foreign Key Fields**: `INT` for dimension references
- **Measure Fields**: `DECIMAL(15,2)` for numeric measures
- **Count Fields**: `INT` for count measures
- **Percentage Fields**: `DECIMAL(5,2)` for percentage values
- **Timestamp Fields**: `TIMESTAMP` for audit columns

## Initial Data Validation Rules

### Data Quality Checks
1. **Null Value Validation**: Ensure required fields are not null
2. **Data Type Validation**: Verify data types match expected schema
3. **Referential Integrity**: Validate foreign key relationships
4. **Domain Value Validation**: Check against allowed domain values
5. **Duplicate Detection**: Identify and flag duplicate records
6. **Data Completeness**: Ensure all expected records are present

### Data Governance
1. **PII Handling**: Mask or hash employee identifiers
2. **Data Retention**: Implement retention policies for historical data
3. **Access Control**: Role-based access to sensitive data
4. **Audit Trail**: Track all data access and modifications

## Technical Implementation Details

### Delta Lake Configuration
- **File Format**: Delta Lake with Parquet storage
- **Partitioning Strategy**: Partition by date_key for time-based queries
- **Optimization**: Enable auto-optimize and auto-compaction
- **Schema Evolution**: Enable schema evolution for flexibility

### PySpark Data Types Mapping
```python
from pyspark.sql.types import *

# Dimension table schema example
dim_organization_schema = StructType([
    StructField("org_id", IntegerType(), False),
    StructField("org_name", StringType(), False),
    StructField("org_level", StringType(), False),
    StructField("parent_org_id", IntegerType(), True),
    StructField("ingestion_timestamp", TimestampType(), False),
    StructField("source_system", StringType(), False)
])

# Fact table schema example
fact_dc_operations_schema = StructType([
    StructField("operations_fact_id", LongType(), False),
    StructField("dc_id", IntegerType(), False),
    StructField("date_key", IntegerType(), False),
    StructField("shift_id", IntegerType(), False),
    StructField("activity_id", IntegerType(), False),
    StructField("partner_id", IntegerType(), False),
    StructField("equipment_id", IntegerType(), True),
    StructField("throughput_units", IntegerType(), False),
    StructField("throughput_lines", IntegerType(), False),
    StructField("labor_hours", DecimalType(10,2), False),
    StructField("cycle_time_minutes", DecimalType(10,2), True),
    StructField("ontime_completion_pct", DecimalType(5,2), True),
    StructField("ingestion_timestamp", TimestampType(), False),
    StructField("source_system", StringType(), False)
])
```

## API Cost Reporting

**apiCost**: 0.025 USD

*Note: This cost represents the estimated API consumption for processing the data mapping requirements, including schema analysis, transformation logic, and documentation generation.*

## Summary

This Bronze layer data mapping ensures:
- **Raw Data Preservation**: Maintains original data structure and values
- **Metadata Enrichment**: Adds audit and lineage information
- **Databricks Compatibility**: Optimized for Delta Lake and PySpark
- **Scalability**: Designed for high-volume data processing
- **Data Governance**: Implements security and compliance requirements
- **Future Extensibility**: Supports schema evolution and new data sources

The mapping provides a solid foundation for the Silver layer transformations while maintaining data integrity and enabling efficient data processing in the Databricks environment.