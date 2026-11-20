
import pandas as pd


def generate_dim_store():

    stores = [
        ("ST001", "Chennai Central", "Chennai", "South"),
        ("ST002", "Coimbatore Mall", "Coimbatore", "South"),
        ("ST003", "Bangalore City", "Bangalore", "South"),
        ("ST004", "Hyderabad Plaza", "Hyderabad", "South"),
        ("ST005", "Mumbai Central", "Mumbai", "West"),
        ("ST006", "Pune Market", "Pune", "West"),
        ("ST007", "Delhi Hub", "Delhi", "North"),
        ("ST008", "Jaipur Retail", "Jaipur", "North"),
        ("ST009", "Kolkata Square", "Kolkata", "East"),
        ("ST010", "Kochi Store", "Kochi", "South"),
    ]

    df = pd.DataFrame(
        stores,
        columns=["store_id", "store_name", "city", "region"]
    )

    return df


if __name__ == "__main__":
    store_df = generate_dim_store()

    store_df.to_csv("data/raw/dim_store.csv", index=False)

    print("Store dimension generated successfully!")
    print(f"Total stores: {len(store_df)}")
    print(store_df)
