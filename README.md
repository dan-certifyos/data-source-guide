# data-source-guide

Published **CertifyOS primary source reference** (HTML/PDF) and pointers to **data source of truth** spreadsheets.

## Contents

- `data-source-of-truth.md` — links to Google Sheet sources of truth by data element.
- `certifyos-primary-source-reference-*.html` — static reference; regenerate PDF from HTML if needed.
- `scripts/sync_medicaid_index_from_sot.py` — rebuilds the **State Medicaid Exclusion Source Index** from `temp-sot-downloads/State Level Exclusions List.xlsx` (export from the [State Medicaid Exclusions & Sanctions](https://docs.google.com/spreadsheets/d/13F4QNq_a9-Rg8-Q-3ACHYftzUE0LgJbESjTGFJqBZ-k/edit) sheet).

## Regenerate Medicaid index from SOT

Place the Excel export at `temp-sot-downloads/State Level Exclusions List.xlsx`, then:

```bash
pip install -r requirements.txt
python3 scripts/sync_medicaid_index_from_sot.py
```

The script classifies each U.S. state and DC: rows whose LINK column points at the generic HHS OIG LEIE download appear in the footnote; all others get a row in the alphabetical index with label and URL from the sheet.

## License

Internal reference material; confirm with CertifyOS before redistributing.
