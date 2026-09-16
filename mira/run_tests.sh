#!/usr/bin/env sh
# Run every MIRA guardrail check. No API key, no network, no dependencies.
set -e
cd "$(dirname "$0")/.."
echo "=== guardrail rules ==="
python3 mira/tests/test_guardrails.py
echo
echo "=== client wiring ==="
python3 mira/tests/test_client.py
