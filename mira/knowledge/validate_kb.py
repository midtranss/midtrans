"""
Knowledge-base validator.

Enforces the sourcing rule in docs/standards/MIRA-GUARDRAILS.md §5 mechanically, so it cannot
be forgotten under deadline pressure:

  * every entry carries source, owner, reviewed_at, expires_at
  * an entry without a named owner is rejected — an unowned fact is an unmaintained fact
  * a `draft` entry can never be served
  * an expired entry can never be served
  * no entry contains a rate, transit time or cost, even in its internal notes

Run:  python3 mira/knowledge/validate_kb.py
Exit: 0 if the base is safe to load, 1 otherwise.

`servable_entries()` is what the application should call — it returns only entries that pass
every check. Loading the YAML directly bypasses the rule.
"""

from __future__ import annotations

import datetime as _dt
import re
import sys
from pathlib import Path

KB_PATH = Path(__file__).parent / "kb-seed.yaml"

REQUIRED = ("source", "owner", "reviewed_at", "expires_at", "status")

# Values that must never appear in an entry, including in internal fields.
_FORBIDDEN = [
    (re.compile(r"\b\d[\d,.]*\s*(?:usd|aed|eur|dollar|درهم|دولار)\b", re.I), "currency amount"),
    (re.compile(r"\b(?:usd|aed|eur)\s*\d", re.I), "currency amount"),
    (re.compile(r"[$€£]\s*\d"), "currency amount"),
    (re.compile(r"\b\d+\s*(?:days?|weeks?|يوم|أيام|أسابيع)\b.{0,40}(?:transit|delivery|مدة|وصول)",
                re.I | re.S), "transit time"),
    (re.compile(r"(?:transit|delivery|مدة|وصول).{0,40}\b\d+\s*(?:days?|weeks?|يوم|أيام)\b",
                re.I | re.S), "transit time"),
]


def _load() -> list[dict]:
    """Minimal YAML reader for this file's shape — avoids a dependency for a 10-entry file."""
    try:
        import yaml  # type: ignore
    except ImportError:
        return _load_fallback()
    data = yaml.safe_load(KB_PATH.read_text(encoding="utf-8"))
    return data.get("entries", []) or []


def _load_fallback() -> list[dict]:
    """Structural parse sufficient for validation when PyYAML is absent."""
    text = KB_PATH.read_text(encoding="utf-8")
    blocks = re.split(r"\n  - id: ", text)[1:]
    entries = []
    for block in blocks:
        entry = {"id": block.split("\n", 1)[0].strip(), "_raw": block}
        for key in REQUIRED:
            m = re.search(rf"^    {key}:\s*(.*)$", block, re.M)
            val = m.group(1).strip() if m else None
            entry[key] = None if val in (None, "null", "") else val.strip('"\'')
        entries.append(entry)
    return entries


def _raw(entry: dict) -> str:
    return entry.get("_raw") or str(entry)


def _expired(entry: dict) -> bool:
    val = entry.get("expires_at")
    if not val:
        return False
    try:
        return _dt.date.fromisoformat(str(val)[:10]) < _dt.date.today()
    except ValueError:
        return True  # an unparseable date is not a valid expiry


def validate(entries: list[dict]) -> tuple[list[str], list[str]]:
    """Return (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()

    for e in entries:
        eid = e.get("id", "<no id>")

        if eid in seen:
            errors.append(f"{eid}: duplicate id")
        seen.add(eid)

        for key in REQUIRED:
            if key not in e:
                errors.append(f"{eid}: missing field `{key}`")

        status = e.get("status")
        if status not in ("draft", "approved", "retired"):
            errors.append(f"{eid}: status must be draft|approved|retired, got {status!r}")

        if status == "approved":
            if not e.get("owner"):
                errors.append(f"{eid}: approved with no owner — an unowned fact is unmaintained")
            if not e.get("reviewed_at"):
                errors.append(f"{eid}: approved with no reviewed_at")
            if not e.get("expires_at"):
                errors.append(f"{eid}: approved with no expires_at")
            if _expired(e):
                errors.append(f"{eid}: approved but expired on {e.get('expires_at')}")
            src = str(e.get("source") or "")
            if not src or src.upper().startswith(("TO BE", "REQUIRED")):
                errors.append(f"{eid}: approved with an unresolved source")
        elif status == "draft":
            warnings.append(f"{eid}: draft — will not be served")

        for pattern, label in _FORBIDDEN:
            if pattern.search(_raw(e)):
                errors.append(f"{eid}: contains a {label} — forbidden by GUARDRAILS §2")

    return errors, warnings


def servable_entries() -> list[dict]:
    """Only entries safe to serve. The application must use this, not the raw YAML."""
    entries = _load()
    errors, _ = validate(entries)
    bad = {err.split(":")[0] for err in errors}
    return [
        e for e in entries
        if e.get("status") == "approved"
        and e.get("id") not in bad
        and not _expired(e)
    ]


def main() -> int:
    entries = _load()
    errors, warnings = validate(entries)
    servable = servable_entries()

    print(f"Knowledge base: {len(entries)} entries")
    print(f"  errors:   {len(errors)}")
    print(f"  drafts:   {len(warnings)}")
    print(f"  servable: {len(servable)}")

    if errors:
        print("\nERRORS — these entries must not load:\n")
        for err in errors:
            print(f"  ✗ {err}")

    if warnings:
        print("\nDRAFTS — not served until an owner approves them:\n")
        for warn in warnings:
            print(f"  · {warn}")

    if not servable:
        print(
            "\nNothing is servable yet. That is the correct state for a freshly seeded base: "
            "\nevery entry needs MIDTRANS operations to confirm the answer and take ownership."
        )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
