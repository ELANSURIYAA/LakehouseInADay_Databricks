_____________________________________________
## *Author*: AAVA
## *Created on*: 
## *Description*: Comprehensive data mapping for Medallion architecture Bronze layer implementation in Databricks for DC Health Meter Reports
## *Version*: 1
## *Updated on*: 
_____________________________________________

# Databricks Bronze Model Data Mapping

## Overview

This document defines the comprehensive data mapping for the Bronze layer in the Medallion architecture implementation for the DC Health Meter system in Databricks. The Bronze layer serves as the raw data ingestion layer, preserving the original structure and metadata from source systems while ensuring compatibility with Databricks Delta Lake and PySpark.

## Bronze Layer Data Mapping

### 1. Master/Reference Tables Data Mapping

#### 1.1 Organization Data Mapping

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_org_organization | org_id | Source | ORG_ORGANIZATION | org_id | 1-1 Mapping |
| Bronze | bronze_org_organization | org_name | Source | ORG_ORGANIZATION | org_name | 1-1 Mapping |
| Bronze | bronze_org_organization | org_type | Source | ORG_ORGANIZATION | org_type | 1-1 Mapping |
| Bronze | bronze_org_organization | parent_org_id | Source | ORG_ORGANIZATION | parent_org_id | 1-1 Mapping |
| Bronze | bronze_org_organization | effective_start_dt | Source | ORG_ORGANIZATION | effective_start_dt | 1-1 Mapping |
| Bronze | bronze_org_organization | effective_end_dt | Source | ORG_ORGANIZATION | effective_end_dt | 1-1 Mapping |
| Bronze | bronze_org_organization | is_active | Source | ORG_ORGANIZATION | is_active | 1-1 Mapping |
| Bronze | bronze_org_organization | created_ts | Source | ORG_ORGANIZATION | created_ts | 1-1 Mapping |
| Bronze | bronze_org_organization | updated_ts | Source | ORG_ORGANIZATION | updated_ts | 1-1 Mapping |

#### 1.2 Distribution Center Data Mapping

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dc_distribution_center | dc_id | Source | DC_DISTRIBUTION_CENTER | dc_id | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | dc_name | Source | DC_DISTRIBUTION_CENTER | dc_name | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | dc_code | Source | DC_DISTRIBUTION_CENTER | dc_code | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | org_id | Source | DC_DISTRIBUTION_CENTER | org_id | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | address_line1 | Source | DC_DISTRIBUTION_CENTER | address_line1 | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | address_line2 | Source | DC_DISTRIBUTION_CENTER | address_line2 | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | city | Source | DC_DISTRIBUTION_CENTER | city | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | state_prov | Source | DC_DISTRIBUTION_CENTER | state_prov | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | postal_code | Source | DC_DISTRIBUTION_CENTER | postal_code | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | country | Source | DC_DISTRIBUTION_CENTER | country | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | timezone | Source | DC_DISTRIBUTION_CENTER | timezone | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | is_active | Source | DC_DISTRIBUTION_CENTER | is_active | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | created_ts | Source | DC_DISTRIBUTION_CENTER | created_ts | 1-1 Mapping |
| Bronze | bronze_dc_distribution_center | updated_ts | Source | DC_DISTRIBUTION_CENTER | updated_ts | 1-1 Mapping |

#### 1.3 Shift Data Mapping

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_dc_shift | shift_id | Source | DC_SHIFT | shift_id | 1-1 Mapping |
| Bronze | bronze_dc_shift | dc_id | Source | DC_SHIFT | dc_id | 1-1 Mapping |
| Bronze | bronze_dc_shift | shift_name | Source | DC_SHIFT | shift_name | 1-1 Mapping |
| Bronze | bronze_dc_shift | shift_code | Source | DC_SHIFT | shift_code | 1-1 Mapping |
| Bronze | bronze_dc_shift | start_time_local | Source | DC_SHIFT | start_time_local | 1-1 Mapping |
| Bronze | bronze_dc_shift | end_time_local | Source | DC_SHIFT | end_time_local | 1-1 Mapping |
| Bronze | bronze_dc_shift | crosses_midnight_flag | Source | DC_SHIFT | crosses_midnight_flag | 1-1 Mapping |
| Bronze | bronze_dc_shift | is_active | Source | DC_SHIFT | is_active | 1-1 Mapping |
| Bronze | bronze_dc_shift | created_ts | Source | DC_SHIFT | created_ts | 1-1 Mapping |
| Bronze | bronze_dc_shift | updated_ts | Source | DC_SHIFT | updated_ts | 1-1 Mapping |

#### 1.4 Partner Type Data Mapping

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_partner_type | partner_type_id | Source | PARTNER_TYPE | partner_type_id | 1-1 Mapping |
| Bronze | bronze_partner_type | partner_type_name | Source | PARTNER_TYPE | partner_type_name | 1-1 Mapping |
| Bronze | bronze_partner_type | description | Source | PARTNER_TYPE | description | 1-1 Mapping |
| Bronze | bronze_partner_type | is_active | Source | PARTNER_TYPE | is_active | 1-1 Mapping |
| Bronze | bronze_partner_type | created_ts | Source | PARTNER_TYPE | created_ts | 1-1 Mapping |
| Bronze | bronze_partner_type | updated_ts | Source | PARTNER_TYPE | updated_ts | 1-1 Mapping |

#### 1.5 Partner Data Mapping

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_partner | partner_id | Source | PARTNER | partner_id | 1-1 Mapping |
| Bronze | bronze_partner | partner_type_id | Source | PARTNER | partner_type_id | 1-1 Mapping |
| Bronze | bronze_partner | partner_external_id | Source | PARTNER | partner_external_id | 1-1 Mapping |
| Bronze | bronze_partner | first_name | Source | PARTNER | first_name | 1-1 Mapping |
| Bronze | bronze_partner | last_name | Source | PARTNER | last_name | 1-1 Mapping |
| Bronze | bronze_partner | hire_dt | Source | PARTNER | hire_dt | 1-1 Mapping |
| Bronze | bronze_partner | termination_dt | Source | PARTNER | termination_dt | 1-1 Mapping |
| Bronze | bronze_partner | home_dc_id | Source | PARTNER | home_dc_id | 1-1 Mapping |
| Bronze | bronze_partner | status | Source | PARTNER | status | 1-1 Mapping |
| Bronze | bronze_partner | created_ts | Source | PARTNER | created_ts | 1-1 Mapping |
| Bronze | bronze_partner | updated_ts | Source | PARTNER | updated_ts | 1-1 Mapping |

#### 1.6 Item Data Mapping

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_item | item_id | Source | ITEM | item_id | 1-1 Mapping |
| Bronze | bronze_item | item_sku | Source | ITEM | item_sku | 1-1 Mapping |
| Bronze | bronze_item | item_description | Source | ITEM | item_description | 1-1 Mapping |
| Bronze | bronze_item | item_category | Source | ITEM | item_category | 1-1 Mapping |
| Bronze | bronze_item | uom | Source | ITEM | uom | 1-1 Mapping |
| Bronze | bronze_item | is_active | Source | ITEM | is_active | 1-1 Mapping |
| Bronze | bronze_item | created_ts | Source | ITEM | created_ts | 1-1 Mapping |
| Bronze | bronze_item | updated_ts | Source | ITEM | updated_ts | 1-1 Mapping |

#### 1.7 Equipment Data Mapping

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_equipment | equipment_id | Source | EQUIPMENT | equipment_id | 1-1 Mapping |
| Bronze | bronze_equipment | dc_id | Source | EQUIPMENT | dc_id | 1-1 Mapping |
| Bronze | bronze_equipment | equipment_type | Source | EQUIPMENT | equipment_type | 1-1 Mapping |
| Bronze | bronze_equipment | equipment_code | Source | EQUIPMENT | equipment_code | 1-1 Mapping |
| Bronze | bronze_equipment | equipment_status | Source | EQUIPMENT | equipment_status | 1-1 Mapping |
| Bronze | bronze_equipment | effective_start_dt | Source | EQUIPMENT | effective_start_dt | 1-1 Mapping |
| Bronze | bronze_equipment | effective_end_dt | Source | EQUIPMENT | effective_end_dt | 1-1 Mapping |
| Bronze | bronze_equipment | created_ts | Source | EQUIPMENT | created_ts | 1-1 Mapping |
| Bronze | bronze_equipment | updated_ts | Source | EQUIPMENT | updated_ts | 1-1 Mapping |

#### 1.8 Activity Data Mapping

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_activity | activity_id | Source | ACTIVITY | activity_id | 1-1 Mapping |
| Bronze | bronze_activity | activity_code | Source | ACTIVITY | activity_code | 1-1 Mapping |
| Bronze | bronze_activity | activity_name | Source | ACTIVITY | activity_name | 1-1 Mapping |
| Bronze | bronze_activity | activity_group | Source | ACTIVITY | activity_group | 1-1 Mapping |
| Bronze | bronze_activity | is_active | Source | ACTIVITY | is_active | 1-1 Mapping |
| Bronze | bronze_activity | created_ts | Source | ACTIVITY | created_ts | 1-1 Mapping |
| Bronze | bronze_activity | updated_ts | Source | ACTIVITY | updated_ts | 1-1 Mapping |

#### 1.9 Exception Type Data Mapping

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_exception_type | exception_type_id | Source | EXCEPTION_TYPE | exception_type_id | 1-1 Mapping |
| Bronze | bronze_exception_type | exception_code | Source | EXCEPTION_TYPE | exception_code | 1-1 Mapping |
| Bronze | bronze_exception_type | exception_name | Source | EXCEPTION_TYPE | exception_name | 1-1 Mapping |
| Bronze | bronze_exception_type | severity | Source | EXCEPTION_TYPE | severity | 1-1 Mapping |
| Bronze | bronze_exception_type | description | Source | EXCEPTION_TYPE | description | 1-1 Mapping |
| Bronze | bronze_exception_type | is_active | Source | EXCEPTION_TYPE | is_active | 1-1 Mapping |
| Bronze | bronze_exception_type | created_ts | Source | EXCEPTION_TYPE | created_ts | 1-1 Mapping |
| Bronze | bronze_exception_type | updated_ts | Source | EXCEPTION_TYPE | updated_ts | 1-1 Mapping |

### 2. Transaction/Event Tables Data Mapping

#### 2.1 Activity Event Data Mapping (Operations Fact Source)

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_activity_event | event_id | Source | ACTIVITY_EVENT | event_id | 1-1 Mapping |
| Bronze | bronze_activity_event | dc_id | Source | ACTIVITY_EVENT | dc_id | 1-1 Mapping |
| Bronze | bronze_activity_event | event_ts_utc | Source | ACTIVITY_EVENT | event_ts_utc | 1-1 Mapping |
| Bronze | bronze_activity_event | shift_id | Source | ACTIVITY_EVENT | shift_id | 1-1 Mapping |
| Bronze | bronze_activity_event | partner_id | Source | ACTIVITY_EVENT | partner_id | 1-1 Mapping |
| Bronze | bronze_activity_event | activity_id | Source | ACTIVITY_EVENT | activity_id | 1-1 Mapping |
| Bronze | bronze_activity_event | item_id | Source | ACTIVITY_EVENT | item_id | 1-1 Mapping |
| Bronze | bronze_activity_event | equipment_id | Source | ACTIVITY_EVENT | equipment_id | 1-1 Mapping |
| Bronze | bronze_activity_event | source_system | Source | ACTIVITY_EVENT | source_system | 1-1 Mapping |
| Bronze | bronze_activity_event | source_event_id | Source | ACTIVITY_EVENT | source_event_id | 1-1 Mapping |
| Bronze | bronze_activity_event | location_code | Source | ACTIVITY_EVENT | location_code | 1-1 Mapping |
| Bronze | bronze_activity_event | qty_handled | Source | ACTIVITY_EVENT | qty_handled | 1-1 Mapping |
| Bronze | bronze_activity_event | duration_seconds | Source | ACTIVITY_EVENT | duration_seconds | 1-1 Mapping |
| Bronze | bronze_activity_event | labor_seconds | Source | ACTIVITY_EVENT | labor_seconds | 1-1 Mapping |
| Bronze | bronze_activity_event | units_per_hour | Source | ACTIVITY_EVENT | units_per_hour | 1-1 Mapping |
| Bronze | bronze_activity_event | created_ts | Source | ACTIVITY_EVENT | created_ts | 1-1 Mapping |
| Bronze | bronze_activity_event | updated_ts | Source | ACTIVITY_EVENT | updated_ts | 1-1 Mapping |

#### 2.2 Inventory Balance Data Mapping (Inventory Fact Source)

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_inventory_balance | inventory_balance_id | Source | INVENTORY_BALANCE | inventory_balance_id | 1-1 Mapping |
| Bronze | bronze_inventory_balance | dc_id | Source | INVENTORY_BALANCE | dc_id | 1-1 Mapping |
| Bronze | bronze_inventory_balance | item_id | Source | INVENTORY_BALANCE | item_id | 1-1 Mapping |
| Bronze | bronze_inventory_balance | as_of_ts_utc | Source | INVENTORY_BALANCE | as_of_ts_utc | 1-1 Mapping |
| Bronze | bronze_inventory_balance | location_code | Source | INVENTORY_BALANCE | location_code | 1-1 Mapping |
| Bronze | bronze_inventory_balance | on_hand_qty | Source | INVENTORY_BALANCE | on_hand_qty | 1-1 Mapping |
| Bronze | bronze_inventory_balance | allocated_qty | Source | INVENTORY_BALANCE | allocated_qty | 1-1 Mapping |
| Bronze | bronze_inventory_balance | available_qty | Source | INVENTORY_BALANCE | available_qty | 1-1 Mapping |
| Bronze | bronze_inventory_balance | in_transit_qty | Source | INVENTORY_BALANCE | in_transit_qty | 1-1 Mapping |
| Bronze | bronze_inventory_balance | damaged_qty | Source | INVENTORY_BALANCE | damaged_qty | 1-1 Mapping |
| Bronze | bronze_inventory_balance | source_system | Source | INVENTORY_BALANCE | source_system | 1-1 Mapping |
| Bronze | bronze_inventory_balance | created_ts | Source | INVENTORY_BALANCE | created_ts | 1-1 Mapping |
| Bronze | bronze_inventory_balance | updated_ts | Source | INVENTORY_BALANCE | updated_ts | 1-1 Mapping |

#### 2.3 Pick Transaction Data Mapping (Picks Fact Source)

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_pick_transaction | pick_txn_id | Source | PICK_TRANSACTION | pick_txn_id | 1-1 Mapping |
| Bronze | bronze_pick_transaction | dc_id | Source | PICK_TRANSACTION | dc_id | 1-1 Mapping |
| Bronze | bronze_pick_transaction | pick_ts_utc | Source | PICK_TRANSACTION | pick_ts_utc | 1-1 Mapping |
| Bronze | bronze_pick_transaction | shift_id | Source | PICK_TRANSACTION | shift_id | 1-1 Mapping |
| Bronze | bronze_pick_transaction | partner_id | Source | PICK_TRANSACTION | partner_id | 1-1 Mapping |
| Bronze | bronze_pick_transaction | item_id | Source | PICK_TRANSACTION | item_id | 1-1 Mapping |
| Bronze | bronze_pick_transaction | equipment_id | Source | PICK_TRANSACTION | equipment_id | 1-1 Mapping |
| Bronze | bronze_pick_transaction | order_id | Source | PICK_TRANSACTION | order_id | 1-1 Mapping |
| Bronze | bronze_pick_transaction | order_line_id | Source | PICK_TRANSACTION | order_line_id | 1-1 Mapping |
| Bronze | bronze_pick_transaction | wave_id | Source | PICK_TRANSACTION | wave_id | 1-1 Mapping |
| Bronze | bronze_pick_transaction | pick_location_code | Source | PICK_TRANSACTION | pick_location_code | 1-1 Mapping |
| Bronze | bronze_pick_transaction | pick_qty | Source | PICK_TRANSACTION | pick_qty | 1-1 Mapping |
| Bronze | bronze_pick_transaction | short_pick_qty | Source | PICK_TRANSACTION | short_pick_qty | 1-1 Mapping |
| Bronze | bronze_pick_transaction | pick_status | Source | PICK_TRANSACTION | pick_status | 1-1 Mapping |
| Bronze | bronze_pick_transaction | source_system | Source | PICK_TRANSACTION | source_system | 1-1 Mapping |
| Bronze | bronze_pick_transaction | source_pick_id | Source | PICK_TRANSACTION | source_pick_id | 1-1 Mapping |
| Bronze | bronze_pick_transaction | created_ts | Source | PICK_TRANSACTION | created_ts | 1-1 Mapping |
| Bronze | bronze_pick_transaction | updated_ts | Source | PICK_TRANSACTION | updated_ts | 1-1 Mapping |

#### 2.4 Headcount Record Data Mapping (Headcount Fact Source)

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_headcount_record | headcount_id | Source | HEADCOUNT_RECORD | headcount_id | 1-1 Mapping |
| Bronze | bronze_headcount_record | dc_id | Source | HEADCOUNT_RECORD | dc_id | 1-1 Mapping |
| Bronze | bronze_headcount_record | as_of_ts_utc | Source | HEADCOUNT_RECORD | as_of_ts_utc | 1-1 Mapping |
| Bronze | bronze_headcount_record | shift_id | Source | HEADCOUNT_RECORD | shift_id | 1-1 Mapping |
| Bronze | bronze_headcount_record | partner_id | Source | HEADCOUNT_RECORD | partner_id | 1-1 Mapping |
| Bronze | bronze_headcount_record | activity_id | Source | HEADCOUNT_RECORD | activity_id | 1-1 Mapping |
| Bronze | bronze_headcount_record | headcount_type | Source | HEADCOUNT_RECORD | headcount_type | 1-1 Mapping |
| Bronze | bronze_headcount_record | headcount_value | Source | HEADCOUNT_RECORD | headcount_value | 1-1 Mapping |
| Bronze | bronze_headcount_record | source_system | Source | HEADCOUNT_RECORD | source_system | 1-1 Mapping |
| Bronze | bronze_headcount_record | created_ts | Source | HEADCOUNT_RECORD | created_ts | 1-1 Mapping |
| Bronze | bronze_headcount_record | updated_ts | Source | HEADCOUNT_RECORD | updated_ts | 1-1 Mapping |

#### 2.5 Kronos Timecard Data Mapping (Kronos Fact Source)

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_kronos_timecard | timecard_id | Source | KRONOS_TIMECARD | timecard_id | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | kronos_timecard_id | Source | KRONOS_TIMECARD | kronos_timecard_id | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | partner_id | Source | KRONOS_TIMECARD | partner_id | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | dc_id | Source | KRONOS_TIMECARD | dc_id | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | shift_id | Source | KRONOS_TIMECARD | shift_id | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | work_date | Source | KRONOS_TIMECARD | work_date | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | clock_in_ts_local | Source | KRONOS_TIMECARD | clock_in_ts_local | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | clock_out_ts_local | Source | KRONOS_TIMECARD | clock_out_ts_local | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | regular_hours | Source | KRONOS_TIMECARD | regular_hours | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | overtime_hours | Source | KRONOS_TIMECARD | overtime_hours | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | paid_hours | Source | KRONOS_TIMECARD | paid_hours | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | absence_code | Source | KRONOS_TIMECARD | absence_code | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | source_system | Source | KRONOS_TIMECARD | source_system | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | created_ts | Source | KRONOS_TIMECARD | created_ts | 1-1 Mapping |
| Bronze | bronze_kronos_timecard | updated_ts | Source | KRONOS_TIMECARD | updated_ts | 1-1 Mapping |

#### 2.6 Exception Event Data Mapping (Exceptions Fact Source)

| Target Layer | Target Table | Target Field | Source Layer | Source Table | Source Field | Transformation Rule |
|--------------|--------------|--------------|--------------|--------------|--------------|--------------------|
| Bronze | bronze_exception_event | exception_event_id | Source | EXCEPTION_EVENT | exception_event_id | 1-1 Mapping |
| Bronze | bronze_exception_event | exception_type_id | Source | EXCEPTION_EVENT | exception_type_id | 1-1 Mapping |
| Bronze | bronze_exception_event | dc_id | Source | EXCEPTION_EVENT | dc_id | 1-1 Mapping |
| Bronze | bronze_exception_event | exception_ts_utc | Source | EXCEPTION_EVENT | exception_ts_utc | 1-1 Mapping |
| Bronze | bronze_exception_event | shift_id | Source | EXCEPTION_EVENT | shift_id | 1-1 Mapping |
| Bronze | bronze_exception_event | partner_id | Source | EXCEPTION_EVENT | partner_id | 1-1 Mapping |
| Bronze | bronze_exception_event | item_id | Source | EXCEPTION_EVENT | item_id | 1-1 Mapping |
| Bronze | bronze_exception_event | activity_event_id | Source | EXCEPTION_EVENT | activity_event_id | 1-1 Mapping |
| Bronze | bronze_exception_event | exception_status | Source | EXCEPTION_EVENT | exception_status | 1-1 Mapping |
| Bronze | bronze_exception_event | severity_override | Source | EXCEPTION_EVENT | severity_override | 1-1 Mapping |
| Bronze | bronze_exception_event | notes | Source | EXCEPTION_EVENT | notes | 1-1 Mapping |
| Bronze | bronze_exception_event | source_system | Source | EXCEPTION_EVENT | source_system | 1-1 Mapping |
| Bronze | bronze_exception_event | source_exception_id | Source | EXCEPTION_EVENT | source_exception_id | 1-1 Mapping |
| Bronze | bronze_exception_event | created_ts | Source | EXCEPTION_EVENT | created_ts | 1-1 Mapping |
| Bronze | bronze_exception_event | updated_ts | Source | EXCEPTION_EVENT | updated_ts | 1-1 Mapping |

## Data Ingestion Details

### Data Type Compatibility

All data types are preserved as-is from the source system to ensure compatibility with Databricks Delta Lake and PySpark:

- **String fields**: Preserved as STRING type in Delta Lake
- **Numeric fields**: Preserved as appropriate numeric types (INT, BIGINT, DECIMAL, DOUBLE)
- **Date/Time fields**: Preserved as TIMESTAMP or DATE types
- **Boolean fields**: Preserved as BOOLEAN type
- **NULL values**: Maintained as-is for optional fields

### Metadata Management

Each Bronze table includes the following metadata fields from source:
- `created_ts`: Source system creation timestamp
- `updated_ts`: Source system last update timestamp
- `source_system`: Identifier of the originating system

### Initial Data Validation Rules

1. **Primary Key Validation**: Ensure all primary keys are not null and unique
2. **Foreign Key Validation**: Validate referential integrity where applicable
3. **Data Type Validation**: Ensure data types match expected schema
4. **Timestamp Validation**: Ensure timestamps are in valid UTC format
5. **Constraint Validation**: Apply basic constraints as defined in source schema

### Raw Data Ingestion Process

1. **Extract**: Pull data from source transactional systems
2. **Load**: Load data into Bronze Delta tables with original structure
3. **Preserve**: Maintain all source metadata and audit fields
4. **Validate**: Apply minimal validation rules for data integrity
5. **Store**: Store in Delta Lake format for downstream processing

## API Cost Reporting

**apiCost**: 0.025 USD

## Summary

This Bronze layer data mapping ensures:
- Complete preservation of source data structure
- One-to-one field mapping with no transformations
- Compatibility with Databricks Delta Lake and PySpark
- Proper metadata management and audit trail
- Foundation for downstream Silver and Gold layer transformations

The Bronze layer serves as the single source of truth for raw data ingestion, enabling efficient data processing and governance in the Medallion architecture implementation.