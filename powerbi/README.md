# Power BI Build Guide

## Import Files

Import the cleaned CSV files from `data/cleaned/`:

- `customers.csv`
- `products.csv`
- `orders.csv`
- `order_items.csv`
- `payments.csv`
- `returns.csv`
- `sales_dashboard.csv`

For the fastest portfolio build, use `sales_dashboard.csv` as the main reporting table. For a more complete model, import all dimension and fact tables.

## Recommended Model Relationships

- `customers[customer_id]` one-to-many `orders[customer_id]`
- `orders[order_id]` one-to-many `order_items[order_id]`
- `products[product_id]` one-to-many `order_items[product_id]`
- `orders[order_id]` one-to-one or one-to-many `payments[order_id]`
- `orders[order_id]` one-to-many `returns[order_id]`

## Suggested DAX Measures

```DAX
Net Revenue = SUM(sales_dashboard[net_revenue])

Gross Revenue = SUM(sales_dashboard[gross_revenue])

Profit = SUM(sales_dashboard[profit])

Orders = DISTINCTCOUNT(sales_dashboard[order_id])

Customers = DISTINCTCOUNT(sales_dashboard[customer_id])

Average Order Value =
DIVIDE([Net Revenue], [Orders])

Returned Orders =
CALCULATE(
    DISTINCTCOUNT(sales_dashboard[order_id]),
    sales_dashboard[is_returned] = TRUE()
)

Return Rate = DIVIDE([Returned Orders], [Orders])

Profit Margin =
DIVIDE([Profit], [Net Revenue])

Discount Amount = SUM(sales_dashboard[discount_amount])

Discount Rate =
DIVIDE([Discount Amount], [Gross Revenue])
```

## Suggested Report Pages

### 1. Executive Overview

- KPI cards: Net Revenue, Profit, Orders, Average Order Value, Return Rate
[powerbi](executive_summary_report.png)
- line chart: Net Revenue and Profit by Month
[powerbi](line_chart_month.png)
- bar chart: Net Revenue by Category
[powerbi](revenue_category.png)

### 2. Product Performance

- matrix: Category, Product, Revenue, Profit, Margin
[powerbi](product_matrix.png)

### 3. Customer and Region Analysis

- bar chart: Revenue by Region
[powerbi](region_net_revune.png)

- stacked bar: Customer Segment by Revenue
[powerbi](customer_segment_net_revuenue.png)
- table: Top Customers by Revenue
[powerbi](top_customer_by_region.png)

### 4. Returns and Discount Risk

- card: Return Rate
[powerbi](return_rate.png)
- table: Products with high returns and low margin

## Portfolio Notes

In the README or portfolio page, explain that the Power BI dashboard uses cleaned exports from a Python data pipeline. This shows that the project covers both code-driven data preparation and business-facing analytics.
