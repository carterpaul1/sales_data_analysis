from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEAN_DATA_DIR = DATA_DIR / "cleaned"

RANDOM_SEED = 42
START_DATE = "2023-01-01"
END_DATE = "2025-12-31"

CUSTOMER_COUNT = 1_500
PRODUCT_COUNT = 120
ORDER_COUNT = 8_000

RAW_FILES = {
    "customers": RAW_DATA_DIR / "customers_raw.csv",
    "products": RAW_DATA_DIR / "products_raw.csv",
    "orders": RAW_DATA_DIR / "orders_raw.csv",
    "order_items": RAW_DATA_DIR / "order_items_raw.csv",
    "payments": RAW_DATA_DIR / "payments_raw.csv",
    "returns": RAW_DATA_DIR / "returns_raw.csv",
}

CLEAN_FILES = {
    "customers": CLEAN_DATA_DIR / "customers.csv",
    "products": CLEAN_DATA_DIR / "products.csv",
    "orders": CLEAN_DATA_DIR / "orders.csv",
    "order_items": CLEAN_DATA_DIR / "order_items.csv",
    "payments": CLEAN_DATA_DIR / "payments.csv",
    "returns": CLEAN_DATA_DIR / "returns.csv",
    "sales_dashboard": CLEAN_DATA_DIR / "sales_dashboard.csv",
}
