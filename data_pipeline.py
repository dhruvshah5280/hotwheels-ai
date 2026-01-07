import pandas as pd
import time

LIVE_CSV = "https://docs.google.com/spreadsheets/d/17f-yGthAsX2hkoP4MRwF7fPEx2qD75Na9xADTAX2v38/export?format=csv"

def refresh():
    df = pd.read_csv(LIVE_CSV)
    df = df[df["item_id"].notna()]
    df.to_csv("hotwheels_inventory.csv", index=False)
    print("🔄 Inventory refreshed from Google Sheets")

while True:
    refresh()
    time.sleep(300)   # refresh every 5 minutes
