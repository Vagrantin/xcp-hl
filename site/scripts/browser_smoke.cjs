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
    assert(await page.locator(`a[href="/${lang}docs/xoa-hl/"]`).count()>0, 'manual entry missing');
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
    // Exercise normal typing; task cases below also cover non-Latin text input.
    await search.pressSequentially('XOA',{delay:100});
    await page.waitForFunction(()=>document.querySelectorAll('.hextra-search-results a').length>0);
    const hrefs=await page.locator('.hextra-search-results a').evaluateAll(a=>a.map(x=>new URL(x.href).pathname));
    assert(hrefs.every(p=>lang ? p.startsWith('/'+lang) : !/^\/(fr|ja)\//.test(p)), 'search crossed languages');
    await page.keyboard.press('Escape');
    // Task queries must rank their guide first, not merely return a result.
    const queries = {
      en: [['virtual machine', 'xoa-hl/create-vm/'], ['back up', 'xoa-hl/backup-restore/'], ['schedules', 'xoa-hl/backup-restore/'], ['retention', 'xoa-hl/backup-restore/'], ['maintain', 'xoa-hl/maintenance/'], ['export', 'xoa-hl/configuration-backup/'], ['troubleshoot', 'xoa-hl/troubleshooting/'], ['backup failures', 'xoa-hl/troubleshooting/'], ['snapshots', 'xoa-hl/vm-operations/'], ['console', 'xoa-hl/vm-operations/'], ['memory', 'xoa-hl/vm-operations/'], ['deletion', 'xoa-hl/vm-operations/'], ['full copy', 'xoa-hl/vm-operations/'], ['storage', 'xoa-hl/storage-networks/'], ['ISO libraries', 'xoa-hl/storage-networks/'], ['NFS storage', 'xoa-hl/storage-networks/'], ['migrate', 'xoa-hl/vm-transfer/'], ['pool ownership', 'xoa-hl/hosts-pools/'], ['host statistics', 'xoa-hl/hosts-pools/'], ['permissions', 'xoa-hl/permissions/'], ['groups', 'xoa-hl/permissions/'], ['one-time code', 'xoa-hl/sign-in-otp/'], ['templates', 'xoa-hl/templates/'], ['guest tools', 'xoa-hl/guest-tools/'], ['concepts', 'xoa-hl/concepts/'], ['configure', 'xoa-hl/configuration/'], ['automate', 'xoa-hl/automation/']],
      fr: [['machine virtuelle', 'xoa-hl/create-vm/'], ['sauvegarde', 'xoa-hl/backup-restore/'], ['planification', 'xoa-hl/backup-restore/'], ['rétention', 'xoa-hl/backup-restore/'], ['mise à jour', 'guides/updates/'], ['maintenir', 'xoa-hl/maintenance/'], ['exporter', 'xoa-hl/configuration-backup/'], ['dépanner', 'xoa-hl/troubleshooting/'], ['échecs de sauvegarde', 'xoa-hl/troubleshooting/'], ['snapshots', 'xoa-hl/vm-operations/'], ['console', 'xoa-hl/vm-operations/'], ['mémoire', 'xoa-hl/vm-operations/'], ['suppression', 'xoa-hl/vm-operations/'], ['copie complète', 'xoa-hl/vm-operations/'], ['disques', 'xoa-hl/storage-networks/'], ['bibliothèques ISO', 'xoa-hl/storage-networks/'], ['stockage NFS', 'xoa-hl/storage-networks/'], ['migrer', 'xoa-hl/vm-transfer/'], ['pools', 'xoa-hl/hosts-pools/'], ['statistiques des hôtes', 'xoa-hl/hosts-pools/'], ['droits', 'xoa-hl/permissions/'], ['groupes', 'xoa-hl/permissions/'], ['code à usage unique', 'xoa-hl/sign-in-otp/'], ['modèle de VM', 'xoa-hl/templates/'], ['outils invités', 'xoa-hl/guest-tools/'], ['concepts', 'xoa-hl/concepts/'], ['configurer', 'xoa-hl/configuration/'], ['automatiser', 'xoa-hl/automation/']],
      ja: [['仮想マシン', 'xoa-hl/create-vm/'], ['バックアップ', 'xoa-hl/backup-restore/'], ['スケジュール', 'xoa-hl/backup-restore/'], ['保持数', 'xoa-hl/backup-restore/'], ['アップデート', 'guides/updates/'], ['保守', 'xoa-hl/maintenance/'], ['エクスポート', 'xoa-hl/configuration-backup/'], ['トラブルシューティング', 'xoa-hl/troubleshooting/'], ['バックアップ障害', 'xoa-hl/troubleshooting/'], ['スナップショット', 'xoa-hl/vm-operations/'], ['コンソール', 'xoa-hl/vm-operations/'], ['メモリ', 'xoa-hl/vm-operations/'], ['削除', 'xoa-hl/vm-operations/'], ['フルコピー', 'xoa-hl/vm-operations/'], ['ストレージ', 'xoa-hl/storage-networks/'], ['ISOライブラリ', 'xoa-hl/storage-networks/'], ['NFSストレージ', 'xoa-hl/storage-networks/'], ['マイグレーション', 'xoa-hl/vm-transfer/'], ['プール', 'xoa-hl/hosts-pools/'], ['ホスト統計', 'xoa-hl/hosts-pools/'], ['権限', 'xoa-hl/permissions/'], ['グループ', 'xoa-hl/permissions/'], ['ワンタイムコード', 'xoa-hl/sign-in-otp/'], ['テンプレート', 'xoa-hl/templates/'], ['ゲストツール', 'xoa-hl/guest-tools/'], ['概念', 'xoa-hl/concepts/'], ['サービスの設定', 'xoa-hl/configuration/'], ['自動化', 'xoa-hl/automation/']],
    };
    for (const [query, route] of queries[code]) {
      await search.fill('');
      await search.pressSequentially(query,{delay:100});
      await page.waitForFunction(({query,expected})=> {
        const input=document.querySelector('.hextra-search-input');
        const first=document.querySelector('.hextra-search-results a');
        return input.value===query && first && new URL(first.href).pathname===expected;
      },{query,expected:`/${lang}docs/${route}`},{timeout:10000});
      const results=await page.locator('.hextra-search-results a').evaluateAll(a=>a.map(x=>new URL(x.href).pathname));
      assert(results.every(p=>lang ? p.startsWith('/'+lang) : !/^\/(fr|ja)\//.test(p)), 'task search crossed languages');
      console.log(`PASS: ${code} task search ${query} → ${results[0]}`);
      await page.keyboard.press('Escape');
    }
    for (const route of ['first-login','create-vm','backup-restore','maintenance','configuration-backup','troubleshooting','vm-operations','storage-networks','vm-transfer','hosts-pools','permissions','sign-in-otp','templates','guest-tools','concepts','configuration','automation']) {
      await page.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/${route}/`,{waitUntil:'networkidle'});
      assert.equal(await page.locator('main h1').count(),1,'tutorial heading missing');
      if (route === 'vm-operations') {
        const oldAnchors = {
          en: ['3-take-and-check-a-stopped-snapshot','4-revert-only-the-test-vm'],
          fr: ['3-créer-et-vérifier-un-snapshot-à-froid','4-restaurer-uniquement-la-vm-de-test'],
          ja: ['3-停止中のスナップショットを作成する','4-テスト-vm-をスナップショットに戻す'],
        };
        for (const id of oldAnchors[code]) {
          assert(await page.evaluate(id=>!!document.getElementById(id)?.closest('h2'),id),'old snapshot heading anchor missing');
        }
      }

      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'tutorial overflow');
      await page.screenshot({path:`browser-evidence/${route}-${code}.png`,fullPage:true});
    }
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
  await page.waitForURL('**/docs/features/#iso-storage');
  await page.setViewportSize({width:390,height:844});
  for(const lang of ['','fr/','ja/']) {
    await page.goto(`http://127.0.0.1:8766/${lang}`,{waitUntil:'networkidle'});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'mobile viewport overflow');
    await page.locator('.hextra-hamburger-menu').click();
    assert.equal(await page.locator('.hextra-hamburger-menu').getAttribute('aria-expanded'),'true');
    await page.locator('.hextra-hamburger-menu').click();
    await page.screenshot({path:`browser-evidence/mobile-${lang.replace('/','')||'en'}.png`,fullPage:true});
    for (const route of ['create-vm','backup-restore','maintenance','configuration-backup','troubleshooting','vm-operations','storage-networks','vm-transfer','hosts-pools','permissions','sign-in-otp','templates','guest-tools','concepts','configuration','automation']) {
      await page.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/${route}/`,{waitUntil:'networkidle'});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'mobile tutorial overflow');
      await page.screenshot({path:`browser-evidence/mobile-${route}-${lang.replace('/','')||'en'}.png`,fullPage:true});
    }
  }
  // A long wrapped section heading must stay below the fixed navbar after
  // following a fragment link from the beginner guide.
  for (const lang of ['', 'fr/', 'ja/']) {
    for (const width of [390, 320]) {
      await page.setViewportSize({width,height:844});
      await page.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/create-vm/`,{waitUntil:'networkidle'});
      await page.locator(`main a[href="/${lang}docs/xoa-hl/storage-networks/#nfs-iso-library"]`).first().click();
      await page.waitForURL(`**/${lang}docs/xoa-hl/storage-networks/#nfs-iso-library`);
      await page.waitForFunction(() => {
        const anchor=document.getElementById('nfs-iso-library');
        const heading=anchor?.closest('h2');
        const nav=document.querySelector('nav.hextra-max-navbar-width');
        return heading && heading.getBoundingClientRect().top >= nav.getBoundingClientRect().bottom - 1;
      });
      console.log(`PASS: ${lang || 'en'} ISO fragment heading visible at ${width}px`);

      await page.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/`,{waitUntil:'networkidle'});
      await page.locator(`main a[href="/${lang}docs/xoa-hl/backup-restore/#backup-schedules"]`).first().click();
      await page.waitForURL(`**/${lang}docs/xoa-hl/backup-restore/#backup-schedules`);
      await page.waitForFunction(() => {
        const heading=document.getElementById('backup-schedules')?.closest('h2');
        const nav=document.querySelector('nav.hextra-max-navbar-width');
        return heading && heading.getBoundingClientRect().top >= nav.getBoundingClientRect().bottom - 1;
      });
      console.log(`PASS: ${lang || 'en'} backup schedule fragment visible at ${width}px`);

      await page.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/`,{waitUntil:'networkidle'});
      await page.locator(`main a[href="/${lang}docs/xoa-hl/troubleshooting/#backup-failures"]`).first().click();
      await page.waitForURL(`**/${lang}docs/xoa-hl/troubleshooting/#backup-failures`);
      await page.waitForFunction(() => {
        const heading=document.getElementById('backup-failures')?.closest('h2');
        const nav=document.querySelector('nav.hextra-max-navbar-width');
        return heading && heading.getBoundingClientRect().top >= nav.getBoundingClientRect().bottom - 1;
      });
      console.log(`PASS: ${lang || 'en'} backup failure fragment visible at ${width}px`);
      // Both new diagnostic tables must fit: a long slash-separated label
      // previously pushed the French stage table outside the mobile reading area.
      const diagnosisTables = await page.evaluate(() => {
        return [...document.querySelectorAll('main table.xoa-backup-diagnosis')]
          .map(table => table.scrollWidth <= table.clientWidth + 1);
      });
      assert.equal(diagnosisTables.length, 2, 'diagnosis tables missing');
      assert(diagnosisTables.every(Boolean), 'diagnosis table requires horizontal scrolling');
      console.log(`PASS: ${lang || 'en'} backup diagnosis tables fit at ${width}px`);

      await page.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/`,{waitUntil:'networkidle'});
      await page.locator(`main a[href="/${lang}docs/xoa-hl/vm-operations/#stopped-snapshot"]`).first().click();
      for (const anchor of ['stopped-snapshot','snapshot-revert','snapshot-cleanup']) {
        if (anchor !== 'stopped-snapshot') {
          await page.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/vm-operations/#${anchor}`,{waitUntil:'networkidle'});
        }
        await page.waitForFunction(anchor => {
          const heading=document.getElementById(anchor)?.closest('h2,h3');
          const nav=document.querySelector('nav.hextra-max-navbar-width');
          return heading && heading.getBoundingClientRect().top >= nav.getBoundingClientRect().bottom - 1;
        },anchor);
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'snapshot pilot overflow');
        await page.screenshot({path:`browser-evidence/${anchor}-${lang.replace('/','')||'en'}-${width}.png`});
        const legacyAligned = await page.evaluate(anchor => {
          const heading=document.getElementById(anchor).closest('h2,h3');
          return [...heading.querySelectorAll('span[id]')].every(span =>
            Math.abs(span.getBoundingClientRect().top-heading.getBoundingClientRect().top)<1);
        },anchor);
        assert(legacyAligned,'snapshot legacy anchor must remain at heading top');
      }
      console.log(`PASS: ${lang || 'en'} snapshot create/revert/cleanup fragments at ${width}px`);
      await page.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/`,{waitUntil:'networkidle'});
      await page.locator(`main a[href="/${lang}docs/xoa-hl/vm-operations/#vm-console"]`).first().click();
      await page.waitForURL(`**/${lang}docs/xoa-hl/vm-operations/#vm-console`);
      await page.waitForFunction(() => {
        const heading=document.getElementById('vm-console')?.closest('h2');
        const nav=document.querySelector('nav.hextra-max-navbar-width');
        return heading && heading.getBoundingClientRect().top >= nav.getBoundingClientRect().bottom - 1;
      });
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'console fragment overflow');
      await page.screenshot({path:`browser-evidence/console-${lang.replace('/','')||'en'}-${width}.png`});
      console.log(`PASS: ${lang || 'en'} console fragment at ${width}px`);

      await page.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/create-vm/`,{waitUntil:'networkidle'});
      await page.locator(`main a[href="/${lang}docs/xoa-hl/templates/#deploy-template"]`).first().click();
      await page.waitForURL(`**/${lang}docs/xoa-hl/templates/#deploy-template`);
      await page.waitForFunction(() => {
        const heading=document.getElementById('deploy-template')?.closest('h2');
        return heading && heading.getBoundingClientRect().top >= document.querySelector('nav.hextra-max-navbar-width').getBoundingClientRect().bottom - 1;
      });
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'template fragment overflow');
      await page.screenshot({path:`browser-evidence/template-deploy-${lang.replace('/','')||'en'}-${width}.png`});
      console.log(`PASS: ${lang || 'en'} template deployment fragment at ${width}px`);

      for (const entry of ['', 'create-vm/']) {
        await page.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/${entry}`,{waitUntil:'networkidle'});
        await page.locator(`main a[href="/${lang}docs/xoa-hl/storage-networks/#nfs-vm-storage"]`).first().click();
        await page.waitForURL(`**/${lang}docs/xoa-hl/storage-networks/#nfs-vm-storage`);
        await page.waitForFunction(() => {
          const heading=document.getElementById('nfs-vm-storage')?.closest('h2');
          return heading && heading.getBoundingClientRect().top >= document.querySelector('nav.hextra-max-navbar-width').getBoundingClientRect().bottom - 1;
        });
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'NFS storage fragment overflow');
        await page.screenshot({path:`browser-evidence/nfs-storage-${entry ? 'beginner' : 'manual'}-${lang.replace('/','')||'en'}-${width}.png`});
        console.log(`PASS: ${lang || 'en'} NFS storage fragment from ${entry || 'manual'} at ${width}px`);
      }

      for (const [entry,anchor] of [['create-vm','install-linux-agent'],['vm-operations','guest-tools-status']]) {
        await page.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/${entry}/`,{waitUntil:'networkidle'});
        await page.locator(`main a[href="/${lang}docs/xoa-hl/guest-tools/#${anchor}"]`).first().click();
        await page.waitForURL(`**/${lang}docs/xoa-hl/guest-tools/#${anchor}`);
        await page.waitForFunction(anchor => {
          const heading=document.getElementById(anchor)?.closest('h2');
          return heading && heading.getBoundingClientRect().top >= document.querySelector('nav.hextra-max-navbar-width').getBoundingClientRect().bottom - 1;
        },anchor);
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'guest tools fragment overflow');
        await page.screenshot({path:`browser-evidence/guest-tools-${anchor}-${lang.replace('/','')||'en'}-${width}.png`});
        console.log(`PASS: ${lang || 'en'} guest tools ${anchor} fragment at ${width}px`);
      }



    }
  }
  await context.close();
  const nojs=await browser.newContext({javaScriptEnabled:false});
  const fallback=await nojs.newPage();
  await fallback.goto('http://127.0.0.1:8766/#download');
  assert(await fallback.locator('#download a').isVisible(),'no-JS old bookmark fallback');
  await fallback.locator('#download a').click();
  assert(fallback.url().endsWith('/docs/start/#start-download'));
  for (const lang of ['','fr/','ja/']) {
    await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/`);
    for (const route of ['vm-operations','storage-networks','vm-transfer','hosts-pools','permissions','sign-in-otp','templates','guest-tools','concepts','configuration','automation']) {
      await fallback.locator(`main a[href="/${lang}docs/xoa-hl/${route}/"]`).first().click();
      assert(await fallback.locator('main h1').isVisible(),'no-JS daily guide');
      await fallback.goBack();
    }
    for (const width of [390, 320]) {
      await fallback.setViewportSize({width,height:844});
      await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/create-vm/`);
      await fallback.locator(`main a[href="/${lang}docs/xoa-hl/storage-networks/#nfs-iso-library"]`).first().click();
      assert(await fallback.evaluate(() => {
        const heading=document.getElementById('nfs-iso-library').closest('h2');
        return heading.getBoundingClientRect().top >= document.querySelector('nav.hextra-max-navbar-width').getBoundingClientRect().bottom - 1;
      }),'no-JS fragment heading hidden under navbar');

      await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/`);
      await fallback.locator(`main a[href="/${lang}docs/xoa-hl/backup-restore/#backup-schedules"]`).first().click();
      assert(await fallback.evaluate(() => {
        const heading=document.getElementById('backup-schedules').closest('h2');
        return heading.getBoundingClientRect().top >= document.querySelector('nav.hextra-max-navbar-width').getBoundingClientRect().bottom - 1;
      }),'no-JS backup schedule fragment hidden under navbar');

      await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/`);
      await fallback.locator(`main a[href="/${lang}docs/xoa-hl/troubleshooting/#backup-failures"]`).first().click();
      assert(await fallback.evaluate(() => {
        const heading=document.getElementById('backup-failures').closest('h2');
        return heading.getBoundingClientRect().top >= document.querySelector('nav.hextra-max-navbar-width').getBoundingClientRect().bottom - 1;
      }),'no-JS backup failure fragment hidden under navbar');

      await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/`);
      await fallback.locator(`main a[href="/${lang}docs/xoa-hl/vm-operations/#stopped-snapshot"]`).first().click();
      for (const anchor of ['stopped-snapshot','snapshot-revert','snapshot-cleanup']) {
        if (anchor !== 'stopped-snapshot') {
          await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/vm-operations/#${anchor}`);
        }
        assert(await fallback.evaluate(anchor => {
          const heading=document.getElementById(anchor)?.closest('h2,h3');
          return heading.getBoundingClientRect().top >= document.querySelector('nav.hextra-max-navbar-width').getBoundingClientRect().bottom - 1;
        },anchor),'no-JS snapshot fragment hidden under navbar');
      }
      await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/`);
      await fallback.locator(`main a[href="/${lang}docs/xoa-hl/vm-operations/#vm-console"]`).first().click();
      assert(await fallback.evaluate(() => {
        const heading=document.getElementById('vm-console').closest('h2');
        return heading.getBoundingClientRect().top >= document.querySelector('nav.hextra-max-navbar-width').getBoundingClientRect().bottom - 1;
      }),'no-JS console fragment hidden under navbar');

      await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/create-vm/`);
      await fallback.locator(`main a[href="/${lang}docs/xoa-hl/templates/#deploy-template"]`).first().click();
      assert(await fallback.evaluate(() => {
        const heading=document.getElementById('deploy-template').closest('h2');
        return heading.getBoundingClientRect().top >= document.querySelector('nav.hextra-max-navbar-width').getBoundingClientRect().bottom - 1;
      }),'no-JS template fragment hidden under navbar');

      for (const entry of ['', 'create-vm/']) {
        await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/${entry}`);
        await fallback.locator(`main a[href="/${lang}docs/xoa-hl/storage-networks/#nfs-vm-storage"]`).first().click();
        assert(await fallback.evaluate(() => {
          const heading=document.getElementById('nfs-vm-storage')?.closest('h2');
          return heading && heading.getBoundingClientRect().top >= document.querySelector('nav.hextra-max-navbar-width').getBoundingClientRect().bottom - 1;
        }),'no-JS NFS storage fragment hidden under navbar');
        console.log(`PASS: ${lang || 'en'} no-JS NFS storage fragment from ${entry || 'manual'} at ${width}px`);
      }

      for (const [entry,anchor] of [['create-vm','install-linux-agent'],['vm-operations','guest-tools-status']]) {
        await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/${entry}/`);
        await fallback.locator(`main a[href="/${lang}docs/xoa-hl/guest-tools/#${anchor}"]`).first().click();
        assert(await fallback.evaluate(anchor => {
          const heading=document.getElementById(anchor)?.closest('h2');
          return heading && heading.getBoundingClientRect().top >= document.querySelector('nav.hextra-max-navbar-width').getBoundingClientRect().bottom - 1;
        },anchor),'no-JS guest tools fragment hidden under navbar');
      }



    }
    await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/maintenance/`);
    await fallback.locator(`main a[href="/${lang}docs/xoa-hl/configuration-backup/"]`).first().click();
    assert(await fallback.locator('main h1').isVisible(),'no-JS configuration guide');
    await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/first-login/`);
    assert(await fallback.locator(`main a[href="/${lang}docs/xoa-hl/create-vm/"]`).first().isVisible(),'no-JS next tutorial link');
    await fallback.goto(`http://127.0.0.1:8766/${lang}docs/xoa-hl/create-vm/`);
    await fallback.locator(`main a[href="/${lang}docs/xoa-hl/backup-restore/"]`).first().click();
    assert(await fallback.locator('main h1').isVisible(),'no-JS backup tutorial');
  }
  assert.deepEqual(errors,[]);
  await browser.close();
  console.log('PASS: languages/ranked task search, tutorials, images/SVG, theme/font persistence, 39 old homepage bookmarks, alias fragment, mobile menus and no-JS fallback');
})().catch(e=>{console.error(e);process.exit(1)});
