from __future__ import annotations

import pandas as pd

from src.config import CLEAN_DATA_DIR, CLEAN_FILES, RAW_FILES

REGION_MAP = {
    "northeast": "Northeast",
    "north east": "Northeast",
    "ne": "Northeast",
    "south": "South",
    "sth": "South",
    "midwest": "Midwest",
    "mid west": "Midwest",
    "mid-west": "Midwest",
    "west": "West",
    "w": "West",
}


def _standardize_region(value: object) -> str:
    if pd.isna(value):
        return "Unknown"
    clean_value = str(value).strip().lower()
    return REGION_MAP.get(clean_value, str(value).strip().title())


def _standardize_text(value: object, fallback: str = "Unknown") -> str:
    if pd.isna(value) or str(value).strip() == "":
        return fallback
    return str(value).strip().title()


def load_raw_data() -> dict[str, pd.DataFrame]:
    return {name: pd.read_csv(path) for name, path in RAW_FILES.items()}


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    customers = customers.drop_duplicates("customer_id").copy()
    customers["email"] = customers["email"].fillna("missing_email@example.com").str.lower()
    customers["region"] = customers["region"].map(_standardize_region)
    customers["loyalty_tier"] = customers["loyalty_tier"].map(lambda value: _standardize_text(value, "Unassigned"))
    customers["signup_date"] = pd.to_datetime(customers["signup_date"], errors="coerce")
    return customers


def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    products = products.drop_duplicates("product_id").copy()
    products["category"] = products["category"].map(_standardize_text)
    products["product_name"] = products["product_name"].map(_standardize_text)
    products["unit_cost"] = pd.to_numeric(products["unit_cost"], errors="coerce").fillna(0).clip(lower=0)
    products["unit_price"] = pd.to_numeric(products["unit_price"], errors="coerce").fillna(0).clip(lower=0)
    products = products[products["unit_price"] >= products["unit_cost"]].copy()
    return products


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    orders = orders.drop_duplicates("order_id").copy()
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    orders["sales_channel"] = orders["sales_channel"].map(_standardize_text)
    orders["region"] = orders["region"].map(_standardize_region)
    orders["order_status"] = orders["order_status"].map(_standardize_text)
    orders = orders[orders["order_date"].notna()].copy()
    return orders


def clean_order_items(order_items: pd.DataFrame, orders: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    order_items = order_items.drop_duplicates("order_item_id").copy()
    order_items["quantity"] = pd.to_numeric(order_items["quantity"], errors="coerce").fillna(0)
    order_items["discount_percent"] = pd.to_numeric(order_items["discount_percent"], errors="coerce").fillna(0)
    order_items = order_items[order_items["quantity"] > 0].copy()
    order_items["discount_percent"] = order_items["discount_percent"].clip(lower=0, upper=60)
    order_items = order_items[order_items["order_id"].isin(orders["order_id"])]
    order_items = order_items[order_items["product_id"].isin(products["product_id"])]
    order_items["gross_revenue"] = order_items["quantity"] * order_items["unit_price"]
    order_items["discount_amount"] = order_items["gross_revenue"] * (order_items["discount_percent"] / 100)
    order_items["net_revenue"] = order_items["gross_revenue"] - order_items["discount_amount"]
    order_items["cost"] = order_items["quantity"] * order_items["unit_cost"]
    order_items["profit"] = order_items["net_revenue"] - order_items["cost"]
    order_items = order_items[order_items["profit"] >= 0].copy()
    return order_items


def clean_payments(payments: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    payments = payments.drop_duplicates("payment_id").copy()
    payments = payments[payments["order_id"].isin(orders["order_id"])]
    payments["payment_method"] = payments["payment_method"].map(_standardize_text)
    payments["payment_status"] = payments["payment_status"].map(_standardize_text)
    return payments


def clean_returns(returns: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    returns = returns.drop_duplicates("return_id").copy()
    returns = returns[returns["order_id"].isin(orders["order_id"])]
    returns["return_date"] = pd.to_datetime(returns["return_date"], errors="coerce")
    returns["return_reason"] = returns["return_reason"].map(_standardize_text)
    returns = returns[returns["return_date"].notna()].copy()
    return returns


def build_sales_dashboard(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    payments: pd.DataFrame,
    returns: pd.DataFrame,
) -> pd.DataFrame:
    dashboard = (
        order_items.merge(orders, on="order_id", how="left")
        .merge(products[["product_id", "product_name", "category"]], on="product_id", how="left")
        .merge(customers[["customer_id", "region", "loyalty_tier"]], on="customer_id", how="left", suffixes=("_order", "_customer"))
        .merge(payments[["order_id", "payment_method", "payment_status"]], on="order_id", how="left")
    )
    returned_order_ids = set(returns["order_id"])
    dashboard["is_returned"] = dashboard["order_id"].isin(returned_order_ids)
    dashboard["order_month"] = dashboard["order_date"].dt.to_period("M").astype(str)
    dashboard["order_year"] = dashboard["order_date"].dt.year
    dashboard["region"] = dashboard["region_order"].fillna(dashboard["region_customer"]).fillna("Unknown")

    customer_totals = dashboard.groupby("customer_id")["net_revenue"].sum().rename("customer_total_revenue")
    dashboard = dashboard.merge(customer_totals, on="customer_id", how="left")
    dashboard["customer_segment"] = pd.cut(
        dashboard["customer_total_revenue"],
        bins=[-1, 250, 750, 1500, float("inf")],
        labels=["New/Low Value", "Developing", "Loyal", "VIP"],
    ).astype(str)

    dashboard["average_order_value"] = dashboard.groupby("order_id")["net_revenue"].transform("sum")
    dashboard["profit_margin"] = (dashboard["profit"] / dashboard["net_revenue"]).replace([float("inf"), -float("inf")], 0).fillna(0)

    ordered_columns = [
        "order_id",
        "order_item_id",
        "customer_id",
        "order_date",
        "order_month",
        "order_year",
        "sales_channel",
        "region",
        "order_status",
        "product_id",
        "product_name",
        "category",
        "quantity",
        "unit_price",
        "unit_cost",
        "discount_percent",
        "gross_revenue",
        "discount_amount",
        "net_revenue",
        "cost",
        "profit",
        "profit_margin",
        "average_order_value",
        "payment_method",
        "payment_status",
        "is_returned",
        "loyalty_tier",
        "customer_segment",
        "customer_total_revenue",
    ]
    return dashboard[ordered_columns]


def clean_all() -> dict[str, pd.DataFrame]:
    CLEAN_DATA_DIR.mkdir(parents=True, exist_ok=True)
    raw = load_raw_data()

    customers = clean_customers(raw["customers"])
    products = clean_products(raw["products"])
    orders = clean_orders(raw["orders"])
    order_items = clean_order_items(raw["order_items"], orders, products)
    payments = clean_payments(raw["payments"], orders)
    returns = clean_returns(raw["returns"], orders)
    sales_dashboard = build_sales_dashboard(customers, products, orders, order_items, payments, returns)

    cleaned = {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items,
        "payments": payments,
        "returns": returns,
        "sales_dashboard": sales_dashboard,
    }

    for name, dataframe in cleaned.items():
        dataframe.to_csv(CLEAN_FILES[name], index=False)

    return cleaned


if __name__ == "__main__":
    cleaned_data = clean_all()
    for dataset_name, dataframe in cleaned_data.items():
        print(f"{dataset_name}: {len(dataframe):,} rows")
