from __future__ import annotations

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

from src.config import (
    CUSTOMER_COUNT,
    END_DATE,
    ORDER_COUNT,
    PRODUCT_COUNT,
    RANDOM_SEED,
    RAW_DATA_DIR,
    RAW_FILES,
    START_DATE,
)

fake = Faker("en_US")

CATEGORIES = {
    "Electronics": ["Headphones", "Bluetooth Speaker", "Tablet Case", "Smart Watch", "USB Hub"],
    "Home": ["Throw Blanket", "Desk Lamp", "Storage Bin", "Cookware Set", "Air Purifier"],
    "Apparel": ["Performance Hoodie", "Trail Jacket", "Running Socks", "Graphic Tee", "Denim Shirt"],
    "Beauty": ["Face Serum", "Body Lotion", "Hair Dryer", "Makeup Brush Set", "Sunscreen"],
    "Sports": ["Yoga Mat", "Water Bottle", "Resistance Bands", "Gym Bag", "Foam Roller"],
    "Office": ["Notebook Pack", "Standing Desk Mat", "Monitor Stand", "Desk Organizer", "Planner"],
}

REGIONS = ["Northeast", "South", "Midwest", "West"]
MESSY_REGIONS = {
    "Northeast": ["northeast", "North East", "NE", "NORTHEAST"],
    "South": ["south", "SOUTH", "Sth"],
    "Midwest": ["mid west", "MIDWEST", "Mid-West"],
    "West": ["west", "WEST", "W"],
}
CHANNELS = ["Online", "Mobile App", "Retail Store", "Marketplace"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Gift Card", "Buy Now Pay Later"]
RETURN_REASONS = ["Damaged", "Wrong Size", "Changed Mind", "Late Delivery", "Not as Described"]


def _date_range() -> tuple[datetime, datetime]:
    return datetime.fromisoformat(START_DATE), datetime.fromisoformat(END_DATE)


def _random_date(start: datetime, end: datetime) -> datetime:
    return start + timedelta(days=random.randint(0, (end - start).days))


def generate_customers() -> pd.DataFrame:
    rows = []
    for idx in range(1, CUSTOMER_COUNT + 1):
        region = random.choice(REGIONS)
        rows.append(
            {
                "customer_id": f"C{idx:05d}",
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email() if random.random() > 0.035 else None,
                "city": fake.city(),
                "state": fake.state_abbr(),
                "region": random.choice(MESSY_REGIONS[region]) if random.random() < 0.12 else region,
                "signup_date": fake.date_between(start_date="-5y", end_date="-30d").isoformat(),
                "loyalty_tier": random.choices(
                    ["Bronze", "Silver", "Gold", "Platinum", None],
                    weights=[48, 28, 14, 6, 4],
                    k=1,
                )[0],
            }
        )

    customers = pd.DataFrame(rows)
    duplicate_rows = customers.sample(15, random_state=RANDOM_SEED)
    return pd.concat([customers, duplicate_rows], ignore_index=True)


def generate_products() -> pd.DataFrame:
    rows = []
    product_id = 1
    for category, names in CATEGORIES.items():
        for _ in range(PRODUCT_COUNT // len(CATEGORIES)):
            base_name = random.choice(names)
            cost = round(random.uniform(5, 180), 2)
            margin = random.uniform(1.25, 2.4)
            category_value = category.lower() if random.random() < 0.1 else category
            rows.append(
                {
                    "product_id": f"P{product_id:04d}",
                    "product_name": f"{fake.color_name()} {base_name}",
                    "category": category_value,
                    "unit_cost": cost,
                    "unit_price": round(cost * margin, 2),
                    "supplier": fake.company(),
                    "active": random.choice([True, True, True, False]),
                }
            )
            product_id += 1
    return pd.DataFrame(rows)


def generate_orders(customers: pd.DataFrame) -> pd.DataFrame:
    start, end = _date_range()
    customer_ids = customers["customer_id"].drop_duplicates().tolist()
    rows = []
    for idx in range(1, ORDER_COUNT + 1):
        order_date = _random_date(start, end)
        region = random.choice(REGIONS)
        rows.append(
            {
                "order_id": f"O{idx:06d}",
                "customer_id": random.choice(customer_ids),
                "order_date": order_date.isoformat(),
                "sales_channel": random.choice(CHANNELS),
                "region": random.choice(MESSY_REGIONS[region]) if random.random() < 0.1 else region,
                "order_status": random.choices(
                    ["Completed", "Completed", "Completed", "Returned", "Cancelled"],
                    weights=[78, 8, 4, 7, 3],
                    k=1,
                )[0],
            }
        )

    orders = pd.DataFrame(rows)
    duplicate_rows = orders.sample(25, random_state=RANDOM_SEED)
    return pd.concat([orders, duplicate_rows], ignore_index=True)


def generate_order_items(orders: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    rows = []
    products_lookup = products.set_index("product_id").to_dict("index")
    product_ids = list(products_lookup.keys())
    item_id = 1

    for order_id in orders["order_id"].drop_duplicates():
        for _ in range(random.randint(1, 4)):
            product_id = random.choice(product_ids)
            product = products_lookup[product_id]
            quantity = random.choices([1, 2, 3, 4, -1], weights=[55, 25, 12, 6, 2], k=1)[0]
            discount_percent = random.choices(
                [0, 5, 10, 15, 20, 25, 110],
                weights=[42, 18, 16, 12, 8, 3, 1],
                k=1,
            )[0]
            rows.append(
                {
                    "order_item_id": f"OI{item_id:07d}",
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": product["unit_price"],
                    "unit_cost": product["unit_cost"],
                    "discount_percent": discount_percent,
                }
            )
            item_id += 1

    return pd.DataFrame(rows)


def generate_payments(orders: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for idx, order in enumerate(orders.drop_duplicates("order_id").itertuples(index=False), start=1):
        rows.append(
            {
                "payment_id": f"PMT{idx:06d}",
                "order_id": order.order_id,
                "payment_method": random.choice(PAYMENT_METHODS),
                "payment_status": "Refunded" if order.order_status == "Returned" else random.choice(["Paid", "Paid", "Paid", "Pending"]),
            }
        )
    return pd.DataFrame(rows)


def generate_returns(orders: pd.DataFrame) -> pd.DataFrame:
    returned_orders = orders.drop_duplicates("order_id")
    returned_orders = returned_orders[returned_orders["order_status"].eq("Returned")]
    rows = []
    for idx, order in enumerate(returned_orders.itertuples(index=False), start=1):
        return_date = datetime.fromisoformat(order.order_date) + timedelta(days=random.randint(2, 45))
        rows.append(
            {
                "return_id": f"R{idx:06d}",
                "order_id": order.order_id,
                "return_date": return_date.isoformat(),
                "return_reason": random.choice(RETURN_REASONS),
            }
        )
    return pd.DataFrame(rows)


def generate_all() -> dict[str, pd.DataFrame]:
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    Faker.seed(RANDOM_SEED)
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers)
    order_items = generate_order_items(orders, products)
    payments = generate_payments(orders)
    returns = generate_returns(orders)

    datasets = {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items,
        "payments": payments,
        "returns": returns,
    }

    for name, dataframe in datasets.items():
        dataframe.to_csv(RAW_FILES[name], index=False)

    return datasets


if __name__ == "__main__":
    generated = generate_all()
    for dataset_name, dataframe in generated.items():
        print(f"{dataset_name}: {len(dataframe):,} rows")
