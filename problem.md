# Problem Brief

## Business question

Build a retail sales and inventory analytics data pipeline that helps a Supply Chain / Replenishment Analyst understand store performance, identify products with low inventory coverage, and analyze sales trends.

The project should answer:

- Which stores and product categories are performing better or worse?
- Which products have low inventory coverage or are at risk of stockouts?
- How do sales change across stores, products, categories, and time?
- What does a simple next-day sales baseline suggest?

## Who would use this?

The primary user is a Supply Chain / Replenishment Analyst.

The analyst reviews sales and inventory data to understand product demand, monitor stock availability, identify replenishment requirements, and support inventory planning decisions.

## Data I will use

The project will use synthetic retail sales and inventory data covering:

- 10 stores
- 50 products
- 365 days

The source data will contain daily aggregated sales and daily inventory snapshots.

Supporting entities include Stores, Products, and Calendar.

The synthetic data will simulate weekday and weekend patterns, seasonality, promotions, discounts, stockouts, inventory variation, and differences in demand across stores and products.

The data is synthetic and is NOT real Walmart data.

A separate testing dataset will contain controlled data quality issues. The clean source dataset will remain unchanged.

## What "done" looks like

1. The pipeline generates and processes data for 10 stores, 50 products, and 365 days.
2. The data is loaded into a PostgreSQL analytical warehouse with appropriate fact and dimension tables.
3. Re-running the pipeline does not create duplicate records.
4. Data quality checks identify invalid, missing, and duplicate records.
5. SQL queries correctly calculate the selected business KPIs.
6. An analytics dashboard presents store performance, sales trends, and inventory coverage.
7. The pipeline supports batch processing initially, with incremental loading added later.
8. Automated tests verify data quality, duplicate prevention, KPI reconciliation, missing data handling, and pipeline reruns.

## Out of scope

- Real-time streaming
- Kubernetes
- Cloud deployment in the first version
- Real retail or Walmart data
- Production-grade replenishment optimization
- Advanced forecasting models

## Known limitations

- Synthetic data cannot prove real-world accuracy.
- Simulated demand patterns may not represent actual retail behaviour.
- Inventory snapshots do not provide a complete inventory movement history.
- Sales observed during stockouts may underestimate actual customer demand.
- The initial sales baseline is not a production forecasting system.