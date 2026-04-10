#!/usr/bin/env python3
"""
Regenerate the State Licensing Authority Index tbody in certifyos-primary-source-reference.html
from 'Credbase Provider Data Sources.xlsx' and patch the HTML file in place.

Usage (from repo root):
  python3 scripts/sync_state_license_index_from_sot.py

Requires: openpyxl
  pip install openpyxl

Default xlsx path: temp-sot-downloads/Credbase Provider Data Sources.xlsx

Columns used (0-indexed) from sheet "Source Log- SOT":
  col 3: state code (2-letter, e.g. "AL")
  col 4: credential code(s) — already short codes, may be newline-separated (e.g. "DDS\nDMD")
  col 6: license verification link (hyperlink via cell.hyperlink.target)
  col 8: board name

URLs: col 6 carries the license verification link as a hyperlink. When the xlsx export does
not preserve formula-computed hyperlinks (which is common for Google Sheets exports), the
script falls back to matching board names against URLs already in the HTML, preserving
existing links for known boards.

After running, follow the Edit → PDF → Publish steps in README.md (run publish.sh).
"""

from __future__ import annotations

import html as html_module
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    from openpyxl import load_workbook
except ImportError:
    print("Install openpyxl: pip install openpyxl", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_XLSX = ROOT / "temp-sot-downloads" / "Credbase Provider Data Sources.xlsx"
HTML_GLOB = "certifyos-primary-source-reference*.html"
SHEET = "Source Log- SOT"

# Canonical ordering for display in idx-sub
CREDENTIAL_ORDER = [
    "MD", "DO", "PA",
    "RN", "APRN", "LPN",
    "PC", "MFT", "CP", "CSW", "ADC",
    "DDS", "DMD",
    "PT",
    "ABA",
]


def _cell_hyperlink(cell) -> str:
    return cell.hyperlink.target if cell.hyperlink else ""


def _extract_html_board_urls(html_path: Path) -> dict[tuple[str, str], str]:
    """Parse the existing HTML to build a (state, board_name) → url lookup.

    Preserves URLs for boards that are already in the HTML, so they survive a
    round-trip even when the xlsx export does not carry formula-computed hyperlinks.
    """
    text = html_path.read_text(encoding="utf-8")
    pattern = (
        r'<span class="idx-state">([A-Z]{2})</span></td>'
        r'<td><span class="idx-source">'
        r'(?:<a href="([^"]+)"[^>]*>)?([^<]+)'
    )
    lookup: dict[tuple[str, str], str] = {}
    for m in re.finditer(pattern, text):
        state = m.group(1)
        url = m.group(2) or ""
        board = html_module.unescape(m.group(3).strip())
        if state and board:
            lookup[(state, board)] = url
    return lookup


def _sort_credentials(creds: list[str]) -> list[str]:
    known = [c for c in CREDENTIAL_ORDER if c in creds]
    unknown = sorted(c for c in creds if c not in CREDENTIAL_ORDER)
    return known + unknown


def load_rows(
    xlsx: Path,
    url_fallback: dict[tuple[str, str], str],
) -> list[tuple[str, str, str, str]]:
    """Return sorted list of (state_code, board_name, url, credential_codes_str).

    Groups by (state_code, board_name), collecting all credential short codes.
    Reads hyperlinks from col 6; falls back to url_fallback for boards already
    known from HTML when the xlsx export does not include formula-resolved links.
    """
    wb = load_workbook(xlsx, data_only=True)
    ws = wb[SHEET]

    groups: dict[tuple[str, str], dict] = defaultdict(lambda: {"credentials": set(), "url": ""})

    for row in ws.iter_rows(min_row=2):
        state_cell = row[3]
        cred_cell = row[4]
        url_cell = row[6]
        board_cell = row[8]

        state = str(state_cell.value).strip() if state_cell.value else None
        if not state or not re.fullmatch(r"[A-Z]{2}", state):
            continue

        board = " ".join(str(board_cell.value).split()) if board_cell.value else ""
        if not board:
            continue

        # col 4 already contains short codes (e.g. "MD", "DDS\nDMD", "RN\nAPRN\nLPN")
        raw_creds = str(cred_cell.value).strip() if cred_cell.value else ""
        for code in raw_creds.splitlines():
            code = code.strip()
            if code:
                groups[(state, board)]["credentials"].add(code)

        # Try hyperlink first, then raw URL value from col 6
        url = _cell_hyperlink(url_cell)
        if not url:
            raw = str(url_cell.value).strip() if url_cell.value else ""
            if raw not in ("", "None", "-", "Link"):
                url = raw

        if url and not groups[(state, board)]["url"]:
            groups[(state, board)]["url"] = url

    rows: list[tuple[str, str, str, str]] = []
    for (state, board), entry in groups.items():
        url = entry["url"] or url_fallback.get((state, board), "")
        creds_str = ", ".join(_sort_credentials(list(entry["credentials"])))
        rows.append((state, board, url, creds_str))

    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


def esc_attr(s: str) -> str:
    return html_module.escape(s, quote=True)


def esc_text(s: str) -> str:
    return html_module.escape(s, quote=False)


def build_cell(state: str, board: str, url: str, creds: str) -> str:
    if url:
        source_html = f'<a href="{esc_attr(url)}" target="_blank">{esc_text(board)}</a>'
    else:
        source_html = esc_text(board)
    sub = f'<br><span class="idx-sub">{esc_text(creds)}</span>' if creds else ""
    return (
        f'<td><span class="idx-state">{esc_text(state)}</span></td>'
        f'<td><span class="idx-source">{source_html}{sub}</span></td>'
    )


def build_tbody_rows(rows: list[tuple[str, str, str, str]]) -> str:
    half = (len(rows) + 1) // 2
    left = rows[:half]
    right = rows[half:]

    while len(right) < len(left):
        right.append(("", "", "", ""))

    table_rows: list[str] = []
    for l, r in zip(left, right):
        left_cells = build_cell(*l) if l[0] else "<td></td><td></td>"
        right_cells = build_cell(*r) if r[0] else "<td></td><td></td>"
        table_rows.append(
            f'<tr>{left_cells}<td class="td-divider"></td>{right_cells}</tr>'
        )
    return "\n".join(table_rows)


def patch_html(html_path: Path, tbody_inner: str, board_count: int) -> None:
    text = html_path.read_text(encoding="utf-8")

    pattern = (
        r"(<!-- STATE LICENSING & BOARD ACTION INDEX -->.*?"
        r'<table class="index-table"[^>]*>\s*'
        r"<thead>.*?</thead>\s*<tbody>\s*)(.*?)(\s*</tbody>\s*</table>\s*"
        r"<!-- CDS SOURCE INDEX -->)"
    )
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        raise SystemExit(
            f"Could not find State Licensing Authority index table block in {html_path}"
        )
    new_text = m.group(1) + tbody_inner + "\n    " + m.group(3)
    text = text[: m.start()] + new_text + text[m.end() :]

    # Update source count in subtitle (e.g. "251 sources across")
    subtitle_pattern = r"\d+ sources across"
    text = re.sub(subtitle_pattern, f"{board_count} sources across", text, count=1)

    html_path.write_text(text, encoding="utf-8")


def main() -> None:
    xlsx = DEFAULT_XLSX
    if not xlsx.is_file():
        print(
            f"Missing {xlsx}; place the SOT export there or edit DEFAULT_XLSX.",
            file=sys.stderr,
        )
        sys.exit(1)

    html_files = sorted(ROOT.glob(HTML_GLOB))
    if not html_files:
        print(f"No {HTML_GLOB} in {ROOT}", file=sys.stderr)
        sys.exit(1)

    # Build URL fallback from the first matching HTML file before patching
    url_fallback = _extract_html_board_urls(html_files[0])

    rows = load_rows(xlsx, url_fallback)
    tbody = build_tbody_rows(rows)

    url_count = sum(1 for _, _, url, _ in rows if url)
    no_url_count = len(rows) - url_count

    for hf in html_files:
        patch_html(hf, tbody, len(rows))
        print(
            f"Patched {hf.name} ({len(rows)} boards, "
            f"{(len(rows) + 1) // 2} table rows, "
            f"{url_count} with URLs, {no_url_count} without)."
        )

    print("\nFirst 5 rows generated:")
    for state, board, url, creds in rows[:5]:
        url_display = url[:60] if url else "(none)"
        print(f"  [{state}] {board[:60]} | url={url_display} | creds={creds}")


if __name__ == "__main__":
    main()
