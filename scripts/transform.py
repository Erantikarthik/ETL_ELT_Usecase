import pandas as pd

df = pd.read_csv("data/raw/orders.csv")

df["total_amount"] = df["quantity"] * df["amount"]

df.to_csv("data/processed/orders_transformed.csv", index=False)

print("Transformation successful!")
print(f"Records transformed: {len(df)}")