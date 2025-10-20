#!/usr/bin/env python3
import os
import sys
import glob
import json
from typing import List
import pandas as pd


def _load_lookup_data(lookup_dir: str) -> pd.DataFrame:
    """
    Load and normalize JSON lookup files from lookup_dir.
    Returns a DataFrame with unique card_id rows and the highest
    available market price (holofoil preferred, then normal, else 0.0).
    """
    required_cols = [
        "card_id",
        "card_name",
        "card_number",
        "set_id",
        "set_name",
        "card_market_value",
    ]
    all_lookup_df: List[pd.DataFrame] = []

    files = sorted(glob.glob(os.path.join(lookup_dir, "*.json")))
    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as exc:
            print(f"Warning: failed to read/parse JSON {filepath}: {exc}", file=sys.stderr)
            continue

        if not isinstance(data, dict) or "data" not in data:
            print(f"Warning: unexpected JSON structure in {filepath}, skipping", file=sys.stderr)
            continue

        df = pd.json_normalize(data["data"])

        # Extract market prices: prefer holofoil then normal, then 0.0
        holo = df.get("tcgplayer.prices.holofoil.market")
        normal = df.get("tcgplayer.prices.normal.market")

        # Start with NaNs so fillna works as intended
        df["card_market_value"] = pd.NA
        if holo is not None:
            df["card_market_value"] = holo
        if normal is not None:
            df["card_market_value"] = df["card_market_value"].fillna(normal)
        df["card_market_value"] = df["card_market_value"].fillna(0.0).astype(float)

        # Rename columns to standardized names
        df = df.rename(
            columns={
                "id": "card_id",
                "name": "card_name",
                "number": "card_number",
                "set.id": "set_id",
                "set.name": "set_name",
            }
        )

        # Ensure required columns exist
        for c in required_cols:
            if c not in df.columns:
                df[c] = pd.NA

        all_lookup_df.append(df[required_cols].copy())

    if not all_lookup_df:
        return pd.DataFrame(columns=required_cols)

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)

    # Keep highest priced duplicate for each card_id
    lookup_df = (
        lookup_df.sort_values("card_market_value", ascending=False)
        .drop_duplicates(subset=["card_id"], keep="first")
        .reset_index(drop=True)
    )

    return lookup_df


def _load_inventory_data(inventory_dir: str) -> pd.DataFrame:
    """
    Load inventory CSV files from inventory_dir and synthesize card_id
    by combining set_id and card_number.
    """
    files = sorted(glob.glob(os.path.join(inventory_dir, "*.csv")))
    inventory_parts: List[pd.DataFrame] = []

    for filepath in files:
        try:
            df = pd.read_csv(filepath, dtype=str)
        except Exception as exc:
            print(f"Warning: failed to read CSV {filepath}: {exc}", file=sys.stderr)
            continue
        inventory_parts.append(df)

    if not inventory_parts:
        return pd.DataFrame()

    inventory_df = pd.concat(inventory_parts, ignore_index=True)

    # Ensure necessary columns exist as strings
    for col in ("set_id", "card_number"):
        if col not in inventory_df.columns:
            inventory_df[col] = ""

    inventory_df["card_id"] = inventory_df["set_id"].astype(str) + "-" + inventory_df[
        "card_number"
    ].astype(str)

    return inventory_df


def update_portfolio(inventory_dir: str, lookup_dir: str, output_file: str) -> None:
    """
    Main ETL: load lookup and inventory, merge, clean, and write final CSV.
    """
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    # Handle empty inventory: write empty CSV with headers and bail out
    final_cols = [
        "index",
        "binder_name",
        "page_number",
        "slot_number",
        "card_id",
        "card_name",
        "card_number",
        "set_id",
        "set_name",
        "card_market_value",
    ]

    if inventory_df.empty:
        print("Error: No inventory data found.", file=sys.stderr)
        empty_df = pd.DataFrame(columns=final_cols)
        empty_df.to_csv(output_file, index=False)
        print(f"Wrote empty portfolio to {output_file}", file=sys.stderr)
        return

    # Merge inventory with lookup on card_id (left join to keep inventory)
    merged = pd.merge(
        inventory_df,
        lookup_df[
            ["card_id", "card_name", "card_number", "set_id", "set_name", "card_market_value"]
        ],
        on="card_id",
        how="left",
        validate="m:1",
    )

    # Fill missing values
    if "card_market_value" in merged.columns:
        merged["card_market_value"] = merged["card_market_value"].fillna(0.0).astype(float)
    else:
        merged["card_market_value"] = 0.0

    merged["set_name"] = merged.get("set_name").fillna("NOT_FOUND")

    # Ensure location columns exist
    for col in ("binder_name", "page_number", "slot_number"):
        if col not in merged.columns:
            merged[col] = ""

    # Create index column by concatenating location fields
    merged["index"] = (
        merged["binder_name"].astype(str)
        + "-"
        + merged["page_number"].astype(str)
        + "-"
        + merged["slot_number"].astype(str)
    )

    # If quantity exists, include it
    if "quantity" in merged.columns and "quantity" not in final_cols:
        final_cols.append("quantity")

    # Ensure all final_cols exist
    for col in final_cols:
        if col not in merged.columns:
            merged[col] = pd.NA

    out_df = merged[final_cols].copy()
    out_df.to_csv(output_file, index=False)
    print(f"Wrote portfolio to {output_file}", file=sys.stderr)


def main() -> None:
    update_portfolio("./card_inventory/", "./card_set_lookup/", "card_portfolio.csv")


def test() -> None:
    update_portfolio(
        "./card_inventory_test/", "./card_set_lookup_test/", "test_card_portfolio.csv"
    )


if __name__ == "__main__":
    print("Starting update_portfolio in Test Mode...", file=sys.stderr)
    test()