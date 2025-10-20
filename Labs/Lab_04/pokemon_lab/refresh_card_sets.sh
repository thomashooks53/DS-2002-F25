#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

echo "Refreshing all card sets in card_set_lookup/"

for FILE in card_set_lookup/*.json; do
    SET_ID=$(basename "$FILE" .json)
    echo "Updating set '$SET_ID'..."
    URL="https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}&pageSize=250"
    if ! curl -sS --fail "$URL" -o "$FILE"; then
        echo "Error: Failed to refresh set '$SET_ID' (file: $FILE)." >&2
    else
        echo "Wrote updated data to '$FILE'"
    fi
done

echo "All card sets have been refreshed."
