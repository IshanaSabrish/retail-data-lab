
import pandas as pd


def generate_dim_product():

    products = [
        # Electronics
        ("P001", "Wireless Mouse", "Electronics", 350, 599),
        ("P002", "Mechanical Keyboard", "Electronics", 1200, 1999),
        ("P003", "USB-C Charger", "Electronics", 450, 799),
        ("P004", "Bluetooth Speaker", "Electronics", 900, 1499),
        ("P005", "Wireless Earbuds", "Electronics", 1100, 1999),
        ("P006", "Power Bank", "Electronics", 800, 1399),
        ("P007", "Webcam", "Electronics", 950, 1599),
        ("P008", "Laptop Stand", "Electronics", 500, 899),
        ("P009", "USB Hub", "Electronics", 300, 549),
        ("P010", "Smart Watch", "Electronics", 1800, 2999),

        # Grocery
        ("P011", "Rice 5kg", "Grocery", 250, 349),
        ("P012", "Wheat Flour 5kg", "Grocery", 180, 249),
        ("P013", "Sunflower Oil 1L", "Grocery", 100, 145),
        ("P014", "Sugar 1kg", "Grocery", 38, 49),
        ("P015", "Toor Dal 1kg", "Grocery", 110, 149),
        ("P016", "Coffee 200g", "Grocery", 140, 199),
        ("P017", "Tea 250g", "Grocery", 90, 129),
        ("P018", "Biscuits Pack", "Grocery", 25, 39),
        ("P019", "Breakfast Cereal", "Grocery", 120, 179),
        ("P020", "Pasta 500g", "Grocery", 45, 69),

        # Clothing
        ("P021", "Cotton T-Shirt", "Clothing", 220, 399),
        ("P022", "Denim Jeans", "Clothing", 650, 1199),
        ("P023", "Casual Shirt", "Clothing", 450, 799),
        ("P024", "Sports Track Pants", "Clothing", 400, 699),
        ("P025", "Summer Dress", "Clothing", 550, 999),
        ("P026", "Hoodie", "Clothing", 700, 1299),
        ("P027", "Formal Trousers", "Clothing", 600, 1099),
        ("P028", "Cotton Socks Pack", "Clothing", 70, 129),
        ("P029", "Casual Shorts", "Clothing", 250, 449),
        ("P030", "Winter Jacket", "Clothing", 1100, 1999),

        # Home & Kitchen
        ("P031", "Water Bottle", "Home & Kitchen", 120, 199),
        ("P032", "Nonstick Pan", "Home & Kitchen", 450, 799),
        ("P033", "Dinner Plate Set", "Home & Kitchen", 500, 899),
        ("P034", "Storage Container Set", "Home & Kitchen", 300, 549),
        ("P035", "Electric Kettle", "Home & Kitchen", 650, 1099),
        ("P036", "Table Lamp", "Home & Kitchen", 400, 699),
        ("P037", "Bedsheet Set", "Home & Kitchen", 550, 999),
        ("P038", "Pillow Pair", "Home & Kitchen", 350, 599),
        ("P039", "Floor Mat", "Home & Kitchen", 180, 299),
        ("P040", "Lunch Box", "Home & Kitchen", 200, 349),

        # Personal Care
        ("P041", "Shampoo 400ml", "Personal Care", 140, 199),
        ("P042", "Body Lotion 200ml", "Personal Care", 110, 169),
        ("P043", "Face Wash 100ml", "Personal Care", 85, 129),
        ("P044", "Toothpaste Pack", "Personal Care", 65, 99),
        ("P045", "Toothbrush Pack", "Personal Care", 40, 69),
        ("P046", "Hand Wash 250ml", "Personal Care", 55, 89),
        ("P047", "Sunscreen 100ml", "Personal Care", 180, 299),
        ("P048", "Hair Oil 200ml", "Personal Care", 90, 139),
        ("P049", "Deodorant 150ml", "Personal Care", 120, 199),
        ("P050", "Face Moisturizer", "Personal Care", 160, 249),
    ]

    df = pd.DataFrame(
        products,
        columns=[
            "product_id",
            "product_name",
            "category",
            "unit_cost",
            "regular_price"
        ]
    )

    return df


if __name__ == "__main__":
    product_df = generate_dim_product()

    product_df.to_csv(
        "data/raw/dim_product.csv",
        index=False
    )

    print("Product dimension generated successfully!")
    print(f"Total products: {len(product_df)}")
    print("\nProducts per category:")
    print(product_df.groupby("category").size())
    print("\nSample records:")
    print(product_df.head())
