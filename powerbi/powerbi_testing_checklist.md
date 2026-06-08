# Power BI Testing Checklist

## CSV Import Checks

- Confirm all cleaned CSV files import successfully.
- Confirm date columns are typed as dates.
- Confirm currency fields are numeric decimals.
- Confirm `is_returned` is typed as true/false.
- Confirm there are no blank primary keys.

## Relationship Checks

- Confirm `customers` filters `orders`.
- Confirm `orders` filters `order_items`.
- Confirm `products` filters `order_items`.
- Confirm `orders` filters `payments`.
- Confirm `orders` filters `returns`.
- Confirm relationship directions do not create ambiguous paths.

## DAX Measure Checks

- Net Revenue equals the sum of `sales_dashboard[net_revenue]`.
- Orders equals distinct order count.
- Average Order Value equals Net Revenue divided by Orders.
- Return Rate changes when category or region slicers are used.
- Profit Margin remains blank or zero-safe when revenue is zero.

## Dashboard Visual QA

- KPI cards fit without clipped text.
- Date slicer filters all visuals.
- Region, category, and channel slicers filter all visuals.
- Charts have readable titles and axis labels.
- Top product visuals sort descending by revenue.
- Returns page clearly identifies categories with high returned order counts.
- Final report pages tell a clear story from overview to deeper analysis.
