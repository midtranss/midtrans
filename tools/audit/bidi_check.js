/* Data runs read the same in every locale.
   Renders every component mount with dir="rtl" lang="ar" and finds every text
   node set in the mono face - references, weights, dates, money, phones - that
   carries a digit. For each, it measures where the first and last characters
   land on screen: a left-to-right run must start on the left. When the page is
   right-to-left and nothing isolates the run, "12 500 KG" is drawn as
   "KG 500 12" and "+963 11 9067" as "9067 11 +963", and this fails.

   It also holds two alignments that the fix could silently flip:
     - a reference cell sits at the start of its column (right, in RTL)
     - a number cell sits at the right in every locale, so units digits line up
   Exits non-zero on any failure.  ROOT=<repo>  PW=<playwright>  CHROME=<binary> */
const fs = require('fs'), path = require('path');
const { chromium } = require(process.env.PW || 'playwright');
const ROOT = process.env.ROOT || path.resolve(__dirname, '..', '..');
const BASE = process.env.BASE || 'http://localhost:8000';

const idx = JSON.parse(fs.readFileSync(path.join(ROOT, '.audit-mounts', 'index.json'), 'utf8'));
const mounts = (Array.isArray(idx) ? idx : (idx.mounts || Object.keys(idx)))
  .map(m => typeof m === 'string' ? m : (m.name || m.component))
  .filter(Boolean);

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const fails = [], seen = { runs: 0, mounts: 0 };

  for (const m of mounts) {
    const url = `${BASE}/.audit-mounts/${m}.light.html`;
    const r = await p.goto(url).catch(() => null);
    /* A page that did not load is a failure, never a skip: skipping silently
       once let this check report PASS having rendered nothing at all. */
    if (!r || !r.ok()) { fails.push(`${m}: mount did not load (${r ? r.status() : 'no response'}) at ${url}`); continue; }
    seen.mounts++;
    const res = await p.evaluate(() => {
      document.documentElement.setAttribute('dir', 'rtl');
      document.documentElement.setAttribute('lang', 'ar');
      void document.body.offsetHeight;
      const MONO = /mono|menlo|consolas|courier/i;
      const out = { runs: 0, bad: [], align: [] };
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let t = walker.nextNode(); t; t = walker.nextNode()) {
        const txt = t.textContent;
        if (!/\d/.test(txt) || txt.trim().length < 3) continue;
        const el = t.parentElement;
        if (!el || !MONO.test(getComputedStyle(el).fontFamily)) continue;
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        const s = txt.search(/\S/), e = txt.length - 1 - [...txt].reverse().join('').search(/\S/);
        if (s < 0 || e <= s) continue;
        const box = i => { const g = document.createRange(); g.setStart(t, i); g.setEnd(t, i + 1); return g.getBoundingClientRect(); };
        const a = box(s), z = box(e);
        if (!a.width || !z.width) continue;
        if (Math.abs(a.top - z.top) > 2) continue;           // wrapped: order across lines is not this test
        out.runs++;
        if (a.left > z.left) out.bad.push(txt.trim().slice(0, 40));
      }
      const hug = el => { const g = document.createRange(); g.selectNodeContents(el);
        const tb = g.getBoundingClientRect(), cb = el.getBoundingClientRect();
        return (tb.left - cb.left) < (cb.right - tb.right) ? 'left' : 'right'; };
      for (const el of document.querySelectorAll('td.mt-table__ref'))
        if (el.textContent.trim() && hug(el) !== 'right') out.align.push('reference cell hugs ' + hug(el) + ' in RTL: ' + el.textContent.trim());
      for (const el of document.querySelectorAll('td.mt-table__num'))
        if (el.textContent.trim() && hug(el) !== 'right') out.align.push('number cell hugs ' + hug(el) + ': ' + el.textContent.trim());
      return out;
    });
    seen.runs += res.runs;
    for (const x of res.bad)   fails.push(`${m}: drawn backwards in RTL: "${x}"`);
    for (const x of res.align) fails.push(`${m}: ${x}`);
  }
  await b.close();
  if (seen.mounts === 0) fails.push('no component rendered - is a server running on ' + BASE + '?');
  if (seen.runs < 20)    fails.push(`only ${seen.runs} data runs measured - too few to mean anything`);
  console.log(`  ${seen.mounts} components rendered right-to-left, ${seen.runs} data runs measured`);
  if (fails.length) {
    console.log(`FAILURES: ${fails.length}`);
    const uniq = [...new Set(fails)];
    for (const f of uniq.slice(0, 40)) console.log(' - ' + f);
    if (uniq.length > 40) console.log(`   … and ${uniq.length - 40} more`);
  } else console.log('PASS  every data run reads left-to-right inside right-to-left pages');
  process.exit(fails.length ? 1 : 0);
})();
