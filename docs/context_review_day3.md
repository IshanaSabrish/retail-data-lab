# Retail Data & AI Lab: review of the five business questions

I used only your four files and executed no queries, so there are no figures below. "Schema" means `schema.sql`. Where the files disagree, I say so rather than pick a side.

## 1. Question-by-question review

| # | Question | Tables and columns required | Metric definition | Grain and grouping | Expected answer format | Ambiguities and missing fields |
|---|---|---|---|---|---|---|
| 1 | Total net sales by store | `fact_sales`: `store_key`, `net_sales`<br>`dim_store`: `store_key`, `store_id` | Sum of `net_sales`. The data model defines it as gross sales − discount − returns, and the schema CHECK enforces this per row. | Source grain: one row per date, store and product. Group by store (`store_key`, `store_id`). | `store_id`, `total_net_sales`. One row per store, 10 expected from the stated data scope. | • No date range is given, so I'd assume all 365 days; please confirm.<br>• Returns are booked on their processing date, so a store total can include returns of earlier purchases.<br>• Stores with no sales rows would vanish from an inner join. Whether to show them with 0 isn't specified.<br>• Sort order and currency aren't specified. |
| 2 | Top five products by net sales | `fact_sales`: `product_key`, `net_sales`<br>`dim_product`: `product_key`, `product_id`, `product_name` | Sum of `net_sales` per product across all stores and dates, then rank descending. | Group by product (`product_key`, `product_id`, `product_name`). Aggregate first, then rank. | `product_id`, `product_name`, `total_net_sales`, `rank`. Five rows, unless ties apply. | • No date range is given, as in Q1.<br>• Tie handling at rank 5 is undefined: `RANK`, `DENSE_RANK` and `ROW_NUMBER` give different row counts or arbitrary cut-offs.<br>• "Rank" is requested, but the ranking function isn't specified.<br>• The data model leaves open whether net sales should be net of returns for products that are mostly returned. The net sales formula already answers this, but confirm it's intended. |
| 3 | Daily sales trend | `fact_sales`: `date_key`, `net_sales`<br>`dim_date`: `date_key`, `full_date` | Sum of `net_sales` per calendar day, across all stores and products. | Group by date (`date_key`, `full_date`). Order ascending by date. | `full_date`, `daily_net_sales`. Up to 365 rows. | • "Trend" is ambiguous: a plain daily series, or a moving average, growth rate or weekday split? The expected-answer column only asks for the daily series.<br>• Company-wide versus per store isn't stated. I'd assume company-wide.<br>• The data model leaves inactive or unstocked combinations undefined, so days with no `fact_sales` rows may be missing. Whether to show them as 0 isn't specified (this needs a `dim_date` left join).<br>• Return-only days can be negative, per the data model. |
| 4 | Products with low closing inventory | `fact_inventory`: `date_key`, `store_key`, `product_key`, `closing_stock`<br>`dim_store`: `store_key`, `store_id`<br>`dim_product`: `product_key`, `product_id` | `closing_stock` on the latest available date, filtered to a "low" threshold. | One row per store-product at the latest date. No aggregation is needed. | `store_id`, `product_id`, `latest_closing_stock`. | • **No threshold for "low" exists** in any file. I can't invent one (a fixed number, a percentile, or a days-of-supply cut-off).<br>• "Latest" is ambiguous: the global maximum date, or the most recent row per store-product? These differ if some combinations stop reporting.<br>• The data model's pending items leave open whether `closing_stock` is available stock or total physical stock.<br>• Missing inventory rows for a combination are not the same as zero stock.<br>• No reorder-point or minimum-stock column exists in the schema. |
| 5 | Stores with stockouts | `fact_inventory`: `store_key`, `closing_stock` (plus `date_key`, `product_key` only if you need the distinct-day grain)<br>`dim_store`: `store_key`, `store_id` | Count of `fact_inventory` rows with `closing_stock = 0`, per store. | Counted at store-product-day grain (the fact grain), grouped by store. | `store_id`, `stockout_store_product_days`. | • The data model lists the exact stockout definition and denominator as pending. The question's wording implies `closing_stock = 0`, but I'd confirm it.<br>• Whether to count only active store-product-days is unspecified. The schema has `bridge_store_product` for this, but no documented rule uses it.<br>• Absent rows aren't counted as stockouts, which could understate them.<br>• Stores with zero stockouts: show with 0, or omit? "Which stores experienced stockouts" suggests omit.<br>• No stockout rate is requested, so no denominator is needed here. |

## 2. Schema and documentation gaps that affect these questions

| Finding | Source | Impact |
|---|---|---|
| `bridge_store_product` exists in the schema but not in the data model or dictionary. | Schema vs docs | Its role (which store-product pairs are active) is undocumented, so I haven't relied on it. |
| `fact_sales.cogs` exists in the schema but not in the data model's column list. | Schema vs data model | None of the five questions need it. I haven't used it. |
| The dictionary's fact table section is "to be completed". | Dictionary §3 | Fact column definitions, units and nullability come only from the schema. |
| `dim_store.city`, `dim_store.region` and `dim_product.category` are NOT NULL in the dictionary but nullable in the schema. | Dictionary vs schema | None of the five questions use these columns, but the documents disagree. |
| `day_of_week` has no documented convention (CHECK 1–7 only). | Dictionary and schema | It matters only if Q3 is extended to weekday analysis. |
| Several design decisions are listed as pending (inactive combinations, stockout definition, stock semantics). | Data model §10 | They directly affect Q3, Q4 and Q5. |

## 3. Double-counting risks when joining sales, product and inventory

| Join pattern | Risk | Why | Safe approach |
|---|---|---|---|
| `fact_sales` → `dim_store` / `dim_product` / `dim_date` on their keys | Low | The business and surrogate keys are unique, so each join is many-to-one and doesn't multiply rows. | Join on the key columns only. |
| `fact_sales` ↔ `fact_inventory` on `store_key` only, `product_key` only, or `date_key` only | **High** | Both facts have many rows per store, product or date, so a partial join is many-to-many. Each sales row repeats once per matching inventory row, which inflates `SUM(net_sales)`. | Join on all three keys `(date_key, store_key, product_key)`, which are unique in both facts, or aggregate each fact separately first and then join the results. |
| Summing `closing_stock` across dates | Medium | It's a snapshot, so adding days together is meaningless. | Use one date (Q4) or count rows (Q5). Never `SUM` it over time. |
| Joining `bridge_store_product` to a fact on one key only | Medium | The bridge is unique per `(store_key, product_key)`. Joining on `store_key` or `product_key` alone repeats fact rows. | Join on both keys, with a date-range predicate if activity windows matter. |
| Joining the bridge's date columns to `dim_date` for filtering | Low | `active_from_date_key` and `active_to_date_key` each point to one date, so this is safe unless you join to a range of dates. | Compare keys with `BETWEEN` rather than joining. |
| Counting stockouts after joining to sales | Low to medium | `COUNT(*)` after a join can include extra rows if the join multiplies. | Count from `fact_inventory` alone, then join to `dim_store` for `store_id`. |

**Rule of thumb:** `uq_sales_daily` and `uq_inventory_daily` make each fact table safe at its own grain. The risk appears only when joins skip one of the three key columns or combine the two facts at different grains.

## 4. Next step

Resolve these before writing the queries:

1. The date range for Q1–Q2.
2. The "low stock" threshold and the meaning of "latest" for Q4.
3. Whether to show zero-sales days (Q3) and zero-stockout stores (Q5).
4. The tie rule for Q2.

I can then draft the five PostgreSQL queries. They'd stay unexecuted until you load data or give me access to run them.