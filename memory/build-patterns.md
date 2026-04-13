# Build Patterns

- [2026-04-06] RULE: GCS `storage.googleapis.com` bypasses IAM entirely — always use `storage.cloud.google.com` for domain-restricted authenticated objects.
- [2026-04-06] RULE: Every HTML edit must be followed by `bash scripts/publish.sh` — never commit HTML without also updating the PDF and GCS.
- [2026-04-06] RULE: No internal links (GSheets, Confluence, Jira) in the HTML or PDF — this is a client-facing document.
- [2026-04-06] RULE: Use `openpyxl` (not `pandas`) when xlsx hyperlinks matter — pandas silently drops them and reads only display text.
- [2026-04-10] RULE: Google Sheets XLOOKUP formulas lose hyperlink objects on xlsx export — always read from per-OS detail sheets (MedOS, MentOS, DentOS, NurseOS, PT, ABA) instead of the "Source Log- SOT" summary sheet when URLs are needed.
- [2026-04-10] RULE: NurseOS sheet in `Credbase Provider Data Sources.xlsx` has a different column layout from the other 5 sheets — License Verification Link is col 18 (not 13), board name is col 20 (not 15).
- [2026-04-10] PATTERN: Parallel subagents on separate branches work for independent HTML table sections. Rebase the second branch after the first merges to resolve README conflicts cleanly.
