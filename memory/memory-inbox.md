# Memory Inbox

Staged learnings pending pruning. Run `/memory-prune` when this grows to 3+ entries.

Format: `- [YYYY-MM-DD] TYPE: content`
Types: `STATE` | `RULE` | `PATTERN` | `SKILL` | `FEEDBACK` | `DECISION`

- [2026-04-06] STATE: Repo: `https://github.com/dan-certifyos/data-source-guide`. Canonical GCS URLs (requires @certifyos.com login): `https://storage.cloud.google.com/certifyos-monitoring-reports/internal/certifyos-primary-source-reference.{html,pdf}`
- [2026-04-06] RULE: GCS `storage.googleapis.com` bypasses IAM entirely — always use `storage.cloud.google.com` for domain-restricted authenticated objects.
- [2026-04-06] RULE: Every HTML edit must be followed by `bash scripts/publish.sh` — never commit HTML without also updating the PDF and GCS.
- [2026-04-06] RULE: No internal links (GSheets, Confluence, Jira) in the HTML or PDF — this is a client-facing document.
- [2026-04-06] STATE: `ws` npm dep is gitignored in `scripts/node_modules/` — run `cd scripts && npm install ws` after a fresh clone before using `gen_pdf.js` or `publish.sh`.
- [2026-04-06] RULE: Use `openpyxl` (not `pandas`) when xlsx hyperlinks matter — pandas silently drops them and reads only display text.
- [2026-04-06] STATE: Chrome 112+ new headless (`--headless`) breaks `Page.printToPDF` via CDP — working flag is `--headless=old`.
- [2026-04-10] STATE: Four sync scripts now exist: `sync_medicaid_index_from_sot.py`, `sync_ba_index_from_sot.py`, `sync_cds_index_from_sot.py`, `sync_state_license_index_from_sot.py`. Each reads an xlsx SOT and patches HTML in place.
- [2026-04-10] RULE: Google Sheets XLOOKUP formulas lose hyperlink objects on xlsx export — always read from per-OS detail sheets (MedOS, MentOS, DentOS, NurseOS, PT, ABA) instead of the "Source Log- SOT" summary sheet when URLs are needed.
- [2026-04-10] RULE: NurseOS sheet in `Credbase Provider Data Sources.xlsx` has a different column layout from the other 5 sheets — License Verification Link is col 18 (not 13), board name is col 20 (not 15).
- [2026-04-10] PATTERN: Parallel subagents on separate branches work for independent HTML table sections. Rebase the second branch after the first merges to resolve README conflicts cleanly.
