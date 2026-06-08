# Data Quality Checks

## Intentional Raw Data Problems

The Faker generation step intentionally creates realistic issues:

- duplicate customer and order records
- missing customer emails
- inconsistent region labels such as `NE`, `North East`, `mid west`, and `W`
- inconsistent product category casing
- missing loyalty tiers
- negative item quantities
- discount percentages above a reasonable business threshold

## Cleaning Rules Applied

The pandas cleaning pipeline:

- removes duplicate primary keys
- fills missing emails with a clear placeholder
- standardizes regions into Northeast, South, Midwest, and West
- standardizes product categories and sales channels
- removes order items with invalid quantities
- caps discount percentages between 0 and 60
- removes invalid dates
- keeps only order items connected to valid orders and products

## Calculated Fields

The cleaned dashboard dataset includes:

- gross revenue
- discount amount
- net revenue
- cost
- profit
- profit margin
- average order value
- return flag
- customer total revenue
- customer segment
- order month and order year

## Validation Checks

Validation confirms:

- all expected files exist
- required columns are present
- primary keys are unique
- revenue and quantity values are valid
- discounts are within accepted bounds
- order dates are within the configured range
