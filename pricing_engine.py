import pandas as pd

df = pd.read_csv("hotwheels_inventory.csv")
df = df[df["item_id"].notna()]

def suggest_price(car_name):
    sold = df[df["status"] == "sold"]
    history = sold[sold["car_name"] == car_name]

    if len(history) < 2:
        return "Not enough history"

    avg = history["sold_price"].mean()
    return round(avg * 1.08, -1)   # 8% profit margin rounded
