#!/usr/bin/env bash
set -euo pipefail

read -r -p "TCG Card Set ID (e.g., base1, base4): " SET_ID

if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi

echo "Fetching cards for set '$SET_ID'..."

URL="https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}&pageSize=250"

if ! curl -sS "$URL" -o "card_set_lookup/${SET_ID}.json"; then
    echo "Error: Failed to fetch data for set '$SET_ID'." >&2
    exit 1
fi

echo "Saved card data to card_set_lookup/${SET_ID}.json"