import streamlit as st
from api_client import fetch_active_orders
from components.order_table import render_order_table
from components.status_form import render_update_form

st.set_page_config(page_title="Eluno Operations", layout="wide")
st.title("👓 Eluno Eyewear Fulfillment Dashboard")

# --- THE PATIENCE MESSAGE ---
st.warning(
    "**Recruiter / Reviewer Note:** This architecture is hosted on a free cloud tier. "
    "If the servers have been inactive, fetching or updating the first order may take **45-60 seconds** "
    "while the backend performs a cold boot. Thank you for your patience!",
    icon="⏳"
)

# 1. Fetch the data (Wrapped in a spinner so the UI doesn't look frozen)
with st.spinner("Fetching live orders and waking up AI backend..."):
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