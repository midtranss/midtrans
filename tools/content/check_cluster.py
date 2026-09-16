#!/usr/bin/env python3
"""
Near-duplicate detection across a cluster of pages.

SEO-STANDARDS.md §2 makes a point that no per-page check can act on:

    Search engines assess doorway-page patterns at SITE level, not page level.

check_page.py reads one page at a time, so it cannot see the pattern that actually carries the
risk — a set of pages that are individually reasonable and collectively a template.

This implements the standard's own test:

    If the page would survive find-and-replace of its location or industry name with another
    and still read correctly, it does not pass.

For every pair of pages, the distinguishing terms of BOTH are masked out — title words, and any
`entities:` listed in front matter — and what remains is compared. Two pages about genuinely
different things diverge once their subject names are removed. Two templated pages do not.

    python3 tools/content/check_cluster.py drafts/*.md
    python3 tools/content/check_cluster.py drafts/*.md --block 0.35 --warn 0.20

Exit 0 clean, 1 findings, 2 could not read the input.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_page import split_front_matter, to_prose  # noqa: E402


# Calibrate these against the real cluster before trusting them — see §3 of
# ../../docs/phases/PHASE-05-CLAIMS-AND-DUPLICATION.md. Distinct pages on adjacent topics
# typically land well below 0.15 on 5-word shingles; a template lands far above it.
BLOCK_AT = 0.35
WARN_AT = 0.20
SHINGLE = 5

_WORD = re.compile(r"[\w؀-ۿ]+")

# Words too common to distinguish anything. Masking a page's title words would otherwise remove
# "the", "for" and "in" from every page and inflate similarity.
_STOP = {
    "the", "a", "an", "and", "or", "of", "for", "to", "in", "on", "at", "by", "with", "from",
    "into", "your", "our", "we", "is", "are", "be", "as", "that", "this", "it", "its",
    "في", "من", "إلى", "على", "عن", "مع", "هذا", "هذه", "التي", "الذي", "أن", "ما", "و",
}


@dataclass
class Page:
    path: str
    title: str
    entities: list
    words: list


@dataclass
class Pair:
    a: str
    b: str
    similarity: float
    level: str
    shared: list


def significant(text: str) -> list:
    return [w for w in _WORD.findall(text.lower()) if w not in _STOP]


def load(path: str) -> Page:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    fields, body, _ = split_front_matter(text)
    prose = to_prose(body)

    title = fields.get("title", "") or os.path.splitext(os.path.basename(path))[0]
    entities = [e.strip() for e in (fields.get("entities") or "").split(",") if e.strip()]
    # The filename is often the clearest statement of the page's subject.
    entities += os.path.splitext(os.path.basename(path))[0].replace("_", "-").split("-")

    return Page(path=path, title=title, entities=entities, words=significant(prose))


def shingles(words: list, mask: set, k: int = SHINGLE) -> set:
    """k-word shingles with the subject terms of both pages replaced by a placeholder."""
    masked = ["·" if w in mask else w for w in words]
    return {tuple(masked[i:i + k]) for i in range(max(0, len(masked) - k + 1))}


def compare(a: Page, b: Page, k: int = SHINGLE) -> tuple[float, list]:
    mask = set(significant(a.title) + significant(b.title))
    for entity in a.entities + b.entities:
        mask.update(significant(entity))

    sa, sb = shingles(a.words, mask, k), shingles(b.words, mask, k)
    if not sa or not sb:
        return 0.0, []

    common = sa & sb
    similarity = len(common) / len(sa | sb)
    examples = [" ".join(s).replace("·", "___") for s in list(common)[:3]]
    return similarity, examples


def analyse(paths: list, block_at: float, warn_at: float, k: int = SHINGLE) -> list:
    pages = [load(p) for p in paths]
    pairs = []
    for i, a in enumerate(pages):
        for b in pages[i + 1:]:
            similarity, shared = compare(a, b, k)
            if similarity >= block_at:
                level = "BLOCKER"
            elif similarity >= warn_at:
                level = "WARNING"
            else:
                continue
            pairs.append(Pair(a.path, b.path, similarity, level, shared))
    return sorted(pairs, key=lambda p: -p.similarity)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", help="Pages in one cluster")
    parser.add_argument("--block", type=float, default=BLOCK_AT)
    parser.add_argument("--warn", type=float, default=WARN_AT)
    parser.add_argument("--shingle", type=int, default=SHINGLE)
    parser.add_argument("--json", dest="json_out")
    args = parser.parse_args()

    if len(args.paths) < 2:
        print("Give at least two pages — this check is about the relationship between them.",
              file=sys.stderr)
        return 2

    try:
        pairs = analyse(args.paths, args.block, args.warn, args.shingle)
    except OSError as exc:
        print(f"Could not read a page: {exc}", file=sys.stderr)
        return 2

    print(f"\nCLUSTER DUPLICATION CHECK   {len(args.paths)} pages, "
          f"{len(args.paths) * (len(args.paths) - 1) // 2} pairs")
    print("=" * 72)

    if not pairs:
        print(f"  No pair above {args.warn:.0%} similarity after masking subject terms.")
    for pair in pairs:
        print(f"\n  {pair.level}  {pair.similarity:.0%} similar after masking")
        print(f"    {pair.a}")
        print(f"    {pair.b}")
        for example in pair.shared:
            print(f"      shared: …{example}…")

    blockers = [p for p in pairs if p.level == "BLOCKER"]
    print("\n" + "-" * 72)
    print(f"  {len(blockers)} blocking pair(s), {len(pairs) - len(blockers)} to review")
    if blockers:
        print("\n  A blocking pair is two pages that read the same once their subject names are")
        print("  removed — the doorway pattern SEO-STANDARDS §2 prohibits. Merge them, or give")
        print("  each the operational substance that makes it a different page.")
    print("\n  Similarity is evidence, not a verdict. Two genuinely distinct pages on adjacent")
    print("  topics can share structure; read the pair before acting. Thresholds need")
    print("  calibrating against this cluster — see PHASE-05-CLAIMS-AND-DUPLICATION.md §3.")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump([vars(p) for p in pairs], fh, ensure_ascii=False, indent=2)
        print(f"\n  report written to {args.json_out}")

    return 1 if pairs else 0


if __name__ == "__main__":
    sys.exit(main())
