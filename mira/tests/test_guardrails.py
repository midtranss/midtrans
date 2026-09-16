"""
Regression suite for MIRA's output guardrails.

Implements the test matrix in ../../docs/standards/MIRA-GUARDRAILS.md §8, plus the
false-positive cases that decide whether the check survives contact with production.

Run:  python3 mira/tests/test_guardrails.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from guardrails import SAFE_FALLBACK, check_response  # noqa: E402

# ---------------------------------------------------------------------------
# MUST BLOCK — a real MIRA saying any of these is a commercial exposure
# ---------------------------------------------------------------------------

MUST_BLOCK = [
    # -- English, direct rate --------------------------------------------------
    ("en", "The rate from Shanghai to Latakia is USD 4500 per 40HC."),
    ("en", "Freight cost is $3,200 for a 20ft container."),
    ("en", "Our price is 2800 USD all in."),
    ("en", "Ocean freight: 1750 per container, plus local charges."),

    # -- English, hedged: the phrasing that breaks unguarded systems -----------
    ("en", "I can't quote exactly, but expect roughly 4000 dollars."),
    ("en", "Rates are typically around USD 3500 these days."),
    ("en", "Just as a ballpark, somewhere near 5000."),
    ("en", "Starting from USD 2,400 depending on the season."),
    ("en", "Give or take, the cost would be about 3000."),

    # -- English, transit time -------------------------------------------------
    ("en", "Transit time is about 28 days from Shanghai."),
    ("en", "It usually takes 3 weeks to arrive at Latakia."),
    ("en", "Expect delivery in approximately 20 days."),

    # -- English, customs cost -------------------------------------------------
    ("en", "Customs duty will be around 15 percent, so roughly 900 USD."),
    ("en", "Clearance fees are 350 AED per shipment."),

    # -- English, acceptance and capacity -------------------------------------
    ("en", "Yes, we can handle that hazardous cargo to Tartous without any issue."),
    ("en", "No problem, we accept this shipment."),
    ("en", "We have space available on next week's vessel."),
    ("en", "Guaranteed space for your containers."),

    # -- Arabic, direct --------------------------------------------------------
    ("ar", "سعر الشحن من شنغهاي إلى اللاذقية هو 4500 دولار للحاوية."),
    ("ar", "التكلفة 3200 دولار لحاوية 20 قدم."),
    ("ar", "الأجرة 2800 دولار شاملة."),

    # -- Arabic, hedged --------------------------------------------------------
    ("ar", "لا أستطيع التسعير بدقة لكن تقريبا 4000 دولار."),
    ("ar", "الأسعار عادة حوالي 3500 دولار."),
    ("ar", "بحدود 5000 دولار تقريبا."),
    ("ar", "تتراوح التكلفة بين 3000 و 4000 دولار."),

    # -- Arabic, transit -------------------------------------------------------
    ("ar", "مدة الشحن حوالي 28 يوم من شنغهاي."),
    ("ar", "يستغرق الوصول 3 أسابيع تقريبا."),
    ("ar", "التسليم خلال 20 يوما."),

    # -- Arabic, Arabic-Indic digits ------------------------------------------
    ("ar", "السعر ٤٥٠٠ دولار للحاوية."),
    ("ar", "المدة ٢٨ يوم للوصول."),

    # -- Arabic, acceptance ----------------------------------------------------
    ("ar", "نعم نستطيع شحن هذه البضاعة الخطرة بدون مشكلة."),
    ("ar", "لا مشكلة، نقبل هذه الشحنة."),
]

# ---------------------------------------------------------------------------
# MUST NOT BLOCK — legitimate answers. A check that fails these gets disabled,
# and a disabled check protects nothing.
# ---------------------------------------------------------------------------

MUST_PASS = [
    # -- The correct refusal itself -------------------------------------------
    ("en", SAFE_FALLBACK["en"]),
    ("ar", SAFE_FALLBACK["ar"]),
    ("en", "I don't quote rates. Our pricing desk works from live carrier data — "
           "shall I pass your enquiry to them?"),
    ("ar", "لا أعطي أسعاراً. فريق التسعير لدينا يعمل على بيانات حيّة — هل أحوّل طلبك إليهم؟"),

    # -- Company facts with years ---------------------------------------------
    ("en", "MIDTRANS has operated from Damascus since 1998."),
    ("ar", "تعمل ميدترانس من دمشق منذ عام 1998."),
    ("en", "We opened the Dubai office in 2010 and Jebel Ali operations in 2014."),

    # -- Container designations ------------------------------------------------
    ("en", "A 40HC container has more internal height than a 40ft standard."),
    ("en", "We handle 20ft, 40ft and 40HC equipment, plus LCL consolidation."),
    ("ar", "نتعامل مع حاويات 20 قدم و 40 قدم و 40 هاي كيوب."),

    # -- Document counts -------------------------------------------------------
    ("en", "You'll need 3 documents: commercial invoice, packing list, and bill of lading."),
    ("ar", "تحتاج 3 وثائق: الفاتورة التجارية وقائمة التعبئة وبوليصة الشحن."),

    # -- HS codes and UN numbers -----------------------------------------------
    ("en", "The HS code determines the tariff classification for your goods."),
    ("en", "For dangerous goods, please provide the UN 1210 classification and the MSDS."),
    ("ar", "للبضائع الخطرة نحتاج رقم الأمم المتحدة وصحيفة بيانات السلامة."),

    # -- Contact details -------------------------------------------------------
    ("en", "You can reach our Dubai office on +971 4 2714480 ext. 100."),

    # -- Explaining cost drivers without values -------------------------------
    ("en", "Freight cost is driven by the commodity, the equipment type, the carrier's current "
           "space situation, and whether you need door delivery."),
    ("ar", "تتأثر تكلفة الشحن بنوع البضاعة ونوع الحاوية ووضع المساحة لدى الناقل وما إذا كنت "
           "تحتاج تسليماً باب لباب."),

    # -- Procedure, no figures -------------------------------------------------
    ("en", "Customs clearance at Latakia begins once the carrier releases the manifest. "
           "Your clearing agent then submits the declaration."),
    ("ar", "يبدأ التخليص الجمركي في اللاذقية بعد أن يُفرج الناقل عن البيان، ثم يقدّم مخلّصك "
           "التصريح الجمركي."),

    # -- AI disclosure ---------------------------------------------------------
    ("en", "I'm MIRA, MIDTRANS's AI assistant — not a member of staff."),
    ("ar", "أنا ميرا، المساعد الذكي لميدترانس — لست موظفة."),

    # -- Out-of-scope decline --------------------------------------------------
    ("en", "That's outside what I can help with — I handle shipping, customs and trade "
           "questions for MIDTRANS."),

    # -- Empty / whitespace ----------------------------------------------------
    ("en", ""),
    ("en", "   "),
]


def main() -> int:
    failures = []

    for lang, text in MUST_BLOCK:
        v = check_response(text, lang=lang)
        if not v.blocked:
            failures.append(("MISSED (should block)", lang, text, ""))

    for lang, text in MUST_PASS:
        v = check_response(text, lang=lang)
        if v.blocked:
            failures.append(("FALSE POSITIVE (should pass)", lang, text, ",".join(v.rules)))

    total = len(MUST_BLOCK) + len(MUST_PASS)
    passed = total - len(failures)

    print(f"MIRA guardrail suite: {passed}/{total} passed")
    print(f"  must-block cases: {len(MUST_BLOCK)}")
    print(f"  must-pass cases:  {len(MUST_PASS)}")

    if failures:
        print(f"\n{len(failures)} FAILURE(S):\n")
        for kind, lang, text, rules in failures:
            snippet = text[:80].replace("\n", " ")
            print(f"  [{kind}] ({lang}) {snippet}")
            if rules:
                print(f"      triggered: {rules}")
        return 1

    print("\nAll cases pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
