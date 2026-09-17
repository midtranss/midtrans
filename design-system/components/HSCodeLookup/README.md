# HSCodeLookup

Searches the harmonised system and returns candidate classifications for a commodity.

Compose `mt-hs` → a Field for the query, `mt-hs__results` as a `<ul>` of `mt-hs__item` rows, then the standing `mt-hs__foot` disclaimer.

**You provide:** the tariff data, the search, and selection handling. Mark the chosen row `data-selected="true"`.

Each row is a code in `mono` tabular figures, a description, and a duty cell. The code is the thing being checked against a document, so it never wraps and never reflows.

**This component does not show duty rates.** The duty cell reads "Duty: on assessment" and nothing else. A duty rate depends on the country of import, origin, trade agreement, valuation method and the declaration as filed — a number shown here would be read as MIDTRANS quoting a customs cost, which is a commitment the company does not make from a lookup table. If a rate is ever displayed, it comes from a filed declaration for a specific shipment, in a Document, not from this tool.

**The result is indicative, and the footer says so in every locale.** The binding determination belongs to the customs authority of the country of import. This line is not dismissible, not collapsed behind a tooltip, and not removed to make the interface tidier — it is the reason the tool can be published at all.

**Write descriptions as the tariff writes them**, not paraphrased. An operator compares this string against a commercial invoice.

**Do not** present a single result as "the" code — always offer the candidates and let a human choose. Do not let the tool feed a classification into a customs declaration without a person confirming it.
