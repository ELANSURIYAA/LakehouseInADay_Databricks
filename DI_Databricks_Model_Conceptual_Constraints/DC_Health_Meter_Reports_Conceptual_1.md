_____________________________________________
## *Author*: AAVA
## *Created on*: 2024-12-19
## *Description*: Conceptual data model for DC Health Meter Reports
## *Version*: 1
## *Updated on*: 2024-12-19
_____________________________________________

# Conceptual Data Model for DC Health Meter Reports

## 1. Domain Overview

The DC Health Meter system covers the distribution center operations domain, focusing on performance monitoring across multiple operational areas including operations performance, inventory management, labor management, picking operations, workforce adherence, and exception tracking. The system provides comprehensive visibility into distribution center health through various operational metrics and KPIs to enable rapid course-correction and performance optimization.

## 2. List of Entity Names with Descriptions

1. **Distribution Center**: Physical distribution center locations that handle inventory and fulfillment operations
2. **Organization**: Hierarchical organizational structure containing regions and network divisions
3. **Date**: Calendar date dimension for temporal reporting and analysis
4. **Shift**: Work shift periods within distribution centers (daily operational periods)
5. **Partner**: Third-party partners or internal teams operating within distribution centers
6. **Partner Type**: Classification of partners (internal, external, contractor types)
7. **Item**: Products, SKUs, and inventory items processed through distribution centers
8. **Activity**: Operational activities performed in distribution centers (receiving, putaway, picking, packing, shipping, cycle count)
9. **Equipment**: Operational equipment used in distribution center activities
10. **Employee**: Workforce members working in distribution centers
11. **Exception Event**: Operational exceptions and issues that impact distribution center performance
12. **Labor Role**: Job roles and positions within distribution center operations

## 3. List of Attributes for Each Entity

### Distribution Center
1. **DC Name**: Name identifier of the distribution center
2. **Region**: Geographic or operational region of the distribution center
3. **Status**: Active/inactive status of the distribution center

### Organization
1. **Hierarchy Level**: Level within organizational structure (network, region, DC)
2. **Organization Name**: Name of the organizational unit

### Date
1. **Date**: Calendar date
2. **Week**: Week period for weekly reporting
3. **Month**: Month period for monthly reporting
4. **Pay Period**: Payroll period for labor reporting

### Shift
1. **Shift Name**: Identifier for the shift period
2. **Start Time**: Shift start time
3. **End Time**: Shift end time

### Partner
1. **Partner Name**: Name of the partner organization or team
2. **Partner Type**: Classification of partner

### Partner Type
1. **Type Name**: Name of the partner type classification
2. **Type Description**: Description of the partner type

### Item
1. **Item Identifier**: Unique identifier for the item/SKU
2. **Category**: Product category classification
3. **Status**: Active/discontinued status of the item
4. **Safety Stock**: Safety stock parameters
5. **Reorder Parameters**: Replenishment parameters

### Activity
1. **Activity Name**: Name of the operational activity
2. **Activity Type**: Type classification of the activity
3. **Sub-activity**: Optional sub-activity classification

### Equipment
1. **Equipment Identifier**: Unique identifier for equipment
2. **Equipment Type**: Type classification of equipment
3. **Status**: Operational status of equipment

### Employee
1. **Employee Identifier**: Unique identifier for employee
2. **Labor Role**: Job role of the employee

### Exception Event
1. **Exception Event ID**: Unique identifier for exception events
2. **Exception Type**: Type of exception (Inventory, Equipment, System, Process, Safety, Quality)
3. **Severity**: Severity level (Low, Medium, High, Critical)
4. **Status**: Current status of the exception
5. **Opened Timestamp**: When the exception was opened
6. **Closed Timestamp**: When the exception was resolved

### Labor Role
1. **Role Name**: Name of the labor role
2. **Role Description**: Description of the labor role responsibilities

## 4. KPI List

1. **Overall DC Health Score**: Composite score (0-100) representing overall distribution center performance
2. **On-time Shipping Percentage**: Percentage of shipments completed on time
3. **Service Level Percentage**: Customer service level achievement percentage
4. **Throughput Units per Hour**: Operational throughput measured in units processed per hour
5. **Pick Accuracy Percentage**: Accuracy rate of picking operations
6. **Inventory Availability Percentage**: Percentage of items available in inventory
7. **Stockout Percentage**: Percentage of items experiencing stockouts
8. **Staffing Variance Percentage**: Variance between planned and actual staffing levels
9. **Kronos Adherence Percentage**: Adherence to scheduled work hours
10. **Exceptions per 1,000 Units**: Rate of exceptions per thousand units processed
11. **Cycle Time**: Time required to complete operational activities
12. **Backlog Units**: Number of units in operational backlog
13. **On-time Start Percentage**: Percentage of activities starting on time
14. **On-time Completion Percentage**: Percentage of activities completed on time
15. **Days of Supply**: Number of days of inventory supply available
16. **Pick Rate**: Picking productivity measured in units per hour
17. **Lines per Hour**: Picking productivity measured in lines per hour
18. **Error Rate per 1,000 Lines**: Error rate in picking operations
19. **First-time-right Percentage**: Percentage of operations completed correctly on first attempt
20. **Labor Hours Variance Percentage**: Variance between scheduled and worked hours
21. **Overtime Hours Percentage**: Percentage of hours worked as overtime
22. **Absence Rate Percentage**: Employee absence rate
23. **Mean Time to Resolve**: Average time to resolve exceptions
24. **Repeat Rate Percentage**: Percentage of recurring exceptions

## 5. Conceptual Data Model Diagram

| Source Entity | Relationship Key Field | Target Entity | Relationship Type |
|---------------|------------------------|---------------|-------------------|
| Organization | organization_hierarchy | Distribution Center | One-to-Many |
| Distribution Center | dc_identifier | Shift | One-to-Many |
| Partner Type | partner_type_id | Partner | One-to-Many |
| Distribution Center | dc_partner_assignment | Partner | Many-to-Many |
| Item | item_activity_relationship | Activity | Many-to-Many |
| Equipment | equipment_activity_relationship | Activity | Many-to-Many |
| Employee | employee_partner_assignment | Partner | Many-to-One |
| Employee | employee_dc_assignment | Distribution Center | Many-to-One |
| Date | date_key | Fact_DC_Operations | One-to-Many |
| Date | date_key | Fact_Inventory | One-to-Many |
| Date | date_key | Fact_Headcount | One-to-Many |
| Date | date_key | Fact_Picks | One-to-Many |
| Date | date_key | Fact_Kronos | One-to-Many |
| Date | date_key | Fact_Exceptions | One-to-Many |
| Shift | shift_key | Fact_DC_Operations | One-to-Many |
| Exception Event | exception_event_id | Fact_Exceptions | One-to-Many |

## 6. Common Data Elements in Report Requirements

1. **DC Name**: Referenced across all reports for distribution center identification
2. **Date**: Common temporal dimension across all reporting requirements
3. **Shift**: Used in DC Health Scorecard, Shift Operations Performance, Picks Productivity, and Labor reports
4. **Partner and Partner Type**: Referenced in multiple reports for partner performance analysis
5. **Activity**: Common operational dimension in Shift Operations Performance and Exception reports
6. **Equipment**: Referenced in Shift Operations Performance and Exception reports
7. **Throughput Units**: Common measure across DC Health Scorecard and Shift Operations Performance
8. **Region**: Organizational dimension used for drill-down and aggregation across reports
9. **Labor Hours**: Common element in productivity and labor management reports
10. **Exception Count**: Referenced in DC Health Scorecard and Exception reports
11. **Item**: Common dimension in Inventory Health and Picks Productivity reports
12. **Health Score Components**: Domain scores used in overall health score calculation
13. **Timestamps**: Start/end times used across operational and exception tracking reports