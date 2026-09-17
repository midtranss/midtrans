#!/usr/bin/env python3
"""Regenerate meridian/meridian.css from the design system.

Meridian is an ADDITIVE skin: every style rule is scoped to [data-skin="meridian"].
The previous generator prefixed at-rules the same way it prefixed selectors, which
produced `[data-skin="meridian"] @keyframes ...` - invalid CSS. Browsers dropped
six of the seven keyframe blocks, so the alert flash, badge entrance, step-done,
toast entrance, skeleton sweep and row entrance were all dead in the skin.
At-rules are handled by kind here, never by string prefixing.
"""
import json, re, pathlib
import pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[2]

ROOT  = ROOT
DS    = ROOT/'design-system'
SCOPE = '[data-skin="meridian"]'
PREFIX = 'meridian-'

tokens = json.loads((DS/'tokens.json').read_text())
bundle = (DS/'components/bundle.css').read_text()

# ---------------------------------------------------------------- tokenizer --
def split_rules(css):
    """Yield (prelude, body|None) at one nesting level. Brace-matching, string
    and comment aware, so a `{` inside content: "..." cannot desynchronise it."""
    i, n, start, depth = 0, len(css), 0, 0
    prelude = None
    while i < n:
        c = css[i]
        if c == '/' and css[i:i+2] == '/*':
            j = css.find('*/', i+2); i = (j + 2) if j != -1 else n; continue
        if c in '"\'':
            q = c; i += 1
            while i < n and css[i] != q:
                i += 2 if css[i] == '\\' else 1
            i += 1; continue
        if c == '{':
            if depth == 0:
                prelude = css[start:i]; body_start = i + 1
            depth += 1; i += 1; continue
        if c == '}':
            depth -= 1
            if depth == 0:
                yield prelude, css[body_start:i]
                start = i + 1
            i += 1; continue
        if c == ';' and depth == 0:
            chunk = css[start:i+1].strip()
            if chunk: yield chunk, None      # a statement at-rule, e.g. @import
            start = i + 1; i += 1; continue
        i += 1

def scope_selector(sel):
    """Prefix each comma-separated part with the skin scope.

    A part that STARTS with an attribute selector is a state that can sit on the
    root element - [lang="ar"], [dir="rtl"], [data-theme="dark"] - and the
    documented install puts data-skin on that same <html>. A descendant form
    alone therefore never matches: Arabic keeps the Latin font and direction
    states never flip. Such parts get BOTH the self form and the descendant
    form, so the rule holds whether the state is on the skin element or inside
    it."""
    out = []
    for part in sel.split(','):
        p = part.strip()
        if not p: continue
        if p in (':root', 'html', ':root, html'): out.append(SCOPE)
        elif p == 'body':                         out.append(f'{SCOPE} body')
        elif p.startswith(':root'):               out.append(SCOPE + p[len(':root'):])
        elif p.startswith('['):
            out.append(f'{SCOPE}{p}')      # the state is on the skin element
            out.append(f'{SCOPE} {p}')     # the state is inside it
        else:                                     out.append(f'{SCOPE} {p}')
    return ',\n'.join(out)

# keyframe names defined in the bundle, so references can be rewritten
KF = set(re.findall(r'@keyframes\s+([A-Za-z_][\w-]*)', bundle))

def rename_anims(body):
    for name in KF:
        body = re.sub(rf'(animation(?:-name)?\s*:[^;]*?\b){re.escape(name)}\b',
                      rf'\g<1>{PREFIX}{name}', body)
    return body

COMMENT = re.compile(r'/\*.*?\*/', re.S)

def peel_comments(prelude):
    """Return (comments_verbatim, selector_text).

    Comments must be lifted out before anything is scoped. They are attached to
    the prelude of the rule that follows them, and a comment containing a comma
    would otherwise be split by the selector scoper and have a scope prefix
    spliced into the middle of an English sentence - which is exactly what the
    previous generator did."""
    comments = COMMENT.findall(prelude)
    return comments, COMMENT.sub('', prelude).strip()

def emit(prelude, body, indent=''):
    """Render one rule, recursing into conditional at-rules."""
    comments, pre = peel_comments(prelude)
    lead = ''.join(indent + c.strip() + '\n' for c in comments)
    return lead + _emit_rule(pre, body, indent)

def _emit_rule(pre, body, indent=''):
    if body is None:
        return indent + pre + '\n'
    if pre.startswith('@'):
        at = pre.split()[0].lower()
        if at == '@keyframes':
            # NEVER scope a keyframes block - just namespace its name.
            name = pre.split(None, 1)[1].strip()
            return f'{indent}@keyframes {PREFIX}{name} {{{body}}}\n'
        if at == '@font-face':
            return f'{indent}{pre} {{{body}}}\n'
        if at in ('@media', '@supports', '@layer', '@container'):
            inner = ''.join(emit(p, b, indent + '  ') for p, b in split_rules(body))
            return f'{indent}{pre} {{\n{inner}{indent}}}\n'
        return f'{indent}{pre} {{{body}}}\n'
    return f'{indent}{scope_selector(pre)} {{{rename_anims(body)}}}\n'

# ------------------------------------------------------------------- output --
L = ['/* ' + '=' * 72,
     '   MIDTRANS - Meridian',
     '   An ADDITIVE theme. Every style rule in this file is scoped to',
     f'   {SCOPE}, so nothing here applies until <html data-skin="meridian">',
     '   is set, and removing this one <link> restores the previous appearance',
     '   exactly.',
     '',
     '   This file never writes to :root, never redefines an existing class',
     '   outside that scope, and never renames or removes anything.',
     '',
     '       <html data-skin="meridian" data-theme="dark">',
     '                 ^ which design system      ^ light or dark, unchanged',
     '',
     '   Keyframes are namespaced (meridian-*) rather than scoped: a @keyframes',
     '   block cannot carry a selector, so prefixing one voids it.',
     '   GENERATED from design-system/tokens.json + components/bundle.css.',
     '   ' + '=' * 72 + ' */', '']

fams = tokens['type']['families']
def token_lines(theme, ind='  '):
    out = []
    for c in tokens['color']['tokens']: out.append(f"{ind}--{c['name']}: {c['value'][theme]};")
    for s in tokens['shadow']['tokens']: out.append(f"{ind}--{s['name']}: {s['value'][theme]};")
    return out

L.append(f'{SCOPE} {{')
L.append(f'  --font-sans: {fams["sans"]};')
L.append('  --font-arabic: "Meridian Cairo";')
L.append(f'  --font-mono: {fams["mono"]};')
for s in tokens['spacing']['tokens']: L.append(f"  --{s['name']}: {s['value']};")
for s in tokens['radius']['tokens']:  L.append(f"  --{s['name']}: {s['value']};")
L += token_lines('light')
L.append('}')

L.append(f'{SCOPE}[data-theme="dark"] {{')
L += token_lines('dark')
L.append('}')

L.append('@media (prefers-color-scheme: dark) {')
L.append(f'  {SCOPE}:not([data-theme="light"]) {{')
L += token_lines('dark', '    ')
L.append('  }')
L.append('}')

# Paper is white whatever the skin was set to. The documented install loads only
# meridian.css - it does not import tokens.css - so the source's print reset
# never reaches it, and an official quotation printed from a dark session came
# out as light text the browser drops the background behind.
L.append('@media print {')
L.append(f'  {SCOPE}, {SCOPE}[data-theme="light"], {SCOPE}[data-theme="dark"] {{')
for c in tokens['color']['tokens']:
    L.append(f"    --{c['name']}: {c['value']['light']};")
for s_ in tokens['shadow']['tokens']:
    L.append(f"    --{s_['name']}: none;")
L.append('  }')
L.append('}')

L += ['', '@font-face {', '  font-family: "Meridian Cairo";',
      '  src: url("fonts/cairo.woff2") format("woff2");',
      '  font-weight: 200 1000;', '  font-style: normal;',
      '  font-display: swap;', '}', '']

# type utility classes
for g in tokens['type']['groups']:
    for st in g['styles']:
        fam = {'sans':'--font-sans','arabic':'--font-arabic','mono':'--font-mono'}[st.get('family') or g['family']]
        L.append(f"{SCOPE} .{st['name']} {{ font-family: var({fam}); font-size: {st['fontSize']}; "
                 f"line-height: {st['lineHeight']}; font-weight: {st['fontWeight']}; "
                 f"letter-spacing: {st.get('letterSpacing') or '0'}; }}")
L.append('')

for prelude, body in split_rules(bundle):
    L.append(emit(prelude, body).rstrip('\n'))

out = '\n'.join(L) + '\n'
(ROOT/'meridian/meridian.css').write_text(out)
print(f'wrote meridian.css: {len(out):,} bytes, {out.count(chr(10)):,} lines')
code = COMMENT.sub('', out)   # self-checks must not read our own prose
print('keyframes emitted:', sorted(re.findall(r'@keyframes\s+([\w-]+)', code)))
bad = re.findall(r'[^\s{};]\s*@(?:keyframes|font-face|media)', code)
print('selector-prefixed at-rules:', len(bad), '(must be 0)')
stray = re.findall(r'\[data-skin="meridian"\][^{;]*?(?:seizure|threshold|Runs once)', code)
print('scope spliced into prose:', len(stray), '(must be 0)')
unref = [n for n in KF if f'{PREFIX}{n}' not in code]
print('keyframes defined but never renamed:', unref, '(must be [])')
