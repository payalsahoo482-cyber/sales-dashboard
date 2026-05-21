import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales & Revenue Analysis Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

if uploaded_file is not None:

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Raw Data")
    st.dataframe(df)

    # Sidebar filters
    st.sidebar.header("Filters")

    if "Product" in df.columns:
        product_filter = st.sidebar.multiselect(
            "Select Product",
            options=df["Product"].unique(),
            default=df["Product"].unique()
        )
        filtered_df = df[df["Product"].isin(product_filter)]
    else:
        filtered_df = df

    # KPIs
    st.subheader("Key Metrics")

    total_sales = filtered_df["Sales"].sum()
    total_revenue = filtered_df["Revenue"].sum()

    top_product = filtered_df.groupby("Product")["Revenue"].sum().idxmax()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", total_sales)
    col2.metric("Total Revenue", f"${total_revenue}")
    col3.metric("Top Product", top_product)

    # Top Products Chart
    st.subheader("Top Performing Products")

    top_products = filtered_df.groupby("Product")["Revenue"].sum().reset_index()

    fig = px.bar(
        top_products,
        x="Product",
        y="Revenue",
        title="Revenue by Product"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Please upload a CSV or Excel file to view the dashboard.")