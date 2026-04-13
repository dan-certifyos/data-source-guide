# Workspace State

- [2026-04-06] STATE: Repo: `https://github.com/dan-certifyos/data-source-guide`. Canonical GCS URLs (requires @certifyos.com login): `https://storage.cloud.google.com/certifyos-monitoring-reports/internal/certifyos-primary-source-reference.{html,pdf}`
- [2026-04-06] STATE: `ws` npm dep is gitignored in `scripts/node_modules/` — run `cd scripts && npm install ws` after a fresh clone before using `gen_pdf.js` or `publish.sh`.
- [2026-04-06] STATE: Chrome 112+ new headless (`--headless`) breaks `Page.printToPDF` via CDP — working flag is `--headless=old`.
- [2026-04-10] STATE: Four sync scripts now exist: `sync_medicaid_index_from_sot.py`, `sync_ba_index_from_sot.py`, `sync_cds_index_from_sot.py`, `sync_state_license_index_from_sot.py`. Each reads an xlsx SOT and patches HTML in place.
