# Retail Data Lab — Data Dictionary

## 1. General Data Standards

| Standard | Decision |
|---|---|
| Database | PostgreSQL |
| Monetary data type | NUMERIC(12,2) |
| Required fields | NOT NULL |
| Optional descriptive fields | Nullable where appropriate |
| Inventory quantity | INTEGER |
| Inventory constraint | CHECK (closing_stock >= 0) |
| Primary keys | Surrogate keys |
| Foreign keys | References to dimension tables |
| Date key format | YYYYMMDD |

---

## 2. Dimension Tables

### 2.1 dim_date

Stores calendar attributes for time-based analysis.

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

Stores descriptive information about retail stores.

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

Stores descriptive information about retail products.

| Column | Data Type | Nullable | Description |
|---|---|---|---|
| product_key | INTEGER | NO | Surrogate primary key |
| product_id | VARCHAR(20) | NO | Business product identifier |
| product_name | VARCHAR(150) | NO | Product name |
| category | VARCHAR(100) | NO | Product category |
| unit_cost | NUMERIC(12,2) | NO | Fixed cost per product unit |
| regular_price | NUMERIC(12,2) | NO | Standard selling price |

**Constraints:**
- PRIMARY KEY (product_key)
- UNIQUE (product_id)
- CHECK (unit_cost >= 0)
- CHECK (regular_price >= 0)

---

## 3. Fact Tables

### 3.1 fact_sales

**Grain:** One row per date, store, and product.

Stores daily aggregated sales, discounts, and returns.

| Column | Data Type | Nullable | Description |
|---|---|---|---|
| sales_key | BIGINT | NO | Surrogate primary key |
| date_key | INTEGER | NO | Foreign key to dim_date |
| store_key | INTEGER | NO | Foreign key to dim_store |
| product_key | INTEGER | NO | Foreign key to dim_product |
| units_sold | INTEGER | NO | Units sold before returns |
| units_returned | INTEGER | NO | Units returned on processing date |
| gross_sales | NUMERIC(12,2) | NO | Sales value before discounts and returns |
| discount_amount | NUMERIC(12,2) | NO | Total discount amount |
| return_amount | NUMERIC(12,2) | NO | Refund value for returns |
| net_sales | NUMERIC(12,2) | NO | Sales after discounts and returns |
| cogs | NUMERIC(12,2) | NO | Net cost of goods sold after accounting for returns |

**Constraints:**
- PRIMARY KEY (sales_key)
- FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
- FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
- FOREIGN KEY (product_key) REFERENCES dim_product(product_key)
- UNIQUE (date_key, store_key, product_key)
- CHECK (units_sold >= 0)
- CHECK (units_returned >= 0)
- CHECK (gross_sales >= 0)
- CHECK (discount_amount >= 0)
- CHECK (return_amount >= 0)

**Important:** Do NOT enforce `units_returned <= units_sold`. Returns can relate to purchases made on previous dates.

**Calculation rules:**

Net Units Sold = Units Sold − Units Returned

Net Sales = Gross Sales − Discount Amount − Return Amount

COGS = (Units Sold − Units Returned) × Unit Cost

**Business assumptions:**
- Returns are recorded on their processing date.
- Returned products are assumed to be accepted back into inventory in saleable condition.
- Unit cost remains fixed throughout the 365-day dataset.
- COGS can be negative on return-only days.
- Negative net sales and negative COGS are valid when returns exceed same-day sales.

### 3.2 fact_inventory

**Grain:** One row per date, store, and product.

Stores daily closing inventory snapshots.

| Column | Data Type | Nullable | Description |
|---|---|---|---|
| inventory_key | BIGINT | NO | Surrogate primary key |
| date_key | INTEGER | NO | Foreign key to dim_date |
| store_key | INTEGER | NO | Foreign key to dim_store |
| product_key | INTEGER | NO | Foreign key to dim_product |
| closing_stock | INTEGER | NO | Available inventory at the end of the day |

**Constraints:**
- PRIMARY KEY (inventory_key)
- FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
- FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
- FOREIGN KEY (product_key) REFERENCES dim_product(product_key)
- UNIQUE (date_key, store_key, product_key)
- CHECK (closing_stock >= 0)

**Interpretation:**
- Zero means no available inventory.
- Unknown inventory measurements must be handled during ingestion and validation rather than silently converted to zero.
- Inventory represents available stock, not necessarily total physical stock including reserved quantities.

---

## 4. KPI Definitions

### 4.1 Total Net Sales

Net Sales = Gross Sales − Discount Amount − Return Amount

Represents revenue after discounts and returns.

### 4.2 Total Units Sold

Net Units Sold = Units Sold − Units Returned

Represents net units sold after returns.

### 4.3 Average Selling Price (ASP)

ASP = Net Sales / Net Units Sold

**Edge cases:**
- If net units sold <= 0, return NULL.

### 4.4 Gross Profit

Gross Profit = Net Sales − COGS

COGS accounts for returned products.

### 4.5 Gross Margin Percentage

Gross Margin % = (Gross Profit / Net Sales) × 100

**Edge cases:**
- If net sales <= 0, return NULL.

### 4.6 Inventory on Hand (IOH)

Inventory on Hand = SUM(closing_stock)

Represents available inventory at the end of the reporting date.

### 4.7 Days of Supply (DOS)

Days of Supply = Current Closing Stock / Average Daily Net Demand over the Trailing 7 Calendar Days

**Edge cases:**
- If average daily net demand <= 0, return NULL.
- If closing stock = 0 and demand is positive, return 0.

### 4.8 Stockout Rate

Stockout Rate = (Stockout Store-Product-Days / Applicable Store-Product-Days) × 100

A stockout occurs when closing_stock = 0.

Inactive and not-yet-ranged store-product combinations are excluded from the denominator.

### 4.9 Inventory Turnover

Inventory Turnover = Total COGS / Average Daily Inventory Value

Inventory Value = Closing Stock × Unit Cost

Average Daily Inventory Value = Average of daily inventory values throughout the reporting period.

**Edge cases:**
- If average daily inventory value = 0, return NULL.

---

## 5. Data Quality Rules

1. Primary keys must be unique and non-null.
2. Foreign keys must reference existing dimension records.
3. Each fact table must contain at most one record per date-store-product combination.
4. Sales, discount, and return amounts must be non-negative.
5. Units sold and units returned must be non-negative.
6. COGS may be negative because returns can exceed same-day sales.
7. Net sales may be negative because returns can exceed same-day sales.
8. Closing stock must be non-negative.
9. Net sales must reconcile with gross sales, discounts, and returns.
10. Net units sold must reconcile with units sold and returned.
11. Missing measurements must not be silently replaced with zero.
12. KPI calculations must handle zero and negative denominators appropriately.
13. Returned products must be accounted for consistently in COGS and inventory calculations.

---

## 6. Pending Design Decisions

The following details must be finalised before implementation:

- Handling of inactive or unstocked store-product combinations.
- Exact definition of applicable store-product-days.
- How daily inventory is updated when returns are processed.
- Treatment of negative net demand in Days of Supply.
- How inventory snapshots are valued when product costs are fixed.
- How promotions and discounts affect gross sales and net sales.

---

**Status:** Initial data dictionary completed. Ready for final schema review and PostgreSQL implementation.