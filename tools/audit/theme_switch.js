/* Proves the Meridian switch does what INSTALL.md says it does:
   - with the skin off, a legacy component keeps its own appearance
   - preview('meridian') restyles it
   - preview('default') returns it byte-identically
   - the transition freeze is applied during the flip and cleaned up after
   Exits non-zero on any failure.  ROOT=<repo>  PW=<playwright path> */
const fs = require('fs'), os = require('os'), path = require('path');
const { chromium } = require(process.env.PW || 'playwright');

const ROOT = process.env.ROOT || path.resolve(__dirname, '..', '..');
const M = path.join(ROOT, 'meridian');

(async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'skin-'));
  fs.mkdirSync(path.join(dir, 'fonts'));
  fs.copyFileSync(path.join(M, 'meridian.css'), path.join(dir, 'meridian.css'));
  fs.copyFileSync(path.join(M, 'fonts', 'cairo.woff2'), path.join(dir, 'fonts', 'cairo.woff2'));
  fs.copyFileSync(path.join(M, 'install', 'meridian-theme.js'), path.join(dir, 'meridian-theme.js'));
  /* A component whose every property collides with one Meridian sets. */
  fs.writeFileSync(path.join(dir, 'legacy.css'),
    '.mt-btn{background:rgb(1,2,3);color:rgb(4,5,6);font-family:"LegacyFace";border-radius:3px;padding:7px}');
  fs.writeFileSync(path.join(dir, 'page.html'),
    '<!doctype html><html lang="en"><head><meta charset="utf-8">' +
    '<link rel="stylesheet" href="legacy.css"><link rel="stylesheet" href="meridian.css">' +
    '<script src="meridian-theme.js"></script></head><body>' +
    '<button class="mt-btn mt-btn--primary" id="b">Book</button>' +
    '<p lang="ar" id="ar">شحنة بحرية</p></body></html>');

  const b = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const p = await b.newPage();
  await p.goto('file://' + path.join(dir, 'page.html'));
  await p.evaluate(() => document.fonts.ready);

  const snap = () => p.evaluate(() => {
    const cs = getComputedStyle(document.getElementById('b'));
    const ar = getComputedStyle(document.getElementById('ar'));
    return { skin: document.documentElement.getAttribute('data-skin'),
             bg: cs.backgroundColor, radius: cs.borderTopLeftRadius, pad: cs.paddingTop,
             font: cs.fontFamily.split(',')[0].replace(/"/g, ''),
             arFont: ar.fontFamily.split(',')[0].replace(/"/g, '') };
  });
  const frames = () => p.evaluate(() => new Promise(r =>
    requestAnimationFrame(() => requestAnimationFrame(() => requestAnimationFrame(r)))));
  const freezes = () => p.evaluate(() => document.querySelectorAll('[data-meridian-freeze]').length);

  const off1 = await snap();
  const applied = await p.evaluate(() => window.MidtransTheme.preview('meridian'));
  const during = await freezes();
  const on = await snap();
  await frames();
  const afterOn = await freezes();
  const back = await p.evaluate(() => window.MidtransTheme.preview('default'));
  const off2 = await snap();
  await frames();
  const afterOff = await freezes();

  const fail = [];
  if (off1.bg !== 'rgb(1, 2, 3)' || off1.radius !== '3px' || off1.font !== 'LegacyFace')
    fail.push('skin off is not the legacy appearance: ' + JSON.stringify(off1));
  if (applied !== 'meridian' || on.skin !== 'meridian') fail.push('preview("meridian") did not apply');
  if (on.bg === off1.bg || on.radius === off1.radius || on.font === off1.font)
    fail.push('skin on did not restyle the component');
  if (on.arFont !== 'Meridian Cairo') fail.push('Arabic is not Cairo under the skin: ' + on.arFont);
  if (back !== 'default' || off2.skin !== null) fail.push('preview("default") did not remove the attribute');
  if (JSON.stringify(off1) !== JSON.stringify(off2))
    fail.push('round trip is not identical:\n    ' + JSON.stringify(off1) + '\n    ' + JSON.stringify(off2));
  if (during === 0) fail.push('no transition freeze during the flip');
  if (afterOn !== 0 || afterOff !== 0) fail.push('freeze style left behind (' + afterOn + '/' + afterOff + ')');

  console.log('  off    ' + JSON.stringify(off1));
  console.log('  on     ' + JSON.stringify(on));
  console.log('  off    ' + JSON.stringify(off2));
  console.log('  freeze during=' + during + ' after=' + afterOn + '/' + afterOff);
  console.log(fail.length ? 'FAILURES: ' + fail.length + '\n - ' + fail.join('\n - ')
                          : 'PASS  legacy preserved, skin applies, round trip identical');
  await b.close();
  fs.rmSync(dir, { recursive: true, force: true });
  process.exit(fail.length ? 1 : 0);
})();
