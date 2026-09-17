# MIDTRANS drafts

Static drafts of every MIDTRANS surface, built on the design system. Nothing here is connected to a server, a database or live data, and nothing here touches the live site or the platform.

## Open them

```
python3 -m http.server 8000
```

Then open `http://localhost:8000/`. Opening `index.html` by double-click also works, except on the Mira and tools pages where the icon sprite is fetched.

## What to check

On every page: the theme button, the direction button, keyboard tab order, and the window at **280px, 402px, 768px, 984px and 1440px**. 984px is a folding phone opened — it is the width most often skipped.

| Page | What it drafts | Watch for |
| --- | --- | --- |
| `website.html` | midtrans.org home | The hero aside disappears below 900px by design; the footer's seven locales |
| `app-shipments.html` | The shipment register | Below 768px the table restates itself as records — it never scrolls sideways |
| `app-shipment.html` | One shipment | The back control, and that unreached timeline steps carry conditions, not dates |
| `tools.html` | Loading calculator, HS lookup | The calculator computes; the cost and duty fields refuse to |
| `quotation.html` | The commercial document | Press Ctrl/Cmd+P — the print layout drops the interface |
| `mira.html` | The assistant | Where Mira stops: rates, transit times, duties and acceptance go to the team |
| `theme/_harness.html` | Every component | Themes, focus rings, breakpoints |

## What is deliberately missing

- **No real figures.** Every amount is a masked placeholder. No rate, transit time, duty or date here came from an operational source.
- **No photography.** No freight image library was available, so the hero uses a facts panel instead.
- **No backend.** The calculator is the only thing that computes, and it computes geometry only.

## Status

Draft, for review. Mark what should change; nothing gets implemented against the live properties until you approve.
