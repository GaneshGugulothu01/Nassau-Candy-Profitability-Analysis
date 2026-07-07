import streamlit as st
import pandas as pd

# ---------------------------------
# PAGE SETTINGS
# ---------------------------------
st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    page_icon="🍫",
    layout="wide"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------
df = pd.read_csv("Cleaned_Nassau_Candy.csv")

# ---------------------------------
# SIDEBAR
# ---------------------------------
st.sidebar.title("Filters")

division = st.sidebar.multiselect(
    "Division",
    options=df["Division"].unique(),
    default=df["Division"].unique()
)

margin = st.sidebar.slider(
    "Minimum Gross Margin (%)",
    0,
    100,
    0
)

product = st.sidebar.text_input("Search Product")

# ---------------------------------
# FILTER DATA
# ---------------------------------
filtered = df[df["Division"].isin(division)]
filtered = filtered[filtered["Gross Margin %"] >= margin]

if product:
    filtered = filtered[
        filtered["Product Name"].str.contains(
            product,
            case=False
        )
    ]

# ---------------------------------
# TITLE
# ---------------------------------
st.title("🍫 Nassau Candy Product Profitability Dashboard")

st.markdown("---")

# ---------------------------------
# KPI CARDS
# ---------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${filtered['Sales'].sum():,.2f}"
)

col2.metric(
    "Gross Profit",
    f"${filtered['Gross Profit'].sum():,.2f}"
)

col3.metric(
    "Average Margin",
    f"{filtered['Gross Margin %'].mean():.2f}%"
)

col4.metric(
    "Products",
    filtered["Product Name"].nunique()
)

st.markdown("---")

# ---------------------------------
# SALES BY DIVISION
# ---------------------------------
st.subheader("Sales by Division")

sales = filtered.groupby("Division")["Sales"].sum()

st.bar_chart(sales)

# ---------------------------------
# PROFIT BY DIVISION
# ---------------------------------
st.subheader("Profit by Division")

profit = filtered.groupby("Division")["Gross Profit"].sum()

st.bar_chart(profit)

# ---------------------------------
# TOP PRODUCTS
# ---------------------------------
st.subheader("Top 10 Profitable Products")

top = filtered.groupby("Product Name")["Gross Profit"].sum()

top = top.sort_values(ascending=False).head(10)

st.bar_chart(top)

# ---------------------------------
# PRODUCT TABLE
# ---------------------------------
st.subheader("Product Profitability")

table = filtered.groupby("Product Name").agg({
    "Sales":"sum",
    "Gross Profit":"sum",
    "Gross Margin %":"mean",
    "Units":"sum"
}).sort_values(
    by="Gross Profit",
    ascending=False
)

st.dataframe(table)

# ---------------------------------
# DOWNLOAD
# ---------------------------------
csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Dataset",
    csv,
    "Filtered_Data.csv",
    "text/csv"
)