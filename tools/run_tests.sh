#!/usr/bin/env sh
# Every check outside mira/. No API key, no network, no dependencies.
set -e
cd "$(dirname "$0")/.."
echo "=== freight calculations ==="
python3 tools/calc/tests/test_freight_math.py
echo
echo "=== measurement tables reproduce ==="
python3 tools/measurement/sample_size.py > /dev/null && echo "sample_size.py: ok"
