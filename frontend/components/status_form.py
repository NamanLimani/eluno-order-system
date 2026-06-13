import streamlit as st
from api_client import update_order

def render_update_form(filtered_df):
    st.subheader("Update Order Status")
    col1, col2 = st.columns(2)
    
    with col1:
        # Populate dropdown only with IDs currently visible in the table
        order_id_to_update = st.selectbox("Select Order ID", filtered_df["id"].tolist())
        new_status = st.selectbox("New Status", ["Processing", "QC Passed", "QC Failed", "Shipped", "Delivered"])
    
    with col2:
        delay_reason = st.text_input("Delay Reason / Log Note (Optional)")
        
        if st.button("Update Order"):
            success = update_order(order_id_to_update, new_status, delay_reason)
            if success:
                st.success(f"Order #{order_id_to_update} updated successfully!")
                st.rerun()
            else:
                st.error("Failed to update order. Check backend connection.")