
import pandas as pd


def generate_bridge_store_product():

    # Load store and product dimensions
    stores = pd.read_csv("data/raw/dim_store.csv")
    products = pd.read_csv("data/raw/dim_product.csv")

    store_ids = stores["store_id"].tolist()
    product_ids = products["product_id"].tolist()

    combinations = []

    # Each store gets 40 products.
    # Rotate the assortment to distribute all 50 products.
    products_per_store = 40

    for store_index, store_id in enumerate(store_ids):

        start = store_index * 5

        selected_products = [
            product_ids[
                (start + i) % len(product_ids)
            ]
            for i in range(products_per_store)
        ]

        for product_id in selected_products:
            combinations.append((store_id, product_id))

    # Create bridge dataframe
    bridge_df = pd.DataFrame(
        combinations,
        columns=["store_id", "product_id"]
    )

    # Assign active dates
    bridge_df["active_from_date_key"] = 20250101
    bridge_df["active_to_date_key"] = pd.NA

    return bridge_df


if __name__ == "__main__":

    bridge_df = generate_bridge_store_product()

    # Save generated dataset
    bridge_df.to_csv(
        "data/raw/bridge_store_product.csv",
        index=False
    )

    print("Store-product bridge generated successfully!")

    print(f"Total combinations: {len(bridge_df)}")
    print(f"Unique stores: {bridge_df['store_id'].nunique()}")
    print(f"Unique products: {bridge_df['product_id'].nunique()}")

    print("\nProducts per store:")
    print(
        bridge_df.groupby("store_id")["product_id"].count()
    )

    print("\nSample records:")
    print(bridge_df.head())
