# D4 — Feature Inventory

**Owner:** _________  **Date:** _________

> Verdict is one of: **Keep** · **Fix** · **Rebuild** · **Retire**.
> **Nothing is retired without explicit written approval.**

| Feature | Exists? | Works? | Monthly usage | Produces enquiries? | Verdict | Notes |
|---|---|---|---|---|---|---|
| Loading Calculator | | | | | | |
| Container Calculator | | | | | | |
| CBM Calculator | | | | | | |
| Volumetric Weight Calculator | | | | | | |
| Commercial Invoice Builder | | | | | | |
| Shipment Tracker | | | | | | |
| MIRA chatbot | | | | | | |
| RFQ / quote form | | | | | | |
| WhatsApp contact | | | | | | |
| Consultation booking | | | | | | |
| Language switcher | | | | | | |
| Blog / knowledge center | | | | | | |

## Pages that already rank and convert — **protect these**

| Page | Language | Organic entrances | Conversions | Note |
|---|---|---|---|---|
| | | | | |

> Phase 01 strengthens these pages. It does not replace or restructure them without evidence.

## MIRA current state (if deployed)

| Item | Finding |
|---|---|
| Deployed? On which pages? | |
| Underlying model / platform | |
| Knowledge source | |
| **Any guardrails currently in place?** | |
| **Has it ever stated a rate, transit time, or acceptance?** | |
| Conversation logs available? | |
| Languages supported | |

> If MIRA is live with no guardrails, that is an **active commercial exposure**, not a Phase 02
> item. Report it immediately to the programme owner.

---

## Partial findings from D3 (2026-09-16) — email evidence only, not verified in code

These came out of the D3 mailbox analysis. They are **indirect evidence** and must be confirmed
against the codebase in D1 before being treated as established.

| Feature | Evidence | Provisional verdict |
|---|---|---|
| **RFQ wizard** | Live. Sequential `QREQ-` references, auto-acknowledgement to the enquirer, structured notification to a named internal list. First submission 11 Sep 2026. | **Keep** — this is the Phase 01 foundation, not a rebuild |
| **Website chat widget** | Live. Observed relaying a visitor message to email, answered manually by named MIDTRANS staff in English and Arabic. | Keep; instrument it |
| **Older website form** | Superseded by the wizard. Structured-field format, ~5 submissions in 12 months. | Retire **only** after the wizard proves itself — needs approval |
| **Customer account / login** | Live. A password-reset flow was observed, including a bilingual EN/AR notice. | Investigate in D1 — scope and purpose unknown |
| Loading / Container / CBM / Volumetric calculators | No evidence either way in email | UNKNOWN — D1 must check |
| Commercial Invoice Builder | No evidence either way in email | UNKNOWN — D1 must check |
| Shipment Tracker | No evidence either way in email | UNKNOWN — D1 must check |

### MIRA status — the answer to the §MIRA question below

**No autonomous AI assistant appears to be live on the website.** The chat widget observed in the
mailbox relays visitor messages to staff, who answer them personally.

**Consequence:** the active commercial exposure this template was written to catch **does not
currently exist**. There is no unguarded AI stating rates or confirming cargo.

This is the best possible starting position for Phase 02: the guardrails in
`../standards/MIRA-GUARDRAILS.md` can be built in from the first day rather than retrofitted onto
something already talking to customers.

**D1 must still confirm this directly in the code.** Absence of evidence in email is not proof
that no AI surface exists.

### Operational software

A freight-forwarding platform and a separate accounting/ERP tool both appear in the mailbox as
active vendor relationships. **D1 must establish what is actually in use, what data it holds, and
whether it can report quote-to-booking conversion** — which D3 could not establish and which the
programme needs for its primary metric.
