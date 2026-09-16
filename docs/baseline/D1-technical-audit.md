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

---

## Partial findings — infrastructure, 2026-09-16

**Method:** read-only queries to the Hostinger API (list websites, list domains, read DNS zone,
read domain details). **No configuration was changed.** No VPS write operation was invoked.

### Domain portfolio

| Domain | Registered | Expires | Nameservers | Notes |
|---|---|---|---|---|
| `mid-trans.com` | **2002** | 2028-06-23 | Cloudflare | Main website |
| `midtrans.org` | **2018** | 2028-05-16 | Cloudflare | Operations email, RFQ notifications |
| `midtrans.net` | — | 2028-04-13 | not checked | Carries `app.` subdomain |
| `midtrans.cloud` | 2026-06-27 | — | — | Free domain |
| `trustbycompass.com` | — | 2029-08-25 | — | **Unrelated brand — confirm whether in scope** |

All domains are registrar-locked with privacy protection enabled. Good practice; record it in the
Trust Center work in Phase 07 only if verifiable externally.

### ⚠️ The Hostinger DNS zone is NOT authoritative

`mid-trans.com` and `midtrans.org` both delegate to **Cloudflare** nameservers
(`bingo.ns.cloudflare.com`, `jason.ns.cloudflare.com`). The DNS zone stored at Hostinger is
therefore **inert** — it serves nothing.

**Proof:** the Hostinger zone for `midtrans.org` contains no MX record, yet `@midtrans.org` mail
demonstrably works through Google Workspace. That mail cannot be routed by this zone.

**Consequences for this audit:**

1. **Any DNS conclusion drawn from the Hostinger zone is invalid.** In particular, the absence of
   a `mira` record there proves nothing about whether `mira.midtrans.org` exists.
2. **The real DNS must be read in Cloudflare.** The Cloudflare connector available in this
   session exposes Workers, R2, KV, D1 and Hyperdrive — **no DNS tools** — so it cannot be read
   from here either.
3. **A stale zone is a latent hazard.** If nameservers are ever pointed back at Hostinger, this
   zone becomes live and would break mail immediately (no MX) . Either bring it into
   sync or delete it deliberately. **Do not delete without approval.**

### Server topology (indicative only — from the inert zone, treat as a lead, not a fact)

| IP | Appears to serve |
|---|---|
| `2.57.91.91` | `mid-trans.com`, `midtrans.org` — the public website |
| `2.25.72.110` | `midtrans.net`, **`app.midtrans.net`** — likely the Platform / ERP |

Two distinct hosts. **Verify against Cloudflare's live zone**, and establish what `app.` serves —
it is not mentioned anywhere in the programme documentation and may be a significant undocumented
system.

### Hosting

- `listWebsites` returns **zero** results: there is no Hostinger shared/managed hosting.
- The infrastructure is a **VPS** (hPanel VPS id `1788560`).

### ❌ The VPS cannot be inspected through this connector

The Hostinger connector's VPS surface in this session is **mutation-only**: create/delete
firewalls and rules, attach SSH keys, create/delete PTR records, create snapshots, create/delete
post-install scripts, deploy/delete Docker Compose projects.

**There is no read capability at all** — no file read, no command execution, no log access, no
VPS detail or project listing.

None of the write tools were invoked, and none should be for an audit. Two are outright
destructive: `deleteProject` is documented as irreversible and deletes all project data, and
`createSnapshot` overwrites the existing snapshot.

### How the remaining D1 work must be done

| Item | Route |
|---|---|
| Codebase, MIRA implementation, i18n, logs | **SSH to the VPS**, or a repository containing the site |
| Live DNS, hreflang at the edge, caching, WAF | **Cloudflare dashboard** (no DNS tooling available here) |
| Whether `mira.midtrans.org` resolves | Cloudflare zone |
| What `app.midtrans.net` is | SSH or the team |

### Highest-priority commands for whoever has SSH

```
# 1. Where is the retired model referenced?
grep -rn "claude-3-5-haiku" /path/to/app

# 2. Does MIRA have any guardrail at all?
grep -rni "system_prompt\|systemPrompt\|instructions" /path/to/mira

# 3. Where does MIRA log conversations?
grep -rni "conversation\|transcript\|chat_log" /path/to/mira
```

Question 2 is the highest-priority open item in the entire programme — see
`D4-feature-inventory.md` § MIRA status.
