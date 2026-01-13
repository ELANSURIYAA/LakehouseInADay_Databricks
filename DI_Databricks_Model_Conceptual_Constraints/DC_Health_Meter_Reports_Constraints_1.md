____________________________________________
## *Author*: AAVA
## *Created on*: 2024-12-19
## *Description*: Model data constraints and business rules for DC Health Meter Reports
## *Version*: 1
## *Updated on*: 2024-12-19
____________________________________________

# Model Data Constraints for DC Health Meter Reports

## 1. Data Expectations

### 1.1 Data Completeness
1. All distribution centers must have complete organizational hierarchy information including DC name, region, and organization structure
2. Daily health score data must be available for all active distribution centers
3. Shift-level operational data must be complete for all scheduled shifts
4. Inventory snapshots must be available daily for all active items in each distribution center
5. Labor and headcount data must be complete for all scheduled employees and shifts
6. Exception events must capture complete information including timestamps, type, severity, and resolution status

### 1.2 Data Accuracy
1. Health scores must accurately reflect the weighted composite of normalized domain scores
2. Throughput calculations must use correct labor hours aligned to the appropriate grain (shift/activity)
3. Pick accuracy percentages must be calculated using validated error counts against total picks
4. Inventory availability calculations must use accurate on-hand and available quantities
5. Staffing variance calculations must use validated planned versus actual headcount data
6. Exception impact measurements must accurately reflect operational disruption

### 1.3 Data Format
1. Health scores must be presented as integers between 0 and 100
2. Percentage metrics must be formatted with appropriate decimal precision
3. Timestamps must follow consistent format and timezone standards
4. Currency and unit measurements must use standardized formats
5. Employee identifiers must follow consistent masking rules for security
6. Exception severity levels must use predefined enumerated values

### 1.4 Data Consistency
1. Distribution center identifiers must be consistent across all fact tables and reports
2. Date and shift references must align across all operational reports
3. Partner and partner type classifications must be consistent across all reports
4. Activity definitions must be standardized across operational and exception reports
5. KPI calculations must use consistent formulas and business rules across reports
6. Organizational hierarchy must be consistent across all drill-down and aggregation operations

## 2. Constraints

### 2.1 Mandatory Fields
1. **DC Name**: Required for all operational records to enable distribution center identification and reporting
2. **Date**: Mandatory for all fact records to enable temporal analysis and trending
3. **Health Score Components**: All domain scores (Ops, Inv, Picks, Labor, Kronos, Exceptions) required for overall health score calculation
4. **Activity Type**: Required for operational performance records to enable activity-based analysis
5. **Exception Type**: Mandatory for all exception events to enable categorization and root cause analysis
6. **Employee Identifier**: Required for labor and Kronos adherence records to enable workforce analysis
7. **Item Identifier**: Mandatory for inventory and picks records to enable item-level analysis

### 2.2 Uniqueness Requirements
1. **DC Health Score Grain**: Unique combination of (DC, Date, Shift, Partner) to prevent duplicate score records
2. **Inventory Snapshot Grain**: Unique combination of (DC, Date, Item) to prevent duplicate inventory records
3. **Pick Aggregates Grain**: Unique combination of (DC, Date, Shift, Partner, Activity, Item) for pick performance records
4. **Timecard Grain**: Unique combination of (Employee, Date, Shift) to prevent duplicate timecard records
5. **Exception Event ID**: Must be unique across all exception records
6. **Item Master**: Item identifier must be unique per item in the item master

### 2.3 Data Type Limitations
1. **Health Score**: Must be integer between 0 and 100
2. **Percentage Metrics**: Must be between 0% and 100% for accuracy, availability, and adherence measures
3. **Quantities**: Pick units, lines, inventory quantities must be non-negative integers
4. **Hours**: Scheduled and worked hours must be non-negative decimal values
5. **Timestamps**: Must follow valid datetime format with end timestamp >= start timestamp
6. **Exception Severity**: Must be one of predefined values (Low, Medium, High, Critical)

### 2.4 Dependencies
1. **Health Score Calculation**: Depends on availability of all six domain scores (Ops, Inv, Picks, Labor, Kronos, Exceptions)
2. **Throughput Calculation**: Depends on both units processed and labor hours worked for the same grain
3. **Staffing Variance**: Depends on both planned and actual headcount data for the same period
4. **Days of Supply**: Depends on available quantity and average daily demand data
5. **Pick Accuracy**: Depends on both total picks and error counts for the same operational period
6. **Exception Resolution**: Depends on both opened and closed timestamps for MTTR calculation

### 2.5 Referential Integrity
1. **DC-Organization Relationship**: Distribution center must exist in organization hierarchy and be active for selected date
2. **Employee-Partner Relationship**: Employee records must reference valid partner assignments
3. **Item-Category Relationship**: Items must reference valid category classifications
4. **Activity-Equipment Relationship**: Equipment assignments must reference valid activity types
5. **Exception-Activity Relationship**: Exception events must reference valid activities when applicable
6. **Shift-DC Relationship**: Shift records must reference valid distribution center assignments

## 3. Business Rules

### 3.1 Data Processing Rules
1. Health Score calculation must use configurable weights for domain score composition
2. Staffing variance percentage calculated as (Actual HC - Planned HC) / Planned HC × 100
3. Exceptions per 1,000 units calculated as Exception Count / Throughput Units × 1,000
4. Backlog calculation must cap negative values at 0 unless explicitly allowed by business rules
5. Days of Supply calculation must handle zero demand scenarios appropriately
6. Overtime percentage must be computed correctly and not result in negative values

### 3.2 Reporting Logic Rules
1. Component domain scores must roll up to overall health score per configured weights
2. Drill-through totals must reconcile to source fact totals for data integrity
3. Measures used in rate calculations must be non-zero where required to prevent division errors
4. Error counts must not exceed total picks in accuracy calculations
5. Available inventory quantities must not exceed on-hand quantities
6. Repeat exception rate must use consistent time window logic for calculation

### 3.3 Transformation Guidelines
1. All percentage metrics must be normalized to 0-100 scale for consistency
2. Timestamp conversions must maintain timezone consistency across all reports
3. Employee identifier masking must be applied consistently based on user access levels
4. Currency and unit standardization must be applied across all financial and operational metrics
5. Exception type mapping must follow predefined categorization rules
6. Activity classifications must be standardized across all operational data sources