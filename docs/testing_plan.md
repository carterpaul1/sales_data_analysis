# Testing Plan

## Purpose

This document explains how the project is tested and what must be verified before it is presented as a portfolio project.

## Automated Tests

Run:

```bash
pytest
```

The automated tests verify:

- raw CSV files are generated
- cleaned CSV files are exported
- required dashboard columns exist
- primary keys are unique after cleaning
- invalid negative quantities are removed
- revenue values are non-negative
- discount percentages are within the accepted range
- order dates stay within the configured project date range
- the Streamlit dashboard input dataset passes validation

## Manual Verification

After running the pipeline, launch the dashboard:

```bash
streamlit run app.py
```

Manually verify:

- dashboard loads without errors
- KPI values appear at the top of the page
- sidebar filters update all charts
- charts are readable on a laptop screen
- detailed sales table is populated
- no chart shows impossible values such as negative revenue

## Expected Outputs

The pipeline should create:

- `data/raw/*.csv`
- `data/cleaned/customers.csv`
- `data/cleaned/products.csv`
- `data/cleaned/orders.csv`
- `data/cleaned/order_items.csv`
- `data/cleaned/payments.csv`
- `data/cleaned/returns.csv`
- `data/cleaned/sales_dashboard.csv`

## Known Limitations

- The data is synthetic and should not be used for real business decisions.
- The Power BI deliverable is documentation and CSV exports, not an included `.pbix` file.
- The dashboard is designed for portfolio demonstration rather than production authentication, scheduling, or deployment.
