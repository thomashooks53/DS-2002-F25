#!/usr/bin/env python3
import os
import sys
import pandas as pd


def generate_summary(portfolio_file: str) -> None:
    if not os.path.exists(portfolio_file):
        print(f"Error: Portfolio file '{portfolio_file}' not found.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(portfolio_file)
    if df.empty:
        print("Portfolio file is empty; no data to summarize.")
        return

    if "card_market_value" not in df.columns:
        df["card_market_value"] = 0.0

    df["card_market_value"] = pd.to_numeric(df["card_market_value"], errors="coerce").fillna(0.0)

    total_portfolio_value = df["card_market_value"].sum()

    # Guard: if all values are zero, idxmax still works; ensure at least one row exists
    most_idx = df["card_market_value"].idxmax()
    most_valuable_card = df.loc[most_idx]

    card_name = most_valuable_card.get("card_name", "<UNKNOWN>")
    card_id = most_valuable_card.get("card_id", "<UNKNOWN>")
    card_value = float(most_valuable_card.get("card_market_value", 0.0))

    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print("Most Valuable Card:")
    print(f"  Name:  {card_name}")
    print(f"  ID:    {card_id}")
    print(f"  Value: ${card_value:,.2f}")


def main() -> None:
    generate_summary("card_portfolio.csv")


def test() -> None:
    generate_summary("test_card_portfolio.csv")


if __name__ == "__main__":
    print("Starting generate_summary in Test Mode...", file=sys.stderr)
    test()
