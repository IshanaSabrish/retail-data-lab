# Retail Data Lab — Data Dictionary

## 1. General Data Standards

| Standard | Decision |
|---|---|
| Database | PostgreSQL |
| Monetary data type | NUMERIC(12,2) |
| Required fields | NOT NULL |
| Optional descriptive fields | Nullable where appropriate |
| Inventory quantity | INTEGER |
| Inventory constraints | CHECK (closing_stock >= 0) |
| Primary keys | Surrogate keys |
| Foreign keys | References to dimension tables |

---

## 2. Dimension Tables

### 2.1 dim_date

| Column | Data Type | Nullable | Description |
|---|---|---|---|
| date_key | INTEGER | NO | Primary key in YYYYMMDD format |
| full_date | DATE | NO | Actual calendar date |
| day | SMALLINT | NO | Day of month |
| month | SMALLINT | NO | Month number (1–12) |
| quarter | SMALLINT | NO | Calendar quarter (1–4) |
| year | SMALLINT | NO | Calendar year |
| day_of_week | SMALLINT | NO | Day of week |
| is_weekend | BOOLEAN | NO | Indicates whether date falls on a weekend |

**Constraints:**
- PRIMARY KEY (date_key)
- UNIQUE (full_date)
- CHECK (month BETWEEN 1 AND 12)
- CHECK (quarter BETWEEN 1 AND 4)

### 2.2 dim_store

| Column | Data Type | Nullable | Description |
|---|---|---|---|
| store_key | INTEGER | NO | Surrogate primary key |
| store_id | VARCHAR(20) | NO | Business store identifier |
| store_name | VARCHAR(100) | NO | Store name |
| city | VARCHAR(100) | NO | Store city |
| region | VARCHAR(100) | NO | Store region |

**Constraints:**
- PRIMARY KEY (store_key)
- UNIQUE (store_id)

### 2.3 dim_product

| Column | Data Type | Nullable | Description |
|---|---|---|---|
| product_key | INTEGER | NO | Surrogate primary key |
| product_id | VARCHAR(20) | NO | Business product identifier |
| product_name | VARCHAR(150) | NO | Product name |
| category | VARCHAR(100) | NO | Product category |
| unit_cost | NUMERIC(12,2) | NO | Cost per product unit |
| regular_price | NUMERIC(12,2) | NO | Standard selling price |

**Constraints:**
- PRIMARY KEY (product_key)
- UNIQUE (product_id)
- CHECK (unit_cost >= 0)
- CHECK (regular_price >= 0)

---

## 3. Fact Tables

*To be completed in the next section.*

## 4. KPI Definitions

*To be completed after fact table definitions.*

## 5. Data Quality Rules

*To be completed after the schema is finalised.*