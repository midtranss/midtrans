#!/usr/bin/env python3
"""
Run the MIRA guardrail check over exported conversation logs.

This answers the highest-priority open question in the programme mechanically rather than by
reading transcripts by hand: **has the live MIRA already stated a rate, transit time, customs
cost, acceptance or capacity?**

    python3 mira/audit_logs.py export.jsonl
    python3 mira/audit_logs.py export.json --json findings.json
    python3 mira/audit_logs.py export.csv --role-field sender --text-field body

Runs entirely locally. Nothing is uploaded, and no network call is made. The input is customer
conversation data, so treat the output as sensitive too: excerpts are redacted for emails and
phone numbers by default, and full message bodies are never printed.

Exit status is 1 when any message would have been blocked, so this can gate a pipeline.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import guardrails  # noqa: E402


# --------------------------------------------------------------------------------------
# Reading exports whose shape we do not control
# --------------------------------------------------------------------------------------

# An export written by someone else will not use our field names. Guess, and let the caller
# override when the guess is wrong — a wrong guess that silently scans nothing is the failure
# mode worth engineering against, so `scanned == 0` is reported as an error, not a pass.

ROLE_FIELDS = ("role", "sender", "author", "from", "speaker", "type", "direction")
TEXT_FIELDS = ("content", "text", "message", "body", "response", "output", "answer")
CONV_FIELDS = ("conversation_id", "session_id", "thread_id", "chat_id", "conversation", "sid")
TIME_FIELDS = ("timestamp", "created_at", "time", "date", "ts")
LANG_FIELDS = ("language", "lang", "locale")

ASSISTANT_VALUES = {
    "assistant", "mira", "bot", "ai", "agent", "system_reply", "outbound",
    "model", "chatbot", "support", "مساعد", "ميرا",
}


@dataclass
class Message:
    text: str
    conversation: str
    role: str
    when: str = ""
    lang: str = "en"
    user_said: str = ""   # the preceding user turn, for guardrail context


@dataclass
class Report:
    scanned: int = 0
    skipped_non_assistant: int = 0
    blocked: list[tuple[Message, guardrails.Verdict]] = field(default_factory=list)
    rule_counts: Counter = field(default_factory=Counter)
    conversations: set = field(default_factory=set)
    flagged_conversations: set = field(default_factory=set)


def _first(d: dict, names: tuple, override: str | None = None) -> str | None:
    if override:
        return str(d[override]) if d.get(override) is not None else None
    for n in names:
        if d.get(n) is not None:
            return str(d[n])
    return None


def _flatten(text_value) -> str:
    """Anthropic-style content is a list of blocks, not a string."""
    if isinstance(text_value, str):
        return text_value
    if isinstance(text_value, list):
        parts = []
        for block in text_value:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "\n".join(parts)
    return ""


def _records_from_json(obj) -> list[dict]:
    """Accept a list of messages, a list of conversations, or a wrapper object."""
    if isinstance(obj, dict):
        for key in ("conversations", "messages", "data", "items", "results", "records"):
            if isinstance(obj.get(key), list):
                obj = obj[key]
                break
        else:
            obj = [obj]

    out: list[dict] = []
    for item in obj:
        if not isinstance(item, dict):
            continue
        nested = None
        for key in ("messages", "turns", "transcript", "history", "events"):
            if isinstance(item.get(key), list):
                nested = key
                break
        if nested:
            conv = _first(item, CONV_FIELDS) or ""
            for msg in item[nested]:
                if isinstance(msg, dict):
                    msg.setdefault("_conversation", conv)
                    out.append(msg)
        else:
            out.append(item)
    return out


def load(path: str, fmt: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        if fmt == "csv":
            return list(csv.DictReader(fh))
        raw = fh.read().strip()

    if not raw:
        return []
    if fmt == "jsonl" or (fmt == "auto" and not raw.startswith(("[", "{"))):
        records = []
        for line in raw.splitlines():
            line = line.strip()
            if line:
                records.append(json.loads(line))
        return _records_from_json(records)

    if fmt == "auto" and raw.startswith("{") and "\n{" in raw:
        # A concatenation of objects, one per line, that happens to start with "{".
        try:
            return _records_from_json([json.loads(l) for l in raw.splitlines() if l.strip()])
        except json.JSONDecodeError:
            pass

    return _records_from_json(json.loads(raw))


def to_messages(records: list[dict], args) -> tuple[list[Message], int]:
    messages, skipped = [], 0
    last_user: dict[str, str] = {}
    for i, rec in enumerate(records):
        role = (_first(rec, ROLE_FIELDS, args.role_field) or "").strip().lower()
        text = _flatten(rec.get(args.text_field) if args.text_field else
                        next((rec[n] for n in TEXT_FIELDS if rec.get(n) is not None), ""))

        conversation = rec.get("_conversation") or _first(rec, CONV_FIELDS) or f"row-{i}"

        wanted = args.role_value.lower() if args.role_value else None
        is_assistant = (role == wanted) if wanted else (role in ASSISTANT_VALUES)
        if not is_assistant:
            # Not scanned — but remembered, because it is what the next MIRA turn answers.
            if text.strip():
                last_user[conversation] = text
            skipped += 1
            continue
        if not text.strip():
            continue

        lang = (_first(rec, LANG_FIELDS) or "en").strip().lower()[:2]
        messages.append(Message(
            text=text,
            conversation=conversation,
            role=role,
            when=_first(rec, TIME_FIELDS) or "",
            lang=lang if lang in ("en", "ar") else "en",
            user_said=last_user.get(conversation, ""),
        ))
    return messages, skipped


# --------------------------------------------------------------------------------------
# Scanning
# --------------------------------------------------------------------------------------

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
_PHONE = re.compile(r"\+?\d[\d\s().-]{7,}\d")


def redact(text: str) -> str:
    text = _EMAIL.sub("[email]", text)
    return _PHONE.sub("[phone]", text)


def scan(messages: list[Message], no_redact: bool = False) -> Report:
    report = Report()
    for msg in messages:
        report.scanned += 1
        report.conversations.add(msg.conversation)
        verdict = guardrails.check_response(msg.text, lang=msg.lang, context=msg.user_said)
        if verdict.blocked:
            if not no_redact:
                for finding in verdict.findings:
                    finding.excerpt = redact(finding.excerpt)
            report.blocked.append((msg, verdict))
            report.flagged_conversations.add(msg.conversation)
            for rule in verdict.rules:
                report.rule_counts[rule] += 1
    return report


# --------------------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------------------

def print_report(report: Report, skipped: int, show: int) -> None:
    print()
    print("MIRA LIVE-LOG AUDIT")
    print("=" * 72)
    print(f"  assistant messages scanned   {report.scanned}")
    print(f"  conversations covered        {len(report.conversations)}")
    print(f"  non-assistant rows skipped   {skipped}")
    print()

    if report.scanned == 0:
        print("  ERROR — nothing was scanned.")
        print("  The role or text field was not recognised in this export. Do NOT read this as")
        print("  a clean result. Inspect one record and pass --role-field / --text-field /")
        print("  --role-value explicitly, then re-run.")
        return

    if not report.blocked:
        print("  No message tripped a guardrail rule.")
        print()
        print("  Read this precisely: it means no PATTERN THIS CHECK DETECTS appeared in the")
        print("  messages scanned. It is not proof that MIRA is safe, and with a small sample it")
        print("  is not even weak evidence — see PHASE-02-D0-AUDIT.md §5 for what a zero result")
        print("  can and cannot support.")
        return

    pct = 100.0 * len(report.blocked) / report.scanned
    conv_pct = 100.0 * len(report.flagged_conversations) / max(len(report.conversations), 1)
    print(f"  ⚠  MESSAGES THAT WOULD BE BLOCKED   {len(report.blocked)}  ({pct:.1f}%)")
    print(f"     conversations affected           {len(report.flagged_conversations)}"
          f"  ({conv_pct:.1f}%)")
    print()
    print("  by rule:")
    for rule, count in report.rule_counts.most_common():
        print(f"    {rule:<26} {count}")
    print()

    by_rule = defaultdict(list)
    for msg, verdict in report.blocked:
        for rule in verdict.rules:
            by_rule[rule].append((msg, verdict))

    print("-" * 72)
    for rule, hits in sorted(by_rule.items(), key=lambda kv: -len(kv[1])):
        print(f"\n{rule}  ({len(hits)})")
        for msg, verdict in hits[:show]:
            excerpt = next(f.excerpt for f in verdict.findings if f.rule == rule)
            when = f" · {msg.when}" if msg.when else ""
            print(f"  [{msg.conversation}{when}]")
            print(f"    …{excerpt}…")
        if len(hits) > show:
            print(f"    … and {len(hits) - show} more (--show {len(hits)} to see all)")

    print()
    print("-" * 72)
    print("  STOP-THE-LINE. Per MIRA-GUARDRAILS.md §7, a confirmed violation in production is")
    print("  not a backlog item. Verify these by hand — the check is deliberately cautious and")
    print("  some will be false positives — then follow the procedure for those that are real.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", help="Exported conversation log (JSONL, JSON, or CSV)")
    parser.add_argument("--format", default="auto", choices=("auto", "jsonl", "json", "csv"))
    parser.add_argument("--role-field", help="Field naming the speaker, if not auto-detected")
    parser.add_argument("--text-field", help="Field holding message text, if not auto-detected")
    parser.add_argument("--role-value", help="Value marking a MIRA message, e.g. 'assistant'")
    parser.add_argument("--show", type=int, default=5, help="Excerpts per rule (default 5)")
    parser.add_argument("--json", dest="json_out", help="Also write findings to this JSON file")
    parser.add_argument("--no-redact", action="store_true",
                        help="Do not mask emails and phone numbers in excerpts")
    args = parser.parse_args()

    try:
        records = load(args.path, args.format)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not read {args.path}: {exc}", file=sys.stderr)
        return 2

    messages, skipped = to_messages(records, args)
    report = scan(messages, no_redact=args.no_redact)
    print_report(report, skipped, args.show)

    if args.json_out:
        payload = {
            "scanned": report.scanned,
            "conversations": len(report.conversations),
            "blocked": len(report.blocked),
            "flagged_conversations": sorted(report.flagged_conversations),
            "by_rule": dict(report.rule_counts),
            "findings": [
                {
                    "conversation": m.conversation,
                    "timestamp": m.when,
                    "lang": m.lang,
                    "rules": v.rules,
                    "excerpts": [f.excerpt for f in v.findings],
                }
                for m, v in report.blocked
            ],
        }
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print(f"\n  findings written to {args.json_out}")

    if report.scanned == 0:
        return 2
    return 1 if report.blocked else 0


if __name__ == "__main__":
    sys.exit(main())
