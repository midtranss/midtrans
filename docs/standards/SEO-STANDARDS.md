# SEO & Content Quality Standards

**Status:** BINDING. Applies to every page in every phase.

---

## نبذة بالعربية

معايير السيو وجودة المحتوى.

المبدأ: **العمق قبل العرض.** صفحة واحدة عميقة مبنية على خبرة MIDTRANS الحقيقية تساوي خمسين صفحة
عامة — وهي شيء لا يستطيع منافس نسخه.

الخطر الأكبر الذي نتجنّبه هنا: صفحات المدن والولايات المتشابهة (Doorway Pages). عقوبتها تقع على
**كامل النطاق**، لا على تلك الصفحات وحدها.

---

## 1. The governing principle

**Depth before breadth.**

One page on customs clearance at the Port of Latakia, written from 27 years of actually doing it
— listing the documents genuinely required, the sequence, and the failure modes that delay
cargo — outperforms fifty generic city pages. It also cannot be copied by a competitor, which
generic pages can.

Page count is not a goal. It is a by-product of having useful things to say.

---

## 2. Thin content and doorway pages — hard prohibition

### The rule

**No page may be published that exists primarily to target a keyword or a location.**

This specifically prohibits the templated location-page pattern proposed in the earlier roadmap
(Texas, Houston, California, Los Angeles, New York, New Jersey, Florida, Atlanta, Chicago) and
any equivalent pattern for industries, commodities, or trade lanes.

### Why this is non-negotiable

Search engines assess doorway-page patterns at **site level**, not page level. A cluster of
near-duplicate location pages does not simply fail to rank — it can suppress the pages that would
otherwise have ranked, including the deep, genuinely useful content the rest of this programme is
built on.

The downside is asymmetric: limited upside on the templated pages, real risk to the entire
domain. Declaring in the plan that the pages "are not doorway pages" provides no protection
whatsoever; only the pages' actual content does.

### The uniqueness test

A location-, industry-, or lane-specific page may be published **only if** it contains, for that
specific subject:

- Specific operational detail — the actual port, terminal, routing, or corridor used
- Specific procedural or documentary requirements that genuinely differ from the generic case
- Genuine MIDTRANS experience — a handled case, a known constraint, a recurring failure mode

If the page would survive find-and-replace of its location or industry name with another and
still read correctly, **it does not pass.** Delete it or merge it into a stronger parent page.

### Consolidation preference

When in doubt: one strong page beats three weak ones. Merge.

---

## 3. Site architecture

```
Pillar  →  Hub  →  Cluster  →  Detail
```

- Every page has exactly one clear parent
- Every page is reachable within three clicks of the homepage
- Breadcrumbs on every page, matching the real hierarchy
- No orphan pages: nothing publishes without inbound internal links

### Internal linking

| Rule | Requirement |
|---|---|
| Descriptive anchors | Describe the destination. Never "click here", never a bare URL. |
| Minimum inbound links | 3 relevant internal links pointing to every new page |
| Outbound links | Links to genuinely related content, not a link block appended for volume |
| Hub completeness | Every hub links to all of its children; every child links back to its hub |
| Cross-language | Internal links stay within the user's language wherever an equivalent exists |

---

## 4. Structured data

Implement only schema types that match what is actually on the page.

| Type | Where |
|---|---|
| `Organization` | Site-wide, with complete and accurate company data |
| `LocalBusiness` | Office and location pages |
| `Service` | Service pages |
| `FAQPage` | Pages with genuine, visible Q&A — never invented to attach schema |
| `Article` | Guides and knowledge content |
| `BreadcrumbList` | Every page |
| `WebPage` | Every page, with `inLanguage` |
| `ImageObject` | Images with meaningful captions and alt text |
| `VideoObject` | Video content only |

### Rules

- Schema must describe what a user actually sees. Marked-up content not visible on the page is a
  violation.
- Never mark up a rating, review, or credential that does not exist.
- Validate every template before rollout, and re-validate after any template change.
- Translate schema content with the page. Do not leave English schema under Arabic content.

---

## 5. Technical baseline

| Area | Requirement |
|---|---|
| **Core Web Vitals** | Pass on mobile. Mobile is the measurement target, not desktop. |
| **Images** | Modern formats, responsive sizes, lazy-loaded below the fold, explicit dimensions to prevent layout shift. Heavy decorative imagery may be dropped on mobile. |
| **Sitemaps** | Generated, segmented by content type, submitted; excludes non-indexable URLs |
| **robots.txt** | Explicit, reviewed, and does not block assets needed for rendering |
| **Indexation** | Deliberate per page. Thin utility pages are `noindex`. |
| **Redirects** | Any URL change ships with a 301. No chains longer than one hop. |
| **404s** | Monitored; a useful 404 page that routes users onward |
| **Pagination / faceting** | Must not generate crawlable duplicate-parameter URLs |

---

## 6. AI search readiness

The goal is content that AI systems can accurately cite — which is largely the same discipline as
content a professional buyer trusts.

- **Answer first.** The page's core question is answered within the first 100 words.
- **Self-contained sections.** Each H2 section should make sense if quoted alone.
- **Named entities used consistently.** MIDTRANS, the ports, the services, the corridors — same
  names every time, so entity resolution is unambiguous.
- **Factual density over adjective density.** Specifics are citable; adjectives are not.
- **Genuine FAQs** answering real questions from RFQs, MIRA transcripts, and sales calls — not
  invented to fill a schema block.
- **No content that contradicts other MIDTRANS content.** Contradictions across pages destroy
  citation reliability. Procedural facts live in one place and are linked to, not duplicated.

---

## 7. Measurement

Report per phase, not per page:

- Qualified RFQ submissions — **the primary metric for the entire programme**
- Assisted conversions by content cluster
- Organic entrances to converting pages
- Query coverage for the target topic cluster
- Pages with zero organic entrances after two review cycles → merge or retire

**Not tracked as a success metric:** total page count, total word count, total keywords ranked.
These measure activity, not results.

---

## 8. Definition of Done

- [ ] Uniqueness test (§2) passed and recorded for every new page
- [ ] Correct parent; breadcrumbs; ≥3 relevant inbound internal links; no orphan
- [ ] Schema implemented, validated, matching visible content, translated
- [ ] Core Web Vitals pass on mobile
- [ ] `hreflang` and `canonical` correct per `LANGUAGE-SCOPE.md`
- [ ] Indexation decision deliberate and recorded
- [ ] Redirects in place for any changed URL
- [ ] Page answers its core question in the first 100 words
- [ ] No contradiction with existing MIDTRANS content
