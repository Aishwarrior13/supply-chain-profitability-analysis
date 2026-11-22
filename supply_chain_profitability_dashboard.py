
# ============================================================
# SUPPLY CHAIN PROFITABILITY PERFORMANCE DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np

# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Supply Chain Profitability Dashboard",
    page_icon="📦",
    layout="wide"
)

# ------------------------------------------------------------
# LOAD DATASET
# ------------------------------------------------------------

@st.cache_data
def load_data():
data = pd.read_csv("APL_Logistics_Cleaned-ZIP.zip", compression="zip")
return data

df = load_data()

# ------------------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------------------

st.sidebar.title("Dashboard Filters")

segments = ["All"] + sorted(df["Customer Segment"].dropna().unique().tolist())
selected_segment = st.sidebar.selectbox("Customer Segment", segments)

markets = ["All"] + sorted(df["Market"].dropna().unique().tolist())
selected_market = st.sidebar.selectbox("Market", markets)

regions = ["All"] + sorted(df["Order Region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Region", regions)

categories = ["All"] + sorted(df["Category Name"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Category", categories)

# Apply filters
filtered_df = df.copy()

if selected_segment != "All":
    filtered_df = filtered_df[
        filtered_df["Customer Segment"] == selected_segment
    ]

if selected_market != "All":
    filtered_df = filtered_df[
        filtered_df["Market"] == selected_market
    ]

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Order Region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category Name"] == selected_category
    ]

# ------------------------------------------------------------
# MAIN TITLE
# ------------------------------------------------------------

st.title("📦 Supply Chain Profitability Performance Analysis")
st.caption("Customer, Product and Financial Performance Dashboard")

st.write(
    "Analyze revenue, profitability, customer contribution, "
    "product performance and discount impact across supply chain operations."
)

st.divider()


# ------------------------------------------------------------
# MODULE 1: REVENUE AND PROFIT OVERVIEW
# ------------------------------------------------------------

st.header("1. Revenue & Profit Overview")

# Calculate financial KPIs
gross_revenue = filtered_df["Sales"].sum()
net_revenue = filtered_df["Order Item Total"].sum()
total_discount = filtered_df["Order Item Discount"].sum()
total_profit = filtered_df["Order Profit Per Order"].sum()

# Calculate margins using both revenue definitions
gross_revenue_margin = (
    total_profit / gross_revenue * 100
    if gross_revenue != 0 else 0
)

net_revenue_margin = (
    total_profit / net_revenue * 100
    if net_revenue != 0 else 0
)

# Transaction performance
total_transactions = len(filtered_df)

profitable_transactions = (
    filtered_df["Order Profit Per Order"] > 0
).sum()

loss_making_transactions = (
    filtered_df["Order Profit Per Order"] < 0
).sum()

zero_profit_transactions = (
    filtered_df["Order Profit Per Order"] == 0
).sum()

# Financial KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Gross Revenue", f"{gross_revenue:,.2f}")
col2.metric("Net Revenue", f"{net_revenue:,.2f}")
col3.metric("Total Profit", f"{total_profit:,.2f}")
col4.metric("Total Discounts", f"{total_discount:,.2f}")

col5, col6, col7, col8 = st.columns(4)

col5.metric("Margin on Gross Revenue", f"{gross_revenue_margin:.2f}%")
col6.metric("Margin on Net Revenue", f"{net_revenue_margin:.2f}%")
col7.metric("Total Transactions", f"{total_transactions:,}")
col8.metric("Loss-Making Transactions", f"{loss_making_transactions:,}")

# Transaction profitability summary
st.subheader("Transaction Profitability Summary")

col9, col10, col11 = st.columns(3)

col9.metric("Profitable Transactions", f"{profitable_transactions:,}")
col10.metric("Loss-Making Transactions", f"{loss_making_transactions:,}")
col11.metric("Zero-Profit Transactions", f"{zero_profit_transactions:,}")

# Market-level financial performance
st.subheader("Revenue and Profit by Market")

market_performance = (
    filtered_df.groupby("Market")
    .agg(
        Transactions=("Market", "size"),
        Net_Revenue=("Order Item Total", "sum"),
        Total_Profit=("Order Profit Per Order", "sum"),
        Total_Discount=("Order Item Discount", "sum")
    )
    .reset_index()
)

market_performance["Profit_Margin_%"] = np.where(
    market_performance["Net_Revenue"] != 0,
    market_performance["Total_Profit"] /
    market_performance["Net_Revenue"] * 100,
    0
)

market_performance = market_performance.sort_values(
    "Total_Profit", ascending=False
)

st.dataframe(
    market_performance.round(2),
    use_container_width=True,
    hide_index=True
)

st.subheader("Profit Margin by Market")

st.bar_chart(
    market_performance.set_index("Market")[["Profit_Margin_%"]]
)

st.caption(
    "Gross revenue is calculated using Sales. Net revenue is calculated "
    "using Order Item Total after discounts. Both margin definitions "
    "are displayed to maintain transparency."
)

# ------------------------------------------------------------
# MODULE 2: CUSTOMER VALUE DASHBOARD
# ------------------------------------------------------------

st.divider()
st.header("2. Customer Value Dashboard")

# Aggregate customer performance
customer_data = (
    filtered_df.groupby("Order Customer Id")
    .agg(
        Transactions=("Order Customer Id", "size"),
        Net_Revenue=("Order Item Total", "sum"),
        Total_Profit=("Order Profit Per Order", "sum"),
        Total_Discount=("Order Item Discount", "sum")
    )
    .reset_index()
)

# Calculate customer profit margin
customer_data["Profit_Margin_%"] = np.where(
    customer_data["Net_Revenue"] != 0,
    customer_data["Total_Profit"] /
    customer_data["Net_Revenue"] * 100,
    0
)

# Calculate Customer Value Index using min-max normalization
components = ["Net_Revenue", "Total_Profit", "Transactions"]

for col in components:
    min_value = customer_data[col].min()
    max_value = customer_data[col].max()

    if max_value == min_value:
        customer_data[col + "_Normalized"] = 0
    else:
        customer_data[col + "_Normalized"] = (
            (customer_data[col] - min_value) /
            (max_value - min_value)
        )

customer_data["Customer_Value_Index"] = (
    customer_data["Net_Revenue_Normalized"] +
    customer_data["Total_Profit_Normalized"] +
    customer_data["Transactions_Normalized"]
) / 3 * 100

# Classify customers into value tiers
customer_data["CVI_Percentile"] = (
    customer_data["Customer_Value_Index"].rank(pct=True)
)

customer_data["Customer_Value_Tier"] = np.select(
    [
        customer_data["CVI_Percentile"] >= 0.80,
        customer_data["CVI_Percentile"] >= 0.20
    ],
    ["High Value", "Medium Value"],
    default="Low Value"
)

# Customer summary KPIs
st.subheader("Customer Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", f"{len(customer_data):,}")
col2.metric(
    "Average Customer Profit",
    f"{customer_data['Total_Profit'].mean():,.2f}"
)
col3.metric(
    "Average Customer Value Index",
    f"{customer_data['Customer_Value_Index'].mean():.2f}"
)

# Top customers by CVI
st.subheader("Top 10 Customers by Customer Value Index")

top_customers = customer_data.sort_values(
    "Customer_Value_Index",
    ascending=False
).head(10)

st.dataframe(
    top_customers[
        [
            "Order Customer Id",
            "Transactions",
            "Net_Revenue",
            "Total_Profit",
            "Profit_Margin_%",
            "Customer_Value_Index",
            "Customer_Value_Tier"
        ]
    ].round(2),
    use_container_width=True,
    hide_index=True
)

# Actual profit leaders and loss-making customers
st.subheader("Customer Profitability Ranking")

profit_col1, profit_col2 = st.columns(2)

with profit_col1:
    st.write("Top 10 Customers by Profit")

    top_profit_customers = customer_data.sort_values(
        "Total_Profit", ascending=False
    ).head(10)

    st.dataframe(
        top_profit_customers[
            [
                "Order Customer Id",
                "Net_Revenue",
                "Total_Profit",
                "Profit_Margin_%"
            ]
        ].round(2),
        use_container_width=True,
        hide_index=True
    )

with profit_col2:
    st.write("Bottom 10 Customers by Profit")

    bottom_profit_customers = customer_data.sort_values(
        "Total_Profit", ascending=True
    ).head(10)

    st.dataframe(
        bottom_profit_customers[
            [
                "Order Customer Id",
                "Net_Revenue",
                "Total_Profit",
                "Profit_Margin_%"
            ]
        ].round(2),
        use_container_width=True,
        hide_index=True
    )

# Customer value tier contribution
st.subheader("Customer Value Tier Performance")

tier_summary = (
    customer_data.groupby("Customer_Value_Tier")
    .agg(
        Customer_Count=("Order Customer Id", "count"),
        Total_Revenue=("Net_Revenue", "sum"),
        Total_Profit=("Total_Profit", "sum"),
        Average_CVI=("Customer_Value_Index", "mean")
    )
    .reset_index()
)

total_tier_revenue = customer_data["Net_Revenue"].sum()
total_tier_profit = customer_data["Total_Profit"].sum()

tier_summary["Customer_Share_%"] = (
    tier_summary["Customer_Count"] /
    len(customer_data) * 100
)

tier_summary["Revenue_Contribution_%"] = (
    tier_summary["Total_Revenue"] / total_tier_revenue * 100
    if total_tier_revenue != 0 else 0
)

tier_summary["Profit_Contribution_%"] = (
    tier_summary["Total_Profit"] / total_tier_profit * 100
    if total_tier_profit != 0 else 0
)

st.dataframe(
    tier_summary.round(2),
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    tier_summary.set_index("Customer_Value_Tier")[
        ["Total_Revenue", "Total_Profit"]
    ]
)

st.caption(
    "Customer Value Index is a relative index based on normalized "
    "revenue, profit and transaction frequency. It is not customer "
    "lifetime value. Actual profit should be checked independently."
)

# ------------------------------------------------------------
# MODULE 3: PRODUCT AND CATEGORY PERFORMANCE
# ------------------------------------------------------------

st.divider()
st.header("3. Product & Category Performance")

# Category-level profitability
st.subheader("Category Performance")

category_performance = (
    filtered_df.groupby("Category Name")
    .agg(
        Transactions=("Category Name", "size"),
        Net_Revenue=("Order Item Total", "sum"),
        Total_Profit=("Order Profit Per Order", "sum"),
        Total_Discount=("Order Item Discount", "sum")
    )
    .reset_index()
)

category_performance["Profit_Margin_%"] = np.where(
    category_performance["Net_Revenue"] != 0,
    category_performance["Total_Profit"] /
    category_performance["Net_Revenue"] * 100,
    0
)

category_performance = category_performance.sort_values(
    "Total_Profit", ascending=False
)

st.dataframe(
    category_performance.round(2),
    use_container_width=True,
    hide_index=True
)

st.subheader("Category Profit Comparison")
st.bar_chart(
    category_performance.set_index("Category Name")[["Total_Profit"]]
)

# Product-level profitability
st.subheader("Top 20 Products by Net Revenue")

product_performance = (
    filtered_df.groupby("Product Name")
    .agg(
        Transactions=("Product Name", "size"),
        Net_Revenue=("Order Item Total", "sum"),
        Total_Profit=("Order Profit Per Order", "sum"),
        Total_Discount=("Order Item Discount", "sum")
    )
    .reset_index()
)

product_performance["Profit_Margin_%"] = np.where(
    product_performance["Net_Revenue"] != 0,
    product_performance["Total_Profit"] /
    product_performance["Net_Revenue"] * 100,
    0
)

top_products = product_performance.sort_values(
    "Net_Revenue", ascending=False
).head(20)

st.dataframe(
    top_products.round(2),
    use_container_width=True,
    hide_index=True
)

# High-revenue, relatively low-margin products
st.subheader("High-Revenue, Low-Margin Products")

revenue_threshold = product_performance["Net_Revenue"].median()
margin_threshold = product_performance["Profit_Margin_%"].median()

high_revenue_low_margin = product_performance[
    (product_performance["Net_Revenue"] > revenue_threshold) &
    (product_performance["Profit_Margin_%"] < margin_threshold)
].sort_values("Net_Revenue", ascending=False)

st.caption(
    f"Products with net revenue above {revenue_threshold:,.2f} "
    f"and profit margin below {margin_threshold:.2f}%."
)

st.dataframe(
    high_revenue_low_margin.round(2),
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Low-margin products are identified relative to the dataset median. "
    "A low margin does not necessarily mean the product is loss-making."
)

# ------------------------------------------------------------
# MODULE 4: DISCOUNT IMPACT ANALYZER
# ------------------------------------------------------------

st.divider()
st.header("4. Discount Impact Analyzer")

# Discount band performance
st.subheader("Profitability by Discount Band")

discount_performance = (
    filtered_df.groupby("Discount_Band")
    .agg(
        Transactions=("Discount_Band", "size"),
        Net_Revenue=("Order Item Total", "sum"),
        Total_Discount=("Order Item Discount", "sum"),
        Total_Profit=("Order Profit Per Order", "sum")
    )
    .reset_index()
)

discount_performance["Profit_Margin_%"] = np.where(
    discount_performance["Net_Revenue"] != 0,
    discount_performance["Total_Profit"] /
    discount_performance["Net_Revenue"] * 100,
    0
)

discount_performance["Loss_Making_Transactions"] = (
    filtered_df.assign(
        Is_Loss=filtered_df["Order Profit Per Order"] < 0
    )
    .groupby("Discount_Band")["Is_Loss"]
    .sum()
    .reindex(discount_performance["Discount_Band"])
    .values
)

discount_performance["Loss_Rate_%"] = np.where(
    discount_performance["Transactions"] != 0,
    discount_performance["Loss_Making_Transactions"] /
    discount_performance["Transactions"] * 100,
    0
)

st.dataframe(
    discount_performance.round(2),
    use_container_width=True,
    hide_index=True
)

st.subheader("Profit Margin Across Discount Bands")
st.bar_chart(
    discount_performance.set_index("Discount_Band")[["Profit_Margin_%"]]
)

# Discount sensitivity scenario
st.subheader("Discount What-If Analysis")

discount_change = st.slider(
    "Hypothetical change in discount rate (percentage points)",
    min_value=-10,
    max_value=10,
    value=0,
    step=5
)

baseline_net_revenue = filtered_df["Order Item Total"].sum()
baseline_profit = filtered_df["Order Profit Per Order"].sum()
baseline_gross_revenue = filtered_df["Sales"].sum()

estimated_profit_change = (
    baseline_gross_revenue * discount_change / 100
)

scenario_net_revenue = (
    baseline_net_revenue + estimated_profit_change
)

scenario_profit = (
    baseline_profit + estimated_profit_change
)

scenario_margin = (
    scenario_profit / scenario_net_revenue * 100
    if scenario_net_revenue != 0 else 0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Estimated Scenario Net Revenue",
    f"{scenario_net_revenue:,.2f}"
)

col2.metric(
    "Estimated Scenario Profit",
    f"{scenario_profit:,.2f}",
    f"{estimated_profit_change:+,.2f}"
)

col3.metric(
    "Estimated Scenario Margin",
    f"{scenario_margin:.2f}%"
)

st.caption(
    "Sensitivity estimate only. Assumes transaction volume, product mix "
    "and costs remain unchanged. It is not a forecast and does not prove "
    "that changing discounts will produce this result."
)

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.divider()

st.caption(
    "Supply Chain Profitability Performance Analysis | "
    "APL Logistics Dataset | Analytical dashboard"
)
