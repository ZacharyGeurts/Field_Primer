#!/bin/bash
# Build Field Technology v4 website
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/generate-textbook-images.py
python3 scripts/generate-v4-covers.py
python3 scripts/fetch-creditor-portraits.py
python3 scripts/build-creditor-pages.py
python3 scripts/build-chapters.py
python3 scripts/build-index.py
echo "v4 site built"