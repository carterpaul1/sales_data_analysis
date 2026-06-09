# Power BI Measures and Visual Build Sheet

Use this file while editing `powerbi_dashboard.pbix` in Power BI Desktop.

## Create Measures

In Power BI Desktop, click the `sales_dashboard` table, then select **Table tools > New measure**. Add each measure below one at a time.

```DAX
Net Revenue = SUM(sales_dashboard[net_revenue])
```

```DAX
Gross Revenue = SUM(sales_dashboard[gross_revenue])
```

```DAX
Profit = SUM(sales_dashboard[profit])
```

```DAX
Orders = DISTINCTCOUNT(sales_dashboard[order_id])
```

```DAX
Customers = DISTINCTCOUNT(sales_dashboard[customer_id])
```

```DAX
Average Order Value = DIVIDE([Net Revenue], [Orders])
```

```DAX
Returned Orders =
CALCULATE(
    DISTINCTCOUNT(sales_dashboard[order_id]),
    sales_dashboard[is_returned] = TRUE()
)
```

```DAX
Return Rate = DIVIDE([Returned Orders], [Orders])
```

```DAX
Profit Margin = DIVIDE([Profit], [Net Revenue])
```

```DAX
Discount Amount = SUM(sales_dashboard[discount_amount])
```

```DAX
Discount Rate = DIVIDE([Discount Amount], [Gross Revenue])
```

```DAX
Total Quantity = SUM(sales_dashboard[quantity])
```

## Format Measures

- Net Revenue: Currency, 0 decimals
- Gross Revenue: Currency, 0 decimals
- Profit: Currency, 0 decimals
- Average Order Value: Currency, 0 decimals
- Discount Amount: Currency, 0 decimals
- Return Rate: Percentage, 1 decimal
- Profit Margin: Percentage, 1 decimal
- Discount Rate: Percentage, 1 decimal
- Orders: Whole number
- Customers: Whole number
- Returned Orders: Whole number
- Total Quantity: Whole number

## Page 1: Executive Overview

Create a page named **Executive Overview**.

Add slicers:

- `sales_dashboard[order_date]` as Between
- `sales_dashboard[region]` as Dropdown
- `sales_dashboard[category]` as Dropdown
- `sales_dashboard[sales_channel]` as Dropdown

Add card visuals:

- Net Revenue
- Profit
- Orders
- Average Order Value
- Return Rate

Add a line chart:

- X-axis: `sales_dashboard[order_month]`
- Y-axis: `Net Revenue`, `Profit`
- Title: Revenue and Profit Trend

Add a clustered bar chart:

- Y-axis: `sales_dashboard[category]`
- X-axis: `Net Revenue`
- Tooltips: `Profit`, `Profit Margin`, `Orders`
- Title: Revenue by Category

Add a donut chart:

- Legend: `sales_dashboard[sales_channel]`
- Values: `Net Revenue`
- Title: Revenue by Sales Channel

## Page 2: Product Performance

Create a page named **Product Performance**.

Add a clustered bar chart:

- Y-axis: `sales_dashboard[product_name]`
- X-axis: `Net Revenue`
- Visual filter: Top N, Top 10 by Net Revenue
- Title: Top 10 Products by Revenue

Add a matrix:

- Rows: `category`, `product_name`
- Values: `Net Revenue`, `Profit`, `Profit Margin`, `Total Quantity`, `Discount Rate`
- Title: Product Profitability Matrix

Add a scatter chart:

- X-axis: `Discount Rate`
- Y-axis: `Profit Margin`
- Size: `Net Revenue`
- Legend: `category`
- Title: Discount Rate vs Profit Margin

## Page 3: Customer and Region Analysis

Create a page named **Customer and Region Analysis**.

Add a clustered bar chart:

- Y-axis: `region`
- X-axis: `Net Revenue`
- Tooltips: `Orders`, `Customers`, `Profit Margin`
- Title: Revenue by Region

Add a stacked column chart:

- X-axis: `customer_segment`
- Y-axis: `Net Revenue`
- Legend: `loyalty_tier`
- Title: Revenue by Customer Segment and Loyalty Tier

Add a table:

- `customer_id`
- `customer_segment`
- `loyalty_tier`
- `region`
- `customer_total_revenue`

Sort the table by `customer_total_revenue` descending.

## Page 4: Returns and Discount Risk

Create a page named **Returns and Discount Risk**.

Add card visuals:

- Returned Orders
- Return Rate
- Discount Amount

Add a clustered bar chart:

- Y-axis: `category`
- X-axis: `Returned Orders`
- Title: Returned Orders by Category

Add a scatter chart:

- X-axis: `Discount Rate`
- Y-axis: `Returned Orders`
- Size: `Net Revenue`
- Legend: `category`
- Title: Discount and Return Risk

Add a table:

- `product_name`
- `category`
- `Net Revenue`
- `Profit`
- `Profit Margin`
- `Returned Orders`
- `Discount Rate`

Sort the table by `Returned Orders` descending.

## Final Polish

- Use a white or very light gray canvas.
- Align KPI cards across the top.
- Use slicers consistently on each page.
- Turn on chart titles.
- Turn on data labels for bar charts.
- Keep currency values rounded to whole dollars.
- Save screenshots into `reports/`.
