---
name: publish-data-source-guide
description: Regenerate the PDF and publish the CertifyOS primary source reference (HTML + PDF) to GCS following the repo's Edit → PDF → Publish workflow. Use after editing certifyos-primary-source-reference.html, or when the user asks to publish, ship, or push the data source guide / primary source reference.
---

# Publish the Data Source Guide

Edit → PDF → Publish workflow for `certifyos-primary-source-reference.html`. Every HTML edit must be followed by a PDF regen and a GCS publish — never ship an HTML change without updating the PDF and GCS.

## Rules (must hold before publishing)

1. **No internal links in the HTML or PDF.** This is a client-facing document. Do not link to internal Google Sheets, Confluence, Jira, or other internal tooling — reference sources by name only.
2. **PDF must match the HTML.** Always regenerate the PDF from the current HTML before publishing.

## Prerequisites

- Node.js, and Chrome installed at `/Applications/Google Chrome.app/` (macOS).
- Node PDF dep installed once: `cd scripts && npm install ws`
- Google Cloud SDK authenticated with a `@certifyos.com` account, with `Storage Object Admin` on `gs://certifyos-monitoring-reports/`.

## Workflow

Run from the repo root.

```
- [ ] 1. Confirm the Rules above hold for the current HTML
- [ ] 2. Regenerate the PDF
- [ ] 3. Publish HTML + PDF to GCS (canonical + dated archive)
- [ ] 4. Verify the public URLs
```

### Preferred: one command

```bash
bash scripts/publish.sh
```

This regenerates the PDF (`node scripts/gen_pdf.js`), uploads the canonical and dated-archive HTML + PDF to `gs://certifyos-monitoring-reports/internal/`, and sets `Content-Type` / `Cache-Control:no-cache` metadata.

### Manual fallback

If `publish.sh` is unavailable, run the equivalent steps:

```bash
node scripts/gen_pdf.js

DATE=$(date +%Y-%m-%d)
BASE="certifyos-primary-source-reference"
BUCKET="gs://certifyos-monitoring-reports/internal"

gsutil cp ${BASE}.html ${BUCKET}/${BASE}.html
gsutil cp ${BASE}.pdf  ${BUCKET}/${BASE}.pdf
gsutil cp ${BASE}.html ${BUCKET}/${BASE}-${DATE}.html
gsutil cp ${BASE}.pdf  ${BUCKET}/${BASE}-${DATE}.pdf

gsutil setmeta -h "Content-Type:text/html"      -h "Cache-Control:no-cache" ${BUCKET}/${BASE}.html
gsutil setmeta -h "Content-Type:application/pdf" -h "Cache-Control:no-cache" ${BUCKET}/${BASE}.pdf
```

The canonical files serve the latest version; the `-${DATE}` copies are immutable version snapshots, so old links keep serving the version current at that publish.

## Verify

Public URLs (require `@certifyos.com` login):

- HTML: `https://storage.cloud.google.com/certifyos-monitoring-reports/internal/certifyos-primary-source-reference.html`
- PDF: `https://storage.cloud.google.com/certifyos-monitoring-reports/internal/certifyos-primary-source-reference.pdf`

## Notes

- When the HTML edit is a published revision, bump the version label in the header (e.g. `CertifyOS · 2026 · v2`) and add an entry to the **Version History** section of `README.md`.
- Index sections (CDS, State Licensing, Board Action, Medicaid) are regenerated from SOT via the `scripts/sync_*_from_sot.py` scripts; after running any of them, follow this same Edit → PDF → Publish workflow.
