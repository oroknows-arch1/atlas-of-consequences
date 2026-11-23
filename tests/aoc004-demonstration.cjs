const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const { AxeBuilder } = require('@axe-core/playwright');

const url = process.env.AOC004_URL || 'http://127.0.0.1:4174/public/demos/aoc-004/';
const viewports = [
  { name: 'mobile', width: 390, height: 844 },
  { name: 'desktop', width: 1440, height: 900 },
];
const routes = ['nengi', 'daniel', 'jian', 'boma'];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];
  try {
    for (const viewport of viewports) {
      const context = await browser.newContext({ viewport });
      const page = await context.newPage();
      const errors = [];
      page.on('console', message => {
        if (message.type() === 'error') errors.push(message.text());
      });
      page.on('pageerror', error => errors.push(error.message));

      await page.goto(url, { waitUntil: 'networkidle' });
      assert.equal(await page.locator('#choices .choice').count(), 4);
      assert.equal(await page.locator('h1').textContent(), 'The Ground Beneath the Rig');
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), true);
      assert.equal(await page.locator('#opening video').count(), 3);
      assert.equal(await page.locator('#opening video').evaluateAll(v => v.every(x => x.muted)), true);
      assert.equal(await page.locator('audio').count(), 0);
      await page.locator('#skipOpening').click();
      await page.waitForTimeout(1100);
      assert.equal(await page.locator('#opening').getAttribute('data-opening-state'), 'skipped');
      assert.equal(await page.locator('.opening-copy').evaluate(el => getComputedStyle(el).opacity), '1');

      for (const route of routes) {
        await page.locator(`#choices .choice[data-route="${route}"]`).click();
        assert.equal(new URL(page.url()).hash, `#story-${route}`);
        assert.equal(await page.locator('#route').isVisible(), true);
        assert.equal(await page.locator('#route .scene').count(), 3);
        assert.equal(await page.locator('#route').evaluate(el => el === document.activeElement), true);
        await page.locator('#return').click();
        assert.equal(new URL(page.url()).hash, '#stories');
        assert.equal(await page.locator('#choices').isVisible(), true);
        await page.goto(`${url}#story-${route}`, { waitUntil: 'networkidle' });
        assert.equal(await page.locator('#route').isVisible(), true);
        assert.equal(await page.locator('#route .scene').count(), 3);
        await page.locator('#return').click();
      }

      for (const id of ['reality', 'consequences', 'place', 'sources']) {
        assert.equal(await page.locator(`#${id}`).count(), 1);
      }

      const accessibility = await new AxeBuilder({ page }).analyze();
      assert.deepEqual(accessibility.violations, []);
      assert.deepEqual(errors, []);
      results.push({ viewport: viewport.name, routes: routes.length, accessibilityViolations: 0, consoleErrors: 0 });
      await context.close();
    }
    process.stdout.write(`${JSON.stringify({ status: 'PASS', results }, null, 2)}\n`);
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
