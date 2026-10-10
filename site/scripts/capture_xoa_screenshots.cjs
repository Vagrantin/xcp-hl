// Appliance captures for Jenkins; never called by public documentation CI.
// Setup and output contract: site/XOA-SCREENSHOTS.md. XO 5 hash routes only.
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

function required(name) {
  const value = process.env[name];
  if (!value || !value.trim()) throw new Error(`Missing ${name}`);
  return value;
}

async function capture() {
  const base = new URL(required('XOA_SCREENSHOT_BASE_URL'));
  assert.equal(base.protocol, 'https:', 'Use the lab appliance HTTPS URL');
  assert(!base.username && !base.password && !base.search && !base.hash, 'Base URL cannot contain credentials, query or hash');
  if (!base.pathname.endsWith('/')) base.pathname += '/';
  const login = required('XOA_SCREENSHOT_LOGIN');
  const password = required('XOA_SCREENSHOT_PASSWORD');
  const versions = {
    imageTag: required('XOA_SCREENSHOT_IMAGE_TAG'),
    appVersion: required('XOA_SCREENSHOT_APP_VERSION'),
    vmVersion: required('XOA_SCREENSHOT_VM_VERSION'),
    hostRelease: required('XOA_SCREENSHOT_HOST_RELEASE'),
    guestOs: required('XOA_SCREENSHOT_GUEST_OS'),
  };
  const uuid = name => {
    const value = required(name);
    assert(/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i.test(value), `${name} must be a fixture UUID`);
    return value;
  };
  const vm = uuid('XOA_SCREENSHOT_VM_UUID');
  const sr = uuid('XOA_SCREENSHOT_ISO_SR_UUID');
  const pool = uuid('XOA_SCREENSHOT_POOL_UUID');
  const template = uuid('XOA_SCREENSHOT_TEMPLATE_UUID');
  const expectedVm = required('XOA_SCREENSHOT_VM_NAME');
  const expectedIso = required('XOA_SCREENSHOT_ISO_NAME');
  const locales = (process.env.XOA_SCREENSHOT_LOCALES || 'en,fr,ja').split(',');
  assert(locales.length > 0 && locales.every(x=>['en','fr','ja'].includes(x)), 'Locales must be en,fr,ja');
  const extraMasks = JSON.parse(process.env.XOA_SCREENSHOT_MASK_SELECTORS || '[]');
  assert(Array.isArray(extraMasks) && extraMasks.every(x=>typeof x==='string'), 'Mask selectors must be a JSON string array');
  const output = path.resolve(process.env.XOA_SCREENSHOT_OUTPUT || 'xoa-captures');
  // Fail instead of mixing this run with old captures, even on reused agents.
  await fs.mkdir(output);
  const browser = await chromium.launch({headless:true});
  const context = await browser.newContext({
    viewport:{width:1440,height:1000}, deviceScaleFactor:1, colorScheme:'light',
    ignoreHTTPSErrors: process.env.XOA_SCREENSHOT_ALLOW_SELF_SIGNED === 'true',
  });
  const page = await context.newPage();
  page.setDefaultTimeout(30000);
  const records = [];
  let currentCapture = 'login';
  const routes = [
    {name:'01-user-language', route:'/user', ready:'form#changePassword'},
    {name:'02-connected-host', route:'/settings/servers', ready:'#form-add-server', masks:['table tbody td:nth-child(2)','table tbody td:nth-child(3)']},
    {name:'03-about-versions', route:'/about', ready:'.page-header'},
    {name:'04-iso-library', route:`/srs/${sr}/disks`, ready:'.page-header', text:expectedIso},
    {name:'05-new-vm-wizard', route:`/vms/new?pool=${pool}&template=${template}`, ready:'form#vmCreation'},
    {name:'06-vm-console', route:`/vms/${vm}/console`, ready:'canvas', text:expectedVm},
    {name:'07-vm-disks', route:`/vms/${vm}/disks`, ready:'.page-header', text:expectedVm},
  ];
  try {
    await page.goto(base.href, {waitUntil:'domcontentloaded'});
    const form = page.locator('form[action^="signin/local"]');
    await form.locator('input[name="username"]').fill(login);
    await form.locator('input[name="password"]').fill(password);
    await form.locator('button').click();
    await page.locator('#xo-app').waitFor();
    // No storageState, tracing, HAR, video or debug HTML is written.
    for (const locale of locales) {
      // The pinned XO5 reducer stores language in this browser cookie.
      await context.addCookies([{name:'lang',value:locale,url:base.href}]);
      for (const item of routes) {
        currentCapture = `${locale}/${item.name}`;
        const url = new URL(base.href);
        url.hash = item.route;
        await page.goto(url.href, {waitUntil:'domcontentloaded'});
        // Force the cookie to be read again even when only the hash changed.
        await page.reload({waitUntil:'domcontentloaded'});
        await page.locator('#xo-app').waitFor();
        await page.locator(item.ready).first().waitFor({state:'visible'});
        if (item.text) await page.getByText(item.text,{exact:true}).first().waitFor({state:'visible'});
        if (item.name === '01-user-language') {
          assert.equal(await page.locator('select.form-control').first().inputValue(),locale,'UI language differs');
        }
        if (item.name === '03-about-versions') {
          await page.getByText(versions.appVersion,{exact:false}).first().waitFor({state:'visible'});
          await page.getByText(versions.vmVersion,{exact:false}).first().waitFor({state:'visible'});
        }
        await page.evaluate(()=>document.fonts.ready);
        if (item.ready === 'canvas') {
          // Canvas existence cannot prove the guest display is ready. Operator review required.
          await page.waitForTimeout(2000);
        }
        const destination = path.join(output,locale);
        await fs.mkdir(destination,{recursive:true});
        const filename = `${locale}/${item.name}.png`;
        const masks = ['input[type="password"]','input[name="username"]',...(item.masks||[]),...extraMasks];
        await page.screenshot({path:path.join(output,filename),fullPage:true,animations:'disabled',
          mask:[page.getByText(login,{exact:true}),...masks.map(s=>page.locator(s))]});
        const bytes = await fs.readFile(path.join(output,filename));
        records.push({file:filename,uiLanguage:locale,view:item.name,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),
          capturedAt:new Date().toISOString(),reviewStatus:'pending'});
        console.log(`Captured ${currentCapture}`);
      }
    }
    await fs.writeFile(path.join(output,'manifest.json'),JSON.stringify({schemaVersion:1,versions,
      browser:browser.version(),viewport:{width:1440,height:1000},documentationCommit:process.env.GIT_COMMIT || 'unrecorded',
      behavior:'capture only; fixture correctness and lab journey unverified',captures:records},null,2)+'\n');
    await fs.writeFile(path.join(output,'SHA256SUMS'),records.map(r=>`${r.sha256}  ${r.file}`).join('\n')+'\n');
  } catch (_) {
    // Playwright errors can include URLs, selectors or input values. Keep console output generic.
    throw new Error(`Capture failed at ${currentCapture}; no complete manifest was produced. Inspect the lab privately.`);
  } finally {
    await context.close();
    await browser.close();
  }
}

capture().catch(error=>{console.error(error.message);process.exitCode=1;});
