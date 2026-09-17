#!/usr/bin/env python3
"""Check that every document total equals the rows above it.

A packing list shipped with totals of 12,026 kg over rows summing to 7,026 kg is
the failure the claims-and-figures guideline exists to prevent: it is the number
a warehouse and a customs officer check piece by piece. Reading the preview did
not catch it; adding it up did.
"""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
TAG  = re.compile(r'<[^>]+>')
NUM  = re.compile(r'^-?[\d,]+\.?\d*$')

def cells(row):
    return [TAG.sub(' ', c).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)]

def num(t):
    t = re.sub(r'\s+', '', t)
    return float(t.replace(',', '')) if NUM.match(t) else None

fails = []
for pv in sorted((ROOT/'design-system/components').glob('Document*/preview.html')):
    html = pv.read_text()
    body = re.search(r'<tbody>(.*?)</tbody>', html, re.S)
    if not body: continue
    rows = [cells(r) for r in re.findall(r'<tr>(.*?)</tr>', body.group(1), re.S)]
    if not rows: continue
    width = max(len(r) for r in rows)
    # column sums, where every populated cell in the column is a number
    sums = {}
    for col in range(width):
        vals = [num(r[col]) for r in rows if col < len(r) and r[col]]
        if vals and all(v is not None for v in vals):
            sums[col] = round(sum(vals), 2)
    # every total row's figure must equal one of those column sums
    for label, fig in re.findall(
            r'<div class="mt-doc__total-row[^"]*">\s*<span>(.*?)</span>\s*<span[^>]*>(.*?)</span>', html, re.S):
        label = TAG.sub('', label).strip()
        raw   = TAG.sub(' ', fig)
        v = num(re.sub(r'[A-Za-z]+', '', raw))
        if v is None: continue
        if not any(abs(v - s) < 0.01 for s in sums.values()):
            fails.append(f"{pv.parent.name}: '{label}' is {v:,.2f}, "
                         f"no column of the rows sums to it (columns: "
                         f"{', '.join(f'{s:,.2f}' for s in sums.values()) or 'none numeric'})")

print("FAIL" if fails else "PASS", f"({len(fails)} document total(s) do not add up)")
for f in fails: print("  ✗", f)
sys.exit(1 if fails else 0)
