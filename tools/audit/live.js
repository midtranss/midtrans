const path=require('path');
const ROOT=path.resolve(__dirname,'..','..');
const { chromium } = require(process.env.PW || 'playwright');
const fs = require('fs');
const BASE = 'http://localhost:8000';
const names = JSON.parse(fs.readFileSync(ROOT + '/.audit-mounts/index.json','utf8'));

const IN_PAGE = () => {
  const out = { fonts: [], contrast: [], taps: [], focus: [], arabic: [] };
  const APPROVED = ['Liberation Sans','Helvetica','Arial','Cairo','Liberation Mono','DejaVu Sans Mono','monospace'];
  const srgb = c => { c/=255; return c<=0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055,2.4); };
  const lum = ([r,g,b]) => 0.2126*srgb(r)+0.7152*srgb(g)+0.0722*srgb(b);
  const parse = s => { const m=String(s).match(/rgba?\(([^)]+)\)/); if(!m) return null;
    const p=m[1].split(',').map(x=>parseFloat(x)); return {rgb:[p[0],p[1],p[2]], a:p.length>3?p[3]:1}; };
  const ratio = (f,b) => { const L1=lum(f), L2=lum(b); const [hi,lo]=L1>L2?[L1,L2]:[L2,L1];
    return (hi+0.05)/(lo+0.05); };
  const over = (fg,bg) => fg.a>=1 ? fg.rgb : fg.rgb.map((c,i)=>c*fg.a + bg[i]*(1-fg.a));

  function effBg(el){
    let n = el;
    while (n && n !== document.documentElement) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c && c.a > 0) {
        if (c.a >= 1) return c.rgb;
        const under = effBg(n.parentElement || document.body);
        return c.rgb.map((x,i)=>x*c.a + under[i]*(1-c.a));
      }
      n = n.parentElement;
    }
    const b = parse(getComputedStyle(document.body).backgroundColor);
    return (b && b.a>0) ? b.rgb : [255,255,255];
  }

  const path = el => { const p=[]; let n=el;
    while(n && n.nodeType===1 && p.length<4){ let s=n.tagName.toLowerCase();
      if(n.className && typeof n.className==='string'){ const cl=n.className.trim().split(/\s+/).filter(Boolean).slice(0,2); if(cl.length) s+='.'+cl.join('.'); }
      p.unshift(s); n=n.parentElement; } return p.join(' > '); };

  const all = [...document.querySelectorAll('*')];
  for (const el of all) {
    const cs = getComputedStyle(el);
    if (cs.display==='none' || cs.visibility==='hidden' || parseFloat(cs.opacity)===0) continue;
    const r = el.getBoundingClientRect();
    const hasText = [...el.childNodes].some(n => n.nodeType===3 && n.textContent.trim().length>0);

    if (hasText && r.width>0 && r.height>0) {
      // resolved font: first family actually used
      const fam = cs.fontFamily;
      const first = fam.split(',')[0].replace(/["']/g,'').trim();
      const ok = APPROVED.some(a => fam.toLowerCase().includes(a.toLowerCase()));
      if (!ok) out.fonts.push({ sel: path(el), fontFamily: fam });

      const fg = parse(cs.color);
      if (fg) {
        const bg = effBg(el);
        const f = over(fg, bg);
        const cr = ratio(f, bg);
        const size = parseFloat(cs.fontSize);
        const wt = parseInt(cs.fontWeight) || 400;
        const large = size >= 24 || (size >= 18.66 && wt >= 700);
        const floor = large ? 3.0 : 4.5;
        if (cr < floor - 0.005) out.contrast.push({ sel: path(el), ratio: +cr.toFixed(2), floor, size, weight: wt,
          color: cs.color, bg: `rgb(${bg.map(Math.round).join(', ')})`, text: el.textContent.trim().slice(0,40) });
      }
    }

    if (/^(a|button)$/i.test(el.tagName) || el.getAttribute('role')==='button' ||
        (/^input$/i.test(el.tagName) && /button|submit|checkbox|radio/i.test(el.type||''))) {
      if (r.width>0 && r.height>0) out.taps.push({ sel: path(el), w:+r.width.toFixed(1), h:+r.height.toFixed(1) });
    }
  }

  // --- focus rings: 2px minimum, 3:1 against what sits behind them ---------
  // Email HTML cannot carry :focus-visible - inline styles only, and the mail
  // client owns the focus ring. Checking it would report the client, not us.
  const EMAIL = document.body.dataset.component === 'EmailTemplate';
  const focusables = EMAIL ? [] : [...document.querySelectorAll('a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])')];
  for (const el of focusables) {
    const cs0 = getComputedStyle(el);
    if (cs0.display === 'none' || cs0.visibility === 'hidden') continue;
    try { el.focus({ preventScroll: true }); } catch (e) { continue; }
    if (document.activeElement !== el) continue;
    const cs = getComputedStyle(el);
    const w = parseFloat(cs.outlineWidth) || 0;
    const style = cs.outlineStyle;
    const ringCol = parse(cs.outlineColor);
    const bg = effBg(el.parentElement || document.body);
    const entry = { sel: path(el), width: w, style, color: cs.outlineColor };
    if (style === 'none' || w < 2) { entry.problem = 'ring thinner than 2px or absent'; out.focus.push(entry); }
    else if (ringCol) {
      const cr = ratio(over(ringCol, bg), bg);
      if (cr < 3 - 0.005) { entry.problem = `ring contrast ${cr.toFixed(2)} < 3`; entry.bg = `rgb(${bg.map(Math.round).join(', ')})`; out.focus.push(entry); }
    }
    el.blur();
  }

  // --- Arabic must resolve to Cairo, and Cairo must actually be loaded -----
  // Check every text-bearing DESCENDANT of an Arabic subtree, not just the
  // element carrying the attribute: a component that declares its own
  // font-family overrides the inherited one, which is how Arabic silently
  // fell back to Helvetica in buttons, badges, table headers and labels.
  const arRoots = [...document.querySelectorAll('[lang="ar"], [lang^="ar-"]')];
  const loaded = document.fonts.check('16px Cairo');
  const ARABIC = /[\u0600-\u06FF]/;
  for (const r of arRoots) {
    const inTree = [r, ...r.querySelectorAll('*')];
    for (const el of inTree) {
      const own = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('');
      if (!ARABIC.test(own)) continue;              // only elements holding Arabic text
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      const fam = cs.fontFamily;
      if (/mono|Consolas|Menlo/i.test(fam)) continue; // reference numbers stay mono by design
      if (!/Cairo/i.test(fam)) out.arabic.push({ sel: path(el), fontFamily: fam, reason: 'Arabic text not in Cairo', text: own.trim().slice(0, 30) });
      else if (!loaded) out.arabic.push({ sel: path(el), fontFamily: fam, reason: 'Cairo not loaded' });
    }
  }
  return out;
};

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const report = { fonts: [], contrast: [], taps: [], focus: [], arabic: [] };
  for (const theme of ['light','dark']) {
    for (const viewport of [{name:'desktop',width:1280,height:900,coarse:false},
                            {name:'phone',width:360,height:780,coarse:true}]) {
      const ctx = await browser.newContext({
        viewport: {width:viewport.width, height:viewport.height},
        hasTouch: viewport.coarse, isMobile: viewport.coarse,
        deviceScaleFactor: 1
      });
      const page = await ctx.newPage();
      for (const n of names) {
        await page.goto(`${BASE}/.audit-mounts/${n}.${theme}.html`, { waitUntil: 'networkidle' });
        await page.evaluate(() => document.fonts.ready);
        await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
        const themeNow = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
        if (themeNow !== theme) throw new Error(`theme mismatch on ${n}: ${themeNow}`);
        const r = await page.evaluate(IN_PAGE);
        const tag = { component: n, theme, viewport: viewport.name };
        r.fonts.forEach(x => report.fonts.push({ ...tag, ...x }));
        r.contrast.forEach(x => report.contrast.push({ ...tag, ...x }));
        r.focus.forEach(x => report.focus.push({ ...tag, ...x }));
        r.arabic.forEach(x => report.arabic.push({ ...tag, ...x }));
        if (viewport.coarse) r.taps.forEach(x => { if (x.h < 44 || x.w < 44) report.taps.push({ ...tag, ...x }); });
      }
      await ctx.close();
    }
  }
  await browser.close();
  fs.writeFileSync('/tmp/claude-0/-home-user-midtrans/b6fd8a7d-89db-5cf7-9118-d06fe6209c6b/scratchpad/audit/live-report.json', JSON.stringify(report,null,1));
  console.log('FONT FAILS   :', report.fonts.length);
  console.log('CONTRAST FAILS:', report.contrast.length);
  console.log('TAP FAILS    :', report.taps.length);
  console.log('FOCUS FAILS  :', report.focus.length);
  console.log('ARABIC FAILS :', report.arabic.length);
})();
