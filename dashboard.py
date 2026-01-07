import pandas as pd
import streamlit as st
import requests
from ai_engine import ask_ai
from pricing_engine import suggest_price

df = pd.read_csv("hotwheels_inventory.csv")
df = df[df["item_id"].notna()]
COLOR_PALETTE = ["black","white","silver","grey","red","blue","green","yellow","orange","purple","pink","brown","gold","teal","turquoise","bronze","maroon","navy","lime","cream","beige"]

st.set_page_config(page_title="Hot Wheels AI", layout="wide")
st.title("🔥 Hot Wheels Trading Command Center")

# ========== AI CHAT ==========
st.sidebar.title("🤖 Ask Your Business AI")
user_q = st.sidebar.text_input("Type your business question")

if user_q:
    st.sidebar.success(ask_ai(user_q))

# ========== FILTERS ==========
col1, col2, col3 = st.columns(3)
case_filter = col1.selectbox("Filter by Case", ["All"] + sorted(df["case"].dropna().unique()))
color_filter = col2.selectbox("Filter by Color", ["All"] + COLOR_PALETTE)

status_filter = col3.selectbox("Status", ["All","sold","available"])

filtered = df.copy()
if case_filter != "All":
    filtered = filtered[filtered["case"] == case_filter]
if color_filter != "All":
    filtered = filtered[filtered["color"] == color_filter]
if status_filter != "All":
    filtered = filtered[filtered["status"] == status_filter]

# ========== KPIs ==========
k1, k2, k3 = st.columns(3)
k1.metric("Inventory", len(filtered))
k2.metric("Total Profit", int(filtered["profit"].sum()))
k3.metric("Avg Days Listed", int(filtered["days_listed"].mean()))

# ========== CHARTS ==========
st.subheader("📊 Profit by Color")
st.bar_chart(filtered.groupby("color")["profit"].sum())

st.subheader("📊 Profit by Case")
st.bar_chart(filtered.groupby("case")["profit"].sum())

# ========== AUTO PRICING ==========
st.subheader("💰 Auto Pricing")
car = st.selectbox("Select Car", sorted(df["car_name"].unique()), index=None, placeholder="Type to search...")
if st.button("Suggest Best Price"):
    st.success(f"Suggested Price: ₹{suggest_price(car)}")

# ========== SLOW MOVERS ==========
st.subheader("🐢 Slow Movers (Discount Targets)")
st.dataframe(df[df["days_listed"] > 30][["car_name","days_listed","listed_price"]])

# ========== INVENTORY TABLE ==========
st.subheader("📦 Live Inventory")
st.dataframe(filtered)

# ========== ADD NEW ITEM ==========
st.subheader("➕ Add New Inventory Item")

with st.form("add_form"):
    item_id = st.text_input("Item ID")
    product_code = st.text_input("Product Code")
    brand = st.text_input("Brand")
    car_name = st.text_input("Car Name")
    series = st.text_input("Series")

    case = st.selectbox("Case", sorted(df["case"].dropna().unique()))
    color = st.selectbox("Color", COLOR_PALETTE)


    year = st.number_input("Year", min_value=1990, max_value=2030)
    condition = st.selectbox("Condition", ["Mint","Good","Used"])
    buy_price = st.number_input("Buy Price")
    listed_price = st.number_input("Listed Price")
    platform = st.selectbox("Platform", ["Instagram","WhatsApp","Offline"])
    date_bought = st.date_input("Date Bought")
    date_listed = st.date_input("Date Listed")
    location = st.text_input("Location")
    notes = st.text_input("Notes")

    submit = st.form_submit_button("Add Item")

if submit:
    payload = {
        "item_id": item_id,
        "product_code": product_code,
        "brand": brand,
        "car_name": car_name,
        "series": series,
        "case": case,
        "color": color,
        "year": year,
        "condition": condition,
        "buy_price": buy_price,
        "listed_price": listed_price,
        "platform": platform,
        "date_bought": str(date_bought),
        "date_listed": str(date_listed),
        "location": location,
        "notes": notes
    }

    requests.post("https://script.google.com/macros/s/AKfycbzUTs2flfpBtXhheZx0KMBsVNEX6jwYW4Zz8KTMzy1C0Qfxo0cIN7SWQWCGcvGvP6st/exec", json=payload)
    st.success("Item added to Google Sheet!")
