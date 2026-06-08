# User Acceptance Testing

## Goal

Confirm that the Streamlit dashboard works as a portfolio demo for a junior developer/data analyst.

## Scenario 1: Executive Overview

1. Launch the dashboard with `streamlit run app.py`.
2. Confirm the page title appears.
3. Confirm the KPI row shows net revenue, profit, orders, average order value, and return rate.
4. Confirm the KPI values are formatted clearly.

Expected result: a reviewer can understand business performance within the first screen.

## Scenario 2: Filter Behavior

1. Change the date range.
2. Select one region.
3. Select one product category.
4. Select one sales channel.

Expected result: KPIs, charts, and the detailed table update together.

## Scenario 3: Business Analysis

1. Review revenue and profit trend.
2. Identify the top sales category.
3. Compare regional performance.
4. Check returns by category.

Expected result: the dashboard supports a short business walkthrough in an interview or portfolio review.

## Scenario 4: Data Table Review

1. Scroll to the detailed sales records table.
2. Confirm rows include date, order, customer, region, channel, category, product, quantity, revenue, profit, and return flag.

Expected result: the dashboard provides enough row-level detail to explain how the visual metrics were produced.
