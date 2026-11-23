# Methodology and analytical guardrails

## Unit of analysis and joins

The primary analytical fact table contains one row per eligible delivered order. Items, payments, and reviews are one-to-many relative to orders. These tables are aggregated to order grain before being joined to the order fact to avoid multiplying order counts.

The separate category detail table remains at item grain. Category late-item shares are not order-level CTQ rates.

## Cohort

- Order status: `delivered`
- Purchase timestamp: 2017-01-01 through 2018-08-31 inclusive
- Actual customer-delivery timestamp: present
- Estimated-delivery timestamp: present

The current cohort contains 96,203 orders.

## Primary CTQ and sensitivity

The primary classification is:

```text
late_calendar = actual_delivery_date > estimated_delivery_date
```

The calendar-date late count is 6,531 of 96,203 orders (6.7888%). The on-time yield is 93.2112%. The Wilson 95% confidence interval for the late rate is 6.6315%–6.9495%.

A separate timestamp comparison is retained:

```text
late_timestamp = actual_delivery_timestamp > estimated_delivery_timestamp
```

It classifies 7,822 orders (8.1307%) as late, 1,291 more than the primary calendar-date definition. All 96,203 estimated-delivery timestamps in the cohort are at midnight. The timestamp result is sensitivity analysis, not a replacement for the primary CTQ.

## Lead time and process stages

- Actual delivery lead time: customer-delivery timestamp minus purchase timestamp.
- Promised lead time: estimated-delivery timestamp minus purchase timestamp.
- Approval to carrier: carrier-handoff timestamp minus approval timestamp.
- Carrier to customer: customer-delivery timestamp minus carrier-handoff timestamp.

Negative or missing process-stage durations are excluded from the stage averages and counted separately in `process_stage_summary.csv`. The source-derived values remain in the order fact for audit. Stage comparisons are observational and may be mathematically coupled with the delivery outcome; they do not prove causation.

## Reviews

The pipeline selects the latest review record per order after sorting by review creation date, answer timestamp, and review ID. Review coverage is 95,560 of 96,203 cohort orders (99.33%). The difference in mean review scores between on-time and late orders is descriptive association, not proof that lateness alone caused the score.

## Seller handoff indicator

For each item, the pipeline compares the calendar date of carrier handoff with the calendar date of the item's shipping-limit timestamp. An order is flagged if at least one item has a later carrier-handoff calendar date. This is an investigation indicator, not a seller-fault label.

## Weekly SPC

Weekly subgroups are formed from purchase weeks (`W-SUN`) using order counts and calendar-date late counts. The pipeline calculates a Laney p′ chart using the overall proportion, standardized subgroup values, the moving range of adjacent standardized values, and the d2 constant 1.128. The current output contains 87 weekly subgroups, 9 upper signals, and 4 lower signals.

Signals identify periods for investigation. They do not identify root causes. The SPC output should be interpreted with the subgroup definition and the limits of the observational dataset in mind.

## Data-quality and validation checks

The pipeline checks required source columns, validates merge cardinality where specified, and writes a validation report. Current hard checks cover:
- unique order IDs in the cohort;
- delivered status and required delivery timestamps;
- consistency of the primary late count with its flag;
- timestamp-late count being at least the calendar-date late count;
- monthly order and late-count reconciliation;
- category item-record reconciliation and mutually exclusive category status;
- process-stage valid-plus-excluded reconciliation.

The current saved validation report records all listed checks as passing.

## Limitations

The dataset does not contain complete warehouse event histories, carrier GPS/scan trails, support-contact records, intervention assignments, or finance-approved cost inputs. Do not infer root causes, seller/carrier responsibility, realized savings, or ROI from these data. Proposed improvement targets or financial scenarios must be labeled as hypotheses or assumptions, not achieved results.
