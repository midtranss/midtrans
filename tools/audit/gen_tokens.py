import json, pathlib
import pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[2]
root = ROOT/'design-system'
t = json.load(open(root/'tokens.json'))
out = []
out.append('/* generated from tokens.json - audit harness only */')
fam = t['type']['families']
out.append('@font-face{font-family:"Cairo";src:url("/design-system/fonts/Cairo-Variable.ttf") format("truetype");font-weight:200 1000;font-style:normal;font-display:swap;}')

def block(sel, decls):
    out.append(sel + '{' + ''.join(f'{k}:{v};' for k,v in decls) + '}')

base = [('--font-sans', fam['sans']), ('--font-arabic', fam['arabic']), ('--font-mono', fam['mono'])]
for s in t['spacing']['tokens']: base.append(('--'+s['name'], s['value']))
for s in t['radius']['tokens']:  base.append(('--'+s['name'], s['value']))

light = list(base)
dark  = []
for c in t['color']['tokens']:
    light.append(('--'+c['name'], c['value']['light']))
    dark.append(('--'+c['name'], c['value']['dark']))
for s in t['shadow']['tokens']:
    light.append(('--'+s['name'], s['value']['light']))
    dark.append(('--'+s['name'], s['value']['dark']))

block(':root, [data-theme="light"]', light)
block('[data-theme="dark"]', dark)
out.append('html,body{font-family:var(--font-sans);color:var(--ink-body);background:var(--surface-page);}')
(root/'..'/'audit-tokens.css').resolve().write_text('\n'.join(out))
print('wrote', (root/'..'/'audit-tokens.css').resolve())
print('color tokens:', len(t['color']['tokens']))
