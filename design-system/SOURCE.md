# MIDTRANS design system — source files

These are the source files of the MIDTRANS design system artifact. The
artifact renders them as a browsable reference; this directory is the
versioned copy.

- `design-system.json` — index (title, namespace, libraries, asset groups)
- `tokens.json` — colour, type, spacing, radius and shadow tokens
- `README.md` — the brand book: usage rules naming tokens
- `guidelines/` — multilingual and RTL rules; rules on claims and figures
- `components/bundle.css` — the component stylesheet
- `components/<Name>/` — guidelines and a live preview per component

## What this was built from

Nothing was extracted from code. This repository was empty at the time of
writing, no hosting account exposed a MIDTRANS site, and the live site was
not reachable from the build environment. The foundations here are derived
from the stated MIDTRANS brand identity: the brand colour #007DC5, white,
steel grey and deep navy; Helvetica for Latin text and Cairo for Arabic;
proper RTL; premium, enterprise-grade, logistics-specific.

No logo and no icon set were available, so neither is included and neither
was drawn. Both gaps are recorded in `README.md`. When the real site or
platform code is available, re-sync from it: values found in code replace
the values here, and the usage notes and prose are kept.
