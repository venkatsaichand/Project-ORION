from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy.stats import norm


RAW_FILES = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "translation": "product_category_name_translation.csv",
}


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)


def wilson_interval(successes: int, total: int, confidence: float = 0.95) -> tuple[float, float]:
    if total <= 0:
        return (np.nan, np.nan)
    z = norm.ppf(1 - (1 - confidence) / 2)
    p = successes / total
    denom = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denom
    margin = z * np.sqrt((p * (1 - p) / total) + (z * z / (4 * total * total))) / denom
    return centre - margin, centre + margin


def laney_pprime(weekly: pd.DataFrame) -> pd.DataFrame:
    """Calculate Laney p' chart limits from weekly counts and subgroup sizes."""
    out = weekly.copy()
    n = out["orders"].astype(float)
    p = out["late_orders"] / n
    pbar = out["late_orders"].sum() / n.sum()
    sigma = np.sqrt(np.maximum(pbar * (1 - pbar) / n, 0))
    z = np.divide(p - pbar, sigma, out=np.zeros_like(p, dtype=float), where=sigma > 0)

    # Moving range of standardized subgroup values; d2=1.128 for a moving range of 2.
    mr = np.abs(np.diff(z))
    sigma_z = float(np.mean(mr) / 1.128) if len(mr) else 1.0
    if not np.isfinite(sigma_z) or sigma_z == 0:
        sigma_z = 1.0

    out["late_rate"] = p
    out["centre_line"] = pbar
    out["sigma_z"] = sigma_z
    out["ucl"] = np.minimum(1.0, pbar + 3 * sigma_z * sigma)
    out["lcl"] = np.maximum(0.0, pbar - 3 * sigma_z * sigma)
    out["z_score"] = z
    out["upper_signal"] = p > out["ucl"]
    out["lower_signal"] = p < out["lcl"]
    return out


def _require_columns(df: pd.DataFrame, columns: Iterable[str], label: str) -> None:
    missing = sorted(set(columns) - set(df.columns))
    if missing:
        raise ValueError(f"{label} is missing required columns: {missing}")


def _save(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def run_pipeline(project_root: Path) -> None:
    project_root = Path(project_root)
    raw_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"
    output_dir = project_root / "outputs"
    processed_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    missing = [name for name in RAW_FILES.values() if not (raw_dir / name).exists()]
    if missing:
        raise FileNotFoundError(
            "These original source CSVs are missing from data/raw/: "
            + ", ".join(missing)
            + "\nCopy all nine original Olist CSV files into data/raw/ and run again."
        )

    cfg = json.loads((project_root / "config.json").read_text(encoding="utf-8"))
    start = pd.Timestamp(cfg["cohort_start"])
    end = pd.Timestamp(cfg["cohort_end"]) + pd.Timedelta(days=1)
    delivered_status = cfg["delivered_status"]

    data = {key: read_csv(raw_dir / filename) for key, filename in RAW_FILES.items()}
    orders = data["orders"].copy()
    items = data["items"].copy()
    payments = data["payments"].copy()
    reviews = data["reviews"].copy()
    products = data["products"].copy()
    customers = data["customers"].copy()
    translation = data["translation"].copy()

    _require_columns(orders, [
        "order_id", "customer_id", "order_status", "order_purchase_timestamp",
        "order_approved_at", "order_delivered_carrier_date",
        "order_delivered_customer_date", "order_estimated_delivery_date"
    ], "orders")
    _require_columns(items, ["order_id", "order_item_id", "product_id", "seller_id",
                             "price", "freight_value", "shipping_limit_date"], "order_items")
    _require_columns(payments, ["order_id", "payment_type", "payment_installments",
                                "payment_value"], "order_payments")
    _require_columns(reviews, ["order_id", "review_id", "review_score",
                               "review_creation_date", "review_answer_timestamp"], "order_reviews")
    _require_columns(products, ["product_id", "product_category_name"], "products")
    _require_columns(customers, ["customer_id", "customer_state"], "customers")

    date_cols = [
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    # Order-grain aggregations: avoid multiplying orders through one-to-many joins.
    item_work = items.copy()
    item_work["shipping_limit_date"] = pd.to_datetime(item_work["shipping_limit_date"], errors="coerce")
    item_agg = item_work.groupby("order_id", as_index=False).agg(
        item_count=("order_item_id", "count"),
        item_value_brl=("price", "sum"),
        freight_value_brl=("freight_value", "sum"),
        seller_count=("seller_id", "nunique"),
        latest_shipping_limit=("shipping_limit_date", "max"),
    )

    payment_agg = payments.groupby("order_id", as_index=False).agg(
        payment_value_brl=("payment_value", "sum"),
        payment_record_count=("payment_type", "size"),
        payment_type_count=("payment_type", "nunique"),
    )

    # Select latest review record per order using review timestamps and stable sort.
    reviews["review_creation_date"] = pd.to_datetime(reviews["review_creation_date"], errors="coerce")
    reviews["review_answer_timestamp"] = pd.to_datetime(reviews["review_answer_timestamp"], errors="coerce")
    reviews_sorted = reviews.sort_values(
        ["order_id", "review_creation_date", "review_answer_timestamp", "review_id"],
        na_position="first"
    )
    latest_reviews = reviews_sorted.drop_duplicates("order_id", keep="last")
    review_agg = latest_reviews[["order_id", "review_score"]].copy()
    review_agg = review_agg.rename(columns={"review_score": "latest_review_score"})

    customer_cols = ["customer_id", "customer_state"]
    customer_dim = customers[customer_cols].drop_duplicates("customer_id")

    fact = orders.merge(customer_dim, on="customer_id", how="left", validate="many_to_one")
    fact = fact.merge(item_agg, on="order_id", how="left", validate="one_to_one")
    fact = fact.merge(payment_agg, on="order_id", how="left", validate="one_to_one")
    fact = fact.merge(review_agg, on="order_id", how="left", validate="one_to_one")

    cohort_mask = (
        fact["order_status"].eq(delivered_status)
        & fact["order_purchase_timestamp"].ge(start)
        & fact["order_purchase_timestamp"].lt(end)
        & fact["order_delivered_customer_date"].notna()
        & fact["order_estimated_delivery_date"].notna()
    )
    cohort = fact.loc[cohort_mask].copy()
    cohort["actual_delivery_date"] = cohort["order_delivered_customer_date"].dt.normalize()
    cohort["estimated_delivery_date"] = cohort["order_estimated_delivery_date"].dt.normalize()
    cohort["late_calendar"] = cohort["actual_delivery_date"] > cohort["estimated_delivery_date"]
    cohort["late_timestamp"] = (
        cohort["order_delivered_customer_date"] > cohort["order_estimated_delivery_date"]
    )
    cohort["delivery_lead_days"] = (
        cohort["order_delivered_customer_date"] - cohort["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    cohort["promised_lead_days"] = (
        cohort["order_estimated_delivery_date"] - cohort["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    cohort["approval_to_carrier_days"] = (
        cohort["order_delivered_carrier_date"] - cohort["order_approved_at"]
    ).dt.total_seconds() / 86400
    cohort["carrier_to_customer_days"] = (
        cohort["order_delivered_customer_date"] - cohort["order_delivered_carrier_date"]
    ).dt.total_seconds() / 86400
    cohort["purchase_month"] = cohort["order_purchase_timestamp"].dt.to_period("M").astype(str)
    cohort["purchase_week"] = (
        cohort["order_purchase_timestamp"].dt.to_period("W-SUN").dt.start_time
    )

    # Item-level category detail is kept separate from the one-row-per-order fact.
    item_detail = item_work.merge(
        products[["product_id", "product_category_name"]].drop_duplicates("product_id"),
        on="product_id", how="left", validate="many_to_one"
    )
    if {"product_category_name", "product_category_name_english"}.issubset(translation.columns):
        item_detail = item_detail.merge(
            translation[["product_category_name", "product_category_name_english"]]
                .drop_duplicates("product_category_name"),
            on="product_category_name", how="left", validate="many_to_one"
        )
    else:
        item_detail["product_category_name_english"] = np.nan
    item_detail = item_detail.merge(
        cohort[["order_id", "late_calendar"]], on="order_id", how="inner", validate="many_to_one"
    )

    # Seller handoff is a descriptive indicator: any item shipping limit earlier than carrier handoff.
    handoff = item_work[["order_id", "shipping_limit_date"]].merge(
        cohort[["order_id", "order_delivered_carrier_date", "late_calendar"]],
        on="order_id", how="inner", validate="many_to_one"
    )
    # Primary handoff indicator uses calendar-date comparison, consistent with
    # the primary delivery CTQ. Keep timestamp comparison out of this measure.
    handoff["item_handoff_late"] = (
        handoff["order_delivered_carrier_date"].notna()
        & handoff["shipping_limit_date"].notna()
        & (
            handoff["order_delivered_carrier_date"].dt.normalize()
            > handoff["shipping_limit_date"].dt.normalize()
        )
    )
    handoff_order = handoff.groupby("order_id", as_index=False).agg(
        any_item_handoff_late=("item_handoff_late", "any")
    )
    cohort = cohort.merge(handoff_order, on="order_id", how="left", validate="one_to_one")
    cohort["any_item_handoff_late"] = cohort["any_item_handoff_late"].fillna(False)

    _save(cohort, processed_dir / "order_fact.csv")
    _save(item_detail, processed_dir / "order_item_detail.csv")

    total = len(cohort)
    late = int(cohort["late_calendar"].sum())
    ontime = total - late
    lo, hi = wilson_interval(late, total)
    ts_late = int(cohort["late_timestamp"].sum())
    midnight_estimates = int(
        (cohort["order_estimated_delivery_date"].dt.time == pd.Timestamp("00:00:00").time()).sum()
    )

    primary = pd.DataFrame([{
        "cohort_orders": total, "late_orders": late, "on_time_orders": ontime,
        "late_rate": late / total if total else np.nan,
        "on_time_yield": ontime / total if total else np.nan,
        "wilson_95_lower": lo, "wilson_95_upper": hi,
        "mean_delivery_lead_days": cohort["delivery_lead_days"].mean(),
        "median_delivery_lead_days": cohort["delivery_lead_days"].median(),
        "mean_promised_lead_days": cohort["promised_lead_days"].mean(),
        "median_promised_lead_days": cohort["promised_lead_days"].median(),
    }])
    _save(primary, output_dir / "primary_ctq_summary.csv")

    sensitivity = pd.DataFrame([{
        "cohort_orders": total, "timestamp_late_orders": ts_late,
        "timestamp_late_rate": ts_late / total if total else np.nan,
        "calendar_date_late_orders": late,
        "additional_timestamp_late_vs_primary": ts_late - late,
        "estimated_delivery_at_midnight_count": midnight_estimates,
        "interpretation": "Sensitivity only; primary CTQ uses calendar-date comparison."
    }])
    _save(sensitivity, output_dir / "timestamp_sensitivity.csv")

    monthly = cohort.groupby("purchase_month", as_index=False).agg(
        orders=("order_id", "nunique"), late_orders=("late_calendar", "sum")
    )
    monthly["on_time_orders"] = monthly["orders"] - monthly["late_orders"]
    monthly["late_rate"] = monthly["late_orders"] / monthly["orders"]
    _save(monthly, output_dir / "monthly_delivery_summary.csv")

    weekly = cohort.groupby("purchase_week", as_index=False).agg(
        orders=("order_id", "nunique"), late_orders=("late_calendar", "sum")
    )
    weekly["purchase_week"] = weekly["purchase_week"].astype(str)
    weekly = laney_pprime(weekly)
    _save(weekly, output_dir / "weekly_laney_p_chart.csv")

    review = cohort.dropna(subset=["latest_review_score"]).copy()
    review["review_band"] = np.where(review["latest_review_score"].between(1, 2), "1-2 stars", "3-5 stars")
    review_summary = review.groupby("late_calendar", as_index=False).agg(
        reviewed_orders=("order_id", "nunique"),
        mean_review_score=("latest_review_score", "mean"),
        one_to_two_star_orders=("review_band", lambda x: (x == "1-2 stars").sum()),
    )
    review_summary["one_to_two_star_share"] = (
        review_summary["one_to_two_star_orders"] / review_summary["reviewed_orders"]
    )
    review_summary["delivery_group"] = np.where(review_summary["late_calendar"], "Late", "On time")
    _save(review_summary, output_dir / "review_summary.csv")

    stage_rows = []
    for col, stage in [
        ("approval_to_carrier_days", "Approval to carrier"),
        ("carrier_to_customer_days", "Carrier to customer"),
    ]:
        for late_flag, group_name in [(False, "On time"), (True, "Late")]:
            group = cohort.loc[cohort["late_calendar"].eq(late_flag)]
            valid_mask = group[col].notna() & (group[col] >= 0)
            values = group.loc[valid_mask, col]
            stage_rows.append({
                "stage": stage, "delivery_group": group_name, "cohort_orders": len(group),
                "valid_orders": len(values), "mean_days": values.mean(),
                "median_days": values.median(),
                "excluded_negative_or_missing": int((~valid_mask).sum())
            })
    _save(pd.DataFrame(stage_rows), output_dir / "process_stage_summary.csv")

    state = cohort.groupby("customer_state", as_index=False).agg(
        orders=("order_id", "nunique"), late_orders=("late_calendar", "sum")
    )
    state["late_rate"] = state["late_orders"] / state["orders"]
    state = state.sort_values("late_orders", ascending=False)
    _save(state, output_dir / "state_delivery_summary.csv")

    # Preserve three distinct data states: translated category, genuinely
    # missing source category, and present Portuguese category without translation.
    item_detail["category_status"] = np.select(
        [
            item_detail["product_category_name"].isna(),
            item_detail["product_category_name"].notna()
            & item_detail["product_category_name_english"].isna(),
        ],
        ["Missing source category", "Untranslated source category"],
        default="Translated category",
    )
    item_detail["category_label"] = item_detail["product_category_name_english"]
    item_detail.loc[
        item_detail["category_status"].eq("Missing source category"),
        "category_label"
    ] = "Missing source category"
    item_detail.loc[
        item_detail["category_status"].eq("Untranslated source category"),
        "category_label"
    ] = "Untranslated source category"

    category = item_detail.groupby(
        ["category_status", "category_label"], dropna=False, as_index=False
    ).agg(
        item_records=("order_id", "size"),
        late_item_records=("late_calendar", "sum")
    )
    category["late_item_share"] = category["late_item_records"] / category["item_records"]
    _save(category.sort_values(["item_records", "category_label"], ascending=[False, True]),
          output_dir / "category_delivery_summary.csv")

    category_quality = item_detail.groupby("category_status", as_index=False).agg(
        item_records=("order_id", "size"),
        late_item_records=("late_calendar", "sum")
    )
    category_quality["late_item_share"] = (
        category_quality["late_item_records"] / category_quality["item_records"]
    )
    _save(category_quality, output_dir / "category_data_quality_summary.csv")

    handoff_summary = cohort.groupby("late_calendar", as_index=False).agg(
        orders=("order_id", "nunique"),
        orders_with_handoff_late_indicator=("any_item_handoff_late", "sum")
    )
    handoff_summary["delivery_group"] = np.where(handoff_summary["late_calendar"], "Late", "On time")
    handoff_summary["indicator_share"] = (
        handoff_summary["orders_with_handoff_late_indicator"] / handoff_summary["orders"]
    )
    _save(handoff_summary, output_dir / "seller_handoff_indicator_summary.csv")

    # Join and source data quality summary.
    dq_rows = []
    for key, df in data.items():
        dq_rows.append({
            "source_table": key, "rows": len(df), "columns": len(df.columns),
            "duplicate_full_rows": int(df.duplicated().sum())
        })
    _save(pd.DataFrame(dq_rows), output_dir / "data_quality_summary.csv")

    # Hard validation checks for grain and key definitions.
    checks = {
        "cohort_has_unique_order_ids": bool(cohort["order_id"].is_unique),
        "cohort_all_delivered": bool(cohort["order_status"].eq(delivered_status).all()),
        "cohort_has_actual_delivery": bool(cohort["order_delivered_customer_date"].notna().all()),
        "cohort_has_estimated_delivery": bool(cohort["order_estimated_delivery_date"].notna().all()),
        "primary_late_count_matches_flag": bool(late == int(cohort["late_calendar"].sum())),
        "timestamp_late_count_at_least_calendar_late": bool(ts_late >= late),
        "monthly_orders_reconcile": bool(int(monthly["orders"].sum()) == total),
        "monthly_late_reconcile": bool(int(monthly["late_orders"].sum()) == late),
        "category_item_records_reconcile": bool(
            int(category["item_records"].sum()) == len(item_detail)
        ),
        "category_statuses_are_mutually_exclusive": bool(
            int(category_quality["item_records"].sum()) == len(item_detail)
        ),
        "stage_valid_plus_excluded_reconcile": bool(
            all(
                int(row.valid_orders + row.excluded_negative_or_missing) == int(row.cohort_orders)
                for row in pd.DataFrame(stage_rows).itertuples()
            )
        ),
    }
    if not all(checks.values()):
        failed = [k for k, v in checks.items() if not v]
        raise AssertionError(f"Validation failed: {failed}")

    report_lines = [
        "PROJECT ORION — PIPELINE VALIDATION",
        "===================================",
        f"Source tables loaded: {len(data)}",
        f"Delivered-order cohort: {total:,}",
        f"Calendar-date late orders: {late:,}",
        f"Calendar-date late rate: {late / total:.4%}" if total else "Calendar-date late rate: N/A",
        f"Timestamp-late orders (sensitivity): {ts_late:,}",
        f"Estimated timestamps at midnight: {midnight_estimates:,}",
        f"Weekly Laney p' upper signals: {int(weekly['upper_signal'].sum())}",
        f"Weekly Laney p' lower signals: {int(weekly['lower_signal'].sum())}",
        f"Late orders with calendar-date handoff indicator: {int(handoff_summary.loc[handoff_summary['delivery_group'].eq('Late'), 'orders_with_handoff_late_indicator'].iloc[0])}",
        "",
        "Checks:"
    ] + [f"[{'PASS' if value else 'FAIL'}] {name}" for name, value in checks.items()]
    report_lines += [
        "",
        "Interpretation note: this is descriptive observational analysis.",
        "SPC signals are investigation triggers, not root causes.",
        "Stage and handoff indicators do not establish responsibility or causation.",
        "No implementation, realized savings, or ROI is claimed."
    ]
    (output_dir / "validation_report.txt").write_text("\n".join(report_lines), encoding="utf-8")
    print("\n".join(report_lines))
    print("\nPipeline completed. Review data/processed/ and outputs/ before using them in Power BI.")
