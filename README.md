# data-source-guide

Published **CertifyOS primary source reference** (HTML/PDF) and pointers to **data source of truth** spreadsheets.

## Contents

- `data-source-of-truth.md` — links to Google Sheet sources of truth by data element.
- `certifyos-primary-source-reference.html` — client-facing reference guide; regenerate PDF from HTML when updated.
- `certifyos-primary-source-reference.pdf` — client-facing PDF; regenerate from HTML after any edits.
- `scripts/sync_state_license_index_from_sot.py` — rebuilds the **State Licensing Authority Index** from `temp-sot-downloads/Credbase Provider Data Sources.xlsx` and patches the HTML in place (no manual paste needed).
- `scripts/sync_ba_index_from_sot.py` — rebuilds the **Board Licensure Action Source Index** directly from `temp-sot-downloads/Board Action Research - SOT.xlsx` and patches the HTML in place (no manual paste needed).
- `scripts/sync_cds_index_from_sot.py` — rebuilds the **CDS State Source Index** from `temp-sot-downloads/CDS Research.xlsx` and patches the HTML in place (no manual paste needed).
- `scripts/sync_medicaid_index_from_sot.py` — rebuilds the **State Medicaid Exclusion Source Index** from `temp-sot-downloads/State Level Exclusions List.xlsx`.
- `scripts/gen_pdf.js` — generates the PDF from the HTML using Chrome DevTools Protocol (no headers/footers).
- `.cursor/skills/publish-data-source-guide/` — Cursor skill for the Edit → PDF → Publish workflow (regenerate PDF, publish HTML + PDF to GCS).

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

> **Sync scripts are disabled by default.** All index sections are now maintained directly in the HTML. The `scripts/sync_*_from_sot.py` scripts refuse to run (exit code 2, no changes) unless you pass `--force` or set `SOT_SYNC_FORCE=1`, because re-syncing from the xlsx can overwrite curated edits. Only force a sync after confirming the relevant xlsx SOT actually reflects the current curated index.

### Board Licensure Action index

Export the Board Action Research sheet to `temp-sot-downloads/Board Action Research - SOT.xlsx`, then (only if you intend to rebuild from the xlsx):

```bash
python3 scripts/sync_ba_index_from_sot.py --force
```

The script reads the board action research spreadsheet, filters out boards with no accessible disciplinary action data, deduplicates, sorts by state then board name, and patches the HTML directly. After running, follow the Edit → PDF → Publish steps above.

### CDS State Source Index

> **Manually curated — do not blindly re-sync.** The CDS State Source Index is hand-maintained to match the 25 DOJ second-license jurisdictions (`pract-state-lic-require.html`), with per-state source links that are **not** all present in `CDS Research.xlsx`. Re-running the sync script would overwrite that work, so it is **guarded**: it exits without changes unless you pass `--force` (or set `SOT_SYNC_FORCE=1`). Prefer editing the HTML directly; only force the sync after confirming the xlsx SOT actually reflects the curated 25-state list.

Export the [CDS Research](https://docs.google.com/spreadsheets/d/...) sheet to `temp-sot-downloads/CDS Research.xlsx`, then (only if you intend to rebuild from the xlsx):

```bash
python3 scripts/sync_cds_index_from_sot.py --force
```

The script reads three sheets (NurseOS, DentOS, MedOS), filters to rows where DataOps is actively collecting, deduplicates by `(state, board)` pair, and patches the HTML directly. Five states with no xlsx rows (AL, DC, MI, NJ, OK) are preserved as no-URL fallback entries. After running, follow the Edit → PDF → Publish steps above.

### State Licensing Authority index

Export the [Credbase Provider Data Sources](https://docs.google.com/spreadsheets/d/1Fs87fkrnFdnEtPsEVrrjpt1bQrAWFL7xF8KcUQs4izA/edit) sheet to `temp-sot-downloads/Credbase Provider Data Sources.xlsx`, then (only if you intend to rebuild from the xlsx):

```bash
python3 scripts/sync_state_license_index_from_sot.py --force
```

The script reads the 6 per-OS detail sheets (MedOS, MentOS, DentOS, NurseOS, PT, ABA), groups rows by (state, board), collects credential short codes per board, resolves license verification URLs from cell hyperlinks, sorts by state then board name, and patches the HTML directly — no manual paste needed. After running, follow the Edit → PDF → Publish steps above.

### State Medicaid Exclusion index

Export the [State Medicaid Exclusions & Sanctions](https://docs.google.com/spreadsheets/d/13F4QNq_a9-Rg8-Q-3ACHYftzUE0LgJbESjTGFJqBZ-k/edit) sheet to `temp-sot-downloads/State Level Exclusions List.xlsx`, then (only if you intend to rebuild from the xlsx):

```bash
python3 scripts/sync_medicaid_index_from_sot.py --force
```

The script classifies each U.S. state and DC: rows whose LINK column points at the generic HHS OIG LEIE download appear in the footnote; all others get a row in the alphabetical index with label and URL from the sheet. After running, follow the Edit → PDF → Publish steps above.

## Rules

1. **No internal links in the HTML or PDF.** This is a client-facing document. Do not link to internal Google Sheets, Confluence pages, Jira tickets, or any other internal tooling. Reference data sources by name only.
2. **Every HTML edit must be followed by PDF regen and GCS publish.** Run `bash scripts/publish.sh` after any change to the HTML. Never commit or share an HTML update without also updating the PDF and GCS.

## Version History

The published reference guide carries a version label in its header (e.g. `CertifyOS · 2026 · v2`). Each published revision is tracked below.

- **v1** — Initial published Primary Source Reference Guide (full source index across Provider Identity, Licensure, Board Certification, Sanctions & Exclusions, and Medicare Participation Status).
- **v2 (2026-06-16)** — CDS updates: removed the DEA-registrant-file CDS row (state-source CDS row retained); removed internal Google Sheet links from the State Medicaid Exclusions row and unwrapped a `google.com/url` redirect in the State Licensing index; added external CDS source links in the CDS State Source Index (DC, MI, NJ, OK, RI); added the second-license jurisdiction list with the DOJ source link to the CDS source overview row.

## License

Internal reference material; confirm with CertifyOS before redistributing.
