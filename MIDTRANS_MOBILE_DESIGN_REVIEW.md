# MIDTRANS Mobile Design Review

## Purpose

This document reviews mobile design concerns for the MIDTRANS website. It is audit-only and does not modify the live site.

## Overall Mobile Concern

MIDTRANS pages are content-rich and operationally detailed. This is good for serious logistics customers, but on mobile it can become visually heavy if content is not broken into clear, scannable modules.

Mobile users likely need to:

- request a quote quickly
- find an office/contact channel
- understand if MIDTRANS handles their route
- confirm documents needed
- compare sea/air/land options
- access WhatsApp
- scan FAQ answers

The current visual structure should be optimized around these tasks.

## Mobile Weaknesses by Area

### Hero Sections

Current risk:

- Long hero copy can push CTA below the fold.
- Multiple CTAs can compete.
- Route/service context may not be immediately scannable.

Recommended:

- Keep mobile hero compact.
- Show primary CTA early.
- Use one secondary action maximum.
- Move supporting proof badges below the CTA.

### Navigation

Current risk:

- Services, trade lanes, tools, quote, contact, track, and platform links can become crowded.

Recommended:

- Use a simple mobile menu.
- Keep `Request Quote` and `Contact` prominent.
- Do not overload mobile header with too many links.

### Service Cards

Current risk:

- Large service grids may become long scroll lists.
- Similar cards can blur together.

Recommended:

- One card per row.
- Strong icon and title.
- Short summary.
- Keep service grouping clear:
  - freight modes
  - customs/documents
  - logistics support
  - special cargo

### Trade Lane Filters

Current risk:

- Multiple dropdowns in one row do not translate well to mobile.
- Long lists of origins/destinations can feel difficult to use.

Recommended:

- Stack filters vertically.
- Add a clear "Search routes" label.
- Show active filters.
- Include reset button.
- Consider collapsed filters after user selects.

### Route Cards

Current risk:

- Route cards with many tags and service bullets can become crowded.

Recommended:

- Show route title, summary, and top 3 mode tags first.
- Hide secondary service bullets behind "More details" only if implementation can preserve SEO and accessibility.
- Keep `Request Quote` visible.

### FAQ

Current risk:

- FAQ sections can become long.

Recommended:

- Use clean FAQ cards or accessible accordions.
- If accordions are used, visible content and FAQ schema must remain aligned.
- Avoid tiny text.

### CTA Placement

Current risk:

- Repeated CTAs may feel noisy.
- WhatsApp may dominate if visually too strong.

Recommended:

- Primary CTA after hero.
- Contextual CTA after major service/route sections.
- Final CTA at page end.
- WhatsApp as secondary quick contact.

### Trust Signals

Current risk:

- Trust information may become plain text and lose impact on mobile.

Recommended:

- Use compact trust badges:
  - Established 1998
  - Dubai/Jebel Ali capability
  - China coordination
  - Sea/Air/Land/Customs

### Forms

Current risk on Get Quote:

- Long forms can be intimidating.
- Many fields may feel heavy.

Recommended:

- Group fields into steps visually:
  1. Contact details
  2. Route details
  3. Cargo details
  4. Service/document notes
- Keep required labels clear.
- Make upload area visually trustworthy.
- Keep anti-spam field clear and accessible.

## Mobile Page Recommendations

### Homepage

Mobile homepage should prioritize:

1. H1
2. Primary quote CTA
3. Trust strip
4. Service categories
5. Trade lane highlights
6. Final contact CTA

### About

Mobile about page should prioritize:

1. Company identity
2. Timeline milestones
3. Geographic footprint
4. Trust signals
5. Related links

### Service Pages

Mobile service pages should prioritize:

1. Service summary
2. Request quote CTA
3. Snapshot panel
4. Benefits
5. Documents
6. Process
7. FAQ

### Trade Lane Pages

Mobile trade lane pages should prioritize:

1. Route hero
2. Origin/destination/modes
3. Documents and customs
4. Freight options
5. CTA
6. FAQ

### Trade Lanes Hub

Mobile trade lanes hub should prioritize:

1. Search/filter controls
2. Featured strategic routes
3. Route groups
4. FAQ
5. CTA

## Mobile Visual System

Recommended mobile style:

- Larger tap targets
- 16px minimum body text
- Strong contrast
- Clear card spacing
- Sticky header only if not too tall
- No horizontal overflow
- Route tags that wrap cleanly
- Buttons full-width where appropriate

## Mobile Risk Level

Medium to high.

Reason:

The website has long pages and many route/service cards. A redesign must be tested carefully on mobile before any rollout.

## Mobile QA Requirements

Every redesigned pilot page should be tested at:

- 390px width
- 430px width
- 768px width
- Desktop width

Checks:

- no horizontal overflow
- one visible H1
- CTA visible early
- route tags wrap
- cards stack cleanly
- FAQ readable
- form fields usable
- header does not block content
- footer remains clean

## Mobile Conclusion

MIDTRANS can keep rich logistics content, but mobile design must convert long operational pages into clear decision steps. The mobile experience should feel like guided shipment planning, not a dense article page.
