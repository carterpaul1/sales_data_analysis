from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import CLEAN_FILES

st.set_page_config(page_title="Retail Sales Analytics", page_icon=":bar_chart:", layout="wide")


@st.cache_data
def load_dashboard_data() -> pd.DataFrame:
    data = pd.read_csv(CLEAN_FILES["sales_dashboard"], parse_dates=["order_date"])
    data["is_returned"] = data["is_returned"].astype(bool)
    return data


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def filter_data(data: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")
    min_date = data["order_date"].min().date()
    max_date = data["order_date"].max().date()
    date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    regions = st.sidebar.multiselect("Region", sorted(data["region"].dropna().unique()), default=sorted(data["region"].dropna().unique()))
    categories = st.sidebar.multiselect("Category", sorted(data["category"].dropna().unique()), default=sorted(data["category"].dropna().unique()))
    channels = st.sidebar.multiselect("Sales channel", sorted(data["sales_channel"].dropna().unique()), default=sorted(data["sales_channel"].dropna().unique()))

    filtered = data.copy()
    if len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered = filtered[(filtered["order_date"] >= start_date) & (filtered["order_date"] <= end_date)]

    filtered = filtered[
        filtered["region"].isin(regions)
        & filtered["category"].isin(categories)
        & filtered["sales_channel"].isin(channels)
    ]
    return filtered


def render_kpis(data: pd.DataFrame) -> None:
    total_revenue = data["net_revenue"].sum()
    total_profit = data["profit"].sum()
    total_orders = data["order_id"].nunique()
    return_rate = data.loc[data["is_returned"], "order_id"].nunique() / total_orders if total_orders else 0
    average_order_value = data.groupby("order_id")["net_revenue"].sum().mean() if total_orders else 0

    columns = st.columns(5)
    columns[0].metric("Net Revenue", format_currency(total_revenue))
    columns[1].metric("Profit", format_currency(total_profit))
    columns[2].metric("Orders", f"{total_orders:,}")
    columns[3].metric("Avg Order Value", format_currency(average_order_value))
    columns[4].metric("Return Rate", f"{return_rate:.1%}")


def render_dashboard(data: pd.DataFrame) -> None:
    st.title("Northstar Outfitters Sales Analytics")
    st.caption("Synthetic retail ecommerce data generated with Faker, cleaned with pandas, and prepared for Power BI.")

    if data.empty:
        st.warning("No data matches the selected filters.")
        return

    render_kpis(data)

    monthly_sales = data.groupby("order_month", as_index=False).agg(net_revenue=("net_revenue", "sum"), profit=("profit", "sum"))
    category_sales = data.groupby("category", as_index=False).agg(net_revenue=("net_revenue", "sum"), profit=("profit", "sum")).sort_values("net_revenue", ascending=False)
    region_sales = data.groupby("region", as_index=False).agg(net_revenue=("net_revenue", "sum"), orders=("order_id", "nunique"))
    channel_sales = data.groupby("sales_channel", as_index=False).agg(net_revenue=("net_revenue", "sum"), profit=("profit", "sum"))
    segment_sales = data.groupby("customer_segment", as_index=False).agg(net_revenue=("net_revenue", "sum"), customers=("customer_id", "nunique"))
    returns = data.groupby("category", as_index=False).agg(returned_orders=("is_returned", "sum"), net_revenue=("net_revenue", "sum"))

    left, right = st.columns(2)
    with left:
        st.subheader("Revenue and Profit Trend")
        st.plotly_chart(px.line(monthly_sales, x="order_month", y=["net_revenue", "profit"], markers=True), use_container_width=True)
    with right:
        st.subheader("Sales by Category")
        st.plotly_chart(px.bar(category_sales, x="category", y="net_revenue", color="profit"), use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Regional Performance")
        st.plotly_chart(px.bar(region_sales, x="region", y="net_revenue", color="orders"), use_container_width=True)
    with right:
        st.subheader("Channel Performance")
        st.plotly_chart(px.pie(channel_sales, names="sales_channel", values="net_revenue", hole=0.45), use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Customer Segments")
        st.plotly_chart(px.bar(segment_sales, x="customer_segment", y="net_revenue", color="customers"), use_container_width=True)
    with right:
        st.subheader("Returns by Category")
        st.plotly_chart(px.scatter(returns, x="net_revenue", y="returned_orders", color="category", size="net_revenue"), use_container_width=True)

    st.subheader("Detailed Sales Records")
    st.dataframe(
        data[
            [
                "order_date",
                "order_id",
                "customer_id",
                "region",
                "sales_channel",
                "category",
                "product_name",
                "quantity",
                "net_revenue",
                "profit",
                "is_returned",
            ]
        ].sort_values("order_date", ascending=False),
        use_container_width=True,
    )


try:
    dashboard_data = load_dashboard_data()
    render_dashboard(filter_data(dashboard_data))
except FileNotFoundError:
    st.error("Cleaned data was not found. Run `python -m src.generate_data` and `python -m src.clean_data` first.")
