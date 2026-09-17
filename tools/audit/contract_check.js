// Check that what a component card promises is what the built system does.
//
// More than half the findings of four review rounds were of one kind: a card
// stated a rule and the CSS did something else. Nothing caught those, because
// the contrast, font and tap checks all test the code against itself.
//
// Prose cannot be parsed reliably, so this does not try. Each claim in
// contracts.json names a sentence from a card and a test of the built system,
// and the sentence must still appear in that card verbatim. Rewrite the card
// and the claim fails until it is updated with it: the two cannot drift apart
// without someone noticing.
const path = require('path');
const fs = require('fs');
const ROOT = path.resolve(__dirname, '..', '..');
const { chromium } = require(process.env.PW || 'playwright');

const BASE = 'http://localhost:8000';
const DS = path.join(ROOT, 'design-system');
const spec = JSON.parse(fs.readFileSync(path.join(__dirname, 'contracts.json'), 'utf8'));

const mountsIndex = path.join(ROOT, '.audit-mounts', 'index.json');
if (!fs.existsSync(mountsIndex)) {
  console.error(`No mounts at ${mountsIndex}.\nRun:  python3 tools/audit/gen_mounts.py`);
  process.exit(1);
}

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const fails = [];
  let checked = 0;

  for (const c of spec.claims) {
    // 1. the sentence must still be in the card it is quoted from
    const cardPath = path.join(DS, c.card);
    if (!fs.existsSync(cardPath)) {
      fails.push(`${c.id}: card ${c.card} does not exist`);
      continue;
    }
    const card = fs.readFileSync(cardPath, 'utf8');
    if (!card.includes(c.quote)) {
      fails.push(`${c.id}: ${c.card} no longer says "${c.quote}" — ` +
                 `the card was rewritten, so this claim needs rewriting with it`);
      continue;
    }

    // 2. the built system must do what the sentence says
    const width = c.width || 1100;
    const ctx = await browser.newContext({
      viewport: { width, height: 900 },
      hasTouch: width < 768, isMobile: width < 768,
    });
    const page = await ctx.newPage();
    const url = `${BASE}/.audit-mounts/${c.mount}.light.html`;
    try {
      const res = await page.goto(url, { waitUntil: 'networkidle' });
      if (!res || !res.ok()) throw new Error(`${res ? res.status() : 'no response'} for ${c.mount}`);
      await page.evaluate(() => document.fonts.ready);
      await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
      const got = await page.evaluate(new Function(c.test));
      checked++;
      if (got !== true) {
        fails.push(`${c.id} @${width}px: the card says "${c.quote}"\n` +
                   `      expected ${c.expect}, found ${got}`);
      }
    } catch (e) {
      fails.push(`${c.id}: could not check — ${e.message}`);
    }
    await ctx.close();
  }

  await browser.close();
  console.log(fails.length ? 'FAIL' : 'PASS',
              `(${checked}/${spec.claims.length} claims checked, ${fails.length} broken)`);
  for (const f of fails) console.log('  x', f);
  if (fails.length) process.exitCode = 1;
})();
