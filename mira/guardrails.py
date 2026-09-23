"""
MIRA output guardrails — layer 2.

Layer 1 is the system prompt (SYSTEM-PROMPT.md). This module is layer 2: a check that runs
*after* the model and does not depend on it. A model instructed not to quote will, under enough
user pressure or unusual phrasing, occasionally quote anyway. This catches that.

Design rules:

  1. Independent of the model. No LLM call, no model-produced signal. Pure inspection.
  2. Precision matters as much as recall. A check that blocks "MIDTRANS has operated since 1998"
     or "a 40ft container holds ..." will be switched off within a week, and then nothing is
     protecting anything. The false-positive tests are as important as the true-positive ones.
  3. Bilingual. Arabic and English are first-class. A guardrail that holds in English and fails
     in Arabic is not a guardrail.
  4. Fail closed, but usefully. A blocked response is replaced by a redirect that still collects
     the enquiry — never a dead end.

Usage:

    from guardrails import check_response, SAFE_FALLBACK

    verdict = check_response(text, lang="ar")
    if verdict.blocked:
        log_violation(verdict)          # stop-the-line signal, see GUARDRAILS.md §7
        text = SAFE_FALLBACK[verdict.lang]

No third-party dependencies.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# --------------------------------------------------------------------------------------
# Normalisation
# --------------------------------------------------------------------------------------

# Arabic-Indic and Eastern Arabic-Indic digits -> ASCII, so "٤٥٠٠" is seen as "4500".
_DIGIT_MAP = {ord(c): str(i % 10) for i, c in enumerate("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹")}

# Arabic diacritics and tatweel carry no meaning here and break naive matching.
_ARABIC_STRIP = re.compile(r"[ً-ٰٟـ]")


def normalize(text: str) -> str:
    """Fold digits, strip diacritics, collapse whitespace. Lowercase for Latin."""
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(_DIGIT_MAP)
    text = _ARABIC_STRIP.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower()


# --------------------------------------------------------------------------------------
# Context vocabulary
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# Word lists — why they are built rather than written out
# --------------------------------------------------------------------------------------
#
# These lists were plain alternations, interpolated straight into the rules. They therefore
# matched INSIDE longer words, and the consequences were not theoretical. Found 2026-09-16 by
# running the content gate over the real MIDTRANS homepage:
#
#   "United Arab Emi-RATE-s"   -> a cost word. THE COMPANY'S OWN ADDRESS, on every page.
#   "600 porcelain cof-FEE cups" -> a cost word. An enquiry already in the register.
#   "the deta-ETA-ils"           -> a transit word. In nearly every freight email written.
#   "needed to-DAY-"             -> a time unit. In the Sprinters enquiry, verbatim.
#   "beurteilen", "importeur"    -> EUR, a currency. Ordinary German, and one enquiry is German.
#
# A rule that blocks a company's own address is not a strict rule, it is a broken one, and
# §8a already records where that leads: somebody switches the check off, and then it protects
# nothing at all.
#
# Latin terms are bounded on both sides, so every inflection that matters has to be listed
# explicitly — which is the point, because the list is then inspectable.
#
# Arabic is NOT bounded the same way. Arabic clitics attach directly to the word — بسعر،
# الأسعار، للرسوم — so a leading boundary would lose real matches. Suffixes are the opposite:
# they change the word (رسم fee -> رسمي official), so those are excluded individually where
# evidence showed a collision.
#
# Residual, known and accepted: أشهر is both "months" and "most famous", spelled identically.
# No pattern separates them. It is a time unit, which only fires with a transit word nearby,
# so the exposure is small and stated rather than hidden.

def _terms(latin: str, arabic: str = "") -> str:
    """Bound the Latin alternatives at both ends; leave the Arabic ones prefix-friendly."""
    parts = [rf"\b(?:{latin})\b"] if latin else []
    if arabic:
        parts.append(arabic)
    return "(?:" + "|".join(parts) + ")"


_MONEY_WORDS = _terms(
    r"usd|u\.s\.d|aed|eur|gbp|sar|syp|dollar|dollars|euro|euros|dirham|dirhams",
    r"دولار|درهم|يورو|ليرة|ريال",
)
_MONEY_SYMBOL = r"[$€£]|\bد\.إ|\bل\.س"

_RATE_UNITS = (
    r"per\s*(?:kg|kilo|cbm|m3|container|teu|feu|ton|tonne|shipment|unit|pallet)|"
    r"/\s*(?:kg|cbm|m3|20'?|40'?|teu|feu|ton)|"
    r"لكل\s*(?:كيلو|كغ|متر|مكعب|حاوية|طن|شحنة|طبلية)|"
    r"للحاوية|للكيلو|للطن|للمتر"
)

_COST_WORDS = _terms(
    # Every inflection spelled out, because the boundaries mean "costs" no longer rides in
    # on "cost". That is the trade: a longer list, and no "accurate" or "coffee".
    r"cost|costs|costing|price|prices|priced|pricing|rate|rates|rated|"
    r"quote|quotes|quoted|quotation|quotations|charge|charges|charged|fee|fees|"
    r"freight|duty|duties|tax|taxes|tariff|tariffs|surcharge|surcharges|"
    r"demurrage|storage",
    # رسم(?!ي) — the fee, not رسمي "official". "كتاباً رسمياً" appears in the reply drafts and
    # in this module's own test corpus, and it was being read as a cost word.
    r"تكلفة|تكاليف|سعر|أسعار|السعر|الأسعار|عرض سعر|رسوم|رسم(?!ي)|أجرة|ضريبة|ضرائب|"
    r"تعرفة|غرامة|أرضيات",
)

_TIME_UNITS = _terms(
    r"days?|weeks?|months?|hours?",
    r"يوم|يوما|أيام|يومين|اسبوع|أسبوع|اسابيع|أسابيع|أسبوعين|شهر|شهور|أشهر|شهرين|ساعة|ساعات",
)

_TRANSIT_WORDS = _terms(
    # "eta" unbounded was matching "details" and "retail" — words in almost every freight email.
    r"transit|transit time|eta|e\.t\.a|arrive|arrives|arrival|delivery time|lead time|"
    r"sailing|takes about|takes around|takes approximately|it takes|duration",
    r"ترانزيت|مدة|المدة|يستغرق|تستغرق|وصول|الوصول|تسليم|التسليم|مده",
)

# A number carrying a PHYSICAL unit is a quantity, not a price. Cargo is always described in
# approximations — "approx. dimensions per vehicle", "approximately 1.0-1.5 CBM", "150-220 kg
# gross", "about 1200 kg" — and every one of those is quoted from a real enquiry in the
# register. Blocking a hedged measurement blocks the ordinary language of the trade, and a rule
# that does that is a rule somebody turns off.
#
# Deliberately NOT here: currencies, and time units. "approximately 950 usd" is a price and
# "approximately 18 days" is a transit claim, and both must keep firing. Nor does this touch
# the rate-unit rule: "950 per cbm" carries "per", which is what makes it a rate rather than a
# measurement, and that rule is checked before this exclusion applies.
_QUANTITY_UNIT = (
    r"\s*(?:cbm|m3|m³|cubic\s*met(?:er|re)s?|kgs?|kilos?|kilograms?|tons?|tonnes?|mts?|"
    r"lbs?|cms?|mms?|mtr?s?|m\b|met(?:er|re)s?|ft|feet|inch(?:es)?|"
    r"pallets?|cartons?|boxes|cases|pieces?|pcs|units?|bags?|drums?|rolls?|"
    r"containers?|vehicles?|cars?|trucks?|sets?|litres?|liters?|l\b|"
    r"متر|أمتار|مكعب|كغ|كجم|كيلو|طن|أطنان|طبلية|طبليات|منصة|منصات|كرتون|كراتين|"
    r"صندوق|صناديق|قطعة|قطع|حاوية|حاويات|مركبة|مركبات|شاحنة|شاحنات|لتر)"
)


def _is_quantity(text: str, end: int) -> bool:
    """Is the number ending at `end` immediately followed by a physical unit?"""
    return bool(re.match(_QUANTITY_UNIT, text[end:end + 24]))


# Hedges do not make a figure safe — they are the most common wrapper around one.
_HEDGES = _terms(
    r"approximately|approximate|approx|around|about|roughly|typically|usually|generally|"
    r"estimate|estimates|estimated|ballpark|in the region of|more or less|give or take|"
    r"starting from|as low as",
    r"تقريبا|تقريبي|حوالي|حوالى|نحو|عادة|غالبا|بحدود|يتراوح|تتراوح|ابتداء من|في حدود|تقدير",
)

# An adverb between the modal and the verb is the natural way a model phrases this
# ("we can certainly accept"), and it defeated the original pattern. Found by running the
# auditor over a realistic sample, not by review.
_ADVERB = r"(?:certainly|definitely|absolutely|easily|readily|surely|normally|usually|generally|typically|of course)"

_ACCEPTANCE = (
    rf"we (?:can|will|could|would)\s+(?:{_ADVERB}\s+)?(?:handle|ship|accept|take|carry|move|do)|"
    r"yes,? we (?:can|do|will)|that (?:is|'s) (?:fine|no problem|possible|doable)|"
    r"no problem|we accept|it can be shipped|this is acceptable|"
    r"نستطيع (?:شحن|نقل|قبول|تحمل)|يمكننا (?:شحن|نقل|قبول)|نقبل|مقبول|"
    r"لا مشكلة|ممكن شحنها|نعم نستطيع|بالتأكيد نستطيع"
)

_CAPACITY = (
    r"space is available|we have space|equipment is available|we have containers available|"
    r"slot is available|"
    # A guarantee of space is a capacity commitment however it is worded, and "guarantee" is
    # itself a forbidden word in WRITING-STANDARDS §4.
    r"we (?:can )?guarantee|guaranteed?\s+(?:you\s+)?(?:space|a\s+slot|slot|equipment|capacity|booking)|"
    r"يوجد مساحة|المساحة متاحة|لدينا مساحة|الحاويات متوفرة|مضمونة|نضمن"
)

# --------------------------------------------------------------------------------------
# Patterns that must NOT trigger (checked first)
# --------------------------------------------------------------------------------------

_ALLOWLIST = [
    # Container type designations: 20ft, 40', 40HC, 20GP, 40HQ, 45HC
    re.compile(r"\b(?:20|40|45)\s*(?:ft|feet|'|’|dc|gp|hc|hq|rf|ot|fr)\b"),
    # Company history and other four-digit years
    re.compile(r"\b(?:18|19|20)\d{2}\b"),
    # HS codes and tariff headings
    re.compile(r"\bhs\s*code\b|\bتعريفة\s*جمركية\b|\bبند\s*جمركي\b"),
    # UN dangerous-goods numbers
    re.compile(r"\bun\s*\d{4}\b|\bأمم\s*متحدة\s*\d{4}\b"),
    # Phone numbers and extensions
    re.compile(r"\+\d[\d\s\-()]{7,}|\bext\.?\s*\d+\b|\bتحويلة\s*\d+\b"),
    # Document counts: "3 documents", "ثلاث وثائق"
    re.compile(r"\b\d+\s*(?:documents?|copies|originals?|وثائق|نسخ|نسخة|أصول)\b"),
    # Ordered-list markers: "1. ", "2) ", "١. ". MIRA asks its qualifying questions as a
    # numbered list, and normalize() collapses newlines, so "…does not price it. 2. Consignee…"
    # put the digit 2 inside a cost context and blocked a legitimate reply. Found by running
    # real drafted replies through the check, not by review.
    # Deliberately narrow: one or two digits, a period or bracket, then whitespace. A figure
    # like "4500" or "4.500" does not match, so this opens no hole for a rate.
    # The sentence-end class must include the Arabic question mark U+061F and the Arabic
    # full stop, or an Arabic numbered list — "ما هي البضاعة؟ ٢. الوزن…" — fails at the
    # second marker while passing at the first. Caught by an Arabic test case, not by review.
    re.compile(r"(?:(?<=[.!?:;،؛؟۔])|^)\s*\d{1,2}[.)]\s"),
]


def _allowlisted_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for pat in _ALLOWLIST:
        spans.extend(m.span() for m in pat.finditer(text))
    return spans


def _in_allowlist(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(start <= pos < end for start, end in spans)


# --------------------------------------------------------------------------------------
# Rules
# --------------------------------------------------------------------------------------

_NUMBER = r"\d[\d,.]*"
_WINDOW = 60  # characters either side that count as "the same statement"


@dataclass
class Finding:
    rule: str
    excerpt: str
    position: int


@dataclass
class Verdict:
    blocked: bool
    findings: list[Finding] = field(default_factory=list)
    lang: str = "en"

    @property
    def rules(self) -> list[str]:
        return sorted({f.rule for f in self.findings})


def _near(text: str, pos: int, vocab: str, window: int = _WINDOW) -> bool:
    """Is any term from `vocab` within `window` characters of `pos`?"""
    lo, hi = max(0, pos - window), min(len(text), pos + window)
    return re.search(vocab, text[lo:hi]) is not None


def _excerpt(text: str, pos: int, pad: int = 45) -> str:
    lo, hi = max(0, pos - pad), min(len(text), pos + pad)
    return ("…" if lo else "") + text[lo:hi].strip() + ("…" if hi < len(text) else "")


_CARGO_VOCAB = (
    r"\b(?:cargo|ship|ships|shipped|shipping|shipment|shipments|container|containers|"
    r"goods|freight|consignment|pallet|pallets|vessel|cbm|lcl|fcl)\b|"
    r"شحنة|شحن|بضاعة|بضائع|حاوية|حاويات|طرد|طرود"
)


def check_response(text: str, lang: str = "en", context: str = "") -> Verdict:
    """Inspect a candidate MIRA response. Returns a Verdict; `blocked` is the decision.

    `context` is the user's preceding message. It is never scanned for violations — the user
    may say whatever they like — but it establishes that the exchange is about a shipment.
    Without it, a reply like "we can definitely handle that" carries no cargo word of its own
    and slips past the acceptance rule. Pass it wherever it is available.
    """
    if not text or not text.strip():
        return Verdict(blocked=False, lang=lang)

    norm = normalize(text)
    topic_is_shipment = bool(re.search(_CARGO_VOCAB, normalize(context))) if context else False
    allowed = _allowlisted_spans(norm)
    findings: list[Finding] = []

    def record(rule: str, pos: int) -> None:
        findings.append(Finding(rule=rule, excerpt=_excerpt(norm, pos), position=pos))

    # Rule 1 — a monetary amount anywhere.
    # All three orderings occur in freight quoting: "$4500", "4500 USD", and "USD 4500".
    # The last is the most common in this trade, and is the one a naive pattern misses.
    money = (
        rf"(?:{_MONEY_SYMBOL})\s*{_NUMBER}"
        rf"|{_NUMBER}\s*(?:{_MONEY_WORDS})"
        rf"|(?:{_MONEY_WORDS})\s*{_NUMBER}"
    )
    for m in re.finditer(money, norm):
        if not _in_allowlist(m.start(), allowed):
            record("money_amount", m.start())

    # Rule 2 — a bare number in a cost context, or carrying a rate unit.
    for m in re.finditer(_NUMBER, norm):
        if _in_allowlist(m.start(), allowed):
            continue
        if re.match(rf"\s*(?:{_RATE_UNITS})", norm[m.end():m.end() + 30]):
            record("rate_unit", m.start())
        elif _near(norm, m.start(), _COST_WORDS) and not _is_quantity(norm, m.end()):
            record("number_in_cost_context", m.start())

    # Rule 3 — a duration in a transit context.
    for m in re.finditer(rf"{_NUMBER}\s*(?:{_TIME_UNITS})", norm):
        if _in_allowlist(m.start(), allowed):
            continue
        if _near(norm, m.start(), _TRANSIT_WORDS):
            record("transit_time", m.start())

    # Rule 4 — a hedge next to a figure. "roughly 4500" is the classic break.
    # Every number in the window is examined, not just the first: an allowlisted list marker
    # sitting before a real figure would otherwise mask it.
    # The window is deliberately tight. At 40 characters it reached past the hedge's own figure
    # to an unrelated one — "600 porcelain coffee cups, approximately 1.0-1.5 CBM" was blocked
    # on the 600, which counts cups and is nothing to do with the hedge. A hedged price sits
    # right against its number ("roughly 4500", "about 300"), so 20 characters covers the real
    # shape and stops reaching into the rest of the sentence.
    for m in re.finditer(_HEDGES, norm):
        lo, hi = max(0, m.start() - 20), min(len(norm), m.end() + 20)
        for num in re.finditer(_NUMBER, norm[lo:hi]):
            if _in_allowlist(lo + num.start(), allowed):
                continue
            # A unit after the figure, or after the far end of a range it opens ("150-220 kg"),
            # makes it a measurement rather than a price.
            after = norm[lo + num.end():]
            if _is_quantity(norm, lo + num.end()) or re.match(
                    rf"\s*[-–]\s*{_NUMBER}{_QUANTITY_UNIT}", after):
                continue
            record("hedged_figure", m.start())
            break

    # Rule 5 — an acceptance commitment, where the exchange is about a shipment.
    # The subject may be established by the response itself or by what the user just asked.
    for m in re.finditer(_ACCEPTANCE, norm):
        if topic_is_shipment or _near(norm, m.start(), _CARGO_VOCAB):
            record("acceptance_commitment", m.start())

    # Rule 6 — a capacity or space guarantee.
    for m in re.finditer(_CAPACITY, norm):
        record("capacity_commitment", m.start())

    return Verdict(blocked=bool(findings), findings=findings, lang=lang)


# --------------------------------------------------------------------------------------
# Replacement response
# --------------------------------------------------------------------------------------

SAFE_FALLBACK = {
    "en": (
        "That depends on details that change week to week — schedule, carrier space, the "
        "commodity, and whether you need customs clearance and delivery at destination. I don't "
        "give figures myself, because an unchecked number is worse than none.\n\n"
        "I'll put this in front of our team so you get a real answer. Could you tell me:\n"
        "• What's the commodity?\n"
        "• Approximate weight or volume?\n"
        "• Door delivery, or port to port?\n"
        "• When is the cargo ready?"
    ),
    "ar": (
        "هذا يعتمد على تفاصيل تتغيّر من أسبوع لآخر — الجدول، ومساحة الناقل، ونوع البضاعة، وما إذا "
        "كنت تحتاج تخليصاً جمركياً وتسليماً في الوجهة. لا أعطي أرقاماً من عندي، لأن رقماً غير "
        "مُتحقَّق منه أسوأ من لا رقم.\n\n"
        "سأضع طلبك أمام فريقنا لتحصل على جواب حقيقي. هل تخبرني:\n"
        "• ما نوع البضاعة؟\n"
        "• الوزن أو الحجم التقريبي؟\n"
        "• تسليم باب لباب، أم من ميناء إلى ميناء؟\n"
        "• متى تكون البضاعة جاهزة؟"
    ),
}
