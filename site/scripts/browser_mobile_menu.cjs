// CI-only regression for xcp-hl#298. Use the real Hugo output and theme JS.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright-core');

(async () => {
  const browser = await chromium.launch({executablePath: process.env.CHROME_BIN || undefined, headless: true});
  try {
    const page = await browser.newPage();
    fs.mkdirSync('browser-evidence', {recursive: true});
    for (const lang of ['', 'fr/', 'ja/']) {
      const code = lang.replace('/', '') || 'en';
      const manual = `/${lang}docs/xoa-hl/`;
      const release = `/${lang}docs/reference/release-matrix/`;
      for (const width of [320, 390, 767]) {
        await page.setViewportSize({width, height: 844});
        for (const route of ['', 'docs/', 'docs/xoa-hl/', 'docs/xoa-hl/first-login/']) {
          await page.goto(`http://127.0.0.1:8766/${lang}${route}`, {waitUntil: 'networkidle'});
          await page.locator('.hextra-hamburger-menu').click();
          const sidebar = page.locator('.hextra-sidebar-container');
          assert.equal(await sidebar.getAttribute('aria-hidden'), 'false');
          // Each shortcut must own one tree, not also recur under Documentation.
          const entry = sidebar.locator(`a[href="${manual}"]:visible`);
          assert.equal(await entry.count(), 1, `${code} ${width}px ${route}: duplicate manual`);
          assert.equal(await sidebar.locator(`a[href="${release}"]:visible`).count(), 1,
            `${code} ${width}px ${route}: duplicate release matrix`);
          const group = entry.locator('xpath=../..');
          const toggle = group.locator(':scope > .hextra-sidebar-item button');
          assert.equal(await toggle.count(), 1, 'manual must remain expandable');
          const chapter = group.locator(`a[href="${manual}first-login/"]:visible`);
          assert.equal(await chapter.count(), 1, 'manual chapters missing');
          await toggle.scrollIntoViewIfNeeded();
          await toggle.click();
          assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
          assert.equal(await group.locator(':scope > .hextra-sidebar-children').evaluate(el => el.clientHeight), 0,
            'manual subtree did not collapse');
          await toggle.click();
          assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
          assert(await group.locator(':scope > .hextra-sidebar-children').evaluate(el => el.clientHeight > 0),
            'manual subtree did not expand');
          if (route === 'docs/xoa-hl/first-login/') {
            assert(await chapter.evaluate(el => el.classList.contains('hextra-sidebar-active-item')),
              'current chapter lost its active state');
          }
          if (width === 390 && route === 'docs/xoa-hl/') {
            await entry.scrollIntoViewIfNeeded();
            await page.screenshot({path: `browser-evidence/mobile-menu-${code}.png`});
          }
          await chapter.click();
          await page.waitForURL(`**${manual}first-login/`);
          assert.equal(await page.locator('main h1').count(), 1);
        }
      }
      // Desktop keeps both its navbar shortcut and its hierarchical sidebar.
      await page.setViewportSize({width: 1440, height: 1000});
      await page.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/first-login/`, {waitUntil: 'networkidle'});
      assert.equal(await page.locator(`nav a[href="${manual}"]:visible`).count(), 1);
      assert.equal(await page.locator(`.hextra-sidebar-container a[href="${manual}"]:visible`).count(), 1);
      console.log(`PASS: ${code} mobile menu: one expandable manual, unique release matrix, chapter navigation and desktop links`);
    }
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
