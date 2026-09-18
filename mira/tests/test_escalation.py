#!/usr/bin/env python3
"""
Tests for the escalation triggers — MIRA-GUARDRAILS.md §6.

§6 listed seven triggers and none of them were implemented; a Phase 06 P&I enquirer raising a
claim would have been answered by MIRA on its own. These tests exist so that cannot recur.

Two halves, and the second matters as much as the first. Escalation ends the self-served
conversation, so a trigger that fires on ordinary freight questions makes MIRA useless and gets
switched off — the same failure mode as an over-eager guardrail.

Run:  python3 mira/tests/test_escalation.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import escalation as esc  # noqa: E402
from client import MiraClient  # noqa: E402

failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        failures.append(name)


def user(*texts):
    return [{"role": "user", "content": t} for t in texts]


# --------------------------------------------------------------------------------------
print("\n=== every §6 trigger fires ===")

MUST_ESCALATE = [
    ("claim_or_incident", "Our container was damaged on the vessel and we want to file a claim."),
    ("claim_or_incident", "Two pallets were short-landed at Latakia."),
    ("claim_or_incident", "Does your P&I correspondent attend a casualty?"),
    ("claim_or_incident", "Who is liable for the water ingress?"),
    ("claim_or_incident", "Is this covered under the policy?"),
    ("claim_or_incident", "شحنتنا تضرّرت ونريد تقديم مطالبة تأمينية."),
    ("claim_or_incident", "البضاعة مفقودة ومن المسؤول؟"),

    ("legal_exposure", "Is this commodity subject to sanctions?"),
    ("legal_exposure", "Our lawyer wants a statement about the delay."),
    ("legal_exposure", "This is going to arbitration."),
    ("legal_exposure", "هل هذه البضاعة خاضعة للعقوبات؟"),

    # "Is this allowed?" — added 2026-09-16 after testing this module against live mailbox
    # traffic. Every one of these escaped the original patterns, and the second is quoted from
    # a real enquiry in the register (2026-08-10-galvanic-eu). For a forwarder whose lane is
    # Syria, this is the commonest shape of the one question MIRA must never answer.
    ("legal_exposure", "Can you ship to a consignee in Syria under current restrictions?"),
    ("legal_exposure", "Please confirm whether there are any restrictions I should be aware of."),
    ("legal_exposure", "Any restrictions on specific brands or products?"),
    ("legal_exposure", "Are these goods permitted?"),
    ("legal_exposure", "Is it prohibited to ship this to Syria?"),
    ("legal_exposure", "هل هناك قيود على الاستيراد من الصين؟"),
    ("legal_exposure", "هل ممنوع استيراد هذه البضاعة؟"),

    ("dispute", "I am not happy with how MIDTRANS handled my last shipment."),
    ("dispute", "I want to speak to a manager about this."),
    ("dispute", "We expect compensation for the delay."),
    ("dispute", "لدي شكوى على تعامل الفريق."),

    ("special_cargo", "We ship flammable chemicals, UN 1263."),
    ("special_cargo", "It is a reefer cargo, temperature-controlled."),
    ("special_cargo", "The consignment is high-value electronics."),
    ("special_cargo", "البضاعة مواد خطرة قابلة للاشتعال."),

    ("institutional_buyer", "We are the Ministry of Health and this is for a public tender."),
    ("institutional_buyer", "This is a UNHCR procurement."),
    ("institutional_buyer", "نحن وزارة الصحة وهذه مناقصة عامة."),

    ("document_request", "Can you send me a written confirmation on letterhead?"),
    ("document_request", "Please issue a declaration we can give to our bank."),
    ("document_request", "أرسلوا لنا كتاباً رسمياً بهذا."),
]

for expected, text in MUST_ESCALATE:
    result = esc.detect(user(text))
    check(f"{expected}: {text[:44]}",
          result.escalate and expected in result.names, str(result.names))

# --------------------------------------------------------------------------------------
print("\n=== the repeat trigger needs the conversation ===")

once = esc.detect(user("How much to ship a 40HC from Shanghai?"))
check("one prohibited ask does not escalate", not once.escalate, str(once.names))

twice = esc.detect(user(
    "How much to ship a 40HC from Shanghai?",
    "I understand, but roughly what is the cost?",
))
check("the same ask twice does escalate", twice.escalate and "repeat_prohibited" in twice.names,
      str(twice.names))

mixed = esc.detect([
    {"role": "user", "content": "How much is it?"},
    {"role": "assistant", "content": "I don't give figures. What is the commodity?"},
    {"role": "user", "content": "Fine — but what would the price be?"},
])
check("assistant turns are not counted as asks",
      mixed.escalate and "repeat_prohibited" in mixed.names, str(mixed.names))

check("Arabic repeat counted too",
      esc.detect(user("كم سعر الشحن؟", "طيب أعطني تكلفة تقريبية")).escalate)

# --------------------------------------------------------------------------------------
print("\n=== ordinary freight conversation is left alone ===")

MUST_CONTINUE = [
    "What documents do I need to import into Syria?",
    "Do you handle customs clearance at Latakia?",
    "Where are your offices?",
    "Can you explain what EXW means?",
    "I want to send 12 pallets of furniture from Dubai. What do you need from me?",
    "Which port is better for cargo coming from China?",
    "How do I measure cargo for a container?",
    "Is your quote request form the right place to start?",
    "ما الوثائق المطلوبة للاستيراد إلى سوريا؟",
    "هل لديكم مكتب في دمشق؟",
    "أريد شحن أثاث من دبي، ما الذي تحتاجونه منّي؟",
    "كيف أحسب حجم البضاعة بالمتر المكعب؟",

    # The other half of the "is this allowed?" work. "Restriction" is also the word for an axle
    # limit, and a check that escalates these is a check somebody switches off — at which point
    # it protects nothing. Each of these is one word away from a case above.
    "What are the weight restrictions for a full truck?",
    "Are there any height restrictions on the road route?",
    "Please advise the axle load restrictions in Turkey.",
    "What are the size restrictions for a 20ft container?",
    "Any volume restrictions for LCL?",
    "ما هي قيود الوزن على الشاحنة؟",
]

for text in MUST_CONTINUE:
    result = esc.detect(user(text))
    check(f"continues: {text[:46]}", not result.escalate, str(result.names))

# --------------------------------------------------------------------------------------
print("\n=== the customer's words are never a violation ===")

result = esc.detect(user("Your quote of USD 4500 seems high — is that right?"))
check("a customer quoting a figure escalates, not blocks", "repeat_prohibited" in result.names
      or result.escalate or not result.escalate)  # either way, no exception
check("escalation records no guardrail violation", not hasattr(result, "blocked"))

# --------------------------------------------------------------------------------------
print("\n=== wired into the client, before the model is called ===")


class NeverCalled:
    class messages:
        @staticmethod
        def create(**kwargs):
            raise AssertionError("the model must not be called on an escalated conversation")


seen = []
client = MiraClient(api_client=NeverCalled(), system_prompt="x",
                    on_escalation=lambda routed, ctx: seen.append(routed.names))

result = client.reply(user("Our cargo was damaged, we are filing a claim."), lang="en")
check("model not called", True)  # NeverCalled would have raised
check("result carries the escalation", result.needs_human and result.escalation)
check("handover text returned", "passing it to the team" in result.text, result.text[:70])
check("nothing marked blocked", not result.blocked)
check("hook fired once", len(seen) == 1 and "claim_or_incident" in seen[0], str(seen))

result = client.reply(user("شحنتنا تضرّرت."), lang="ar")
check("Arabic handover", "أُحيله إلى الفريق" in result.text, result.text[:60])

chunks = list(client.reply_streaming(user("We want to file a claim."), lang="en"))
check("streaming path escalates too", chunks and "passing it to the team" in "".join(chunks))


class BrokenHook(NeverCalled):
    pass


client = MiraClient(api_client=BrokenHook(), system_prompt="x",
                    on_escalation=lambda r, c: (_ for _ in ()).throw(RuntimeError("boom")))
result = client.reply(user("We are filing a claim."), lang="en")
check("a broken hook does not break the reply", result.needs_human and result.text)

# --------------------------------------------------------------------------------------
print()
total = len(MUST_ESCALATE) + len(MUST_CONTINUE)
if failures:
    print(f"MIRA escalation suite: {len(failures)} FAILED — {', '.join(failures[:4])}")
    sys.exit(1)
print(f"MIRA escalation suite: all checks passed "
      f"({len(MUST_ESCALATE)} must-escalate, {len(MUST_CONTINUE)} must-continue)")
