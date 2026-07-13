#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE="$ROOT/resume/latex/chen_sihan_adventurex_resume.tex"
BUILD_DIR="$ROOT/tmp/pdfs/formal-resume"
OUTPUT="$ROOT/output/pdf/陈思翰_AdventureX_正式简历.pdf"

mkdir -p "$BUILD_DIR" "$(dirname "$OUTPUT")"

tectonic -X compile "$SOURCE" --outdir "$BUILD_DIR" --keep-logs
cp "$BUILD_DIR/chen_sihan_adventurex_resume.pdf" "$OUTPUT"

find "$BUILD_DIR" -maxdepth 1 -name 'page-*.png' -delete
pdftoppm -png -r 150 "$OUTPUT" "$BUILD_DIR/page" >/dev/null 2>&1

echo "$OUTPUT"
