const path=require('path');
const ROOT=path.resolve(__dirname,'..','..');
const { chromium } = require(process.env.PW || 'playwright');
const LEGACY = ['.legacy-card', '.legacy-btn', '.legacy-card h3', '.legacy-card p'];
const PROPS = ['backgroundColor','color','borderRadius','fontFamily','fontSize','lineHeight',
               'padding','border','boxShadow','fontWeight','margin'];

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const ctx0 = await b.newContext();
  const p = await ctx0.newPage();
  await p.goto('http://localhost:8000/drafts/skin-proof.html', { waitUntil: 'networkidle' });

  const snap = () => p.evaluate(({LEGACY, PROPS}) => {
    const o = {};
    for (const sel of LEGACY) {
      const el = document.querySelector(sel); if (!el) { o[sel] = 'MISSING'; continue; }
      const cs = getComputedStyle(el);
      o[sel] = PROPS.map(k => `${k}:${cs[k]}`).join('|');
    }
    return o;
  }, {LEGACY, PROPS});

  const set = (skin, theme) => p.evaluate(({skin, theme}) => {
    const h = document.documentElement;
    skin ? h.setAttribute('data-skin','meridian') : h.removeAttribute('data-skin');
    theme ? h.setAttribute('data-theme',theme) : h.removeAttribute('data-theme');
  }, {skin, theme});

  await set(false, null); const off      = await snap();
  await set(true,  null); const on       = await snap();
  await set(true,  'dark'); const onDark = await snap();

  let leaks = 0;
  for (const sel of LEGACY) {
    if (off[sel] !== on[sel])     { console.log(`LEAK skin-on   ${sel}\n  off: ${off[sel]}\n  on : ${on[sel]}`); leaks++; }
    if (off[sel] !== onDark[sel]) { console.log(`LEAK skin+dark ${sel}\n  off: ${off[sel]}\n  on : ${onDark[sel]}`); leaks++; }
  }
  console.log('ISOLATION LEAKS :', leaks, '(must be 0)');
  console.log('  legacy sample :', off['.legacy-card'].slice(0, 96));

  // --- the Meridian side must actually be styled when the skin is on -------
  await set(true, null);
  const styled = await p.evaluate(() => {
    const el = document.querySelector('.mt-card'); if (!el) return 'MISSING';
    const cs = getComputedStyle(el);
    return { radius: cs.borderRadius, bg: cs.backgroundColor, font: cs.fontFamily.split(',')[0] };
  });
  console.log('MERIDIAN APPLIED:', JSON.stringify(styled));

  // --- the alert flash must actually run -----------------------------------
  const flash = await p.evaluate(async () => {
    const host = document.createElement('div');
    host.className = 'mt-alert mt-alert--warning';
    host.setAttribute('data-flash','');
    document.body.appendChild(host);
    await new Promise(r => requestAnimationFrame(r));
    const cs = getComputedStyle(host);
    const anims = host.getAnimations().map(a => ({ name: a.animationName, dur: a.effect.getTiming().duration }));
    const r = { animationName: cs.animationName, duration: cs.animationDuration, running: anims };
    host.remove();
    return r;
  });
  console.log('ALERT FLASH     :', JSON.stringify(flash));

  // --- Arabic with the skin on the SAME element, as the install documents ---
  // [data-skin="meridian"] [lang="ar"] is a descendant selector; with both on
  // <html> it never matched, and Arabic fell back to Helvetica and to the
  // browser's serif. The generator now emits the self form too.
  const arPage = await ctx0.newPage();
  await arPage.setContent(`<!doctype html><html lang="ar" dir="rtl" data-skin="meridian">
    <head><meta charset="utf-8"><link rel="stylesheet" href="http://localhost:8000/meridian/meridian.css"></head>
    <body><div class="mt-card"><h2 class="mt-card__title">الشحنات</h2></div>
    <button class="mt-btn mt-btn--primary">طلب</button></body></html>`,
    { waitUntil: 'networkidle' });
  await arPage.evaluate(() => document.fonts.ready);
  const ar = await arPage.evaluate(() =>
    ['.mt-card__title', '.mt-btn--primary'].map(s => getComputedStyle(document.querySelector(s)).fontFamily));
  const arBad = ar.filter(f => !/Cairo/i.test(f));
  console.log('ARABIC ON SKIN  :', arBad.length === 0 ? 'Cairo ✓' : `NOT Cairo: ${arBad.join(' | ')}`);
  await arPage.close();

  const failures =
    leaks +
    (styled === 'MISSING' || styled.radius === '0px' ? 1 : 0) +
    (flash.running && flash.running.length ? 0 : 1) +
    arBad.length;
  console.log('FAILURES        :', failures);
  await b.close();
  if (failures) process.exitCode = 1;   // a check that cannot fail is not a check
})();
