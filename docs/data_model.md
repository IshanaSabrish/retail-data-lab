# Retail Data Lab — Data Model

## 1. Overview

This project uses a relational star schema to support retail sales and inventory analytics.

The warehouse contains:
- Two fact tables: `fact_sales` and `fact_inventory`.
- Three shared dimension tables: `dim_date`, `dim_store`, and `dim_product`.

The design supports reporting at store, product, category, daily, weekly, and monthly levels.

## 2. Business Requirements

The data model must support analysis of:

1. Sales performance across stores.
2. Product and store-level inventory availability.
3. Sales trends over time.
4. Product returns and their impact on net sales.
5. Inventory-related KPIs such as days of supply, stockout rate, and inventory turnover.

## 3. Fact Table Grain

### fact_sales

**Grain:** One row per date, store, and product.

Each row represents the daily aggregated sales and return activity for one product at one store.

### fact_inventory

**Grain:** One row per date, store, and product.

Each row represents the closing inventory quantity for one product at one store on a particular date.

## 4. Dimension Tables

### dim_date

Stores calendar attributes for time-based analysis.

Proposed columns:
- `date_key` — Primary key.
- `full_date` — Actual calendar date.
- `day`
- `month`
- `quarter`
- `year`
- `day_of_week`
- `is_weekend`

### dim_store

Stores descriptive information about retail stores.

Proposed columns:
- `store_key` — Primary key.
- `store_id` — Business identifier.
- `store_name`
- `city`
- `region`

### dim_product

Stores descriptive information about retail products.

Proposed columns:
- `product_key` — Primary key.
- `product_id` — Business identifier.
- `product_name`
- `category`
- `unit_cost`
- `regular_price`

## 5. Fact Tables

### fact_sales

Stores daily aggregated sales and return measurements.

Proposed columns:
- `sales_key` — Primary key.
- `date_key` — Foreign key to `dim_date`.
- `store_key` — Foreign key to `dim_store`.
- `product_key` — Foreign key to `dim_product`.
- `units_sold`
- `units_returned`
- `gross_sales`
- `discount_amount`
- `return_amount`
- `net_sales`

**Calculation rules:**

Net units sold = Units sold − Units returned

Net sales = Gross sales − Discount amount − Return amount

Returns are recorded against their processing date rather than the original purchase date.

A return-only day may therefore have negative net sales.

### fact_inventory

Stores daily closing inventory snapshots.

Proposed columns:
- `inventory_key` — Primary key.
- `date_key` — Foreign key to `dim_date`.
- `store_key` — Foreign key to `dim_store`.
- `product_key` — Foreign key to `dim_product`.
- `closing_stock`

`closing_stock` represents the available inventory quantity at the end of the day.

## 6. Relationships

Both fact tables reference all three shared dimensions.

| Fact table | Dimension | Relationship |
|---|---|---|
| fact_sales | dim_date | Many-to-one |
| fact_sales | dim_store | Many-to-one |
| fact_sales | dim_product | Many-to-one |
| fact_inventory | dim_date | Many-to-one |
| fact_inventory | dim_store | Many-to-one |
| fact_inventory | dim_product | Many-to-one |

Dimension primary keys are referenced as foreign keys in the fact tables.

## 7. Key Strategy

The warehouse will use surrogate keys for dimension tables.

Examples:
- `store_key`
- `product_key`
- `date_key`

Business identifiers such as `store_id` and `product_id` will also be retained.

Each fact table will have a composite uniqueness constraint on:

`(date_key, store_key, product_key)`

This prevents duplicate records at the defined daily grain.

## 8. Data Scope

The synthetic dataset will contain:
- 10 stores.
- 50 products.
- 365 days of data.

A complete store-product-date grid would contain:

10 × 50 × 365 = **182,500 combinations**.

The treatment of inactive or unstocked combinations will be defined during data generation.

## 9. Warehouse Design Principles

1. Maintain a clearly defined grain for every fact table.
2. Separate measurable business events from descriptive attributes.
3. Reuse shared dimensions across fact tables.
4. Enforce primary key, foreign key, and uniqueness constraints.
5. Prevent duplicate daily records.
6. Keep sales, discounts, and returns separately identifiable.
7. Maintain consistent KPI calculation rules.
8. Validate transformed data against source values.

## 10. Pending Design Decisions

The following details must be finalised before implementation:

- Handling of inactive or unstocked store-product combinations.
- Treatment of zero and negative net units when calculating average selling price.
- Inventory valuation method for inventory turnover.
- Handling of zero demand when calculating days of supply.
- Exact stockout definition and applicable store-product-day denominator.
- Whether product costs and prices remain fixed or change over the reporting period.
- Whether daily inventory represents available stock or total physical stock, including reserved quantities.

---

**Status:** Initial data model approved. Pending detailed data dictionary and final KPI definitions.