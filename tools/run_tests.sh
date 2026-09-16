#!/usr/bin/env sh
# Every check outside mira/. No API key, no network, no dependencies.
set -e
cd "$(dirname "$0")/.."
echo "=== freight calculations ==="
python3 tools/calc/tests/test_freight_math.py
echo
echo "=== content gate ==="
python3 tools/content/tests/test_check_page.py
echo
echo "=== cluster duplication ==="
python3 tools/content/tests/test_check_cluster.py
echo
echo "=== measurement tables reproduce ==="
python3 tools/measurement/sample_size.py > /dev/null && echo "sample_size.py: ok"
