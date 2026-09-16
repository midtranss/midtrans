#!/usr/bin/env python3
"""
Pre-publication check for MIDTRANS content pages.

Phase 04 publishes 25-40 pages of Syrian trade procedure written by people, under a hard rule:
no duty rate, no clearance time, no cost, no compliance determination. One slip reaches a
customer as MIDTRANS's published position. This runs before a page goes live.

    python3 tools/content/check_page.py drafts/syria-import-documents.md
    python3 tools/content/check_page.py drafts/*.md --json report.json

What it can decide, it decides. What it cannot, it refuses to pretend about: the uniqueness test
in SEO-STANDARDS.md §2 is a human judgement, and all this tool does is refuse to pass a page
whose reviewer has not recorded one. See ../../docs/phases/PHASE-04-EDITORIAL-GATE.md §4.

Exit 0 clean, 1 findings, 2 could not read the input.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "mira"))

try:
    import guardrails
except ImportError:  # pragma: no cover - the suite asserts this does not happen
    guardrails = None


BLOCKER, WARNING, NOTE = "BLOCKER", "WARNING", "NOTE"


@dataclass
class Finding:
    level: str
    rule: str
    message: str
    line: int = 0
    excerpt: str = ""


@dataclass
class PageReport:
    path: str
    findings: list = field(default_factory=list)
    words: int = 0
    front_matter: dict = field(default_factory=dict)

    @property
    def blockers(self):
        return [f for f in self.findings if f.level == BLOCKER]

    @property
    def passed(self):
        return not self.blockers


# --------------------------------------------------------------------------------------
# What the standards forbid, in the words the standards use
# --------------------------------------------------------------------------------------

# WRITING-STANDARDS.md §"Never use"
NEVER_USE = [
    "best", "largest", "number one", "world class", "world-class", "industry leading",
    "industry-leading", "premier", "revolutionary", "cutting edge", "cutting-edge",
    "guaranteed", "unmatched", "leading provider", "one-stop shop", "one stop shop",
    "seamless", "hassle-free", "hassle free",
]

# Determinations that belong to a lawyer or a compliance officer, never to a content page.
# PHASE-04 puts sanctions and restricted-party questions explicitly out of scope.
COMPLIANCE_CLAIMS = [
    r"is (?:not )?sanctioned", r"is (?:not )?prohibited by law", r"you (?:may|can) legally",
    r"it is legal to", r"it is illegal to", r"complies with (?:all|the) (?:regulations|sanctions)",
    r"not subject to sanctions", r"exempt from sanctions", r"no licence (?:is )?required",
    r"no license (?:is )?required", r"we confirm (?:that )?(?:this|the shipment) (?:is|will)",
    r"مطابق للعقوبات", r"غير خاضع للعقوبات", r"مسموح قانونيا", r"لا يحتاج (?:إلى )?ترخيص",
]

# Clearance duration is a commitment, hedged or not. PHASE-04 §Out of scope.
CLEARANCE_TIME = (
    r"clear(?:s|ed|ance)?\s+(?:in|within|takes?|normally takes?|usually takes?)\s+"
    r"(?:about\s+|around\s+|roughly\s+|approximately\s+)?\d"
    r"|(?:takes?|normally|usually|typically)\s+(?:about\s+|around\s+)?\d+\s*"
    r"(?:-|–|to)?\s*\d*\s*(?:working\s+)?(?:day|days|week|weeks|hour|hours)"
    r"\s+(?:to\s+)?clear"
    r"|التخليص\s+(?:يستغرق|يأخذ|خلال)\s*\d"
    r"|يستغرق\s+التخليص"
)

# WRITING-STANDARDS.md §3 anti-AI-writing patterns.
AI_TELLS = [
    (r"in today'?s (?:fast[- ]paced|ever[- ]changing|globali[sz]ed|competitive)",
     "empty transition"),
    (r"in this (?:article|guide|post),? we(?:'ll| will)", "self-referential structure"),
    (r"in conclusion,", "hollow conclusion"),
    (r"it'?s (?:important|crucial|essential) to (?:note|remember|understand)", "filler"),
    (r"when it comes to", "filler"),
    (r"navigating the (?:complex|complexities|world) of", "stock phrase"),
    (r"efficient,? reliable,? and cost[- ]effective", "triadic filler"),
    (r"\bunlock(?:ing)? the (?:power|potential)\b", "stock phrase"),
    (r"contact us today", "generic close — WRITING-STANDARDS requires a specific next step"),
    (r"\bdelve into\b", "stock phrase"),
]

REQUIRED_FRONT_MATTER = {
    "title": "the page's own title",
    "language": "en or ar — the language this file is written in, not translated into",
    "owner": "a person's name. Not a team, not a role",
    "reviewed_at": "YYYY-MM-DD, when a human last checked the facts",
    "expires_at": "YYYY-MM-DD, when the procedure must be re-checked",
    "uniqueness": "the reviewer's recorded answer to SEO-STANDARDS §2 — see §4 of the gate doc",
    "uniqueness_reviewed_by": "who applied that test",
}


# --------------------------------------------------------------------------------------
# Reading a draft
# --------------------------------------------------------------------------------------

_FM = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
_TAG = re.compile(r"<[^>]+>")
_CODE = re.compile(r"```.*?```", re.S)


def split_front_matter(text: str) -> tuple[dict, str, int]:
    """Minimal YAML front matter: flat key: value pairs. Returns (fields, body, offset)."""
    match = _FM.match(text)
    if not match:
        return {}, text, 0
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.strip().startswith("#"):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip("'\"")
    offset = text[: match.end()].count("\n")
    return fields, text[match.end():], offset


def to_prose(body: str) -> str:
    """Strip code blocks and HTML tags — a rate inside a code sample is an example, not a claim."""
    return _TAG.sub(" ", _CODE.sub(" ", body))


def line_of(body: str, position: int, offset: int) -> int:
    return body[:position].count("\n") + 1 + offset


def excerpt_at(text: str, position: int, pad: int = 50) -> str:
    start, end = max(0, position - pad), min(len(text), position + pad)
    return " ".join(text[start:end].split())


# --------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------

def check_front_matter(report: PageReport, fields: dict) -> None:
    for key, why in REQUIRED_FRONT_MATTER.items():
        if not fields.get(key):
            report.findings.append(Finding(
                BLOCKER, "front_matter", f"Missing `{key}` — {why}"))

    for key in ("reviewed_at", "expires_at"):
        value = fields.get(key, "")
        if value and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            report.findings.append(Finding(
                BLOCKER, "front_matter", f"`{key}` must be YYYY-MM-DD, got {value!r}"))

    owner = fields.get("owner", "")
    if owner and owner.strip().lower() in {
        "operations", "ops", "team", "the team", "marketing", "midtrans", "tbd", "n/a",
    }:
        report.findings.append(Finding(
            BLOCKER, "front_matter",
            f"`owner` is {owner!r}. A page without a named person has no owner — "
            "the same rule the knowledge base applies."))

    uniqueness = fields.get("uniqueness", "")
    if uniqueness and len(uniqueness.split()) < 12:
        report.findings.append(Finding(
            BLOCKER, "uniqueness",
            "`uniqueness` is too short to be a real answer. State what on this page a "
            "competitor could not have written, specifically. See the gate doc §4."))


def check_prohibited(report: PageReport, prose: str, offset: int) -> None:
    if guardrails is None:
        report.findings.append(Finding(
            BLOCKER, "tooling",
            "mira/guardrails.py could not be imported, so the commercial-statement check "
            "did not run. A skipped safety check is not a pass."))
        return

    verdict = guardrails.check_response(prose)
    for finding in verdict.findings:
        report.findings.append(Finding(
            BLOCKER, f"prohibited:{finding.rule}",
            "A rate, figure in a cost context, duration, or commitment. "
            "WRITING-STANDARDS §4 and PHASE-04 §Out of scope.",
            line=line_of(prose, finding.position, offset),
            excerpt=finding.excerpt))

    for match in re.finditer(CLEARANCE_TIME, prose, re.I):
        report.findings.append(Finding(
            BLOCKER, "clearance_time",
            "A clearance duration. Explain the sequence and what drives it, never how long.",
            line=line_of(prose, match.start(), offset),
            excerpt=excerpt_at(prose, match.start())))

    for pattern in COMPLIANCE_CLAIMS:
        for match in re.finditer(pattern, prose, re.I):
            report.findings.append(Finding(
                BLOCKER, "compliance_determination",
                "A regulatory or legal determination. Out of scope for every page in "
                "this programme — route it to a specialist.",
                line=line_of(prose, match.start(), offset),
                excerpt=excerpt_at(prose, match.start())))


def check_language(report: PageReport, prose: str, offset: int) -> None:
    lowered = prose.lower()
    for word in NEVER_USE:
        for match in re.finditer(rf"\b{re.escape(word)}\b", lowered):
            report.findings.append(Finding(
                BLOCKER, "forbidden_word",
                f"`{word}` is on the never-use list in WRITING-STANDARDS.",
                line=line_of(prose, match.start(), offset),
                excerpt=excerpt_at(prose, match.start())))

    for pattern, label in AI_TELLS:
        for match in re.finditer(pattern, lowered):
            report.findings.append(Finding(
                WARNING, "ai_writing",
                f"{label} — WRITING-STANDARDS §3.",
                line=line_of(prose, match.start(), offset),
                excerpt=excerpt_at(prose, match.start())))


def check_structure(report: PageReport, body: str, prose: str, offset: int) -> None:
    headings = re.findall(r"^(#{1,6})\s+(.+)$", body, re.M)
    h1s = [h for h in headings if len(h[0]) == 1]

    if len(h1s) != 1:
        report.findings.append(Finding(
            BLOCKER, "structure",
            f"Exactly one H1 required, found {len(h1s)}. WRITING-STANDARDS §5."))

    levels = [len(h[0]) for h in headings]
    for previous, current in zip(levels, levels[1:]):
        if current > previous + 1:
            report.findings.append(Finding(
                WARNING, "structure",
                f"Heading level jumps from H{previous} to H{current}. No skipped levels."))
            break

    # Answer-first: the opening must carry substance before the first H2.
    after_h1 = re.split(r"^#\s+.+$", body, maxsplit=1, flags=re.M)
    opening = re.split(r"^##\s", after_h1[-1], maxsplit=1, flags=re.M)[0] if after_h1 else ""
    opening_words = len(to_prose(opening).split())
    if opening_words < 40:
        report.findings.append(Finding(
            WARNING, "answer_first",
            f"The opening before the first H2 is {opening_words} words. WRITING-STANDARDS "
            "requires the core question answered within the first 100 words."))

    if report.words < 300:
        report.findings.append(Finding(
            WARNING, "thin",
            f"{report.words} words. SEO-STANDARDS §2 prefers one strong page to three weak "
            "ones — consider merging this into a parent."))

    internal = [l for l in re.findall(r"\]\(([^)]+)\)", body)
                if not l.startswith(("http://", "https://", "#", "mailto:", "tel:"))]
    if len(internal) < 3:
        report.findings.append(Finding(
            WARNING, "internal_links",
            f"{len(internal)} internal links. SEO-STANDARDS requires at least 3 relevant "
            "inbound links per page and no orphans; outbound links are how you build them."))

    if not re.search(r"contact|enquir|quote|request|team|تواصل|طلب|فريق", prose, re.I):
        report.findings.append(Finding(
            WARNING, "closing",
            "No next step found. WRITING-STANDARDS §5 requires a clear, specific close."))


def check_arabic(report: PageReport, fields: dict, prose: str) -> None:
    declared = (fields.get("language") or "").lower()
    arabic_chars = len(re.findall(r"[؀-ۿ]", prose))
    latin_words = len(re.findall(r"\b[A-Za-z]{4,}\b", prose))

    if declared == "ar":
        if arabic_chars < 200:
            report.findings.append(Finding(
                BLOCKER, "language",
                f"Declared `language: ar` but only {arabic_chars} Arabic characters found."))
        # A page that is mostly English with Arabic headings is a translated shell.
        elif latin_words > arabic_chars / 4:
            report.findings.append(Finding(
                WARNING, "language",
                "Heavily Latin for an Arabic page. WRITING-STANDARDS §6: Arabic is written, "
                "not translated. Technical terms are expected; English sentences are not."))
    elif declared == "en" and arabic_chars > 400:
        report.findings.append(Finding(
            WARNING, "language",
            "Substantial Arabic in a page declared `language: en`. Check the front matter."))
    elif declared not in ("en", "ar", ""):
        report.findings.append(Finding(
            BLOCKER, "language",
            f"`language: {declared}` — Phase 04 is T2, EN and AR only "
            "(../standards/LANGUAGE-SCOPE.md)."))


def check_page(path: str) -> PageReport:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    fields, body, offset = split_front_matter(text)
    prose = to_prose(body)
    report = PageReport(path=path, front_matter=fields, words=len(prose.split()))

    check_front_matter(report, fields)
    check_prohibited(report, prose, offset)
    check_language(report, prose, offset)
    check_structure(report, body, prose, offset)
    check_arabic(report, fields, prose)
    return report


# --------------------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------------------

def print_report(report: PageReport) -> None:
    status = "PASS" if report.passed else "BLOCKED"
    print(f"\n{status}  {report.path}  ({report.words} words)")
    if not report.findings:
        print("  no findings")
        return
    order = {BLOCKER: 0, WARNING: 1, NOTE: 2}
    for finding in sorted(report.findings, key=lambda f: (order[f.level], f.line)):
        where = f":{finding.line}" if finding.line else ""
        print(f"  {finding.level:<8} {finding.rule}{where}")
        print(f"           {finding.message}")
        if finding.excerpt:
            print(f"           …{finding.excerpt}…")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", help="Draft pages (markdown, with front matter)")
    parser.add_argument("--json", dest="json_out", help="Write the full report to this file")
    parser.add_argument("--warnings-are-blocking", action="store_true",
                        help="Treat warnings as blockers (use once the cluster is stable)")
    args = parser.parse_args()

    reports = []
    for path in args.paths:
        try:
            reports.append(check_page(path))
        except OSError as exc:
            print(f"Could not read {path}: {exc}", file=sys.stderr)
            return 2

    for report in reports:
        print_report(report)

    blocked = [r for r in reports if not r.passed]
    warned = [r for r in reports
              if any(f.level == WARNING for f in r.findings) and r.passed]

    print("\n" + "-" * 70)
    print(f"  {len(reports)} page(s)   {len(blocked)} blocked   {len(warned)} with warnings only")
    if blocked:
        print("\n  A blocked page does not publish. Every blocker is a rule from")
        print("  WRITING-STANDARDS, SEO-STANDARDS, or PHASE-04's out-of-scope list.")
    print("\n  This tool cannot apply the uniqueness test (SEO-STANDARDS §2). It only refuses")
    print("  to pass a page whose reviewer has not recorded one. A clean run is a licence to")
    print("  review, not a licence to publish.")

    if args.json_out:
        payload = [{
            "path": r.path,
            "passed": r.passed,
            "words": r.words,
            "front_matter": r.front_matter,
            "findings": [vars(f) for f in r.findings],
        } for r in reports]
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print(f"\n  report written to {args.json_out}")

    if blocked:
        return 1
    if warned and args.warnings_are_blocking:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
