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

_MONEY_WORDS = (
    r"usd|u\.s\.d|aed|eur|gbp|sar|syp|dollar|dollars|euro|euros|dirham|dirhams|"
    r"دولار|درهم|يورو|ليرة|ريال"
)
_MONEY_SYMBOL = r"[$€£]|\bد\.إ|\bل\.س"

_RATE_UNITS = (
    r"per\s*(?:kg|kilo|cbm|m3|container|teu|feu|ton|tonne|shipment|unit|pallet)|"
    r"/\s*(?:kg|cbm|m3|20'?|40'?|teu|feu|ton)|"
    r"لكل\s*(?:كيلو|كغ|متر|مكعب|حاوية|طن|شحنة|طبلية)|"
    r"للحاوية|للكيلو|للطن|للمتر"
)

_COST_WORDS = (
    r"cost|costs|price|prices|rate|rates|quote|quotation|charge|charges|fee|fees|"
    r"freight|duty|duties|tax|taxes|tariff|surcharge|demurrage|storage|"
    r"تكلفة|تكاليف|سعر|أسعار|السعر|الأسعار|عرض سعر|رسوم|رسم|أجرة|ضريبة|ضرائب|تعرفة|غرامة|أرضيات"
)

_TIME_UNITS = (
    r"days?|weeks?|months?|hours?|"
    r"يوم|يوما|أيام|يومين|اسبوع|أسبوع|اسابيع|أسابيع|أسبوعين|شهر|شهور|أشهر|شهرين|ساعة|ساعات"
)

_TRANSIT_WORDS = (
    r"transit|transit time|eta|e\.t\.a|arrive|arrival|delivery time|lead time|sailing|"
    r"takes about|takes around|takes approximately|it takes|duration|"
    r"ترانزيت|مدة|المدة|يستغرق|تستغرق|وصول|الوصول|تسليم|التسليم|مده"
)

# Hedges do not make a figure safe — they are the most common wrapper around one.
_HEDGES = (
    r"approximately|approx|around|about|roughly|typically|usually|generally|estimate|estimated|"
    r"ballpark|in the region of|more or less|give or take|starting from|as low as|"
    r"تقريبا|تقريبي|حوالي|حوالى|نحو|عادة|غالبا|بحدود|يتراوح|تتراوح|ابتداء من|في حدود|تقدير"
)

_ACCEPTANCE = (
    r"we can (?:handle|ship|accept|take|carry|move|do)|"
    r"we will (?:handle|ship|accept|take|carry|move)|"
    r"yes,? we (?:can|do|will)|that (?:is|'s) (?:fine|no problem|possible|doable)|"
    r"no problem|we accept|it can be shipped|this is acceptable|"
    r"نستطيع (?:شحن|نقل|قبول|تحمل)|يمكننا (?:شحن|نقل|قبول)|نقبل|مقبول|"
    r"لا مشكلة|ممكن شحنها|نعم نستطيع|بالتأكيد نستطيع"
)

_CAPACITY = (
    r"space is available|we have space|equipment is available|we have containers available|"
    r"guaranteed space|slot is available|"
    r"يوجد مساحة|المساحة متاحة|لدينا مساحة|الحاويات متوفرة|مضمونة"
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


def check_response(text: str, lang: str = "en") -> Verdict:
    """Inspect a candidate MIRA response. Returns a Verdict; `blocked` is the decision."""
    if not text or not text.strip():
        return Verdict(blocked=False, lang=lang)

    norm = normalize(text)
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
        elif _near(norm, m.start(), _COST_WORDS):
            record("number_in_cost_context", m.start())

    # Rule 3 — a duration in a transit context.
    for m in re.finditer(rf"{_NUMBER}\s*(?:{_TIME_UNITS})", norm):
        if _in_allowlist(m.start(), allowed):
            continue
        if _near(norm, m.start(), _TRANSIT_WORDS):
            record("transit_time", m.start())

    # Rule 4 — a hedge next to a figure. "roughly 4500" is the classic break.
    for m in re.finditer(_HEDGES, norm):
        lo, hi = max(0, m.start() - 40), min(len(norm), m.end() + 40)
        num = re.search(_NUMBER, norm[lo:hi])
        if num and not _in_allowlist(lo + num.start(), allowed):
            record("hedged_figure", m.start())

    # Rule 5 — an acceptance commitment near cargo/shipment language.
    for m in re.finditer(_ACCEPTANCE, norm):
        if _near(norm, m.start(), r"cargo|shipment|container|goods|freight|شحنة|بضاعة|حاوية|بضائع"):
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
