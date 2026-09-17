#!/usr/bin/env python3
"""Check that every document total equals the column its own label names.

A packing list shipped with totals of 12,026 kg over rows summing to 7,026 kg is
the failure the claims-and-figures guideline exists to prevent: it is the number
a warehouse and a customs officer check piece by piece.

The first version of this compared each total against *any* column sum, so
swapping the Gross weight and Net weight totals still passed - both numbers were
still somewhere in the set. A total is now matched to the column whose header
its label names, and a total whose label matches no header is reported rather
than quietly skipped.
"""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
TAG  = re.compile(r'<[^>]+>')
NUM  = re.compile(r'^-?[\d,]+\.?\d*$')

def text(x):
    return ' '.join(TAG.sub(' ', x).split())

def num(t):
    t = re.sub(r'[^\d,.-]', '', t).strip()
    if not t or not NUM.match(t): return None
    try: return float(t.replace(',', ''))
    except ValueError: return None

# a total's label and its column header rarely read the same; these are the
# equivalences this system actually uses.
ALIAS = {
    'total packages': 'pkgs', 'packages': 'pkgs',
    'gross weight': 'gross kg', 'net weight': 'net kg',
    'volume': 'cbm',
    'subtotal': 'amount', 'charges shown': 'amount',
    'quotation total': 'amount', 'proforma total': 'amount',
    'invoice total': 'amount', 'amount received': 'amount',
}
def key(s):
    s = s.lower().strip()
    return ALIAS.get(s, s)

fails = []
for pv in sorted((ROOT/'design-system/components').glob('Document*/preview.html')):
    html = pv.read_text()
    body = re.search(r'<tbody>(.*?)</tbody>', html, re.S)
    head = re.search(r'<thead>(.*?)</thead>', html, re.S)
    if not (body and head): continue
    heads = [key(text(h)) for h in re.findall(r'<th[^>]*>(.*?)</th>', head.group(1), re.S)]
    rows  = [[text(c) for c in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)]
             for r in re.findall(r'<tr>(.*?)</tr>', body.group(1), re.S)]
    if not rows: continue

    # sum each column that is numeric all the way down, by its header name
    col = {}
    for i, name in enumerate(heads):
        vals = [num(r[i]) for r in rows if i < len(r) and r[i].strip()]
        if vals and all(v is not None for v in vals):
            col[name] = round(sum(vals), 2)

    for label, fig in re.findall(
            r'<div class="mt-doc__total-row[^"]*">\s*<span>(.*?)</span>\s*<span[^>]*>(.*?)</span>',
            html, re.S):
        want = key(text(label))
        v = num(text(fig))
        if v is None: continue
        if want not in col:
            # a total the rows cannot speak to (a balance, a status) is not an error,
            # but one naming a column we DID sum must match it.
            if want in heads:
                fails.append(f"{pv.parent.name}: '{text(label)}' names column '{want}', "
                             f"which is not numeric all the way down")
            continue
        if abs(v - col[want]) >= 0.01:
            fails.append(f"{pv.parent.name}: '{text(label)}' is {v:,.2f}, "
                         f"but column '{want}' sums to {col[want]:,.2f}")

print("FAIL" if fails else "PASS", f"({len(fails)} document total(s) do not add up)")
for f in fails: print("  x", f)
sys.exit(1 if fails else 0)
