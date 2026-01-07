import os, requests, pandas as pd

PHOTO_FOLDER = "/home/dhruv/HotWheels_Photos"
WEBHOOK = "https://script.google.com/macros/s/AKfycbxvWfKH4ukWMpIwnWC-OVw0Oya-AQMZmT12bu_SCsMr08BU69l5hPPl1HG82yBaXLGl/exec"

df = pd.read_csv("hotwheels_inventory.csv")
df = df[df["item_id"].notna()]

payload = []

for photo in os.listdir(PHOTO_FOLDER):
    if photo.endswith(".jpg"):
        item_id = photo.replace(".jpg","")
        payload.append({
            "item_id": item_id,
            "photo_url": f"https://drive.google.com/uc?export=view&id={photo}"
        })

requests.post(WEBHOOK, json=payload)
print("📸 Photos pushed into Google Sheet UI")
