import re, json, sys
import pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[2]
COMMENT = re.compile(r'/\*.*?\*/', re.S)
def split_rules(css):
    i, n, start, depth = 0, len(css), 0, 0
    prelude = None; body_start = 0
    while i < n:
        c = css[i]
        if c == '/' and css[i:i+2] == '/*':
            j = css.find('*/', i+2); i = (j+2) if j != -1 else n; continue
        if c in '"\'':
            q = c; i += 1
            while i < n and css[i] != q: i += 2 if css[i] == '\\' else 1
            i += 1; continue
        if c == '{':
            if depth == 0: prelude = css[start:i]; body_start = i+1
            depth += 1; i += 1; continue
        if c == '}':
            depth -= 1
            if depth == 0:
                yield prelude, css[body_start:i]; start = i+1
            i += 1; continue
        i += 1

css = open(ROOT/'design-system/components/bundle.css').read()
decl = {}
for pre, body in split_rules(css):
    pre  = COMMENT.sub('', pre).strip()
    body = COMMENT.sub('', body)
    if pre.startswith('@'): continue
    has = bool(re.search(r'(?:^|;)\s*font-family\s*:', body))
    for part in pre.split(','):
        p = part.strip()
        if not p: continue
        decl[p] = decl.get(p, False) or has
roots = sorted({m.group(1) for p in decl for m in [re.fullmatch(r'\.(mt-[a-z0-9]+)', p)] if m})
missing = [r for r in roots if not decl.get(f'.{r}')]
print(json.dumps({'roots': len(roots), 'missing': missing}, indent=1))
