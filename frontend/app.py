import streamlit as st
from api_client import fetch_active_orders
from components.order_table import render_order_table
from components.status_form import render_update_form

st.set_page_config(page_title="Eluno Operations", layout="wide")
st.title("👓 Eluno Eyewear Fulfillment Dashboard")

# 1. Fetch the data
orders = fetch_active_orders()

if not orders:
    st.info("No active orders found in the system. Create an order via the API Docs to see it here!")
else:
    # 2. Render the Table (and get back the filtered dataframe)
    filtered_df = render_order_table(orders)
    
    st.divider()
    
    # 3. Render the Update Form
    if not filtered_df.empty:
        render_update_form(filtered_df)