# Data dictionary

This document describes the generated analytical tables. Raw source CSVs and the larger processed fact/detail tables are excluded from the public Git repository; the pipeline regenerates the latter from the original source files.

## Processed analytical tables

### `data/processed/order_fact.csv`
One row per eligible delivered order. Includes source order fields, customer state, order-grain item/payment/review aggregates, delivery classifications, lead-time measures, process-stage durations, and the seller handoff indicator.

Important fields:
- `late_calendar`: primary calendar-date CTQ Boolean
- `late_timestamp`: full-timestamp sensitivity Boolean
- `delivery_lead_days`: purchase to actual delivery
- `promised_lead_days`: purchase to estimated delivery
- `approval_to_carrier_days`: approval to carrier handoff
- `carrier_to_customer_days`: carrier handoff to customer delivery
- `any_item_handoff_late`: at least one item handoff after shipping limit by calendar date

### `data/processed/order_item_detail.csv`
Item-grain table joined to product category and the order's primary late flag. Do not sum order counts from this table without accounting for multiple items per order.

## Tracked summary outputs

### `outputs/primary_ctq_summary.csv`
Cohort size, late/on-time counts and rates, Wilson interval, and actual/promised lead-time summaries.

### `outputs/timestamp_sensitivity.csv`
Timestamp-based late count/rate alongside the primary calendar-date result, additional timestamp-late count, and count of estimated timestamps at midnight.

### `outputs/monthly_delivery_summary.csv`
Monthly order counts, late counts, on-time counts, and late rate by purchase month.

### `outputs/weekly_laney_p_chart.csv`
Weekly subgroup order counts, late counts/rate, centre line, Laney p′ dispersion estimate, control limits, standardized score, and upper/lower signal flags.

### `outputs/review_summary.csv`
Latest review-score summaries by primary delivery group, including reviewed-order counts and 1–2-star shares.

### `outputs/process_stage_summary.csv`
Valid nonnegative process-stage duration counts, means, medians, cohort sizes, and excluded negative/missing duration counts by delivery group.

### `outputs/state_delivery_summary.csv`
Order counts, late counts, and late rates by customer state.

### `outputs/category_delivery_summary.csv`
Item-record counts and late-item shares by category status/label. This is item-grain, not order-grain.

### `outputs/category_data_quality_summary.csv`
Separates item records with a missing source category, a present source category without an English translation, and a translated category.

### `outputs/seller_handoff_indicator_summary.csv`
Order counts and share with at least one item handoff-late indicator, by delivery group.

### `outputs/data_quality_summary.csv`
Source row/column counts and exact duplicate full-row counts for the nine loaded source tables.

### `outputs/validation_report.txt`
Source-table count, cohort and CTQ totals, SPC signal counts, seller handoff indicator count, and hard validation-check results.

## Grain reminders

- `order_fact.csv` is order-grain.
- `order_item_detail.csv` and category summaries are item-grain.
- Never compare item counts directly with order counts without labeling the different grains.
