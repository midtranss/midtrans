#!/usr/bin/env sh
#
# Find every reference to a retired Claude model, and every `-latest` alias.
#
# READ-ONLY. Prints findings; changes nothing. Run it on the server, or anywhere the
# application source lives.
#
#   sh find_retired_models.sh /path/to/app
#
# Why this exists
# ---------------
# An Anthropic notice dated 11 Sep 2026 reported that the API key named
# "MIRA - mira.midtrans.org" was calling claude-3-5-haiku-20241022 via the
# `claude-3-5-haiku-latest` alias. That model was retired on 19 Feb 2026. The call returns
# not_found_error and — per the notice itself — "does not appear on the Usage page".
#
# The alias is the root cause. A pinned model ID turns a retirement into a visible decision;
# an alias turns it into a silent outage that can run for months.

set -u
ROOT="${1:-.}"

EXCLUDE='-path */node_modules/* -o -path */.git/* -o -path */vendor/* -o -path */__pycache__/* -o -path */dist/* -o -path */build/*'

echo "Scanning: $ROOT"
echo "=============================================================="
echo

echo "### 1. Retired / legacy model IDs"
echo "---------------------------------"
find "$ROOT" \( $EXCLUDE \) -prune -o -type f -print 2>/dev/null \
  | xargs grep -Hn -E 'claude-3-5-haiku|claude-3-5-sonnet|claude-3-opus|claude-3-haiku|claude-3-sonnet|claude-2|claude-instant' 2>/dev/null \
  | head -40
echo

echo "### 2. Aliases — the actual root cause"
echo "--------------------------------------"
find "$ROOT" \( $EXCLUDE \) -prune -o -type f -print 2>/dev/null \
  | xargs grep -Hn -E 'claude[a-z0-9.-]*-latest' 2>/dev/null \
  | head -40
echo

echo "### 3. Every model= assignment (review each one)"
echo "------------------------------------------------"
find "$ROOT" \( $EXCLUDE \) -prune -o -type f -print 2>/dev/null \
  | xargs grep -Hn -E '["'\''"]?model["'\''"]?\s*[:=]\s*["'\''"]claude' 2>/dev/null \
  | head -40
echo

echo "### 4. Model names in config and environment files"
echo "--------------------------------------------------"
find "$ROOT" \( $EXCLUDE \) -prune -o \
     \( -name '*.env*' -o -name '*.yml' -o -name '*.yaml' -o -name '*.toml' \
        -o -name '*.ini' -o -name '*.cfg' -o -name 'config*.json' \) -print 2>/dev/null \
  | xargs grep -Hn -i 'claude\|anthropic.*model' 2>/dev/null \
  | grep -vi 'api[_-]\?key\|secret\|token\|password' \
  | head -30
echo

echo "=============================================================="
echo "WHAT TO DO WITH THE OUTPUT"
echo "=============================================================="
cat <<'GUIDE'

  1. Replace every retired ID with the pinned current one:

         claude-3-5-haiku-20241022   ->  claude-haiku-4-5
         claude-3-5-haiku-latest     ->  claude-haiku-4-5

     Use the plain ID. Do not append a date suffix.

  2. Remove every `-latest` alias. Pinning is the fix; updating the alias is not.
     An alias means the next retirement is another silent outage.

  3. Haiku 4.5 notes:
       * context window is 200K
       * if you use extended thinking, it takes {type: "enabled", budget_tokens: N}
       * the newer `adaptive` thinking mode and the `effort` parameter are NOT
         supported on this model and will error

  4. Add alerting on a 404 from the model call. `mira/client.py` already does this —
     a NotFoundError is raised as _ModelNotFound and logged CRITICAL. Wire
     on_api_error to whatever pages a human.

  5. Re-run this script after the change. Sections 1 and 2 should both be empty.

GUIDE
