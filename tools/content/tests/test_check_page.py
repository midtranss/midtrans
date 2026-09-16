#!/usr/bin/env python3
"""
Tests for the pre-publication content check.

The suite is built around one asymmetry: a false blocker costs a writer five minutes, and a
missed rate reaches a customer as MIDTRANS's published position. So the must-block cases are
strict — and the must-pass cases are here in equal number, because a checker that blocks good
writing gets switched off, and then protects nothing.

Run:  python3 tools/content/tests/test_check_page.py
"""

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))          # tools/content/tests
sys.path.insert(0, os.path.dirname(HERE))                  # tools/content

import check_page as cp  # noqa: E402

failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        failures.append(name)


GOOD_FRONT = """---
title: Documents required to import into Syria
language: en
owner: Khaldoun Alhaj
reviewed_at: 2026-09-16
expires_at: 2027-03-16
uniqueness: Records the three document errors our Latakia desk sees most often and what each
  costs the shipper in re-issuance, which no published guide states.
uniqueness_reviewed_by: Khaldoun Alhaj
---
"""

GOOD_BODY = """
# Documents required to import into Syria

Every import into Syria turns on four documents, and three of them are commonly prepared in a
form the clearing agent has to send back. This page sets out what each one is, who issues it,
and the specific errors our Latakia desk sees repeatedly. Read the origin certificate section
first — it causes more re-issuance than the other three combined.

## The commercial invoice

The invoice must name the consignee exactly as it appears on the import record. A trading name
that differs by a word is the most frequent cause of a document being returned.

See also the [clearance sequence](../clearance-sequence.md), the
[origin certificate guide](../origin-certificate.md) and the
[Latakia port page](../ports/latakia.md).

## The certificate of origin

The certificate is issued by the chamber of commerce at origin, and it must name the same
consignee as the invoice. Where the goods are manufactured in one country and shipped from
another, the certificate states the country of manufacture — not the port of loading. That
distinction is the single error we send back most often, and it is the one a first-time
shipper is least likely to anticipate, because the forwarder at origin will usually fill the
form from the booking rather than from the manufacturing record.

Re-issuing a certificate means going back to the chamber at origin. The cargo has usually
already sailed by the time the error surfaces.

## The packing list

The packing list must reconcile to the invoice line by line. A consolidated line covering
several invoice lines will be queried, and a weight that disagrees with the bill of lading
will be queried harder.

## Preparing before you book

Assemble the set before the cargo moves, not after. Three of the four documents are issued
at origin, and every one of them is slower to correct once the vessel has sailed.

Our team reviews a document set on request. Send what you have and we will tell you what a
clearing agent is likely to reject, before it costs you a re-issuance.
"""


def write(body, suffix=".md"):
    fh = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False, encoding="utf-8")
    fh.write(body)
    fh.close()
    return fh.name


def report_for(body):
    return cp.check_page(write(body))


def rules(report):
    return {f.rule for f in report.findings}


def blockers(report):
    return {f.rule for f in report.blockers}


# --------------------------------------------------------------------------------------
print("\n=== a good page passes ===")

good = report_for(GOOD_FRONT + GOOD_BODY)
check("clean page has no blockers", good.passed, str([(f.rule, f.message) for f in good.blockers]))
check("clean page has no warnings either", not good.findings,
      str([(f.rule, f.excerpt) for f in good.findings]))
check("word count computed", good.words > 100, good.words)

# --------------------------------------------------------------------------------------
print("\n=== prohibited commercial statements ===")

for label, sentence in [
    ("a rate", "Clearance at Latakia costs USD 350 per container."),
    ("a hedged rate", "Expect roughly 350 USD for the clearance formalities."),
    ("duty as a figure", "The duty payable is around 12,000 SYP on this commodity."),
    ("capacity", "We guarantee space on the weekly service."),
]:
    r = report_for(GOOD_FRONT + GOOD_BODY + "\n\n## Cost\n\n" + sentence + "\n")
    check(f"blocks {label}", not r.passed and any(b.startswith("prohibited") for b in blockers(r)),
          str(blockers(r)))

for label, sentence in [
    ("clearance duration", "Clearance normally takes 5 to 7 working days at the port."),
    ("hedged duration", "Customs clearance takes about 4 days once documents are lodged."),
]:
    r = report_for(GOOD_FRONT + GOOD_BODY + "\n\n## Timing\n\n" + sentence + "\n")
    check(f"blocks {label}", not r.passed, str(blockers(r)))

for label, sentence in [
    ("sanctions determination", "This commodity is not sanctioned and may be imported freely."),
    ("licence determination", "No licence is required for this shipment."),
    ("legality claim", "It is legal to import this category without further approval."),
]:
    r = report_for(GOOD_FRONT + GOOD_BODY + "\n\n## Compliance\n\n" + sentence + "\n")
    check(f"blocks {label}", "compliance_determination" in blockers(r), str(blockers(r)))

# --------------------------------------------------------------------------------------
print("\n=== forbidden words and AI tells ===")

r = report_for(GOOD_FRONT + GOOD_BODY.replace(
    "This page sets out", "As the leading provider in the region, this page sets out"))
check("blocks a never-use phrase", "forbidden_word" in blockers(r), str(blockers(r)))

r = report_for(GOOD_FRONT + GOOD_BODY +
               "\n\n## More\n\nIn today's fast-paced global economy, documents matter.\n")
check("warns on an AI tell", "ai_writing" in rules(r), str(rules(r)))
check("an AI tell does not block", r.passed, str(blockers(r)))

r = report_for(GOOD_FRONT + GOOD_BODY + "\n\n## Next\n\nContact us today.\n")
check("warns on a generic close", "ai_writing" in rules(r))

# A legitimate use of a flagged word must not fire: "best" inside "best practice" is still on
# the list, but the word boundary must not catch it inside another word.
r = report_for(GOOD_FRONT + GOOD_BODY.replace("first", "bestowed"))
check("no false positive inside a longer word", "forbidden_word" not in blockers(r),
      str([f.excerpt for f in r.blockers]))

# --------------------------------------------------------------------------------------
print("\n=== front matter ===")

r = report_for(GOOD_BODY)
check("missing front matter blocks", "front_matter" in blockers(r))
check("names every missing field",
      sum(1 for f in r.blockers if f.rule == "front_matter") == len(cp.REQUIRED_FRONT_MATTER),
      str([f.message for f in r.blockers if f.rule == "front_matter"]))

r = report_for(GOOD_FRONT.replace("owner: Khaldoun Alhaj", "owner: Operations") + GOOD_BODY)
check("a team is not an owner", "front_matter" in blockers(r),
      str([f.message for f in r.blockers]))

r = report_for(GOOD_FRONT.replace("reviewed_at: 2026-09-16", "reviewed_at: Sept 2026") + GOOD_BODY)
check("a loose date blocks", "front_matter" in blockers(r))

r = report_for(GOOD_FRONT.replace(
    "uniqueness: Records the three document errors our Latakia desk sees most often and what each\n  costs the shipper in re-issuance, which no published guide states.",
    "uniqueness: It is unique.") + GOOD_BODY)
check("a token uniqueness answer blocks", "uniqueness" in blockers(r), str(blockers(r)))

# --------------------------------------------------------------------------------------
print("\n=== structure ===")

r = report_for(GOOD_FRONT + GOOD_BODY + "\n# A second H1\n\nMore text here for the body.\n")
check("two H1s block", "structure" in blockers(r))

r = report_for(GOOD_FRONT + "\n# Title\n\n## Straight to a section\n\nShort.\n")
check("thin page warns", "thin" in rules(r), str(rules(r)))
check("no opening warns", "answer_first" in rules(r), str(rules(r)))
check("too few internal links warns", "internal_links" in rules(r), str(rules(r)))

# --------------------------------------------------------------------------------------
print("\n=== language ===")

ARABIC_BODY = """
# الوثائق المطلوبة للاستيراد إلى سوريا

كل عملية استيراد إلى سوريا تقوم على أربع وثائق، وثلاث منها تُعدّ عادةً بصيغة يعيدها وكيل التخليص.
هذه الصفحة تشرح كل وثيقة، ومن يصدرها، والأخطاء المتكرّرة التي يراها مكتبنا في اللاذقية.
ابدأ بقسم شهادة المنشأ — فهي سبب إعادة الإصدار أكثر من الثلاث الأخريات مجتمعة.

## الفاتورة التجارية

يجب أن تحمل الفاتورة اسم المرسل إليه كما هو مسجّل تماماً. اختلاف كلمة واحدة في الاسم التجاري هو
السبب الأكثر تكراراً لإعادة الوثيقة.

انظر أيضاً [تسلسل التخليص](../clearance-sequence.md) و[دليل شهادة المنشأ](../origin.md)
و[صفحة مرفأ اللاذقية](../ports/latakia.md).

## قبل الحجز

جهّز المجموعة قبل تحرّك البضاعة. يراجع فريقنا مجموعة الوثائق عند الطلب — أرسلها ونخبرك بما
سيرفضه وكيل التخليص.
"""

ar_front = GOOD_FRONT.replace("language: en", "language: ar")
r = report_for(ar_front + ARABIC_BODY)
check("a written Arabic page passes", r.passed, str([(f.rule, f.message) for f in r.blockers]))
check("Arabic page has no language warning", "language" not in rules(r), str(rules(r)))

r = report_for(ar_front + GOOD_BODY)
check("English body declared as Arabic blocks", "language" in blockers(r), str(blockers(r)))

r = report_for(GOOD_FRONT.replace("language: en", "language: fr") + GOOD_BODY)
check("a language outside T2 blocks", "language" in blockers(r), str(blockers(r)))

# --------------------------------------------------------------------------------------
print("\n=== code blocks are examples, not claims ===")

r = report_for(GOOD_FRONT + GOOD_BODY + "\n\n## Sample\n\n```\nrate: USD 4500 per 40HC\n```\n")
check("a figure inside a code block does not block", r.passed, str(blockers(r)))

# --------------------------------------------------------------------------------------
print("\n=== the safety check cannot silently skip ===")

check("guardrails imported", cp.guardrails is not None,
      "mira/guardrails.py not importable — the commercial check would not run")

saved = cp.guardrails
cp.guardrails = None
r = report_for(GOOD_FRONT + GOOD_BODY)
check("missing guardrails blocks rather than passes", "tooling" in blockers(r), str(blockers(r)))
cp.guardrails = saved

# --------------------------------------------------------------------------------------
print("\n=== exit codes ===")

import subprocess  # noqa: E402

CLI = os.path.join(os.path.dirname(HERE), "check_page.py")


def run(path, *extra):
    return subprocess.run([sys.executable, CLI, path, *extra], capture_output=True, text=True)

res = run(write(GOOD_FRONT + GOOD_BODY))
check("exit 0 on a clean page", res.returncode == 0, res.stdout[-300:])
check("output refuses to overclaim", "not a licence to publish" in res.stdout)

res = run(write(GOOD_FRONT + GOOD_BODY + "\n\n## Cost\n\nAbout USD 350 per container.\n"))
check("exit 1 on a blocker", res.returncode == 1, res.stdout[-300:])

path = write(GOOD_FRONT + GOOD_BODY + "\n\n## More\n\nIn conclusion, documents matter.\n")
check("exit 0 with warnings by default", run(path).returncode == 0)
check("exit 1 with --warnings-are-blocking",
      run(path, "--warnings-are-blocking").returncode == 1)

check("exit 2 on an unreadable file",
      run("/tmp/definitely-not-here-9482.md").returncode == 2)

# --------------------------------------------------------------------------------------
print()
if failures:
    print(f"Content gate suite: {len(failures)} FAILED — {', '.join(failures)}")
    sys.exit(1)
print("Content gate suite: all checks passed")
