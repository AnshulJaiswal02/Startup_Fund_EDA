"""Clean startup funding data and export dashboard/data.js."""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "startup_funding.csv"
DASHBOARD = ROOT / "dashboard"
OUT_JS = DASHBOARD / "data.js"

CITY_MAP = {
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "gurgaon": "Gurugram",
    "gurugram": "Gurugram",
    "new delhi": "New Delhi",
    "delhi": "New Delhi",
    "nw delhi": "New Delhi",
    "new delhi / us": "New Delhi",
    "mumbai": "Mumbai",
    "pune": "Pune",
    "hyderabad": "Hyderabad",
    "chennai": "Chennai",
    "noida": "Noida",
    "ahmedabad": "Ahmedabad",
    "jaipur": "Jaipur",
    "kolkata": "Kolkata",
    "indore": "Indore",
    "chandigarh": "Chandigarh",
    "goa": "Goa",
}

INDUSTRY_MAP = {
    "consumer internet": "Consumer Internet",
    "technology": "Technology",
    "ecommerce": "E-Commerce",
    "e-commerce": "E-Commerce",
    "e commerce": "E-Commerce",
    "healthcare": "Healthcare",
    "health and wellness": "Healthcare",
    "health and wellness.": "Healthcare",
    "finance": "FinTech",
    "fintech": "FinTech",
    "fin-tech": "FinTech",
    "financial services": "FinTech",
    "logistics": "Logistics",
    "logistics tech": "Logistics",
    "education": "EdTech",
    "ed-tech": "EdTech",
    "edtech": "EdTech",
    "e-tech": "EdTech",
    "online education platform": "EdTech",
    "food & beverage": "Food & Beverage",
    "food and beverage": "Food & Beverage",
    "food & beverages": "Food & Beverage",
    "hospitality": "Hospitality",
    "transportation": "Transportation",
    "transport": "Transportation",
    "saas": "SaaS / Software",
    "software": "SaaS / Software",
    "it": "SaaS / Software",
    "real estate": "Real Estate",
    "others": "Others",
}


def clean_text(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = str(value)
    text = text.replace(r"\xc2\xa0", " ").replace("\xa0", " ")
    text = re.sub(r"\\x[0-9a-fA-F]{2}", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if not text or text.lower() in {"nan", "n/a", "na", "none"}:
        return None
    return text


def parse_date(value: object) -> pd.Timestamp | pd.NaT:
    text = clean_text(value)
    if not text:
        return pd.NaT
    text = text.replace(".", "/").replace("//", "/")
    text = re.sub(r"(\d{2})/(\d{2})(\d{4})", r"\1/\2/\3", text)
    if re.fullmatch(r"\d{2}/\d{3}", text):
        return pd.NaT
    if text == "01/07/015":
        text = "01/07/2015"
    try:
        return pd.to_datetime(text, dayfirst=True, errors="coerce")
    except Exception:
        return pd.NaT


def parse_amount(value: object) -> float:
    text = clean_text(value)
    if not text:
        return np.nan
    lowered = text.lower().replace(" ", "")
    if lowered in {"undisclosed", "unknown", "n/a", "na"}:
        return np.nan
    text = text.replace("+", "").replace(",", "")
    text = re.sub(r"[^0-9.]", "", text)
    if not text:
        return np.nan
    try:
        return float(text)
    except ValueError:
        return np.nan


def normalize_city(value: object) -> str:
    text = clean_text(value)
    if not text:
        return "Unknown"
    key = text.lower().split("/")[0].strip()
    key = re.sub(r"[^a-z ]", "", key).strip()
    return CITY_MAP.get(key, text.split("/")[0].strip().title())


def normalize_industry(value: object) -> str:
    text = clean_text(value)
    if not text:
        return "Unknown"
    key = re.sub(r"[^a-z0-9 &-]", "", text.lower()).strip()
    key = key.replace("  ", " ")
    return INDUSTRY_MAP.get(key, text.title())


def normalize_stage(value: object) -> str:
    text = clean_text(value)
    if not text:
        return "Unknown"
    key = text.lower().replace("\n", " ").replace("\\n", " ")
    key = re.sub(r"[^a-z0-9 /+-]", " ", key)
    key = re.sub(r"\s+", " ", key).strip()
    if "debt" in key:
        return "Debt"
    if "pre-series a" in key or "pre series a" in key or "pre-seriesa" in key:
        return "Pre-Series A"
    if "series h" in key:
        return "Series H+"
    if "series g" in key:
        return "Series G"
    if "series f" in key:
        return "Series F"
    if "series e" in key:
        return "Series E"
    if "series d" in key:
        return "Series D"
    if "series c" in key:
        return "Series C"
    if "series b" in key:
        return "Series B"
    if "series a" in key:
        return "Series A"
    if "private equity" in key or key in {"pe", "privateequity"}:
        return "Private Equity"
    if "angel" in key and "seed" in key:
        return "Seed / Angel"
    if "angel" in key:
        return "Angel"
    if "seed" in key:
        return "Seed"
    if "venture" in key:
        return "Venture"
    if "crowd" in key:
        return "Crowdfunding"
    if "bridge" in key:
        return "Bridge"
    return "Other"


def split_investors(value: object) -> list[str]:
    text = clean_text(value)
    if not text:
        return []
    parts = re.split(r",|&| and ", text, flags=re.IGNORECASE)
    names = []
    for part in parts:
        name = part.strip(" .")
        skip = {"undisclosed", "undisclosed investors", "n/a", "others", "other", "undisclosed investor"}
        if name and name.lower() not in skip:
            names.append(name)
    return names


def load_clean() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH, encoding="utf-8", encoding_errors="replace")
    df.columns = [
        "sr_no",
        "raw_date",
        "startup",
        "industry_raw",
        "subvertical",
        "city_raw",
        "investors_raw",
        "stage_raw",
        "amount_raw",
        "remarks",
    ]
    df["startup"] = df["startup"].map(clean_text)
    df.loc[df["startup"].str.startswith("http", na=False), "startup"] = "WealthBucket"
    df["date"] = df["raw_date"].map(parse_date)
    df["year"] = df["date"].dt.year.astype("Int64")
    df["month"] = df["date"].dt.month.astype("Int64")
    df["ym"] = df["date"].dt.to_period("M").astype(str)
    df["amount_usd"] = df["amount_raw"].map(parse_amount)
    df["city"] = df["city_raw"].map(normalize_city)
    df["industry"] = df["industry_raw"].map(normalize_industry)
    df["stage"] = df["stage_raw"].map(normalize_stage)
    df["has_amount"] = df["amount_usd"].notna()
    return df


def money(value: float) -> str:
    if pd.isna(value):
        return "—"
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"


def records(frame: pd.DataFrame) -> list[dict]:
    return json.loads(frame.to_json(orient="records"))


def build_payload(df: pd.DataFrame) -> dict:
    disclosed = df[df["has_amount"]].copy()
    yearly = (
        df.dropna(subset=["year"])
        .groupby("year")
        .agg(deals=("startup", "size"), funding=("amount_usd", "sum"), median=("amount_usd", "median"))
        .reset_index()
    )
    monthly = (
        disclosed.dropna(subset=["date"])
        .groupby("ym")
        .agg(funding=("amount_usd", "sum"), deals=("startup", "size"))
        .reset_index()
        .sort_values("ym")
    )
    industries = (
        disclosed.groupby("industry")
        .agg(funding=("amount_usd", "sum"), deals=("startup", "size"))
        .reset_index()
        .sort_values("funding", ascending=False)
        .head(12)
    )
    cities = (
        disclosed.groupby("city")
        .agg(funding=("amount_usd", "sum"), deals=("startup", "size"))
        .reset_index()
        .sort_values("funding", ascending=False)
        .head(12)
    )
    stages = (
        df.groupby("stage")
        .agg(deals=("startup", "size"), funding=("amount_usd", "sum"))
        .reset_index()
        .sort_values("deals", ascending=False)
    )
    startups = (
        disclosed.groupby("startup")
        .agg(funding=("amount_usd", "sum"), deals=("startup", "size"), industry=("industry", "first"), city=("city", "first"))
        .reset_index()
        .sort_values("funding", ascending=False)
        .head(15)
    )
    investor_rows = []
    for _, row in df.iterrows():
        for name in split_investors(row["investors_raw"]):
            investor_rows.append({"investor": name, "amount": row["amount_usd"], "startup": row["startup"]})
    inv = pd.DataFrame(investor_rows)
    investors = (
        inv.groupby("investor")
        .agg(deals=("startup", "size"), funding=("amount", "sum"))
        .reset_index()
        .sort_values("deals", ascending=False)
        .head(15)
    )
    heatmap_cities = cities["city"].head(8).tolist()
    heatmap_industries = industries["industry"].head(8).tolist()
    heat = (
        disclosed[disclosed["city"].isin(heatmap_cities) & disclosed["industry"].isin(heatmap_industries)]
        .groupby(["city", "industry"], as_index=False)["amount_usd"]
        .sum()
    )
    mega = disclosed.nlargest(12, "amount_usd")[
        ["date", "startup", "industry", "city", "stage", "amount_usd", "investors_raw"]
    ].copy()
    mega["date"] = mega["date"].dt.strftime("%d %b %Y")
    mega["amount_label"] = mega["amount_usd"].map(money)
    mega = mega.rename(columns={"investors_raw": "investors"})

    bins = [0, 250_000, 1_000_000, 5_000_000, 20_000_000, 50_000_000, 100_000_000, np.inf]
    labels = ["<250K", "250K–1M", "1–5M", "5–20M", "20–50M", "50–100M", "100M+"]
    disclosed["bucket"] = pd.cut(disclosed["amount_usd"], bins=bins, labels=labels, right=False)
    buckets = disclosed["bucket"].value_counts().reindex(labels).fillna(0).reset_index()
    buckets.columns = ["bucket", "deals"]

    return {
        "generated": pd.Timestamp.now().strftime("%Y-%m-%d"),
        "kpis": {
            "deals": int(len(df)),
            "startups": int(df["startup"].nunique()),
            "disclosed": int(df["has_amount"].sum()),
            "total_funding": float(disclosed["amount_usd"].sum()),
            "total_funding_label": money(disclosed["amount_usd"].sum()),
            "median_deal": float(disclosed["amount_usd"].median()),
            "median_deal_label": money(disclosed["amount_usd"].median()),
            "mean_deal": float(disclosed["amount_usd"].mean()),
            "mean_deal_label": money(disclosed["amount_usd"].mean()),
            "years": "2015–2020",
            "cities": int(df.loc[df["city"] != "Unknown", "city"].nunique()),
        },
        "yearly": records(yearly),
        "monthly": records(monthly),
        "industries": records(industries),
        "cities": records(cities),
        "stages": records(stages),
        "startups": records(startups.assign(funding_label=startups["funding"].map(money))),
        "investors": records(investors.assign(funding_label=investors["funding"].map(money))),
        "heatmap": {
            "cities": heatmap_cities,
            "industries": heatmap_industries,
            "cells": records(heat),
        },
        "mega": records(mega),
        "buckets": records(buckets),
        "insights": [
            "Deal volume peaked in 2016, then cooled through 2019–2020 as later-stage cheques grew larger.",
            "Bengaluru, Mumbai, New Delhi and Gurugram absorb most disclosed capital — a four-city funding core.",
            "Consumer Internet and Technology dominate deal count; E-Commerce and FinTech punch above their weight in dollars.",
            "Seed and Private Equity labels cover most historical records; named Series A–C rounds become clearer after 2017.",
            "Mean deal size is pulled up by mega-rounds (Flipkart, Paytm) and at least one suspect row (Rapido at $3.9B) — always sanity-check $1B+ cheques; median is the fairer typical ticket.",
        ],
    }


def main() -> None:
    DASHBOARD.mkdir(exist_ok=True)
    df = load_clean()
    payload = build_payload(df)
    OUT_JS.write_text(
        "window.FUNDING_DATA = " + json.dumps(payload, default=str) + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT_JS} | deals={payload['kpis']['deals']} funding={payload['kpis']['total_funding_label']}")


if __name__ == "__main__":
    main()
