# Memory Inbox

Staged learnings pending pruning. Run `/memory-prune` when this grows to 3+ entries.

Format: `- [YYYY-MM-DD] TYPE: content`
Types: `STATE` | `RULE` | `PATTERN` | `SKILL` | `FEEDBACK` | `DECISION`

- [2026-06-18] DECISION: CDS State Source Index aligned to the 25 DOJ second-license jurisdictions so "collected" matches "required" (25); GU/PR included once source links existed.
- [2026-06-18] RULE: All four SOT index sync scripts (scripts/sync_*_from_sot.py) are now disabled by default — they exit 2 with no changes unless you pass --force or set SOT_SYNC_FORCE=1. Indexes are maintained directly in the HTML; re-syncing can overwrite curated edits (e.g. CDS per-state sources are not all in CDS Research.xlsx).
- [2026-06-18] RULE: StrReplace batch-deleting adjacent full-line table rows with a leading "\n" consumes the shared newline and concatenates rows; prefer one block replace of the whole <tbody>, or re-read between single-line deletions.
- [2026-06-18] RULE: gen_pdf.js output is non-deterministic (byte diffs each run); after scripts/publish.sh, commit the regenerated PDF so git matches the GCS artifact.
- [2026-06-18] STATE: Project skills live at .cursor/skills/<name>/SKILL.md and are not gitignored in this repo (verified via git check-ignore).
- [2026-06-18] SKILL: Added publish-data-source-guide skill (prefers `bash scripts/publish.sh`) for the Edit→PDF→Publish workflow.
