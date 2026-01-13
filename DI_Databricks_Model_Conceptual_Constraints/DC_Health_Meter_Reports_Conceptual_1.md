_____________________________________________
## *Author*: AAVA
## *Created on*: 2024-12-19
## *Description*: Conceptual data model for DC Health Meter Reports
## *Version*: 1
## *Updated on*: 2024-12-19
_____________________________________________

# Conceptual Data Model for DC Health Meter Reports

## 1. Domain Overview

The DC Health Meter system covers the distribution center performance monitoring domain, focusing on comprehensive operational analytics across multiple business areas including operations performance, inventory management, labor productivity, picking operations, workforce management, and exception handling. The system provides real-time and historical visibility into distribution center health through standardized metrics and KPIs that enable rapid course-correction and performance optimization.

## 2. List of Entity Names with Descriptions

1. **Distribution Center**: Physical distribution center locations that handle inventory storage, picking, packing, and shipping operations
2. **Organization**: Hierarchical organizational structure containing regions and network-level groupings for distribution centers
3. **Date**: Calendar date dimension for time-based reporting and trending analysis
4. **Shift**: Work shift periods within distribution centers (e.g., day shift, night shift, weekend shifts)
5. **Partner**: Third-party logistics providers or internal teams operating within distribution centers
6. **Partner Type**: Classification of partners by operational model (internal, 3PL, contractor, etc.)
7. **Item**: Products, SKUs, or inventory items processed through distribution center operations
8. **Activity**: Operational activities performed in distribution centers (receiving, putaway, picking, packing, shipping, cycle count)
9. **Equipment**: Physical equipment and systems used in distribution center operations
10. **Employee**: Workforce members assigned to distribution center operations
11. **Exception Event**: Operational disruptions, issues, or anomalies that impact distribution center performance
12. **Labor Role**: Job functions and positions within distribution center operations

## 3. List of Attributes for Each Entity

### Distribution Center
1. **DC Name**: Business name identifier for the distribution center
2. **Region**: Geographic or organizational region assignment
3. **Active Status**: Operational status indicating if DC is currently active
4. **Location**: Physical location information

### Organization
1. **Organization Name**: Name of the organizational unit
2. **Hierarchy Level**: Level within organizational structure (network, region, DC)
3. **Parent Organization**: Reference to parent organizational unit

### Date
1. **Calendar Date**: Specific calendar date
2. **Day of Week**: Day of the week designation
3. **Week Number**: Week number within year
4. **Month**: Month designation
5. **Quarter**: Quarter designation
6. **Year**: Year designation

### Shift
1. **Shift Name**: Identifier for the shift period
2. **Start Time**: Scheduled start time for the shift
3. **End Time**: Scheduled end time for the shift
4. **Shift Type**: Classification of shift (regular, overtime, weekend)

### Partner
1. **Partner Name**: Business name of the partner organization
2. **Partner Status**: Active status of partner relationship
3. **Contract Type**: Type of partnership agreement

### Partner Type
1. **Type Name**: Classification name for partner type
2. **Type Description**: Detailed description of partner type characteristics

### Item
1. **Item Name**: Product or SKU name
2. **Category**: Product category classification
3. **Status**: Item status (active, discontinued, seasonal)
4. **Item Characteristics**: Physical or operational characteristics affecting handling

### Activity
1. **Activity Name**: Name of the operational activity
2. **Activity Type**: Classification of activity type
3. **Standard Duration**: Expected time for activity completion
4. **Equipment Required**: Equipment dependencies for the activity

### Equipment
1. **Equipment Name**: Identifier for the equipment
2. **Equipment Type**: Classification of equipment
3. **Capacity**: Operational capacity of the equipment
4. **Status**: Current operational status

### Employee
1. **Employee Name**: Name of the workforce member
2. **Employee Status**: Employment status
3. **Hire Date**: Date of employment start

### Exception Event
1. **Exception Type**: Category of exception (inventory, equipment, system, process, safety, quality)
2. **Severity**: Impact level (low, medium, high, critical)
3. **Status**: Current status (open, in progress, closed)
4. **Opened Timestamp**: When exception was first identified
5. **Closed Timestamp**: When exception was resolved
6. **Description**: Detailed description of the exception
7. **Impact Units**: Quantified impact on operational units
8. **Impact Minutes**: Time impact of the exception

### Labor Role
1. **Role Name**: Name of the job function
2. **Role Description**: Detailed description of role responsibilities
3. **Skill Level**: Required skill level for the role

## 4. KPI List

1. **Overall DC Health Score**: Composite score (0-100) representing overall distribution center performance
2. **On-time Shipping Percentage**: Percentage of shipments completed on schedule
3. **Throughput Units per Hour**: Operational efficiency measured in units processed per hour
4. **Pick Accuracy Percentage**: Accuracy rate of picking operations
5. **Inventory Availability Percentage**: Percentage of items available for fulfillment
6. **Staffing Variance Percentage**: Variance between planned and actual headcount
7. **Kronos Adherence Percentage**: Adherence to scheduled work hours
8. **Exceptions per 1,000 Units**: Exception rate normalized per thousand units processed
9. **Cycle Time**: Time required to complete operational activities
10. **Backlog Units**: Volume of work pending completion
11. **On-time Start Percentage**: Percentage of activities starting on schedule
12. **On-time Completion Percentage**: Percentage of activities completed on schedule
13. **Stockout Percentage**: Percentage of items with zero availability
14. **Days of Supply**: Inventory coverage measured in days
15. **Pick Rate**: Picking productivity measured in units per hour
16. **Error Rate per 1,000 Lines**: Error frequency per thousand pick lines
17. **Labor Hours Variance Percentage**: Variance between scheduled and worked hours
18. **Overtime Hours Percentage**: Percentage of total hours worked as overtime
19. **Absence Rate Percentage**: Employee absence frequency
20. **Mean Time to Resolve**: Average time to resolve exceptions
21. **Repeat Rate Percentage**: Frequency of recurring exceptions

## 5. Conceptual Data Model Diagram

| Source Entity | Relationship Key Field | Target Entity | Relationship Type |
|---------------|------------------------|---------------|-------------------|
| Organization | organization_key | Distribution Center | One-to-Many |
| Distribution Center | dc_key | Shift | One-to-Many |
| Partner Type | partner_type_key | Partner | One-to-Many |
| Distribution Center | dc_key | Partner | Many-to-Many |
| Item | item_key | Activity | Many-to-Many |
| Equipment | equipment_key | Activity | Many-to-Many |
| Employee | partner_key | Partner | Many-to-One |
| Employee | dc_key | Distribution Center | Many-to-One |
| Employee | labor_role_key | Labor Role | Many-to-One |
| Exception Event | exception_key | Distribution Center | Many-to-One |
| Date | date_key | All Fact Tables | One-to-Many |
| Shift | shift_key | Operational Facts | One-to-Many |

## 6. Common Data Elements in Report Requirements

1. **DC Name**: Referenced across all six report types for location-based analysis
2. **Date**: Universal time dimension used in all reporting requirements
3. **Shift**: Common operational time period used in operations, picks, and labor reports
4. **Partner and Partner Type**: Consistent partner identification across operations, picks, and labor reports
5. **Activity**: Operational activity classification used in operations and exception reports
6. **Equipment**: Equipment identification used in operations and exception reports
7. **Item**: Product/SKU reference used in inventory and picks reports
8. **Throughput Units**: Volume measure used in health scorecard and operations reports
9. **Labor Hours**: Time measure used in operations, picks, and labor reports
10. **Exception Count**: Exception volume used in health scorecard and exception reports
11. **Region**: Geographic grouping used across multiple reports for hierarchical analysis
12. **Health Score Components**: Domain scores (Ops, Inv, Picks, Labor, Kronos, Exceptions) referenced in health scorecard
13. **Timestamp Fields**: Start/end times used in operations and exception reports for cycle time calculations
14. **Variance Calculations**: Planned vs actual comparisons used in labor and operations reports
15. **Accuracy Metrics**: Quality measures used in picks and inventory reports