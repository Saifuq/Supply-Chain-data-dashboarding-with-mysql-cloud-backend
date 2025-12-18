import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_utils import get_all_data

# Page Config
st.set_page_config(
    page_title="Supply Chain Dashboard",
    page_icon="📦",
    layout="wide"
)

# Title
st.title("Supply Chain 360: Revenue Growth & Operational Efficiency")

# Load Data
@st.cache_data
def load_data():
    df = get_all_data()
    # Rename SKU to Product Type for clarity if needed, or just use SKU
    if 'SKU' in df.columns:
        df['Product Type'] = df['SKU']
    return df

df = load_data()

if df.empty:
    st.warning("No data found. Please check database connection.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filters")
product_types = st.sidebar.multiselect(
    "Product Type",
    options=df['Product Type'].unique(),
    default=df['Product Type'].unique()
)

# Filter Data
df_filtered = df[df['Product Type'].isin(product_types)]

# KPIs
col1, col2, col3 = st.columns(3)
total_revenue = df_filtered['Revenue_generated'].sum()
avg_lead_time = df_filtered['Lead_times'].mean()
total_orders = df_filtered['Number_of_products_sold'].sum()

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Avg Lead Time", f"{avg_lead_time:.1f} days")
col3.metric("Total Products Sold", f"{total_orders:,}")

st.markdown("---")

# Row 1: Revenue by Transportation & Lead Time by Transportation
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Revenue by Transportation Modes")
    rev_by_transport = df_filtered.groupby('Transportation_modes')['Revenue_generated'].sum().reset_index()
    fig_transport_rev = px.bar(
        rev_by_transport,
        x='Revenue_generated',
        y='Transportation_modes',
        orientation='h',
        text_auto='.2s',
        color_discrete_sequence=['#0099ff']
    )
    fig_transport_rev.update_layout(xaxis_title="Revenue Generated", yaxis_title="Transportation Modes")
    st.plotly_chart(fig_transport_rev, use_container_width=True)

with row1_col2:
    st.subheader("Lead Times by Transportation Modes")
    lead_by_transport = df_filtered.groupby('Transportation_modes')['Lead_times'].sum().reset_index()
    fig_transport_lead = px.bar(
        lead_by_transport,
        x='Transportation_modes',
        y='Lead_times',
        text_auto=True,
        color_discrete_sequence=['#0099ff']
    )
    fig_transport_lead.update_layout(xaxis_title="Transportation Modes", yaxis_title="Sum of Lead Times")
    st.plotly_chart(fig_transport_lead, use_container_width=True)

# Row 2: Revenue by Product Type & Demographics
row2_col1, row2_col2 = st.columns([1, 2])

with row2_col1:
    st.subheader("Revenue by Product Type")
    rev_by_product = df_filtered.groupby('Product Type')['Revenue_generated'].sum().reset_index()
    fig_product_rev = px.pie(
        rev_by_product,
        values='Revenue_generated',
        names='Product Type',
        hole=0.4
    )
    st.plotly_chart(fig_product_rev, use_container_width=True)

with row2_col2:
    st.subheader("Revenue by Product & Demographics")
    # Treemap
    fig_treemap = px.treemap(
        df_filtered,
        path=['Product Type', 'Customer_demographics'],
        values='Revenue_generated',
        color='Product Type'
    )
    st.plotly_chart(fig_treemap, use_container_width=True)

# Row 3: Map & Advanced Analysis
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.subheader("Location Analysis")
    # Assuming 'Location' column has city names. We need coordinates for a map.
    # For now, we'll just show a scatter plot or table if lat/lon is missing.
    # If 'Location' is just city names, we can't easily plot on a map without geocoding.
    # The user's screenshot showed a map.
    # I'll check if there are lat/lon columns or if I need to mock/geocode.
    # The schema didn't show lat/lon. It just showed 'Location'.
    # I'll display a table for now or a placeholder map if I can't geocode.
    # Actually, let's just show the data distribution by Location.
    loc_counts = df_filtered['Location'].value_counts().reset_index()
    loc_counts.columns = ['Location', 'Count']
    fig_map_bar = px.bar(loc_counts, x='Location', y='Count', title="Orders by Location")
    st.plotly_chart(fig_map_bar, use_container_width=True)
    st.info("Note: To display a geographic map, Latitude and Longitude columns are required.")

with row3_col2:
    st.subheader("Advanced Analysis: Correlations")
    # Select numeric columns for correlation
    numeric_df = df_filtered.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Matrix")
    st.plotly_chart(fig_corr, use_container_width=True)

# Download Data
st.markdown("---")
st.subheader("Raw Data")
st.dataframe(df_filtered)

csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    "Download Raw Data as CSV",
    csv,
    "supply_chain_data.csv",
    "text/csv",
    key='download-csv'
)
