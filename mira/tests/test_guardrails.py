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
    # Currency-before-number is the most common form in freight quoting, and the one a
    # naive pattern misses. This case was added after it slipped through in testing.
    ("en", "The rate from Shanghai to Latakia is USD 4500 per 40HC."),
    ("en", "AED 350 per shipment for clearance."),
    ("en", "EUR 1,900 door to door."),
    ("ar", "دولار 4500 للحاوية."),
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



# --------------------------------------------------------------------------------------
# Regressions found by running audit_logs.py over a realistic sample rather than by review.
# Each of these passed the check before 2026-09-16.
# --------------------------------------------------------------------------------------

MUST_BLOCK += [
    # An adverb between the modal and the verb defeated the acceptance pattern.
    ("en", "We can certainly accept that shipment."),
    ("en", "We would readily take that cargo."),
    ("en", "We will definitely move your consignment."),
    # A guarantee of space, worded actively rather than as "guaranteed space".
    ("en", "We guarantee space on next week's vessel."),
    ("en", "We can guarantee a slot for you."),
    ("ar", "نضمن لك مكاناً على الباخرة."),
]

MUST_PASS += [
    # Ordered-list markers are numbers. MIRA asks its qualifying questions as a numbered list,
    # and normalize() collapses newlines, so a marker landed inside a cost context and blocked
    # a legitimate reply. Found by running real drafted replies through the check.
    ("en", "To price this we need four things: 1. Gross weight per vehicle. 2. Invoice value, "
           "since insurance is rated on it. 3. Consignee in Syria. 4. Ready date."),
    ("en", "Two things would help now: 1. approximate number of pallets, a range is fine. "
           "2. approximate value of the consignment, for insurance."),
    ("en", "1) What is the commodity? 2) Approximate weight? 3) Door delivery or port to port?"),
    ("ar", "نحتاج أربعة أمور: 1. مدينة الموردين في الصين. 2. الوزن الإجمالي التقريبي. "
           "3. المرسل إليه في سوريا. 4. التاريخ التقريبي للجهوزية."),
    ("ar", "١. ما هي البضاعة؟ ٢. الوزن التقريبي؟ ٣. تسليم للباب أم من مرفأ إلى مرفأ؟"),
]

MUST_BLOCK += [
    # And the allowlist must not become a way to smuggle a figure past the check.
    ("en", "1. The rate is USD 4500. 2. Transit is 22 days."),
    ("en", "Our best guess: 1. it is about 3200 dollars."),
    ("en", "It depends. 4500 USD for a 40HC."),
    ("ar", "1. السعر حوالي 3200 دولار. 2. المدة 25 يوما."),
]

# Cases where the subject of the reply lives in the user's question, not the reply itself.
# check_response takes the preceding user turn as `context`; it is never scanned itself.
# --------------------------------------------------------------------------------------
# 2026-09-16 — the word lists matched inside longer words
#
# Found by running the content gate over the real MIDTRANS homepage, not by review. The lists
# were plain alternations with no boundaries, so:
#
#   "United Arab Emi-RATE-s"      a cost word — THE COMPANY'S OWN ADDRESS, on every page
#   "600 porcelain cof-FEE cups"  a cost word — an enquiry already in the register
#   "the deta-ETA-ils"            a transit word — in nearly every freight email written
#   "needed to-DAY-"              a time unit — in the Sprinters enquiry, verbatim
#   "beurteilen" / "importeur"    EUR, a currency — ordinary German, and one enquiry is German
#
# A rule that blocks a company's own address is not strict, it is broken, and §8a records where
# that leads: the check gets switched off and then protects nothing.
#
# Two further shapes came out of the same pass. A number carrying a PHYSICAL unit is a quantity,
# not a price — cargo is always described in approximations, and every one of these is quoted
# from a real enquiry. And the hedge window at 40 characters reached past its own figure to an
# unrelated one.

MUST_PASS += [
    # The company's own contact details.
    ("en", "Our Dubai office is in Deira, Port Saeed, United Arab Emirates, office 611."),
    ("en", "Tel: +97142714480/1  Mob: +971552928560"),
    # Ordinary English that happens to contain a cost or transit word.
    ("en", "We operate 3 weekly departures."),
    ("en", "Please send 4 separate packing lists."),
    ("en", "Please confirm the 2 details below and the 3 retail SKUs."),
    ("en", "Accurate figures for 2 pallets, please."),
    ("en", "The quote is needed today for 6 vehicles."),
    # Cargo described the way cargo is always described — hedged measurements.
    ("en", "600 porcelain Turkish coffee cups, approximately 1.0-1.5 CBM."),
    ("en", "Approx. dimensions per vehicle: 6.97 m x 2.02 m x 2.62 m"),
    ("en", "150-220 kg gross, roughly 1200 kg in total."),
    ("en", "Estimated cargo: approximately 1.0-1.5 CBM and 150-220 kg gross"),
    ("ar", "الكمية حوالي 5 أمتار مكعبة و 200 كغ."),
    # Arabic: رسم is a fee, رسمي is "official". The drafts and this suite both contain it.
    ("ar", "أرسلوا لنا كتاباً رسمياً بهذا خلال 3 أيام."),
    # German — one enquiry in the register is in German, and "eur" sits inside both of these.
    ("en", "Wir bitten um Ihre Beurteilung als Importeur von 2 Fahrzeugen."),
]

MUST_BLOCK += [
    # Everything above had to stop working WITHOUT any of these starting to leak.
    ("en", "It is roughly 4500 all in."),
    ("en", "The all-in is approximately 3,800."),
    ("en", "The clearance fee is about 300."),
    ("en", "Storage is about 25 per day after free time."),
    ("en", "Approximately 950 USD per CBM."),
    ("en", "It usually takes around 15 days to arrive."),
    ("en", "Transit time is approximately 18 days."),
]

MUST_BLOCK_IN_CONTEXT = [
    ("en", "We can definitely handle that.", "Can you ship chemicals to Syria?"),
    ("en", "Yes, we can. No problem at all.", "Do you move pallets from Jebel Ali?"),
    ("ar", "نعم نستطيع، لا مشكلة.", "هل تستطيعون شحن بضاعة من الصين؟"),
]

MUST_PASS_IN_CONTEXT = [
    # The user's own words are not MIRA's commitment, whatever they contain.
    ("en", "I'll put this to our team and come back to you.",
     "Is the rate USD 4500 per container and 22 days transit?"),
    ("ar", "سأعرض هذا على فريقنا وأعود إليك.", "هل السعر 4500 دولار والمدة 22 يوماً؟"),
    # A shipment subject does not make every helpful sentence a commitment.
    ("en", "Our team reviews each request before confirming anything.",
     "Can you ship my cargo next week?"),
    ("en", "The documents usually needed are an invoice, a packing list and a bill of lading.",
     "What do I need to ship goods to Damascus?"),
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

    for lang, text, ctx in MUST_BLOCK_IN_CONTEXT:
        v = check_response(text, lang=lang, context=ctx)
        if not v.blocked:
            failures.append(("MISSED IN CONTEXT (should block)", lang, text, ctx))

    for lang, text, ctx in MUST_PASS_IN_CONTEXT:
        v = check_response(text, lang=lang, context=ctx)
        if v.blocked:
            failures.append(("FALSE POSITIVE IN CONTEXT", lang, text, ",".join(v.rules)))

    total = (len(MUST_BLOCK) + len(MUST_PASS)
             + len(MUST_BLOCK_IN_CONTEXT) + len(MUST_PASS_IN_CONTEXT))
    passed = total - len(failures)

    print(f"MIRA guardrail suite: {passed}/{total} passed")
    print(f"  must-block cases: {len(MUST_BLOCK)}")
    print(f"  must-pass cases:  {len(MUST_PASS)}")
    print(f"  with conversation context: "
          f"{len(MUST_BLOCK_IN_CONTEXT)} block / {len(MUST_PASS_IN_CONTEXT)} pass")

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
