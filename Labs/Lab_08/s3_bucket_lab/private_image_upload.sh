#!/bin/bash

set -e

FILE=$1
BUCKET=$2
EXPIRATION=$3

if [ $# -ne 3 ]; then
  echo "Usage: $0 <local_file> <bucket_name> <expiration_in_seconds>" >&2
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "Error: File '$FILE' not found!" >&2
  exit 1
fi

aws s3 cp "$FILE" "s3://$BUCKET/" >/dev/null

URL=$(aws s3 presign "s3://$BUCKET/$(basename "$FILE")" --expires-in "$EXPIRATION")

echo "Presigned URL:"
echo "$URL"
