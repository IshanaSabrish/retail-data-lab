
import pandas as pd
import numpy as np


def generate_fact_inventory(seed=42):

    rng = np.random.default_rng(seed)

    # Load generated datasets
    sales = pd.read_csv("data/raw/fact_sales.csv")
    products = pd.read_csv("data/raw/dim_product.csv")

    # Map product selling prices
    price_map = products.set_index("product_id")["regular_price"].to_dict()

    inventory_records = []
    adjusted_sales = []

    # Process each store-product combination independently
    for (store_id, product_id), group in sales.groupby(
        ["store_id", "product_id"],
        sort=True
    ):

        group = group.sort_values("date_key").copy()

        # Estimate initial stock from planned annual demand
        planned_units = int(group["units_sold"].sum())

        stock_factor = rng.uniform(0.85, 1.10)
        opening_stock = int(np.ceil(planned_units * stock_factor))

        regular_price = float(price_map[product_id])

        for row in group.itertuples(index=False):

            requested_units = int(row.units_sold)

            # Actual sales cannot exceed available stock
            observed_units = min(requested_units, opening_stock)

            # Preserve the original discount rate
            if row.gross_sales > 0:
                discount_rate = (
                    row.discount_amount / row.gross_sales
                )
            else:
                discount_rate = 0.0

            # Returns cannot exceed observed sales
            returned_units = min(
                int(row.units_returned),
                observed_units
            )

            gross_sales = round(
                observed_units * regular_price, 2
            )

            discount_amount = round(
                gross_sales * discount_rate, 2
            )

            return_amount = round(
                returned_units
                * regular_price
                * (1 - discount_rate),
                2
            )

            net_sales = round(
                gross_sales - discount_amount - return_amount,
                2
            )

            unit_cost = float(
                products.loc[
                    products["product_id"] == product_id,
                    "unit_cost"
                ].iloc[0]
            )

            cogs = round(
                (observed_units - returned_units) * unit_cost,
                2
            )

            # Calculate closing inventory
            closing_stock = (
                opening_stock
                - observed_units
                + returned_units
            )

            inventory_records.append({
                "date_key": int(row.date_key),
                "store_id": store_id,
                "product_id": product_id,
                "closing_stock": closing_stock
            })

            adjusted_sales.append({
                "date_key": int(row.date_key),
                "store_id": store_id,
                "product_id": product_id,
                "units_sold": observed_units,
                "units_returned": returned_units,
                "gross_sales": gross_sales,
                "discount_amount": round(discount_amount, 2),
                "return_amount": return_amount,
                "net_sales": net_sales,
                "cogs": cogs
            })

            # Today's closing stock becomes tomorrow's opening stock
            opening_stock = closing_stock

    inventory_df = pd.DataFrame(inventory_records)
    sales_df = pd.DataFrame(adjusted_sales)

    # Update sales with inventory-constrained observed sales
    sales_df.to_csv(
    "data/raw/fact_sales_adjusted.csv",
    index=False
)
    

    inventory_df.to_csv(
        "data/raw/fact_inventory.csv",
        index=False
    )

    return inventory_df, sales_df


if __name__ == "__main__":

    inventory_df, sales_df = generate_fact_inventory()

    print("Inventory fact generated successfully!")

    print(f"Inventory records: {len(inventory_df)}")
    print(f"Adjusted sales records: {len(sales_df)}")

    print(
        "Stockout records:",
        (inventory_df["closing_stock"] == 0).sum()
    )

    print("\nTotal closing inventory:")
    print(inventory_df["closing_stock"].sum())

    print("\nSample inventory records:")
    print(inventory_df.head())
