const path=require('path');
const ROOT=path.resolve(__dirname,'..','..');
const { chromium } = require(process.env.PW || 'playwright');
const LEGACY = ['.legacy-card', '.legacy-btn', '.legacy-card h3', '.legacy-card p'];
const PROPS = ['backgroundColor','color','borderRadius','fontFamily','fontSize','lineHeight',
               'padding','border','boxShadow','fontWeight','margin'];

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const p = await b.newPage();
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
  await b.close();
})();
