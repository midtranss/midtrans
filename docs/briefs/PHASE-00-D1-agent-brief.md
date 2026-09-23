# Paste-ready brief — Phase 00 / D1: Technical Audit

**How to use:** paste everything below the line into Codex, Claude Code, or any coding agent that
has access to the MIDTRANS website repository. Output goes into
`docs/baseline/D1-technical-audit.md`.

**Do not paste this into an agent that lacks repository access** — it will produce a plausible
audit of a codebase it never read. That failure mode is exactly what this audit exists to prevent.

---

You are performing a **read-only technical audit** of the MIDTRANS website codebase
(mid-trans.com). This is a freight forwarding and logistics company operating since 1998 from
Damascus, Latakia, Tartous, Dubai and Jebel Ali. The site is multilingual: EN, AR, FR, DE, TR, ZH,
SV.

## Absolute constraints

1. **Change nothing.** No commits, no edits, no dependency installs, no migrations, no
   deployments. This is an audit, not a fix. If you find something broken, **record it — do not
   repair it.**
2. **Never read, export, copy, or modify production customer data.** Record database *schema* and
   row *counts*. Never record actual records, names, email addresses, or shipment details.
3. **Never invent a finding.** If you cannot determine something, write `UNKNOWN — could not
   determine because <reason>`. An honest gap is usable; a guess corrupts every decision built on
   this audit.
4. **Do not connect to production databases or services** unless explicitly authorised, and never
   with write credentials.
5. **Do not include secrets in your output.** If you find a credential committed to the
   repository, report *that it exists and where*, never its value.

## What to produce

Fill in every section of `docs/baseline/D1-technical-audit.md`. Report findings as evidence, with
`file_path:line_number` references so each can be verified.

### Section 1 — Stack and infrastructure
Framework, language, versions, hosting, build tooling, deploy process, CI configuration, whether
a staging environment exists.

### Section 2 — Routing and content
How pages are defined, total route count, how a new page is added, whether a developer is required
for content edits, CMS presence.

### Section 3 — Internationalisation (**audit this hardest — it is the highest-risk area**)
- Which of the seven languages are *actually* live, versus merely configured
- The i18n mechanism and where translation strings live
- The URL pattern per language, and whether it is consistent across every page
- **Any page that is partially translated or silently falls back to English** — list each one
- Whether Arabic RTL is real directional layout or mirrored CSS
- Whether the Cairo font is actually loaded for Arabic
- Whether the language switcher preserves page context or drops the user to the homepage

### Section 4 — Technical SEO
hreflang (present, reciprocal, x-default), canonical tags, sitemaps, robots.txt, redirect chains,
structured data types present and their validation errors.

### Section 5 — Performance
Core Web Vitals on **mobile** for the top 20 pages. If traffic data is unavailable, use the 20
pages most linked from navigation and say so.

### Section 6 — Data and integrations
Database schema overview, what customer data is stored and where, retention policy, analytics
tooling, whether conversion tracking is configured and trustworthy, consent management, form
destinations, third-party scripts and their performance cost.

### Section 7 — Accessibility and dependencies
Baseline accessibility check on the main templates; outdated or unmaintained packages; known
vulnerabilities.

### Section 8 — Findings
Each finding with severity and which downstream phase it affects. End with an explicit list of
**blockers for Phase 01** (building the RFQ funnel).

## Specific questions that must be answered

These determine whether the programme's plan holds:

1. Does a working RFQ or quote form exist today? Where do its submissions go?
2. Is conversion tracking configured, and is the data trustworthy enough to establish a baseline?
3. Is MIRA deployed? On which pages? **Does it have any guardrail preventing it from stating
   rates, transit times, customs costs, or cargo acceptance?**
4. Which of these exist and work: Loading Calculator, Container Calculator, CBM Calculator,
   Volumetric Weight Calculator, Commercial Invoice Builder, Shipment Tracker?
5. How much work is it to add a new page in all seven languages?
6. What is the single largest technical obstacle to building a multi-step RFQ wizard here?

## Critical flag

If MIRA is live **with no guardrails**, stop and report it immediately and prominently at the top
of your output. A proactive assistant that can state a rate or confirm cargo acceptance is an
active commercial and legal exposure for MIDTRANS, not a future work item.

## Output format

Markdown, filling the existing template structure. Every claim carries a
`file_path:line_number` reference or a named source. Anything you could not verify is marked
`UNKNOWN` with the reason.
