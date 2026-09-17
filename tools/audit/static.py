import json, re, pathlib, sys
import pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[2]
root = ROOT/'design-system'
t = json.loads((root/'tokens.json').read_text())
css = (root/'components/bundle.css').read_text()
fails, warns = [], []

# --- 1. no raw colours outside the token file -------------------------------
stripped = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
for m in re.finditer(r'(?<![\w-])#[0-9a-fA-F]{3,8}\b', stripped):
    line = stripped[:m.start()].count('\n') + 1
    fails.append(f"raw hex {m.group(0)} at bundle.css:{line}")
for m in re.finditer(r'\brgba?\([\d.\s,%]+\)', stripped):
    line = stripped[:m.start()].count('\n') + 1
    warns.append(f"literal {m.group(0)} at bundle.css:{line}")

# --- 2. every var() resolves ------------------------------------------------
defined = {c['name'] for c in t['color']['tokens']}
for k in ('spacing','radius','shadow'): defined |= {s['name'] for s in t[k]['tokens']}
defined |= {'font-sans','font-arabic','font-mono'} | set(re.findall(r'--([a-z0-9-]+)\s*:', css))
undef = sorted(set(re.findall(r'var\(\s*--([a-z0-9-]+)', css)) - defined)
for u in undef: fails.append(f"var(--{u}) is never defined")

# --- 3. RTL safety: no physical direction properties ------------------------
PHYS = r'\b(margin|padding)-(left|right)\s*:|\b(left|right)\s*:(?!\s*0[;\s}])|\btext-align\s*:\s*(left|right)\b|\bborder-(left|right)(-[a-z]+)?\s*:'
for m in re.finditer(PHYS, stripped):
    line = stripped[:m.start()].count('\n') + 1
    warns.append(f"physical property at bundle.css:{line}: {m.group(0).strip()}")

# --- 4. decided token values -------------------------------------------------
EXPECT = {'brand-accent': ('#007dc5','#007dc5'), 'brand-primary': ('#0074b7','#3ea7e4'),
          'border-focus': ('#007dc5','#007dc5'), 'status-info': ('#0070b0','#67c0f2')}
for c in t['color']['tokens']:
    if c['name'] in EXPECT:
        got = (c['value']['light'], c['value']['dark']); exp = EXPECT[c['name']]
        if got != exp: fails.append(f"{c['name']} is {got}, decided {exp}")
RADII = {'radius-sm':'4px','radius-md':'8px','radius-lg':'12px','radius-pill':'999px'}
for s in t['radius']['tokens']:
    if RADII.get(s['name']) != s['value']:
        fails.append(f"{s['name']} is {s['value']}, decided {RADII.get(s['name'])}")

# --- 5. Arabic is Cairo, exclusively ----------------------------------------
fam = t['type']['families']['arabic']
if fam.strip() != 'Cairo': fails.append(f"arabic family is {fam!r}, decided 'Cairo' exclusively")
if not re.search(r'\[lang="ar"\][^{]*\{[^}]*font-family:\s*var\(--font-arabic\)', css):
    fails.append("no [lang=\"ar\"] rule binds font-family to --font-arabic")

# --- 6. flash stays under the seizure threshold ------------------------------
kf = re.search(r'@keyframes mt-flash\s*\{(.*?)\n\}', css, re.S)
peaks = len(re.findall(r'box-shadow:[^;]*currentColor', kf.group(1))) if kf else 0
for m in re.finditer(r'animation:\s*mt-flash\s+([\d.]+)(m?s)', css):
    dur = float(m.group(1)) / (1000 if m.group(2) == 'ms' else 1)
    hz = peaks / dur  # one flash per visible-ring keyframe per cycle
    if hz > 3: fails.append(f"flash runs at {hz:.2f}Hz ({peaks} peaks / {dur}s), over the 3Hz seizure limit")

# --- 7. every text-bearing component root declares its own family ------------
# An additive skin lands on a host page that already sets a body font, and an
# inherited family loses to it. These roots hold no text, so they are exempt.
TEXTLESS = {'mt-avatar','mt-c1','mt-c2','mt-c3','mt-c4','mt-icon','mt-skeleton',
            'mt-sw1','mt-sw2','mt-sw3','mt-sw4','mt-typing'}
def split_rules(src):
    i, n, start, depth, pre, bs = 0, len(src), 0, 0, None, 0
    while i < n:
        c = src[i]
        if c == '/' and src[i:i+2] == '/*':
            j = src.find('*/', i+2); i = (j+2) if j != -1 else n; continue
        if c in '"\'':
            q = c; i += 1
            while i < n and src[i] != q: i += 2 if src[i] == '\\' else 1
            i += 1; continue
        if c == '{':
            if depth == 0: pre, bs = src[start:i], i+1
            depth += 1; i += 1; continue
        if c == '}':
            depth -= 1
            if depth == 0: yield pre, src[bs:i]; start = i+1
            i += 1; continue
        i += 1
COM = re.compile(r'/\*.*?\*/', re.S)
decl = {}
for pre, body in split_rules(css):
    pre = COM.sub('', pre).strip()
    if pre.startswith('@'): continue
    has = bool(re.search(r'(?:^|;)\s*font-family\s*:', COM.sub('', body)))
    for part in pre.split(','):
        q = part.strip()
        if q: decl[q] = decl.get(q, False) or has
for q in list(decl):
    m = re.fullmatch(r'\.(mt-[a-z0-9]+)', q)
    if m and m.group(1) not in TEXTLESS and not decl[q]:
        fails.append(f"{q} holds text but never declares font-family - it would "
                     f"inherit the host page's font")

# --- 8. every ink token holds its floor on the surfaces it claims -----------
# A token's usage text names the surfaces it is for. Those pairs are checked
# here, because a component preview only covers the pairings it happens to use:
# brand-link failed on brand-soft for a while with every preview passing.
def _lum(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def _cr(a, b):
    l1, l2 = _lum(a), _lum(b); hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)
V = {c['name']: c['value'] for c in t['color']['tokens']}
CONTRACT = [                      # (ink, surfaces, floor)
    ('ink-body',      ['surface-page','surface-card','surface-sunken','brand-soft'], 4.5),
    ('ink-strong',    ['surface-page','surface-card','surface-sunken'],              4.5),
    ('ink-muted',     ['surface-page','surface-card','surface-sunken'],              4.5),
    ('ink-inverse',   ['surface-inverse'],                                           4.5),
    ('ink-on-brand',  ['brand-primary'],                                             4.5),
    ('brand-link',    ['surface-page','surface-card','surface-sunken','brand-soft'], 4.5),
    ('status-success',['status-success-soft','surface-card'],                        4.5),
    ('status-warning',['status-warning-soft','surface-card'],                        4.5),
    ('status-danger', ['status-danger-soft','surface-card'],                         4.5),
    ('status-info',   ['status-info-soft','surface-card'],                           4.5),
    ('status-neutral',['status-neutral-soft','surface-card'],                        4.5),
    ('border-strong', ['surface-page','surface-card','surface-sunken'],              3.0),
    ('border-focus',  ['surface-page','surface-card','surface-sunken','surface-inverse'], 3.0),
]
for ink, surfaces, floor in CONTRACT:
    for surf in surfaces:
        for theme in ('light', 'dark'):
            if ink not in V or surf not in V: continue
            r = _cr(V[ink]['value'][theme] if 'value' in V[ink] else V[ink][theme],
                    V[surf]['value'][theme] if 'value' in V[surf] else V[surf][theme])
            if r < floor - 0.005:
                fails.append(f"{ink} on {surf} ({theme}) is {r:.2f}, its usage claims that "
                             f"surface and the floor is {floor}")

print("FAIL" if fails else "PASS", f"({len(fails)} fail, {len(warns)} warn)")
for f in fails: print("  ✗", f)
for w in warns[:12]: print("  ·", w)
sys.exit(1 if fails else 0)
