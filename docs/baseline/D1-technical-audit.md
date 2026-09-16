# D1 — Technical Audit

**Owner:** _________  **Date:** _________  **Repo / source audited:** _________

> Read-only audit. Change nothing. Record schema and volumes, never customer records.

## 1. Stack and infrastructure

| Item | Finding |
|---|---|
| Framework + version | |
| Language + runtime version | |
| Hosting provider | |
| Build tooling | |
| Deploy process (how does a change reach production?) | |
| CI present? What does it run? | |
| Staging environment exists? | |
| Repository location + who has write access | |

## 2. Routing and content

| Item | Finding |
|---|---|
| How are pages defined? (file-based / config / CMS) | |
| Total route count | |
| How does someone add a new page? | |
| Is a developer required for content edits? | |
| CMS in use (if any) | |

## 3. Internationalisation — highest-risk area

| Item | Finding |
|---|---|
| Which of EN/AR/FR/DE/TR/ZH/SV are actually live? | |
| i18n library / mechanism | |
| Where do translation strings live? | |
| URL pattern per language (`/ar/`, `?lang=ar`, subdomain…) | |
| Is the pattern consistent across all pages? | |
| How is a new language version of a page created? | |
| Are any pages partially translated or falling back silently? | |
| RTL implementation for Arabic — real RTL or mirrored CSS? | |
| Arabic font — is Cairo actually loaded? | |
| Language switcher: preserves page context, or drops to homepage? | |

## 4. Technical SEO

| Item | Finding |
|---|---|
| `hreflang` present? Reciprocal? `x-default` set? | |
| `canonical` — self-referencing per language? | |
| Sitemap(s) — present, segmented, submitted? | |
| `robots.txt` contents; does it block rendering assets? | |
| Indexed page count (Search Console) | |
| Redirect chains longer than one hop | |
| 404s currently being hit | |
| Structured data types present; validation errors | |

## 5. Performance (top 20 pages by traffic, mobile)

| Page | LCP | CLS | INP | Pass? |
|---|---|---|---|---|
| | | | | |

Heaviest assets / main causes of failure: _________

## 6. Data and integrations

| Item | Finding |
|---|---|
| Database + schema overview (no records) | |
| What customer data is stored, and where | |
| Data retention policy in place? | |
| Analytics tool + is conversion tracking configured? | |
| Consent management present? (EU markets are targeted) | |
| Forms: where do submissions go? | |
| WhatsApp / chat / tracking integrations | |
| Third-party scripts and their performance cost | |

## 7. Accessibility and dependencies

| Item | Finding |
|---|---|
| Baseline a11y check on main templates | |
| Outdated or unmaintained packages | |
| Known vulnerabilities | |

## 8. Findings

| # | Finding | Severity | Affects which phase |
|---|---|---|---|
| | | | |

**Blockers for Phase 01:** _________
