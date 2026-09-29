// CI-only interaction checks. Node/Playwright are not Hugo build dependencies.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright-core');
(async () => {
  const browser = await chromium.launch({executablePath: process.env.CHROME_BIN || undefined, headless:true});
  const context = await browser.newContext({viewport:{width:1440,height:1000}, colorScheme:'dark'});
  const page = await context.newPage();
  const errors=[];
  page.on('pageerror', error=>errors.push(String(error)));
  page.on('response', response=> { if(response.status()>=400) errors.push(`${response.status()} ${response.url()}`); });
  fs.mkdirSync('browser-evidence',{recursive:true});
  for (const lang of ['','fr/','ja/']) {
    const code=lang.replace('/','') || 'en';
    await page.goto(`http://127.0.0.1:8766/${lang}`,{waitUntil:'networkidle'});
    assert.equal(await page.locator('html').getAttribute('lang'),code);
    assert(await page.locator('a[href$=".iso"]').count()>0);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
    await page.screenshot({path:`browser-evidence/home-${code}.png`,fullPage:true});
    await page.goto(`http://127.0.0.1:8766/${lang}docs/start/`,{waitUntil:'networkidle'});
    assert.equal(await page.locator('figure.screenshot').count(),11);
    assert.equal(await page.locator('svg[aria-labelledby="arch-title arch-desc"]').count(),1);
    const pictures=page.locator('figure.screenshot img');
    for(let i=0;i<await pictures.count();i++) {
      await pictures.nth(i).scrollIntoViewIfNeeded();
      await pictures.nth(i).evaluate(img=>img.decode());
    }
    const diagram=page.locator('svg[aria-labelledby="arch-title arch-desc"]');
    await diagram.scrollIntoViewIfNeeded();
    await diagram.evaluate(el=>window.scrollBy(0,el.getBoundingClientRect().top-100));
    await diagram.screenshot({path:`browser-evidence/architecture-${code}.png`});
    const search=page.locator('.hextra-search-input:visible').first();
    const indexResponse=page.waitForResponse(response=>response.url().endsWith(`${code}.search-data.json`));
    await search.focus();
    await (await indexResponse).finished();
    // Hextra searches on keyup, so exercise the real keyboard interaction.
    await search.pressSequentially('XOA',{delay:100});
    await page.waitForFunction(()=>document.querySelectorAll('.hextra-search-results a').length>0);
    const hrefs=await page.locator('.hextra-search-results a').evaluateAll(a=>a.map(x=>new URL(x.href).pathname));
    assert(hrefs.every(p=>lang ? p.startsWith('/'+lang) : !/^\/(fr|ja)\//.test(p)), 'search crossed languages');
    await page.keyboard.press('Escape');
  }
  await page.goto('http://127.0.0.1:8766/',{waitUntil:'networkidle'});
  assert(await page.locator('html').evaluate(el=>el.classList.contains('dark')),'system dark theme');
  await page.locator('.hextra-theme-toggle:visible').first().click();
  await page.locator('button[data-item="light"]:visible').first().click();
  await page.locator('.hextra-font-size-inc').first().click();
  await page.reload({waitUntil:'networkidle'});
  assert.equal(await page.locator('html').evaluate(el=>el.classList.contains('dark')),false,'saved light theme');
  assert.equal(await page.locator('html').getAttribute('data-font-scale'),'l','saved font size');
  await page.locator('.hextra-font-size-reset').first().click();
  const mappings=JSON.parse(fs.readFileSync('site/assets/legacy-home.json','utf8'));
  for (const [lang,entries] of Object.entries(mappings)) {
    const prefix=lang==='en'?'':lang+'/';
    for(const entry of entries) {
      await page.goto(`http://127.0.0.1:8766/${prefix}#${encodeURIComponent(entry.old)}`,{waitUntil:'networkidle'});
      await page.waitForURL(`**/${prefix}docs/start/#${entry.target}`);
    }
  }
  await page.goto('http://127.0.0.1:8766/features.html#iso-storage',{waitUntil:'networkidle'});
  await page.waitForURL('**/docs/guides/features/#iso-storage');
  await page.setViewportSize({width:390,height:844});
  for(const lang of ['','fr/','ja/']) {
    await page.goto(`http://127.0.0.1:8766/${lang}`,{waitUntil:'networkidle'});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'mobile viewport overflow');
    await page.locator('.hextra-hamburger-menu').click();
    assert.equal(await page.locator('.hextra-hamburger-menu').getAttribute('aria-expanded'),'true');
    await page.locator('.hextra-hamburger-menu').click();
    await page.screenshot({path:`browser-evidence/mobile-${lang.replace('/','')||'en'}.png`,fullPage:true});
  }
  await context.close();
  const nojs=await browser.newContext({javaScriptEnabled:false});
  const fallback=await nojs.newPage();
  await fallback.goto('http://127.0.0.1:8766/#download');
  assert(await fallback.locator('#download a').isVisible(),'no-JS old bookmark fallback');
  await fallback.locator('#download a').click();
  assert(fallback.url().endsWith('/docs/start/#start-download'));
  assert.deepEqual(errors,[]);
  await browser.close();
  console.log('PASS: languages/search, images/SVG, theme/font persistence, 39 old homepage bookmarks, alias fragment, mobile menus and no-JS fallback');
})().catch(e=>{console.error(e);process.exit(1)});
