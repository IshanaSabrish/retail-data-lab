
import pandas as pd


def generate_dim_date(start_date="2025-01-01", days=365):
    """
    Generate a date dimension for the retail analytics warehouse.
    One row represents one calendar date.
    """

    dates = pd.date_range(
        start=start_date,
        periods=days,
        freq="D"
    )

    df = pd.DataFrame({
        "full_date": dates
    })

    df["date_key"] = df["full_date"].dt.strftime("%Y%m%d").astype(int)
    df["day"] = df["full_date"].dt.day
    df["month"] = df["full_date"].dt.month
    df["quarter"] = df["full_date"].dt.quarter
    df["year"] = df["full_date"].dt.year
    df["day_of_week"] = df["full_date"].dt.day_of_week + 1
    df["is_weekend"] = df["full_date"].dt.day_of_week >= 5

    return df


if __name__ == "__main__":
    date_df = generate_dim_date()

    date_df.to_csv(
        "data/raw/dim_date.csv",
        index=False
    )

    print("Date dimension generated successfully!")
    print(f"Total records: {len(date_df)}")
    print(date_df.head())
    print(date_df.tail())
