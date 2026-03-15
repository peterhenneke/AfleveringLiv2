#!/usr/bin/env bash
# Compile main.tex to PDF
# Run with: bash scripts/compile.sh

set -e

cd "$(dirname "$0")/.."

echo "==> First pass..."
pdflatex -interaction=nonstopmode main.tex

echo "==> Second pass (resolves TOC & references)..."
pdflatex -interaction=nonstopmode main.tex

echo "==> Cleaning auxiliary files..."
rm -f main.aux main.log main.toc main.out texput.log

echo "==> Done! Output: main.pdf"
