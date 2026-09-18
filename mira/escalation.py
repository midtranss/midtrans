#!/usr/bin/env python3
"""
Escalation triggers — hand the conversation to a human.

This implements `../docs/standards/MIRA-GUARDRAILS.md` §6, which was documented but not built.
Phase 06 depends on it: a P&I or maritime enquirer raising a claim, an incident, or coverage is
exactly the conversation MIRA must not hold.

**Escalation is a different decision from blocking.** `guardrails.check_response` inspects what
MIRA is about to say and suppresses it. This inspects what the **customer** said and routes the
conversation. A customer may say anything; the question is only whether a person should take over.

The customer's text is never treated as a violation. Nothing here is MIRA's fault, and nothing
here is recorded against MIRA's guardrail record.

Two properties are deliberate:

* **Fail loud, not quiet.** A missed escalation means MIRA answers a claims question on its own.
  The patterns are therefore broad, and §5 of the phase document records the precision cost so
  MIDTRANS can tighten them against real traffic rather than against a guess.
* **The repeat trigger needs history.** §6's first trigger is "any prohibited category asked
  twice", which cannot be seen in a single message. `detect()` takes the conversation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from guardrails import normalize


# --------------------------------------------------------------------------------------
# §6, trigger by trigger
# --------------------------------------------------------------------------------------

TRIGGERS = {
    # "Claim, damage, loss, incident, or insurance language."
    "claim_or_incident": (
        r"\bclaim(?:s|ed|ing)?\b|\bdamag(?:e|ed|es)\b|\bshort[- ]?(?:age|landed|shipped)\b|\bloss\b|"
        r"\blost\b|\bstolen\b|\btheft\b|\bpilferage\b|\bincident\b|\bcasualt(?:y|ies)\b|"
        r"\binsur(?:ance|ed|er|ers)\b|\bp\s*&\s*i\b|\bunderwriter\b|\bsurvey report\b|"
        r"\bgeneral average\b|\bsalvage\b|\bcollision\b|\bgrounding\b|\bliab(?:le|ility)\b|"
        r"\bcover(?:age|ed)\b|\bpolicy\b|\bdeductible\b|\bsubrogat|"
        r"مطالب(?:ة|ات)|ضرر|تضرر|تلف|فقدان|مفقود|سرق|حادث|تأمين|مؤمن|مسؤولي(?:ة|ات)|تغطية|بوليصة تأمين"
    ),
    # "Sanctions, compliance, restricted party, or legal exposure language."
    "legal_exposure": (
        r"\bsanction(?:s|ed|ing)?\b|\bembargo\b|\bofac\b|\brestricted part|\bdenied part|"
        r"\bexport control\b|\bdual[- ]use\b|\bcomplian(?:ce|t)\b|\blawyer\b|\battorney\b|"
        r"\blegal action\b|\bcourt\b|\blitigat|\barbitrat|\bsue\b|\bsuing\b|\bprosecut|"
        # "Is this allowed?" — the question a customer actually asks a Syria forwarder, and a
        # determination MIRA must never make. Found by testing this module against live traffic:
        # "can you ship to a consignee in Syria under current restrictions?" escaped every
        # other pattern here, and one enquiry in the register asks it almost word for word
        # ("whether there are any restrictions I should be aware of" — 2026-08-10-galvanic-eu).
        #
        # "Restriction" is also the word for an axle-load limit. A check that escalates "what
        # are the weight restrictions?" is a check somebody switches off, and a switched-off
        # check protects nothing — MIRA-GUARDRAILS §8a, learned the same way. So the trade
        # senses are enumerated rather than matching the bare word: a physical qualifier sits
        # between "any" and "restrictions" and no alternative fires.
        r"\b(?:trade|import|export|shipping|shipment|customs|banking|payment|current|any)\s+"
        r"restrictions?\b|"
        r"\brestrictions?\s+(?:on|for)\s+(?:ship|import|export|send|cargo|goods|brand|"
        r"product|commodit)|"
        # Known and accepted over-trigger: "is the vessel allowed to berth at night?" escalates,
        # and that is a port-hours question, not a legal one. It stands, because escalation and
        # blocking fail in opposite directions. An over-escalation costs a colleague a glance;
        # an over-block gags a legitimate answer, and MIRA-GUARDRAILS §8a records what that
        # leads to — a check somebody switches off, protecting nothing. The precision bar here
        # is therefore lower than the output guardrail's, deliberately. Note also that the
        # near-identical "is the vessel allowed to call at Latakia?" IS a sanctions question,
        # so the ambiguity is in the trade, not in the pattern.
        #
        # Up to two words may sit between the subject and the verb — "are these goods
        # permitted", "is this commodity allowed" — which is how the question is actually put.
        r"\b(?:is|are)\s+(?:it|this|these|they|there|the)\s+(?:\w+\s+){0,2}"
        r"(?:prohibited|banned|forbidden|permitted|allowed)\b|"
        r"\b(?:prohibited|banned|forbidden)\s+(?:goods|items|products|cargo|to\s+\w+)\b|"
        r"عقوبات|حظر|امتثال|محام|قضائ|محكمة|تحكيم|مقاضاة|"
        r"قيود\s*(?:على|تجاري|الاستيراد|التصدير|الشحن)|"
        r"(?:ممنوع|محظور|مسموح)\s*(?:استيراد|تصدير|شحن|إدخال|إرسال)"
    ),
    # "Named dispute, complaint, or dissatisfaction with MIDTRANS."
    "dispute": (
        r"\bcomplain(?:t|ts|ing)?\b|\bdissatisf|\bunacceptable\b|\bunhappy\b|"
        r"\bnot happy\b|\bdisappointed\b|\brefund\b|\bcompensat|\bdispute\b|"
        r"\bspeak to (?:a |your )?(?:manager|supervisor|someone senior)\b|"
        r"\bescalate\b|\bnegligen|\byour fault\b|\blet me down\b|"
        r"شكوى|أشتكي|غير راض|غير مقبول|مستاء|تعويض|استرداد|نزاع|إهمال|مسؤولكم|خطؤكم"
    ),
    # "Cargo described as dangerous, perishable, live, or high-value."
    "special_cargo": (
        r"\bdangerous goods\b|\bhazardous\b|\bimo class\b|\bun\s?\d{4}\b|\bmsds\b|\bsds\b|"
        r"\bexplosive|\bflammable|\bcorrosive|\btoxic\b|\bradioactive\b|"
        r"\bperishable\b|\breefer\b|\btemperature[- ]controlled\b|\bcold chain\b|"
        r"\blive animals?\b|\blivestock\b|\bhigh[- ]value\b|\bvaluables?\b|\bbullion\b|"
        r"\bpharmaceutical|\bnarcotic|\bweapons?\b|\bammunition\b|"
        r"بضائع خطرة|مواد خطرة|قابل للاشتعال|سام|مشع|متفجر|قابل للتلف|مبرد|سلسلة تبريد|"
        r"حيوانات حية|ثمين|أدوية|أسلحة|ذخيرة"
    ),
    # "Government, tender, or institutional buyer identifying themselves."
    "institutional_buyer": (
        r"\bministr(?:y|ies)\b|\bgovernment\b|\bgovernmental\b|\bembassy\b|\bconsulate\b|"
        r"\bmunicipalit|\bpublic sector\b|\btender\b|\bprocurement\b|\brfp\b|\bbid bond\b|"
        r"\bunited nations\b|\bunhcr\b|\bunicef\b|\bwfp\b|\bicrc\b|\bred cross\b|\bngo\b|"
        r"وزارة|حكوم|سفارة|قنصلية|بلدية|قطاع عام|مناقصة|عطاء|الأمم المتحدة|منظمة غير حكومية"
    ),
    # "Any request for a written confirmation or document MIRA would have to author."
    "document_request": (
        r"\b(?:send|give|issue|provide|write|draft|sign)\s+(?:me\s+|us\s+)?"
        r"(?:a|an|the)?\s*(?:written\s+)?"
        r"(?:confirmation|letter|certificate|undertaking|guarantee letter|declaration|"
        r"statement|attestation|reference|quotation in writing|letterhead)\b"
        r"|\bin writing\b|\bon (?:your )?letterhead\b|\bofficial (?:letter|document)\b|"
        r"\bconfirm (?:this |that )?in writing\b|"
        r"خطابا?\s+رسميا?|كتابا?\s+رسميا?|تأكيدا?\s+خطيا?|شهادة|تعهد|إفادة|على ورق رسمي|خطيا"
    ),
}

# Prohibited-category requests, for §6's "asked twice" trigger. These describe what the CUSTOMER
# is asking for — not what MIRA said — so they are separate from guardrails.py's response rules.
PROHIBITED_REQUEST = (
    r"\bhow much\b|\bwhat(?:'s| is| are)? the (?:rate|price|cost|charge|fee)\b|"
    r"\bquote\b|\bquotation\b|\bpricing\b|\bprice\b|\bcost\b|\bcharges?\b|\btariff\b|"
    r"\bhow long\b|\bhow many days\b|\btransit time\b|\btransit\b|\beta\b|\bwhen will it arrive\b|"
    r"\bcan you (?:take|accept|carry|handle|ship)\b|\bdo you have space\b|\bis there space\b|"
    r"كم (?:سعر|تكلفة|يكلف|تكلف|يستغرق|المدة)|سعر|تكلفة|كلفة|أجرة|عرض سعر|كم يوم|"
    r"مدة الشحن|متى تصل|هل تقبلون|هل يوجد مساحة|هل تستطيعون شحن"
)


@dataclass
class Trigger:
    name: str
    excerpt: str
    turn: int


@dataclass
class Escalation:
    escalate: bool
    triggers: list = field(default_factory=list)

    @property
    def names(self) -> list:
        return sorted({t.name for t in self.triggers})

    def __bool__(self) -> bool:
        return self.escalate


HANDOVER = {
    "en": (
        "This needs one of our people rather than me. I'm passing it to the team now, with "
        "what you've told me so far, so you don't have to repeat it.\n\n"
        "If it's urgent, our contact details are on the contact page — say so in your message "
        "and it will be treated that way."
    ),
    "ar": (
        "هذا يحتاج أحد زملائي لا أنا. أُحيله إلى الفريق الآن مع ما ذكرته، حتى لا تضطرّ "
        "لإعادته.\n\n"
        "وإن كان الأمر عاجلاً، بيانات التواصل في صفحة الاتصال — اذكر ذلك في رسالتك "
        "ليُعامَل على هذا الأساس."
    ),
}


def _excerpt(text: str, position: int, pad: int = 45) -> str:
    start, end = max(0, position - pad), min(len(text), position + pad)
    return " ".join(text[start:end].split())


def detect(messages, repeat_threshold: int = 2) -> Escalation:
    """Scan a conversation's USER turns for §6's triggers.

    `messages` is a sequence of {"role": ..., "content": ...} in order. Assistant turns are
    ignored: MIRA quoting a customer's word back is not a customer raising it.
    """
    triggers: list = []
    prohibited_asks = 0

    for index, message in enumerate(messages or []):
        if message.get("role") != "user":
            continue

        content = message.get("content", "")
        if isinstance(content, list):
            content = "\n".join(
                block.get("text", "")
                for block in content
                if isinstance(block, dict) and block.get("type") == "text"
            )
        if not isinstance(content, str) or not content.strip():
            continue

        norm = normalize(content)

        for name, pattern in TRIGGERS.items():
            match = re.search(pattern, norm)
            if match:
                triggers.append(Trigger(name, _excerpt(norm, match.start()), index))

        if re.search(PROHIBITED_REQUEST, norm):
            prohibited_asks += 1

    if prohibited_asks >= repeat_threshold:
        triggers.append(Trigger(
            "repeat_prohibited",
            f"a prohibited category was asked {prohibited_asks} times",
            -1))

    return Escalation(escalate=bool(triggers), triggers=triggers)


def handover(lang: str = "en") -> str:
    return HANDOVER.get(lang, HANDOVER["en"])
