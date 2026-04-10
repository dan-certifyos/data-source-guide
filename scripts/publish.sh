#!/usr/bin/env bash
# Regenerate PDF and publish HTML + PDF to GCS.
# Run from the repo root: bash scripts/publish.sh
set -euo pipefail

BASE="certifyos-primary-source-reference"
DATE=$(date +%Y-%m-%d)
BUCKET="gs://certifyos-monitoring-reports/internal"

echo "==> Generating PDF..."
node scripts/gen_pdf.js

echo "==> Uploading to GCS..."
gsutil cp "${BASE}.html" "${BUCKET}/${BASE}.html"
gsutil cp "${BASE}.pdf"  "${BUCKET}/${BASE}.pdf"
gsutil cp "${BASE}.html" "${BUCKET}/${BASE}-${DATE}.html"
gsutil cp "${BASE}.pdf"  "${BUCKET}/${BASE}-${DATE}.pdf"

echo "==> Setting metadata..."
gsutil setmeta -h "Content-Type:text/html"       -h "Cache-Control:no-cache" "${BUCKET}/${BASE}.html"
gsutil setmeta -h "Content-Type:application/pdf" -h "Cache-Control:no-cache" "${BUCKET}/${BASE}.pdf"

echo ""
echo "Done. Published canonical + archive ${BASE}-${DATE}."
echo ""
echo "  HTML: https://storage.cloud.google.com/certifyos-monitoring-reports/internal/${BASE}.html"
echo "  PDF:  https://storage.cloud.google.com/certifyos-monitoring-reports/internal/${BASE}.pdf"
