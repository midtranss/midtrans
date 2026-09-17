#!/bin/sh
# Every check, in the order that fails cheapest first. Needs a server on :8000
# and, for the browser checks, PW and CHROME if the defaults do not resolve.
set -e
cd "$(dirname "$0")/../.."
python3 tools/audit/gen_tokens_css.py    > /dev/null
python3 tools/audit/gen_theme_package.py > /dev/null
python3 tools/audit/gen_meridian.py      > /dev/null
python3 tools/audit/gen_mounts.py        > /dev/null
fail=0
echo "— source ";    python3 tools/audit/static.py        || fail=1
echo "— totals ";    python3 tools/audit/doc_totals.py    || fail=1
echo "— contracts "; node tools/audit/contract_check.js   || fail=1
echo "— browser ";   node tools/audit/live.js             || fail=1
echo "— skin ";      node tools/audit/meridian_proof.js   || fail=1
echo "— switch ";    node tools/audit/theme_switch.js     || fail=1
exit $fail
