from __future__ import annotations

import pandas as pd

from src.clean_data import clean_all
from src.config import CLEAN_FILES, END_DATE, RAW_FILES, START_DATE
from src.generate_data import generate_all
from src.validation import required_clean_files_exist, required_raw_files_exist, validate_dashboard


def test_raw_data_files_are_generated() -> None:
    generate_all()
    assert required_raw_files_exist()
    for path in RAW_FILES.values():
        assert path.exists()
        assert path.stat().st_size > 0


def test_clean_data_files_are_exported() -> None:
    generate_all()
    clean_all()
    assert required_clean_files_exist()
    for path in CLEAN_FILES.values():
        assert path.exists()
        assert path.stat().st_size > 0


def test_required_dashboard_columns_exist() -> None:
    generate_all()
    clean_all()
    dashboard = pd.read_csv(CLEAN_FILES["sales_dashboard"])
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
    assert required_columns.issubset(dashboard.columns)


def test_primary_keys_are_unique_after_cleaning() -> None:
    generate_all()
    clean_all()
    key_map = {
        "customers": "customer_id",
        "products": "product_id",
        "orders": "order_id",
        "order_items": "order_item_id",
        "payments": "payment_id",
        "returns": "return_id",
    }
    for dataset_name, key in key_map.items():
        dataframe = pd.read_csv(CLEAN_FILES[dataset_name])
        assert dataframe[key].is_unique


def test_numeric_values_are_valid_after_cleaning() -> None:
    generate_all()
    clean_all()
    dashboard = pd.read_csv(CLEAN_FILES["sales_dashboard"])
    assert (dashboard["quantity"] > 0).all()
    assert (dashboard["net_revenue"] >= 0).all()
    assert (dashboard["profit"] >= 0).all()
    assert dashboard["discount_percent"].between(0, 60).all()


def test_order_dates_are_within_configured_range() -> None:
    generate_all()
    clean_all()
    dashboard = pd.read_csv(CLEAN_FILES["sales_dashboard"], parse_dates=["order_date"])
    assert dashboard["order_date"].min() >= pd.Timestamp(START_DATE)
    assert dashboard["order_date"].max() <= pd.Timestamp(END_DATE)


def test_streamlit_input_dataset_passes_validation() -> None:
    generate_all()
    clean_all()
    dashboard = pd.read_csv(CLEAN_FILES["sales_dashboard"], parse_dates=["order_date"])
    assert validate_dashboard(dashboard) == []
