# Project ORION
## E-commerce delivery performance analysis | Olist dataset

Project ORION is a reproducible Python analytics project examining delivery performance in the Brazilian Olist e-commerce dataset. It applies data-quality checks, order-grain data preparation, descriptive analysis, statistical estimation, and weekly process monitoring.

The analytical baseline and definitions below reflect the current validated project outputs. The Python pipeline rebuilds the analytical tables from the nine source CSV files. The Power BI dashboard is a planned supplementary deliverable and is not represented as completed in this repository.

## Project findings

The current validated cohort contains **96,203 delivered orders** purchased from **January 1, 2017 through August 31, 2018**, with valid actual and estimated delivery timestamps.

| Measure | Result |
|---|---:|
| Delivered-order cohort | 96,203 |
| Calendar-date late orders | 6,531 |
| Primary calendar-date late rate | **6.7888%** |
| On-time orders | 89,672 |
| On-time yield | **93.2112%** |
| Wilson 95% confidence interval for late rate | 6.6315%–6.9495% |
| Timestamp-based late rate (sensitivity only) | 8.1307% |
| Estimated delivery timestamps at midnight | 96,203 of 96,203 |
| Weekly Laney p′ upper signals | 9 |
| Weekly Laney p′ lower signals | 4 |

The primary CTQ compares calendar dates. The separate timestamp-based result is a sensitivity measure and must not replace the primary baseline. Since all estimated timestamps in this cohort are at midnight, timestamp comparison classifies an additional 1,291 orders as late.

Other descriptive findings include:
- Mean actual delivery lead time: **12.54 days**; median: **10.21 days**.
- Mean promised lead time: **23.65 days**; median: **23.22 days**.
- Latest scored review coverage: **95,560 orders (99.33%)**. Mean review score was 4.291 for on-time orders and 2.271 for late orders.
- The process-stage summaries exclude negative or missing durations and report their exclusions separately.
- Category summaries are at **item grain**, not order grain.

These are historical descriptive findings. Associations and SPC signals do not establish root causes, fault, or causation.

## What the project contains

- `run_all.py` — project entry point.
- `src/orion_pipeline.py` — data preparation, analysis, summaries, and hard validation checks.
- `config.json` — cohort dates and delivered-order status.
- `data/raw/` — location for the nine original source CSVs (not committed).
- `data/processed/` — generated order- and item-grain analytical tables (not committed; reproducible).
- `outputs/` — compact summary CSVs and the validation report (included as project evidence).
- `docs/` — data dictionary, methodology, and Power BI rebuild guidance.
- `tests/` — focused helper tests.

## Source data

Place these nine CSV files in `data/raw/`:

1. `olist_customers_dataset.csv`
2. `olist_geolocation_dataset.csv`
3. `olist_order_items_dataset.csv`
4. `olist_order_payments_dataset.csv`
5. `olist_order_reviews_dataset.csv`
6. `olist_orders_dataset.csv`
7. `olist_products_dataset.csv`
8. `olist_sellers_dataset.csv`
9. `product_category_name_translation.csv`

The source CSVs are excluded from GitHub to keep the repository lightweight. Obtain the Olist dataset independently and follow the source's applicable terms. Do not substitute previously processed tables for the original source files.

## Reproduce the analysis (Windows PowerShell)

From the project root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copy all nine source CSVs into `data\raw\`, then run:

```powershell
.\.venv\Scripts\python.exe run_all.py
```

To run the focused helper tests (optional development step), install the development requirements and run:

```powershell
.\\.venv\\Scripts\\python.exe -m pip install -r requirements-dev.txt
.\\.venv\\Scripts\\python.exe -m pytest -v
```

The pipeline writes:
- `data/processed/order_fact.csv` — one row per eligible delivered order.
- `data/processed/order_item_detail.csv` — item-level category detail.
- Summary CSVs and `validation_report.txt` under `outputs/`.

The compact files in `outputs/` are committed as a snapshot of the current validated run. Re-running the pipeline regenerates them. The larger processed fact tables and raw source data remain local and are excluded from Git.

## Analytical definitions

### Cohort
Orders must have:
- status `delivered`;
- purchase timestamp from 2017-01-01 through 2018-08-31 inclusive;
- a valid actual customer-delivery timestamp; and
- a valid estimated-delivery timestamp.

### Primary CTQ
An order is late when:

```text
actual_delivery_date > estimated_delivery_date
```

This is a calendar-date comparison. Delivery on the estimated calendar date is classified as on time, even if the actual timestamp is later than the estimated timestamp's midnight value.

### Sensitivity measure
A separate comparison uses the full timestamps:

```text
actual_delivery_timestamp > estimated_delivery_timestamp
```

It is reported only as sensitivity analysis.

### Data grain and interpretation
- The main fact table has one row per eligible order. One-to-many item, payment, and review records are aggregated before joining to avoid multiplying order counts.
- Product-category results are item-level. They must not be interpreted as order-level late rates.
- Review results are descriptive associations, not evidence that lateness alone caused a review score.
- Process-stage durations are observational. Negative or missing durations are excluded from duration summaries, with counts retained.
- The seller handoff measure is an indicator for investigation, not proof of seller fault.
- Weekly Laney p′ signals are investigation triggers, not root causes.

## Repository contents and exclusions

The repository tracks source code, documentation, configuration, and compact analytical summaries. It intentionally excludes:
- original raw CSV files;
- generated large processed fact/detail CSVs;
- the local Python virtual environment and cache files;
- local editor settings and environment-secret files.

See `.gitignore` for the exact rules.

## Limitations

The dataset does not provide complete warehouse event histories, carrier GPS/scan trails, support-contact records, intervention assignments, or finance-approved cost inputs. Therefore, this analysis does not establish root causes or responsibility, and it does not claim implemented improvements, realized savings, or ROI.

## Documentation

- [Methodology and analytical guardrails](docs/METHODOLOGY.md)
- [Data dictionary](docs/DATA_DICTIONARY.md)
- [Power BI rebuild guide](docs/POWER_BI_GUIDE.md)
