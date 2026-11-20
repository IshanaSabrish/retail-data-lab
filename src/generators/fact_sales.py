
import pandas as pd
import numpy as np


def generate_fact_sales(seed=42):

    rng = np.random.default_rng(seed)

    # Load dimension and bridge datasets
    dates = pd.read_csv("data/raw/dim_date.csv")
    stores = pd.read_csv("data/raw/dim_store.csv")
    products = pd.read_csv("data/raw/dim_product.csv")
    bridge = pd.read_csv("data/raw/bridge_store_product.csv")

    # Convert dates
    dates["full_date"] = pd.to_datetime(dates["full_date"])

    records = []

    # Different demand levels for products
    product_demand = {
        "Electronics": 2.0,
        "Grocery": 8.0,
        "Clothing": 3.0,
        "Home & Kitchen": 2.5,
        "Personal Care": 5.0
    }

    # Store-level demand differences
    store_multiplier = {
        store_id: rng.uniform(0.75, 1.30)
        for store_id in stores["store_id"]
    }

    # Generate sales for every active combination and date
    for _, mapping in bridge.iterrows():

        store_id = mapping["store_id"]
        product_id = mapping["product_id"]

        product = products[
            products["product_id"] == product_id
        ].iloc[0]

        category = product["category"]
        unit_cost = float(product["unit_cost"])
        regular_price = float(product["regular_price"])

        base_demand = product_demand[category]
        store_factor = store_multiplier[store_id]

        for _, date in dates.iterrows():

            date_key = int(date["date_key"])
            month = int(date["month"])
            is_weekend = bool(date["is_weekend"])

            # Weekend demand variation
            weekday_factor = 1.25 if is_weekend else 1.0

            # Monthly seasonal variation
            seasonal_factor = 1.0 + 0.20 * np.sin(
                2 * np.pi * (month - 1) / 12
            )

            # Random daily demand variation
            random_factor = rng.uniform(0.75, 1.25)

            expected_demand = (
                base_demand
                * store_factor
                * weekday_factor
                * seasonal_factor
                * random_factor
            )

            units_sold = int(
                rng.poisson(max(expected_demand, 0))
            )

            # Promotions: 15% chance of a discount
            discount_rate = 0.0

            if rng.random() < 0.15:
                discount_rate = rng.uniform(0.05, 0.20)

            gross_sales = round(
                units_sold * regular_price, 2
            )

            discount_amount = round(
                gross_sales * discount_rate, 2
            )

            # Returns: approximately 3% of sold units
            units_returned = int(
                rng.binomial(units_sold, 0.03)
            )

            return_amount = round(
                units_returned * regular_price
                * (1 - discount_rate), 2
            )

            net_sales = round(
                gross_sales - discount_amount - return_amount,
                2
            )

            # COGS based on net units sold
            cogs = round(
                (units_sold - units_returned) * unit_cost,
                2
            )

            records.append({
                "date_key": date_key,
                "store_id": store_id,
                "product_id": product_id,
                "units_sold": units_sold,
                "units_returned": units_returned,
                "gross_sales": gross_sales,
                "discount_amount": discount_amount,
                "return_amount": return_amount,
                "net_sales": net_sales,
                "cogs": cogs
            })

    sales_df = pd.DataFrame(records)

    return sales_df


if __name__ == "__main__":

    sales_df = generate_fact_sales()

    sales_df.to_csv(
        "data/raw/fact_sales.csv",
        index=False
    )

    print("Sales fact generated successfully!")

    print(f"Total records: {len(sales_df)}")

    print("\nTotal net sales:")
    print(round(sales_df["net_sales"].sum(), 2))

    print("\nTotal units sold:")
    print(sales_df["units_sold"].sum())

    print("\nTotal units returned:")
    print(sales_df["units_returned"].sum())

    print("\nSample records:")
    print(sales_df.head())
