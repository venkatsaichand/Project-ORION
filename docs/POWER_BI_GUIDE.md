# Power BI rebuild guide

The Power BI dashboard is a supplementary deliverable to be completed after the repository publication. This guide records the approved analytical conventions for that later rebuild; it does not imply that a finished PBIX is included here.

## Data preparation

1. Run `run_all.py` successfully before opening Power BI.
2. Import the newly generated CSVs from `outputs/` and `data/processed/`.
3. Use `order_fact.csv` for order-level KPIs and monthly/state/review/stage visuals.
4. Use `order_item_detail.csv` for item/category analysis. Clearly label item-grain measures.
5. Use the saved summary outputs as reconciliation references, not manually retyped old dashboard values.

## Approved metric conventions

- Use `late_calendar` as the primary delivery outcome.
- Keep `late_timestamp` on a separate sensitivity page or clearly labeled comparison.
- Use `primary_ctq_summary.csv` for the headline baseline.
- Label payment value as payment value associated with late orders, not loss or financial damage.
- Label seller handoff results as indicators, not responsibility attribution.
- Label SPC signals as investigation triggers, not root causes.
- Do not present proposed scenarios as achieved results or savings.

## Suggested report pages

- Executive baseline
- Monthly and weekly performance
- Geographic distribution
- Product category (item-grain)
- Customer review association
- Process-stage duration
- SPC and investigation priorities
- Definitions, coverage, and limitations

Before publishing the dashboard, reconcile every KPI against the generated CSVs and `validation_report.txt`. Preserve the distinctions between order grain and item grain and between the primary calendar-date CTQ and timestamp sensitivity.
