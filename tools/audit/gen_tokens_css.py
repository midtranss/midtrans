#!/usr/bin/env python3
"""Regenerate design-system/tokens.css from tokens.json.

tokens.css is what components actually consume, and it had drifted badly from
tokens.json: 14 colours differed, all three radii were a step small (3/6/10
instead of 4/8/12), and ink-inverse-muted and chart-1..4 were missing entirely.
Run this after any edit to tokens.json.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
t = json.loads((ROOT/'design-system/tokens.json').read_text())
L = ['/* MIDTRANS — generated from tokens.json. Do not edit by hand:',
     '   run tools/audit/gen_tokens_css.py instead. */',
     ':root, [data-theme="light"] {']
for c in t['color']['tokens']:
    L.append(f"  --{c['name']}: {c['value']['light']}; /* {c['usage']} */")
for s in t['shadow']['tokens']:
    L.append(f"  --{s['name']}: {s['value']['light']}; /* {s['usage']} */")
L.append('}')
L.append('[data-theme="dark"] {')
for c in t['color']['tokens']:  L.append(f"  --{c['name']}: {c['value']['dark']};")
for s in t['shadow']['tokens']: L.append(f"  --{s['name']}: {s['value']['dark']};")
L.append('}')
L.append(':root {')
for s in t['spacing']['tokens']: L.append(f"  --{s['name']}: {s['value']}; /* {s['usage']} */")
for s in t['radius']['tokens']:  L.append(f"  --{s['name']}: {s['value']}; /* {s['usage']} */")
fams = t['type']['families']
L.append(f"  --font-sans: {fams['sans']};")
L.append(f"  --font-arabic: {fams['arabic']};")
L.append(f"  --font-mono: {fams['mono']};")
VAR = {'sans': '--font-sans', 'arabic': '--font-arabic', 'mono': '--font-mono'}
for g in t['type']['groups']:
    for st in g['styles']:
        v = VAR[st.get('family') or g['family']]
        L.append(f"  --text-{st['name']}: {st['fontWeight']} {st['fontSize']}/{st['lineHeight']} "
                 f"var({v}); /* {st.get('usage','')} */")
L.append('}')
for g in t['type']['groups']:
    for st in g['styles']:
        v = VAR[st.get('family') or g['family']]
        L += [f".{st['name']} {{", f"  font-family: var({v});", f"  font-size: {st['fontSize']};",
              f"  line-height: {st['lineHeight']};", f"  font-weight: {st['fontWeight']};",
              f"  letter-spacing: {st.get('letterSpacing') or '0'};", '}']
# Paper is white and ink is dark, whatever the screen was set to. Without this,
# an official quotation printed from a dark session comes out either ink-heavy
# or as light text the browser drops the background behind - unreadable either
# way. The light values are re-declared at print, so every component follows
# with no per-component print rules.
L.append('@media print {')
L.append('  :root, [data-theme="light"], [data-theme="dark"] {')
for c in t['color']['tokens']:
    L.append(f"    --{c['name']}: {c['value']['light']};")
for s_ in t['shadow']['tokens']:
    L.append(f"    --{s_['name']}: none;")
L.append('  }')
L.append('}')
for f in t['type']['fonts']:
    L += ['@font-face {', f"  font-family: \"{f['family']}\";",
          f"  src: url(\"{f['file']}\") format(\"truetype\");",
          f"  font-weight: {f['weight']};", f"  font-style: {f['style']};",
          '  font-display: swap;', '}']
(ROOT/'design-system/tokens.css').write_text('\n'.join(L) + '\n')
print('wrote design-system/tokens.css')
