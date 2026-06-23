# MIDTRANS Trade Lane Page Design Concept

## Purpose

This document defines a visual direction for MIDTRANS trade lane and route pages. It is a design audit output only and does not modify any route or trade lane page.

Pages reviewed:

- Trade lanes hub `/trade-lanes/`
- China to Syria `/shipping-from-china-to-syria/`
- Land Freight Dubai to Syria `/land-freight-dubai-to-syria/`
- Jebel Ali Customs Clearance `/jebel-ali-customs-clearance/`
- Dubai-to-Syria route references from the current trade lane hub

## Current Trade Lane Findings

MIDTRANS has strong route-specific content. Route pages explain:

- origin and destination logic
- available freight modes
- documents
- customs risks
- cargo readiness
- supplier coordination
- final delivery or handover scope

The trade lane hub includes many routes and filters, which is valuable. But visually, the page can become dense and repetitive.

## Main Weaknesses

### 1. Trade Lane Hub Density

The hub contains many route cards and route groups.

Weaknesses:

- Too much information can appear at once.
- Filters may feel crowded.
- Route cards need clearer priority.
- Strategic lanes should stand out more than secondary generated routes.
- Duplicate or similar route entries reduce confidence.

### 2. Route Card Design

Route cards should clearly communicate:

- origin
- destination
- mode
- customs/document relevance
- CTA

Weaknesses:

- Mode tags like Sea/Air/Land/LCL/FCL/Customs can feel visually compressed.
- Supported service lists are inconsistent in perceived weight.
- Route details links and quote CTAs need stronger hierarchy.

### 3. Route Page Hero

Route pages have strong operational intros, but need better route identity.

Weaknesses:

- Hero could visually show the route corridor.
- Origin and destination are not always visually separated.
- Freight mode availability should be immediately visible.
- Customs/document warning should appear as an operational note.

### 4. Repetition

Many route pages use similar operational patterns. This is structurally useful but visually risks feeling template-like.

Weaknesses:

- Similar headings and sections reduce page uniqueness.
- Related link sections can feel repeated.
- FAQ layout should support route-specific confidence.

## Recommended Trade Lane Hub Structure

### 1. Strategic Route Hero

Hero should state:

`Trade lanes and freight routes for Syria, UAE, Jebel Ali, China, Turkey and Europe`

Visual should include:

- route map abstraction
- region tags
- freight mode icons
- quote CTA

### 2. Route Search and Filters

Filters should be redesigned as a premium route finder.

Recommended layout:

- Origin dropdown
- Destination dropdown
- Region dropdown
- Mode dropdown
- Reset button

Visual improvements:

- Larger spacing
- Clear labels
- One row desktop
- Stacked mobile
- Results count
- No overcrowded compressed controls

### 3. Featured Strategic Lanes

Featured cards should be visually stronger than normal route cards.

Each featured card should include:

- Route title
- Origin/destination visual
- Short route-specific summary
- Mode tags
- Key services
- Primary CTA: `Request a Quote`
- Secondary CTA: `Route details`

### 4. Grouped Route Sections

Group route cards under:

- Strategic trade lanes
- Syria trade lanes
- Jebel Ali and Syrian ports
- GCC trade lanes
- China trade lanes
- Europe trade lanes
- Turkey trade lanes
- Specialized freight routes

Each group should include:

- short intro
- count
- route cards
- optional "view more" behavior on mobile

## Recommended Route Page Structure

### 1. Route Hero

Route hero should include:

- H1
- origin/destination labels
- available modes
- short summary
- quote and WhatsApp CTA

Visual:

- horizontal route line
- origin node
- destination node
- customs/document checkpoint
- mode icons

### 2. Route Snapshot

Compact card grid:

- Origin coverage
- Destination coverage
- Available modes
- Typical cargo
- Required documents
- Customs notes

### 3. Route Overview

Keep intro but improve scan:

- short paragraphs
- callout box for "before cargo moves"
- bullets for practical requirements

### 4. Freight Mode Section

For China to Syria:

- Sea freight
- LCL
- FCL
- Air freight where relevant
- Multimodal

For Dubai to Syria:

- Land freight
- Sea freight
- Air freight
- LTL/FTL where applicable

Each mode should use a small card.

### 5. Documents and Customs

Use a strong checklist panel:

- invoice
- packing list
- HS code
- certificate of origin
- permit exposure
- consignee readiness

This is central to MIDTRANS positioning and should be visually prominent.

### 6. MIDTRANS Role on Corridor

This should be a process section:

1. Supplier/cargo facts
2. Route feasibility
3. Document readiness
4. Mode selection
5. Customs exposure
6. Follow-up and handover

### 7. Related Services

Related links should be grouped:

- freight service
- customs service
- connected route
- quote/contact

### 8. FAQ

FAQ must remain route-specific.

Design:

- two-column desktop
- one-column mobile
- no hidden FAQ in schema
- answers should feel practical

## Trade Lane Card Style

Recommended card anatomy:

```text
[Region label]
Route title
Origin -> Destination
Short route-specific summary
[Sea] [Air] [Land] [LCL] [FCL] [Customs]
Key service bullets
Request Quote | Route Details
```

Visual:

- white card
- subtle route line
- mode tags with consistent colors
- strong CTA hierarchy
- route-specific icon or node graphic

## Mode Tag System

Recommended colors:

- Sea: blue
- Air: sky
- Land: green
- Customs: amber
- LCL/FCL: navy outline
- Project: purple or dark accent
- Vehicle: steel grey

Mode tags should remain consistent across the website.

## Mobile Behavior

Trade lanes mobile must reduce density:

- Filters stacked
- Featured route cards first
- Collapsible route groups
- Shorter cards with expandable details
- Sticky "Request Quote" only if approved
- Route tags wrap cleanly

## Risk Level

High for `/trade-lanes/` because it is a protected strategic hub.

High for key route pages such as China to Syria and Dubai to Syria because they carry commercial SEO value.

## Recommended Pilot

Recommended first visual pilot page:

`/shipping-from-china-to-syria/`

Reason:

- It is a strategic route page.
- It contains rich operational content.
- It can validate the route-page template.
- It is less structurally broad than the full trade lanes hub.

Implementation should be staging-only until approved.
