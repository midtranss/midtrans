# Properties and domains

MIDTRANS runs one design system across several web properties. This section records which property is which, what each one uses, and what is verified as live.

## The estate, as DNS actually reports it

| Property | Status | Role | Surface set |
| --- | --- | --- | --- |
| `midtrans.org` | Live | The corporate website | Hero, ServiceCard, TradeLaneCard, CTABlock, Footer |
| `mid-trans.com` | Live, **same server as `midtrans.org`** | Second corporate domain | Must not serve duplicate content — see below |
| `midtrans.net` | Live | Platform root | Footer, and the platform shell |
| `app.midtrans.net` | Live | ERP, CRM, operations | DataTable, KeyValue, Field, StatusBadge, Milestone, Document, Alert |
| `chat.midtrans.org` | **No DNS record** | Planned: logistics chatbot | Chat surfaces, not yet designed |
| `desk.midtrans.net` | **No DNS record** | Planned: support desk | DataTable, Field, StatusBadge, Alert |
| `mira.midtrans.net` | **No DNS record** | Planned: Mira assistant | Chat surfaces, not yet designed |
| `midtrans.cloud` | No DNS records | Held, unused | — |
| `trustbycompass.com` | Separate registration | **A different project. Excluded by the owner.** | Out of scope — do not theme it |

Three of the named properties do not resolve. They are planned, not live. Design for them, but do not write copy or documentation that implies they exist.

`trustbycompass.com` sits in the same registrar account but is a separate project and is not a MIDTRANS property. It never loads this system, and no work here applies to it.

## One system, layered

Every property loads the same two files and the same font: `tokens.css`, `components/bundle.css`, `fonts/Cairo-Variable.ttf`. Nothing below that layer is duplicated or re-themed per property.

What differs is which components a property uses, not what they look like. A button on the corporate site and a button in the ERP are the same button.

- **Public sites** (`midtrans.org`, `mid-trans.com`) lead with the marketing set and carry at most one `surface-inverse` band per screen.
- **Operational surfaces** (`app.midtrans.net`, `desk.midtrans.net`) lead with the dense set — tables, key-value detail, forms — and use `space-3` padding where the public site uses `space-5`. Density is the only permitted difference.
- **Assistant surfaces** (`chat.midtrans.org`, `mira.midtrans.net`) inherit the same tokens. An assistant reply that states a rate, a transit time, a duty or an acceptance is governed by the claims section, exactly as a page is.

## The duplicate-domain problem

`midtrans.org` and `mid-trans.com` resolve to the same IP. If both serve the same pages, search engines see duplicate content and neither ranks properly.

Pick one canonical host and keep it. The other either 301-redirects to it, or serves its own distinct content. Every page carries a `<link rel="canonical">` to the canonical host, and the `hreflang` alternates for all seven locales point at that host only. This is decided once, at the server, not per page.

## The browser icon

Every property uses `midtrans-app-icon-512.png` as its favicon and touch icon, and `theme_color: "#007DC5"` in its web manifest. One icon across the estate is what makes a MIDTRANS tab recognisable among twenty open tabs.
