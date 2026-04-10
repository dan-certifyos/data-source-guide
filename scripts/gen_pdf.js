#!/usr/bin/env node
/**
 * Generate a PDF from the primary source reference HTML using Chrome's
 * built-in --print-to-pdf CLI flag (no extra deps needed).
 *
 * Run from the repo root: node scripts/gen_pdf.js
 * Requires: Google Chrome at /Applications/Google Chrome.app/
 */

const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const HTML_GLOB = fs
  .readdirSync(ROOT)
  .filter((f) => f.match(/^certifyos-primary-source-reference.*\.html$/))
  .sort()
  .pop();

if (!HTML_GLOB) {
  console.error("No certifyos-primary-source-reference-*.html found in repo root.");
  process.exit(1);
}

const HTML_PATH = path.join(ROOT, HTML_GLOB);
const PDF_PATH = HTML_PATH.replace(/\.html$/, ".pdf");
const HTML_URL = `file://${HTML_PATH}`;
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

console.log(`Source : ${HTML_GLOB}`);
console.log(`Output : ${path.basename(PDF_PATH)}`);

const result = spawnSync(
  CHROME,
  [
    "--headless=old",
    "--no-sandbox",
    "--disable-gpu",
    `--print-to-pdf=${PDF_PATH}`,
    "--no-pdf-header-footer",
    "--print-to-pdf-no-header",
    HTML_URL,
  ],
  { stdio: "inherit" }
);

if (result.status !== 0) {
  console.error(`Chrome exited with status ${result.status}`);
  process.exit(result.status || 1);
}

const size = fs.statSync(PDF_PATH).size;
console.log(`PDF written: ${PDF_PATH} (${(size / 1024).toFixed(0)} KB)`);
