from __future__ import annotations

import pandas as pd

from src.config import CLEAN_FILES, END_DATE, RAW_FILES, START_DATE


def required_clean_files_exist() -> bool:
    return all(path.exists() for path in CLEAN_FILES.values())


def required_raw_files_exist() -> bool:
    return all(path.exists() for path in RAW_FILES.values())


def load_clean_dashboard() -> pd.DataFrame:
    return pd.read_csv(CLEAN_FILES["sales_dashboard"], parse_dates=["order_date"])


def validate_dashboard(dashboard: pd.DataFrame) -> list[str]:
    failures = []
    required_columns = {
        "order_id",
        "order_item_id",
        "customer_id",
        "order_date",
        "sales_channel",
        "region",
        "category",
        "quantity",
        "discount_percent",
        "net_revenue",
        "profit",
        "is_returned",
        "customer_segment",
    }

    missing_columns = required_columns.difference(dashboard.columns)
    if missing_columns:
        failures.append(f"Missing required columns: {sorted(missing_columns)}")

    if dashboard["order_item_id"].duplicated().any():
        failures.append("Duplicate order_item_id values found.")

    if (dashboard["quantity"] <= 0).any():
        failures.append("Quantity must be positive.")

    if (dashboard["net_revenue"] < 0).any():
        failures.append("Net revenue must not be negative.")

    if (dashboard["profit"] < 0).any():
        failures.append("Profit must not be negative.")

    if dashboard["discount_percent"].between(0, 60).all() is False:
        failures.append("Discount percent must be between 0 and 60.")

    start_date = pd.Timestamp(START_DATE)
    end_date = pd.Timestamp(END_DATE)
    if dashboard["order_date"].min() < start_date or dashboard["order_date"].max() > end_date:
        failures.append("Order dates are outside configured range.")

    return failures
