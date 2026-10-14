// Keyboard and enlarged-layout regression evidence, independent of audit scores.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright-core');
const origin = 'http://127.0.0.1:8766';
const routes = ['start', 'xoa-hl', ...[
  'first-login', 'create-vm', 'backup-restore', 'maintenance',
  'configuration-backup', 'troubleshooting', 'vm-operations', 'storage-networks',
  'vm-transfer', 'hosts-pools', 'permissions', 'sign-in-otp', 'concepts', 'configuration', 'automation',
].map(route => `xoa-hl/${route}`)];

async function focused(locator) {
  return locator.evaluate(element => element === document.activeElement);
}

// Reach controls through the real tab order; do not programmatically focus them.
async function tabTo(page, locator) {
  for (let attempt = 0; attempt < 160; attempt++) {
    if (await focused(locator)) return;
    await page.keyboard.press('Tab');
  }
  assert.fail(`Not reachable by Tab: ${locator}`);
}

async function readableLayout(page, label) {
  const problems = await page.evaluate(() => {
    const problems = [];
    if (document.documentElement.scrollWidth > innerWidth + 1) problems.push('page overflow');
    for (const element of document.querySelectorAll('nav.hextra-max-navbar-width > *, .hextra-breadcrumb a, .content h1')) {
      const box = element.getBoundingClientRect();
      if (!box.width || !box.height) continue;
      if (box.left < -1 || box.right > innerWidth + 1) problems.push('clipped navigation/heading');
    }
    for (const element of document.querySelectorAll('.hextra-breadcrumb a')) {
      const box = element.getBoundingClientRect();
      if (box.width < 24 || box.height < 24) problems.push('small breadcrumb target');
      if (element.scrollWidth > element.clientWidth + 1) problems.push('clipped breadcrumb text');
    }
    return problems;
  });
  assert.deepEqual(problems, [], label);
}

(async () => {
  fs.mkdirSync('browser-evidence', {recursive: true});
  const browser = await chromium.launch({executablePath: process.env.CHROME_BIN || undefined, headless: true});
  const context = await browser.newContext({viewport: {width: 1440, height: 1000}});
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  const evidence = [];
  for (const lang of ['', 'fr/', 'ja/']) {
    const code = lang.slice(0, -1) || 'en';
    const url = `${origin}/${lang}docs/xoa-hl/configuration-backup/`;
    await page.setViewportSize({width: 1440, height: 1000});
    await page.goto(url, {waitUntil: 'networkidle'});
    await page.keyboard.press('Tab');
    const skip = page.locator('body > a[href="#content"]');
    assert(await focused(skip), 'skip link must be first');
    assert(await skip.isVisible(), 'focused skip link visible');
    await page.keyboard.press('Enter');
    assert(page.url().endsWith('#content'), 'skip destination');

    await page.goto(url, {waitUntil: 'networkidle'});
    const inc = page.locator('.hextra-font-size-inc').first();
    await tabTo(page, inc);
    for (const button of await page.locator('.hextra-font-size button').all()) {
      assert((await button.getAttribute('aria-label')).includes(await button.textContent()), 'visible label in accessible name');
    }
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('html').getAttribute('data-font-scale'), 'l');
    await page.keyboard.press('Space');
    assert.equal(await page.locator('html').getAttribute('data-font-scale'), 'xl');
    assert(await inc.isDisabled(), 'maximum scale');
    await page.reload({waitUntil: 'networkidle'});
    assert.equal(await page.locator('html').getAttribute('data-font-scale'), 'xl', 'keyboard preference persisted');
    await tabTo(page, page.locator('.hextra-font-size-reset').first());
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('html').getAttribute('data-font-scale'), 'm');

    const theme = page.locator('.hextra-theme-toggle:visible').first();
    await tabTo(page, theme);
    await page.keyboard.press('Enter');
    assert(await focused(page.locator('.hextra-theme-toggle-options:visible [data-item="light"]')), 'theme initial focus');
    await page.keyboard.press('ArrowDown');
    assert(await focused(page.locator('.hextra-theme-toggle-options:visible [data-item="dark"]')), 'theme arrow focus');
    await page.keyboard.press('Escape');
    assert(await focused(theme), 'theme focus restored');
    assert.equal(await theme.getAttribute('aria-expanded'), 'false');

    const language = page.locator('.hextra-language-switcher:visible').first();
    await tabTo(page, language);
    await page.keyboard.press('ArrowDown');
    const languageItems = page.locator('.hextra-language-options:visible a');
    assert(await focused(languageItems.first()), 'language initial focus');
    await page.keyboard.press('End');
    assert(await focused(languageItems.last()), 'language End');
    await page.keyboard.press('Escape');
    assert(await focused(language), 'language focus restored');

    await page.goto(url, {waitUntil: 'networkidle'});
    const search = page.locator('.hextra-search-input:visible').first();
    await page.keyboard.press('Control+k');
    assert(await focused(search), 'search shortcut');
    await search.pressSequentially({en: 'automate', fr: 'automatiser', ja: '自動化'}[code]);
    await page.waitForFunction(expected => {
      const first = document.querySelector('.hextra-search-results a');
      return first && first.href === expected;
    }, `${origin}/${lang}docs/xoa-hl/automation/`);
    await page.keyboard.press('ArrowDown');
    assert(await page.evaluate(() => !!document.activeElement.closest('.hextra-search-results')), 'search result keyboard focus');
    // Hextra preselects result zero; Down moves to one, Up returns to zero.
    await page.keyboard.press('ArrowUp');
    assert.equal(await page.evaluate(() => document.activeElement.href), `${origin}/${lang}docs/xoa-hl/automation/`);
    await page.keyboard.press('Enter');
    await page.waitForURL(`${origin}/${lang}docs/xoa-hl/automation/`);

    await page.setViewportSize({width: 320, height: 800});
    await page.goto(url, {waitUntil: 'networkidle'});
    const hamburger = page.locator('.hextra-hamburger-menu');
    await tabTo(page, hamburger);
    await page.keyboard.press('Enter');
    assert.equal(await hamburger.getAttribute('aria-expanded'), 'true');
    assert(await page.evaluate(() => !!document.activeElement.closest('.hextra-sidebar-container')), 'mobile focus enters sidebar');
    await page.keyboard.press('Escape');
    assert(await focused(hamburger), 'mobile focus restored');
    assert.equal(await hamburger.getAttribute('aria-expanded'), 'false');
    assert.equal(await page.locator('.hextra-sidebar-container').getAttribute('aria-hidden'), 'true');
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => !!document.activeElement.closest('.hextra-sidebar-container')), false, 'closed sidebar excluded from Tab');
    evidence.push(`${code}: keyboard skip/font/theme/language/search/mobile navigation`);
    console.log(`PASS: ${evidence.at(-1)}`);

    // CSS viewport equivalents for 1440px at 200% and 1280px at 400% zoom.
    // This is reflow evidence, not browser UI zoom or pinch-zoom simulation.
    for (const width of [720, 320]) {
      await page.setViewportSize({width, height: 900});
      for (const route of ['', ...routes.map(route => `docs/${route}/`)]) {
        await page.goto(`${origin}/${lang}${route}`, {waitUntil: 'networkidle'});
        await readableLayout(page, `${code} ${route} ${width}px`);
      }
      await page.screenshot({path: `browser-evidence/reflow-${width}-${code}.png`, fullPage: true});
      evidence.push(`${code}: 16 entry/manual pages at ${width} CSS px`);
    }
    // Text resizing is separate from zoom; exercise the long title and navbar.
    for (const width of [1440, 390]) {
      await page.setViewportSize({width, height: 1000});
      await page.goto(url, {waitUntil: 'networkidle'});
      await page.evaluate(() => document.documentElement.style.fontSize = '200%');
      await readableLayout(page, `${code} 200% root text ${width}px`);
      await page.screenshot({path: `browser-evidence/text-200-${width}-${code}.png`});
      if (width === 390) {
        await tabTo(page, hamburger);
        await page.keyboard.press('Enter');
        await page.waitForFunction(() => {
          const nav = document.querySelector('nav.hextra-max-navbar-width').getBoundingClientRect();
          const focus = document.activeElement.getBoundingClientRect();
          return focus.top >= nav.bottom && focus.bottom <= innerHeight;
        });
        await page.keyboard.press('Escape');
        assert(await focused(hamburger), 'enlarged mobile focus restored');
      }
      evidence.push(`${code}: 200% root text at ${width}px`);
    }
  }
  assert.deepEqual(errors, []);
  fs.writeFileSync('browser-evidence/accessibility-interactions.json', JSON.stringify({checks: evidence}, null, 2) + '\n');
  await browser.close();
  evidence.forEach(check => console.log(`PASS: ${check}`));
})().catch(error => {console.error(error); process.exit(1)});
