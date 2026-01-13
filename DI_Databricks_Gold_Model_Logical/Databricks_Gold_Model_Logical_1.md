_____________________________________________
## *Author*: Ascendion AVA+
## *Created on*: 
## *Description*: Gold Layer Logical Data Model for DC Health Meter Reports in Medallion Architecture
## *Version*: 1 
## *Updated on*: 
_____________________________________________

# Gold Layer Logical Data Model for DC Health Meter Reports

## 1. Gold Layer Logical Model

### 1.1 Fact Tables

#### 1.1.1 Go_Health_Score_Fact
**Description**: Central fact table capturing daily health scores and operational KPIs for distribution centers
**Table Type**: Fact
**SCD Type**: N/A

| Column Name | Description | Data Type | PII Classification |
|-------------|-------------|-----------|--------------------|
| dc_name | Distribution center business name identifier | VARCHAR(100) | Non-PII |
| calendar_date | Date of health score measurement | DATE | Non-PII |
| shift_name | Work shift identifier | VARCHAR(50) | Non-PII |
| partner_name | Partner organization name | VARCHAR(100) | Non-PII |
| overall_health_score | Composite health score (0-100) | DECIMAL(5