#!/usr/bin/env python3
"""
Generate the Board Licensure Action Source Index HTML table rows
from 'Board Action Research - SOT.xlsx' and write them to a temp file
for injection into certifyos-primary-source-reference-*.html.

Usage (from repo root):
  python3 scripts/gen_ba_index.py

Input:  temp-sot-downloads/Board Action Research - SOT.xlsx
Output: temp-sot-downloads/board_rows.html  (tbody fragment only)

After running, follow the Edit → PDF → Publish steps in README.md.

Requires: openpyxl
  pip install openpyxl
"""

import html
import sys
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("Install openpyxl: pip install openpyxl", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
EXCEL = ROOT / "temp-sot-downloads" / "Board Action Research - SOT.xlsx"
OUT = ROOT / "temp-sot-downloads" / "board_rows.html"
SHEET = "Board Action- Research"

PROCUREMENT_MAP = {
    "free": "Download",
    "view-only access; downloads not supported": "Scraper",
    "look up available": "Lookup",
    "not available": "Not available",
    "outreach": "Outreach required",
}


def map_access(proc: str) -> str:
    if not proc:
        return ""
    key = proc.strip().lower()
    for k, v in PROCUREMENT_MAP.items():
        if key.startswith(k):
            return v
    return proc.strip()


def cell_html(state: str, board: str, url: str, access: str) -> str:
    esc_board = html.escape(board)
    if url:
        esc_url = html.escape(url)
        source_html = f'<a href="{esc_url}" target="_blank">{esc_board}</a>'
    else:
        source_html = esc_board
    sub = f'<span class="idx-sub">{html.escape(access)}</span>' if access else ""
    return (
        f'<td><span class="idx-state">{html.escape(state)}</span></td>'
        f'<td><span class="idx-source">{source_html}{sub}</span></td>'
    )


def main() -> None:
    if not EXCEL.is_file():
        print(
            f"Missing {EXCEL}; place the SOT export there or edit EXCEL path.",
            file=sys.stderr,
        )
        sys.exit(1)

    wb = openpyxl.load_workbook(EXCEL, data_only=True)
    ws = wb[SHEET]

    rows = []
    seen: set[tuple[str, str]] = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        state = str(row[0]).strip() if row[0] else None
        if not state or state in ("None", "#N/A") or state.startswith("#"):
            continue
        board = " ".join(str(row[2]).split()) if row[2] else ""
        proc = str(row[3]).strip() if row[3] else ""
        scrapable = str(row[4]).strip() if row[4] else ""
        url = str(row[12]).strip() if row[12] else ""

        if proc.lower().startswith("not available") or scrapable == "Not Scrapable":
            continue

        key = (state, board)
        if key in seen:
            continue
        seen.add(key)

        if url in ("-", "None", ""):
            url = ""

        rows.append((state, board, url, ""))

    rows.sort(key=lambda r: (r[0], r[1]))

    half = (len(rows) + 1) // 2
    left = rows[:half]
    right = rows[half:]

    while len(right) < len(left):
        right.append(("", "", "", ""))

    table_rows = []
    for l, r in zip(left, right):
        left_cells = cell_html(*l) if l[0] else "<td></td><td></td>"
        right_cells = cell_html(*r) if r[0] else "<td></td><td></td>"
        table_rows.append(
            f"<tr>{left_cells}<td class=\"td-divider\"></td>{right_cells}</tr>"
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(table_rows), encoding="utf-8")

    print(f"Written {len(rows)} boards ({len(table_rows)} table rows) to {OUT.name}")
    print("First 3 rows:")
    for r in table_rows[:3]:
        print(" ", r[:120])


if __name__ == "__main__":
    main()
