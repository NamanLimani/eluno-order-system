import streamlit as st
import pandas as pd

def render_order_table(orders):
    df = pd.DataFrame(orders)
    
    # Render Sidebar Filters
    st.sidebar.header("Filter Orders")
    status_filter = st.sidebar.multiselect("Status", df["status"].unique())
    lens_filter = st.sidebar.multiselect("Lens Type", df["lens_type"].unique())
    store_filter = st.sidebar.multiselect("Store Location", df["store_location"].unique())

    # Apply Filters
    filtered_df = df.copy()
    if status_filter:
        filtered_df = filtered_df[filtered_df["status"].isin(status_filter)]
    if lens_filter:
        filtered_df = filtered_df[filtered_df["lens_type"].isin(lens_filter)]
    if store_filter:
        filtered_df = filtered_df[filtered_df["store_location"].isin(store_filter)]

    # Render Main Table
    st.subheader(f"Active Orders ({len(filtered_df)})")
    display_df = filtered_df.drop(columns=["lens_details"], errors='ignore')
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    return filtered_df  # Return the filtered dataframe so the update form can use it