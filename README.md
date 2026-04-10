# data-source-guide

Published **CertifyOS primary source reference** (HTML/PDF) and pointers to **data source of truth** spreadsheets.

## Contents

- `data-source-of-truth.md` — links to Google Sheet sources of truth by data element.
- `certifyos-primary-source-reference.html` — client-facing reference guide; regenerate PDF from HTML when updated.
- `certifyos-primary-source-reference.pdf` — client-facing PDF; regenerate from HTML after any edits.
- `scripts/sync_ba_index_from_sot.py` — rebuilds the **Board Licensure Action Source Index** directly from `temp-sot-downloads/Board Action Research - SOT.xlsx` and patches the HTML in place (no manual paste needed).
- `scripts/sync_cds_index_from_sot.py` — rebuilds the **CDS State Source Index** from `temp-sot-downloads/CDS Research.xlsx` and patches the HTML in place (no manual paste needed).
- `scripts/gen_ba_index.py` — legacy: same source, but writes a fragment to `temp-sot-downloads/board_rows.html` for manual inspection.
- `scripts/sync_medicaid_index_from_sot.py` — rebuilds the **State Medicaid Exclusion Source Index** from `temp-sot-downloads/State Level Exclusions List.xlsx`.
- `scripts/gen_pdf.js` — generates the PDF from the HTML using Chrome DevTools Protocol (no headers/footers).

## Prerequisites

**System (one-time):**
- Python 3.10+
- Node.js
- [Google Chrome](https://www.google.com/chrome/) installed at `/Applications/Google Chrome.app/` (macOS)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) authenticated with a `@certifyos.com` account

**Install Python deps:**
```bash
pip install -r requirements.txt
```

**Install Node dep for PDF generation** (run once from this folder):
```bash
cd scripts && npm install ws
```

**GCS access:** requires `Storage Object Admin` role on `gs://certifyos-monitoring-reports/`. Files are restricted to `@certifyos.com` accounts.

## Edit → PDF → Publish

After editing the HTML:

```bash
# 1. Regenerate PDF
node scripts/gen_pdf.js

# 2. Push to GCS (canonical stable URL + dated archive)
DATE=$(date +%Y-%m-%d)
BASE="certifyos-primary-source-reference"

gsutil cp ${BASE}.html gs://certifyos-monitoring-reports/internal/${BASE}.html
gsutil cp ${BASE}.pdf  gs://certifyos-monitoring-reports/internal/${BASE}.pdf
gsutil cp ${BASE}.html gs://certifyos-monitoring-reports/internal/${BASE}-${DATE}.html
gsutil cp ${BASE}.pdf  gs://certifyos-monitoring-reports/internal/${BASE}-${DATE}.pdf

gsutil setmeta \
  -h "Content-Type:text/html" -h "Cache-Control:no-cache" \
  gs://certifyos-monitoring-reports/internal/${BASE}.html
gsutil setmeta \
  -h "Content-Type:application/pdf" -h "Cache-Control:no-cache" \
  gs://certifyos-monitoring-reports/internal/${BASE}.pdf
```

**Public URLs** (requires `@certifyos.com` login):
- HTML: `https://storage.cloud.google.com/certifyos-monitoring-reports/internal/certifyos-primary-source-reference.html`
- PDF: `https://storage.cloud.google.com/certifyos-monitoring-reports/internal/certifyos-primary-source-reference.pdf`

> Dated archive copies (e.g. `certifyos-primary-source-reference-2026-04-06.*`) are preserved in GCS as version snapshots. Old links continue to serve the version that was current at the time of that publish.

## Rebuild index sections from SOT

### Board Licensure Action index

Export the Board Action Research sheet to `temp-sot-downloads/Board Action Research - SOT.xlsx`, then:

```bash
python3 scripts/sync_ba_index_from_sot.py
```

The script reads the board action research spreadsheet, filters out boards with no accessible disciplinary action data, deduplicates, sorts by state then board name, and patches the HTML directly — no manual paste needed. After running, follow the Edit → PDF → Publish steps above.

### CDS State Source Index

Export the [CDS Research](https://docs.google.com/spreadsheets/d/...) sheet to `temp-sot-downloads/CDS Research.xlsx`, then:

```bash
python3 scripts/sync_cds_index_from_sot.py
```

The script reads three sheets (NurseOS, DentOS, MedOS), filters to rows where DataOps is actively collecting, deduplicates by `(state, board)` pair, and patches the HTML directly — no manual paste needed. Five states with no xlsx rows (AL, DC, MI, NJ, OK) are preserved as no-URL fallback entries. After running, follow the Edit → PDF → Publish steps above.

### State Medicaid Exclusion index

Export the [State Medicaid Exclusions & Sanctions](https://docs.google.com/spreadsheets/d/13F4QNq_a9-Rg8-Q-3ACHYftzUE0LgJbESjTGFJqBZ-k/edit) sheet to `temp-sot-downloads/State Level Exclusions List.xlsx`, then:

```bash
python3 scripts/sync_medicaid_index_from_sot.py
```

The script classifies each U.S. state and DC: rows whose LINK column points at the generic HHS OIG LEIE download appear in the footnote; all others get a row in the alphabetical index with label and URL from the sheet. After running, follow the Edit → PDF → Publish steps above.

## Rules

1. **No internal links in the HTML or PDF.** This is a client-facing document. Do not link to internal Google Sheets, Confluence pages, Jira tickets, or any other internal tooling. Reference data sources by name only.
2. **Every HTML edit must be followed by PDF regen and GCS publish.** Run `bash scripts/publish.sh` after any change to the HTML. Never commit or share an HTML update without also updating the PDF and GCS.

## License

Internal reference material; confirm with CertifyOS before redistributing.
