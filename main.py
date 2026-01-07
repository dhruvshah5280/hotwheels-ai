import pandas as pd

df = pd.read_csv("hotwheels_inventory.csv")

# Keep only real inventory rows
df = df[df["item_id"].notna()]

print("\n===== HOT WHEELS BUSINESS SNAPSHOT =====")
print("Total REAL items:", len(df))
print("Sold items:", df[df["status"] == "sold"].shape[0])
print("Unsold items:", df[df["status"] != "sold"].shape[0])
print("Total profit:", df["profit"].sum())

print("\nTop 5 Profit Cars:")
print(df.sort_values("profit", ascending=False)[["car_name", "profit"]].head())

print("\nSlow Movers (30+ days):")
print(df[df["days_listed"] > 30][["car_name", "days_listed"]])
