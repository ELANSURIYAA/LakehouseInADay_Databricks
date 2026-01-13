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
1. All distribution centers must have complete organizational hierarchy information (DC name, region, organization)
2. Daily health score data must be available for all active distribution centers
3. Shift-level operational data must be complete for all scheduled shifts
4. Inventory snapshots must be available daily for all active items in each DC
5. Labor and headcount data must be complete for all scheduled shifts and employees
6. Exception events must have complete lifecycle information from opening to closure
7. Partner information must be complete for all operational activities involving third-party logistics providers

### 1.2 Data Accuracy
1. Health scores must accurately reflect the weighted composite of all domain scores
2. Throughput calculations must use correct labor hours aligned to the same operational grain
3. Pick accuracy percentages must be calculated from validated error counts and total picks
4. Inventory availability calculations must reflect real-time stock positions
5. Staffing variance calculations must use consistent planned vs actual headcount definitions
6. Kronos adherence percentages must be based on actual worked hours within scheduled windows
7. Exception impact measurements must accurately quantify operational disruption

### 1.3 Data Format
1. All timestamp fields must follow consistent datetime format with timezone information
2. Percentage fields must be expressed as decimal values between 0 and 1 or 0 and 100 as specified
3. Health scores must be numeric values between 0 and 100
4. Exception severity must use predefined enumerated values (Low, Medium, High, Critical)
5. Activity types must conform to predefined operational categories
6. Partner types must use standardized classification values
7. All quantity fields must be non-negative numeric values

### 1.4 Data Consistency
1. DC names and identifiers must be consistent across all fact tables and reports
2. Date dimensions must be consistent across all time-based calculations and trending
3. Partner and partner type relationships must be consistent across operational data
4. Item identifiers must be consistent across inventory and picking operations
5. Employee identifiers must be consistent across labor and operational assignments
6. Exception type classifications must be consistent across all exception tracking
7. Organizational hierarchy must be consistent across all regional and network rollups

## 2. Constraints

### 2.1 Mandatory Fields
1. **DC Name**: Required for all operational records to enable location-based analysis
2. **Date**: Required for all fact records to enable time-based reporting and trending
3. **Health Score Components**: All six domain scores (Ops, Inv, Picks, Labor, Kronos, Exceptions) required for overall health score calculation
4. **Activity Type**: Required for all operational records to enable activity-based analysis
5. **Partner Information**: Required for all partner-operated activities to enable performance comparison
6. **Exception Type and Severity**: Required for all exception events to enable proper categorization and prioritization
7. **Employee Role**: Required for all labor records to enable role-based analysis

### 2.2 Uniqueness Requirements
1. **Health Score Grain**: No duplicate health score records for unique combination (DC, Date, Shift, Partner)
2. **Inventory Snapshot Grain**: No duplicate inventory records for unique combination (DC, Date, Item)
3. **Pick Aggregate Grain**: No duplicate pick records for unique combination (DC, Date, Shift, Partner, Activity, Item)
4. **Timecard Grain**: No duplicate timecard records for unique combination (Employee, Date, Shift)
5. **Exception Event**: Each exception event must have unique exception event identifier
6. **Item Master**: Each item must have unique item identifier across the system
7. **Employee Master**: Each employee must have unique employee identifier

### 2.3 Data Type Limitations
1. **Quantities**: All unit quantities, headcount, and volume fields must be non-negative integers
2. **Hours**: All labor hours, cycle time, and duration fields must be non-negative decimal values
3. **Percentages**: All percentage fields must be between 0% and 100% (or 0 and 1 depending on format)
4. **Health Scores**: Must be numeric values between 0 and 100 inclusive
5. **Timestamps**: Must be valid datetime values with proper timezone handling
6. **Rates**: All rate calculations (units/hour, errors per 1000) must handle division by zero scenarios
7. **Variance Calculations**: Must handle scenarios where planned values are zero

### 2.4 Dependencies
1. **Health Score Calculation**: Depends on availability of all six domain component scores
2. **Throughput Calculations**: Depend on both volume data and corresponding labor hours
3. **Accuracy Calculations**: Depend on both error counts and total transaction counts
4. **Variance Calculations**: Depend on both planned and actual values being available
5. **Days of Supply**: Depends on both available quantity and average daily demand data
6. **Exception Resolution**: Depends on both opened and closed timestamp availability
7. **Drill-through Functionality**: Depends on maintaining referential links between summary and detail data

### 2.5 Referential Integrity
1. **DC-Organization Relationship**: All distribution centers must reference valid organizational hierarchy
2. **Employee-Partner Relationship**: All employees must be assigned to valid partners
3. **Item-Category Relationship**: All items must belong to valid product categories
4. **Activity-Equipment Relationship**: Equipment-dependent activities must reference valid equipment
5. **Exception-DC Relationship**: All exceptions must be associated with valid distribution centers
6. **Fact-Dimension Relationships**: All fact records must reference valid dimension records
7. **Partner-PartnerType Relationship**: All partners must be classified under valid partner types

## 3. Business Rules

### 3.1 Data Processing Rules
1. **Health Score Weighting**: Health score calculation must use configurable weights for each domain component that sum to 100%
2. **Backlog Calculation**: Backlog values must not become negative and should be capped at zero unless explicitly allowed by business rules
3. **Overtime Classification**: Hours worked beyond standard shift duration must be classified as overtime according to labor policies
4. **Exception Aging**: Open exceptions must be aged based on business days, excluding weekends and holidays
5. **Inventory Allocation**: Available inventory must not exceed on-hand inventory (available <= on-hand)
6. **Shift Boundary Handling**: Activities spanning multiple shifts must be allocated to the appropriate shift based on start time
7. **Partner Performance Aggregation**: Partner metrics must be aggregated consistently across all operational areas

### 3.2 Reporting Logic Rules
1. **Drill-down Hierarchy**: Must support consistent drill-down paths (Network → Region → DC → Shift)
2. **Drill-through Reconciliation**: Summary totals must reconcile to underlying detail totals in drill-through scenarios
3. **Time Period Aggregation**: Weekly and monthly aggregations must use consistent business calendar definitions
4. **Target Comparison**: All KPIs must support comparison against configurable target values
5. **Trending Analysis**: Historical comparisons must use consistent baseline periods and calculation methods
6. **Exception Impact Allocation**: Exception impacts must be allocated to affected operational metrics consistently
7. **Security Filtering**: Data access must be filtered based on user role and organizational assignment

### 3.3 Transformation Guidelines
1. **Normalization for Health Score**: Domain scores must be normalized to 0-100 scale before weighted aggregation
2. **Rate Calculation Standardization**: All rate calculations must use consistent time units (hours) and volume units
3. **Percentage Calculation Consistency**: All percentage calculations must handle zero denominators gracefully
4. **Timestamp Standardization**: All timestamps must be converted to consistent timezone for cross-DC analysis
5. **Missing Data Handling**: Missing data points must be handled consistently (null vs zero) based on business context
6. **Outlier Detection**: Statistical outliers in operational metrics must be flagged for validation
7. **Data Quality Scoring**: Each data element must include quality indicators for completeness and accuracy assessment