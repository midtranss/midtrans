# Language Scope

**Status:** BINDING. No content is produced without an assigned language tier.

---

## نبذة بالعربية

اللغة قرار تجاري، لا قرار تقني.

لن نترجم كل شيء إلى سبع لغات. كل نوع محتوى يحصل على "طبقة لغوية" محدّدة حسب العائد المتوقع منه.
هذا وحده يخفض حجم العمل بنحو ٦٠٪ مقابل الترجمة الشاملة، دون خسارة عائد تُذكر.

القاعدة: لا يُكتب أي محتوى قبل تحديد طبقته اللغوية.

---

## 1. Why this file exists

The roadmap that preceded this programme sized the project in pages and never mentioned
language. That is the single most expensive omission available in a multilingual project.

MIDTRANS operates in seven languages: **EN, AR, FR, DE, TR, ZH, SV**.

Applied naively, a 1,500-page target becomes 10,500 URLs. Every one of them needs translation,
review, hreflang, canonical handling, and ongoing maintenance as procedures change. A Phase
requiring 5,000-word pillar pages becomes 175,000 words for five pages.

That project does not finish. It stalls somewhere around 40% and leaves half-translated pages
live, which is worse than not starting.

**So language coverage is decided per content type, by expected return — before writing begins.**

---

## 2. The tiers

| Tier | Languages | Applies to |
|---|---|---|
| **T1 — Full** | EN, AR, FR, DE, TR, ZH, SV | Corporate identity and core service pages |
| **T2 — Core** | EN, AR | Syria-specific procedural and trade content |
| **T3 — Market** | EN + the target market's language | Market-specific commercial content |
| **T4 — English only** | EN | Content whose audience reads English professionally |

---

## 3. Assignment by content type

| Content | Tier | Reasoning |
|---|---|---|
| Homepage | T1 | Entry point from every market |
| About, company history, Trust Center | T1 | Identity; read from everywhere |
| Locations and offices | T1 | Identity |
| Contact | T1 | Must not be a dead end in any language |
| Core service pages (sea, air, road, customs, warehousing, project cargo) | T1 | The commercial core of the business |
| MIRA landing page | T1 | Entry point to the primary engagement layer |
| Syria import / export procedures | **T2** | Arabic-speaking traders + international importers who read English |
| Syrian customs, documentation, border procedures | **T2** | Same audience |
| Latakia / Tartous / Damascus logistics pages | **T2** | Same audience |
| Tools — landing pages | T1 | Broad utility, high entry value |
| Tools — guides and FAQs | **T2** | Depth is read by the operating audience |
| US market content | **T4** | Audience is US exporters. No one reads it in Swedish. |
| China trade content | **T3** (ZH + EN) | Manufacturers and trading intermediaries |
| UAE trade content | **T3** (AR + EN) | Gulf trade operates in both |
| Turkey trade content | **T3** (TR + EN) | |
| Germany / France / Netherlands / Sweden trade content | **T3** (market language + EN) | One market at a time, per Phase 07 gating |
| Maritime and P&I content | **T4** | International maritime operates in English as a working language |
| Business representation and market entry | **T3** by target market | Written for the market being approached |
| Case studies | **T4** initially, promote to T1 on demand | Prove demand before paying for seven translations |
| Blog and knowledge articles | Per-article decision, recorded before writing | Default T4 unless a case is made |

### The promotion rule

Any content may be promoted to a higher tier **when data shows demand** — search traffic,
enquiries, or MIRA conversations in that language. Promotion is a data-driven decision made at a
phase gate, never an assumption made in advance.

Demotion is also permitted. A translated page with no traffic after two review cycles is a
maintenance liability, and retiring it is a legitimate outcome.

---

## 4. Technical requirements

These apply to every page, in every tier.

- **`hreflang`** — complete reciprocal annotations across all available language versions of a
  page, plus `x-default`. A page in three languages declares three alternates; it does not
  declare four.
- **`canonical`** — self-referencing per language version. A localised page never canonicalises
  to the English original.
- **URL structure** — one consistent scheme across the whole site, decided in Phase 00 against
  the existing codebase and not changed afterwards.
- **No partial publication** — a page ships in a language or it does not exist in that language.
  A page that is half-translated, or that falls back silently to English mid-content, must not be
  live.
- **Language switcher preserves context** — switching language on a page goes to that page's
  equivalent, never to the homepage. If no equivalent exists, the switcher must not offer that
  language for that page.
- **RTL** — Arabic is fully right-to-left: layout, navigation, form fields, tables, icons with
  direction, and scroll behaviour. Font: Cairo.
- **Structured data** — `inLanguage` set correctly on every page; schema translated, not left in
  English under localised content.

---

## 5. Sizing consequence

| Approach | Approx. URLs at 400 pages of unique content |
|---|---|
| Naive: everything in 7 languages | ~2,800 |
| This tiering | ~1,050 |

Roughly a 60% reduction in translation, review, and maintenance load — concentrated entirely on
content whose additional languages were never going to be read.

---

## 6. Definition of Done

- [ ] Every content item has a recorded tier **before** writing starts
- [ ] `hreflang` reciprocal and complete; validated by crawl, not by inspection
- [ ] `canonical` self-referencing per language
- [ ] Language switcher context-preserving, and hides unavailable languages
- [ ] Arabic RTL verified on mobile and desktop, including bidirectional text
- [ ] No half-translated page live
- [ ] `inLanguage` correct in structured data
