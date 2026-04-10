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
