/* Proves the veneer paints without moving anything.
   Builds a page with its own stylesheet - deliberately unlike the design
   system - applies each layer, and fails if the colour or surface layer moved
   a single box by more than half a pixel, or if turning the veneer off does
   not return the page to exactly what it was.
   The type layer is EXPECTED to reflow; it is reported, not judged.
   Exits non-zero on any failure.  ROOT=<repo>  PW=<playwright>  CHROME=<binary> */
const fs = require('fs'), os = require('os'), path = require('path');
const { chromium } = require(process.env.PW || 'playwright');
const ROOT = process.env.ROOT || path.resolve(__dirname, '..', '..');

const IDS = ['nav','hero','h1','hp','grid','c1','c2','c3','tbl','frm','inp','sel','btn','ar','foot'];

const LEGACY = `
body{margin:0;font-family:Georgia,serif;font-size:14px;line-height:1.5;color:#333;background:#fbfbf7}
.nav{background:#1b3a5c;padding:12px 20px}
.nav a{color:#cfe2f3;margin-right:16px;text-decoration:none;font-size:13px}
.hero{padding:40px 20px;background:#eef3f7}
.hero h1{margin:0 0 10px;font-size:30px;line-height:1.2;color:#14293f}
.hero p{margin:0;font-size:16px;max-width:600px}
.grid{display:flex;gap:16px;padding:24px 20px}
.card{flex:1;border:1px solid #c9d3dd;border-radius:2px;padding:16px;background:#fff}
.card h3{margin:0 0 8px;font-size:17px} .card p{margin:0;font-size:13px}
table{width:100%;border-collapse:collapse;margin:0 20px}
th,td{border:1px solid #c9d3dd;padding:8px;text-align:left;font-size:13px}
form{padding:24px 20px}
button{background:#1b3a5c;color:#fff;border:1px solid #1b3a5c;border-radius:2px;padding:9px 18px;font-size:14px}
.foot{background:#14293f;color:#b9c9d8;padding:20px;font-size:12px}`;

const PAGE = `<!doctype html><html lang="en"><head><meta charset="utf-8">
<link rel="stylesheet" href="legacy.css"><link rel="stylesheet" href="midtrans-veneer.css"></head><body>
<div class="nav" id="nav"><a href="#">Services</a><a href="#">Trade lanes</a><a href="#">Contact</a></div>
<div class="hero" id="hero"><h1 id="h1">Sea freight to Syria, UAE and Jebel Ali</h1>
<p id="hp">MIDTRANS has moved cargo through the eastern Mediterranean since 1998.</p></div>
<div class="grid" id="grid">
<div class="card" id="c1"><h3>Sea freight</h3><p>FCL and LCL, with in-house customs clearance.</p></div>
<div class="card" id="c2"><h3>Air freight</h3><p>Consolidations and charters on request.</p></div>
<div class="card" id="c3"><h3>Land freight</h3><p>Cross-border trucking across the GCC and Levant.</p></div></div>
<table id="tbl"><tr><th>Lane</th><th>Mode</th></tr><tr><td>Jebel Ali to Lattakia</td><td>Sea</td></tr></table>
<form id="frm"><input id="inp" placeholder="Your email"><select id="sel"><option>Sea</option></select>
<button id="btn" type="button">Request a quotation</button></form>
<p lang="ar" id="ar" style="padding:0 20px">&#1588;&#1581;&#1606;&#1577; &#1576;&#1581;&#1585;&#1610;&#1577;</p>
<div class="foot" id="foot">MIDTRANS SHIPPING AND SERVICES</div></body></html>`;

/* Two box models, because a border-adding rule is only safe under one of them
   and most older sites are the other. */
const MODELS = {
  'border-box': '*{box-sizing:border-box}\ninput,select{border:1px solid #bbb;border-radius:2px;padding:8px;font-size:14px;width:220px}',
  'content-box': 'input,select{border:0;padding:8px;font-size:14px;width:220px}',
};

(async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'veneer-'));
  fs.mkdirSync(path.join(dir, 'fonts'));
  fs.copyFileSync(path.join(ROOT, 'veneer', 'midtrans-veneer.css'), path.join(dir, 'midtrans-veneer.css'));
  fs.copyFileSync(path.join(ROOT, 'veneer', 'fonts', 'cairo.woff2'), path.join(dir, 'fonts', 'cairo.woff2'));
  fs.writeFileSync(path.join(dir, 'page.html'), PAGE);

  const b = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const fail = [];

  for (const [model, extra] of Object.entries(MODELS)) {
    fs.writeFileSync(path.join(dir, 'legacy.css'), extra + '\n' + LEGACY);
    const p = await b.newPage({ viewport: { width: 1000, height: 900 } });
    await p.goto('file://' + path.join(dir, 'page.html'));
    await p.evaluate(() => document.fonts.ready);

    const snap = () => p.evaluate(ids => {
      const s = document.createElement('style');
      s.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}';
      document.head.appendChild(s); void document.body.offsetHeight;
      const o = {};
      for (const id of ids) {
        const e = document.getElementById(id); if (!e) continue;
        const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
        o[id] = { x:+r.x.toFixed(2), y:+r.y.toFixed(2), w:+r.width.toFixed(2), h:+r.height.toFixed(2),
                  color:cs.color, bg:cs.backgroundColor, size:cs.fontSize, lh:cs.lineHeight,
                  font:cs.fontFamily.split(',')[0].replace(/"/g,''),
                  radius:cs.borderTopLeftRadius, shadow:cs.boxShadow };
      }
      s.remove(); return o;
    }, IDS);
    const set = v => p.evaluate(x => x === null ? document.documentElement.removeAttribute('data-mt')
                                                : document.documentElement.setAttribute('data-mt', x), v);
    const moved = (a, z) => {
      const out = [];
      for (const k of Object.keys(a)) { if (!z[k]) continue;
        for (const f of ['x','y','w','h']) if (Math.abs(a[k][f] - z[k][f]) > 0.5) out.push(`${k}.${f} ${a[k][f]}->${z[k][f]}`); }
      return out;
    };
    const painted = (a, z) => {
      let n = 0;
      for (const k of Object.keys(a)) { if (!z[k]) continue;
        for (const f of ['color','bg','font','size','lh','radius','shadow']) if (a[k][f] !== z[k][f]) n++; }
      return n;
    };

    await set(null);                  const off = await snap();
    await set('colour');              const col = await snap();
    await set('colour surface');      const srf = await snap();
    await set('colour surface type'); const typ = await snap();
    await set(null);                  const back = await snap();

    const mc = moved(off, col), ms = moved(off, srf), mt = moved(off, typ);
    const rt = moved(off, back).length + painted(off, back);

    console.log(`  ${model}`);
    console.log(`    colour        moved ${mc.length}   painted ${painted(off, col)}`);
    console.log(`    colour+surface moved ${ms.length}   painted ${painted(off, srf)}`);
    console.log(`    +type         moved ${mt.length}   painted ${painted(off, typ)}   (reflow is expected here)`);
    console.log(`    round trip    ${rt === 0 ? 'identical' : rt + ' difference(s)'}`);

    if (mc.length) fail.push(`${model}: colour layer moved ${mc.length} box(es) - ${mc.slice(0,4).join(', ')}`);
    if (ms.length) fail.push(`${model}: surface layer moved ${ms.length} box(es) - ${ms.slice(0,4).join(', ')}`);
    if (rt) fail.push(`${model}: turning the veneer off did not restore the page`);
    /* "something changed" is too weak a test: the Arabic rule alone satisfies
       it, so a typo in the colour selector passed once. Assert the token
       values themselves land. */
    const want = { 'hp.color': 'rgb(31, 52, 72)',    // ink-body
                   'h1.color': 'rgb(10, 36, 64)',    // ink-strong
                   'inp.radius': '8px' };            // radius-md, surface layer
    /* NOT the site's .card: the veneer names no class the site owns, so a
       <div class="card"> is invisible to it. Only element selectors land. */
    const got = { 'hp.color': col.hp.color, 'h1.color': col.h1.color, 'inp.radius': srf.inp.radius };
    for (const [k, v] of Object.entries(want))
      if (got[k] !== v) fail.push(`${model}: ${k} is ${got[k]}, expected ${v} - the layer is not applied`);
    if (!mt.length) fail.push(`${model}: type layer moved nothing - it is not being applied`);
    await p.close();
  }

  await b.close();
  fs.rmSync(dir, { recursive: true, force: true });
  console.log(fail.length ? `FAILURES: ${fail.length}\n - ` + fail.join('\n - ')
                          : 'PASS  colour and surface paint without moving anything, under both box models');
  process.exit(fail.length ? 1 : 0);
})();
