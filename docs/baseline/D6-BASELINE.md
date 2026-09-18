# D6 — Baseline Document

**Owner:** _________  **Signed off by:** _________  **Date:** _________

> This is the single artefact every later phase gate is measured against.
> Confidence is recorded explicitly. A number nobody trusts is labelled `LOW`, not carried
> forward silently. A number that could not be established is `UNKNOWN`, never estimated.

## Primary metric

| Metric | Value | Period | Source | Confidence |
|---|---|---|---|---|
| **Qualified RFQ / month** | | | | HIGH / MED / LOW / UNKNOWN |

## Supporting metrics

| Metric | Value | Period | Source | Confidence |
|---|---|---|---|---|
| Total enquiries / month | | | | |
| Website-sourced enquiries / month | | | | |
| Organic sessions / month | | | | |
| RFQ form completion rate | | | | |
| Mobile share of traffic | | | | |
| Indexed pages | | | | |
| Mobile CWV pass rate | | | | |
| **Reply rate — enquiries answered** | **2 of 30 threads had any reply** | 1 Mar – 11 Sep 2026 | Mailbox, quote-subject threads to the public addresses; 14 non-replies confirmed by a sent-mail search | **MED** — one method, one window; see `D3-rfq-analysis.md` §8b |
| Median time to first reply | UNKNOWN | | Needs the same sample, timed | |
| Enquiry → quote rate | | | | |
| Quote → booking rate | | | | |

## By language

| Language | Sessions | Enquiries | Qualified | Live pages |
|---|---|---|---|---|
| EN | | | | |
| AR | | | | |
| FR | | | | |
| DE | | | | |
| TR | | | | |
| ZH | | | | |
| SV | | | | |

## Gaps

| What could not be established | Why | How it will be established |
|---|---|---|
| Whether the unanswered enquirers were answered by WhatsApp or phone | Neither channel is visible in email. `D3` §8c shows WhatsApp **is** in active use — two answered enquiries move to it deliberately — so an email-only reply rate under-reports by an unknown amount | **MIDTRANS checks directly** for the named enquiries. Then make the email handover mandatory, so the reply becomes countable — `PHASE-01-MEASUREMENT-FRAMEWORK.md` §7a |
| Who owns `info@mid-trans.com` and `info@midtrans.org` | Not visible from the mailbox | Ask operations |
| Pre-wizard follow-up rate | Requires reading each answered thread; the sample shows almost none were answered, so the denominator is too small to compute one | Re-derive once the reply rate is fixed |
| Pre-wizard `/get-quote/` sessions and submissions | Analytics history; retention may have expired | Check the analytics tool now |

## Findings that change the plan

| # | Finding | Change required | Approved by |
|---|---|---|---|
| 1b | **The failure is coverage, not capability.** In the five days after launch several enquiries were answered, one in 20 minutes — while four of six unanswered ones in the same window were never opened | Establish who owns `info@` and what routes a message there. `D3` §8c | |
| 1 | **Website enquiries are going unanswered.** 2 of 30 quote threads replied; 14 non-replies confirmed against the sent folder; 4 well-specified end-customer enquiries read in full, all unanswered, one still unread after a week | The Phase 01 gate metric changes from follow-up rate to **reply rate** — a better form cannot raise a number lost after intake. `PHASE-01-MEASUREMENT-FRAMEWORK.md` §7a | |
| 2 | MIRA is live and its guardrail status is unestablished | Phase 02 D0 audit becomes immediate, ahead of Phase 01's gate | |
| 3 | `/get-quote/` already exists and ranks | The RFQ wizard is a replacement, not a new build | |

## Gate decision

- [ ] Baseline signed off by the programme owner
- [ ] Qualified-RFQ-per-month figure stated, with confidence level
- [ ] Open decisions in `../phases/00-MASTER-PLAN.md` §10 closed
- [ ] Roles in §8 assigned by name
- [ ] Phase 01 estimate re-confirmed against the real codebase
- [ ] Any plan-invalidating finding escalated and resolved

**Decision:** ⬜ Proceed to Phase 01  ⬜ Re-scope  ⬜ Re-diagnose
**Decided by:** _________  **Date:** _________
