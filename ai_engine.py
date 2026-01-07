import pandas as pd

df = pd.read_csv("hotwheels_inventory.csv")
df = df[df["item_id"].notna()]

def ask_ai(q):
    q = q.lower()

    # Best profit cars
    if "best" in q or "most profit" in q:
        top = df.sort_values("profit", ascending=False).head(3)
        return "\n".join([f"{r.car_name} → ₹{r.profit}" for _, r in top.iterrows()])

    # Slow movers
    if "slow" in q or "not selling" in q:
        slow = df[df["days_listed"] > 30]
        return "\n".join([f"{r.car_name} → {int(r.days_listed)} days" for _, r in slow.iterrows()])

    # Discount suggestions
    if "discount" in q:
        slow = df[df["days_listed"] > 45]
        return "\n".join([f"Discount: {r.car_name}" for _, r in slow.iterrows()])

    # Buying targets
    if "buy" in q or "restock" in q:
        fast = df[(df["days_listed"] < 15) & (df["profit"] > 200)]
        return "\n".join([f"Buy more: {r.car_name}" for _, r in fast.iterrows()])

    # Color performance
    if "color" in q:
        colors = df.groupby("color")["profit"].sum().sort_values(ascending=False)
        return colors.to_string()

    # Case performance
    if "case" in q:
        cases = df.groupby("case")["profit"].sum().sort_values(ascending=False)
        return cases.to_string()

    # Price prediction
    if "predict" in q or "price" in q:
        sold = df[df["status"] == "sold"]
        avg = sold.groupby("car_name")["sold_price"].mean().sort_values(ascending=False)
        return avg.head(5).to_string()

    # Totals
    if "total profit" in q:
        return f"Total profit: ₹{df['profit'].sum()}"

    if "inventory" in q:
        return f"Total inventory: {len(df)}"

    return "Try: best cars, slow movers, discount, restock, color profit, case profit, predict prices"
