#!/usr/bin/env python3
"""Mount every component preview as a standalone page the browser can load.

The previews in components/*/preview.html are fragments: the artifact platform
supplies the tokens around them. To measure anything locally they need a host
page. The theme is baked into the markup rather than set by script after load -
setting it afterwards starts the 120ms colour transitions, and styles read
during that window are wrong (it invented 23 contrast failures once).
"""
import pathlib, json
ROOT = pathlib.Path(__file__).resolve().parents[2]
out = ROOT/'.audit-mounts'
out.mkdir(exist_ok=True)
for f in out.glob('*.html'): f.unlink()
names = []
for c in sorted(p for p in (ROOT/'design-system/components').iterdir() if p.is_dir()):
    pv = c/'preview.html'
    if not pv.exists(): continue
    frag = pv.read_text()
    for theme in ('light', 'dark'):
        (out/f'{c.name}.{theme}.html').write_text(
f'''<!doctype html><html lang="en" data-theme="{theme}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{c.name} {theme}</title>
<link rel="stylesheet" href="/design-system/tokens.css">
<link rel="stylesheet" href="/design-system/components/bundle.css">
<style>*,*::before,*::after{{transition:none !important;animation:none !important;}}</style>
</head><body data-component="{c.name}">
{frag}
</body></html>''')
    names.append(c.name)
(out/'index.json').write_text(json.dumps(names))
(out/'meridian-parse.html').write_text(
'<!doctype html><html><head><meta charset="utf-8">'
'<link rel="stylesheet" href="/meridian/meridian.css"></head><body></body></html>')
print(f'{len(names)} components, {len(names)*2} mount pages')
