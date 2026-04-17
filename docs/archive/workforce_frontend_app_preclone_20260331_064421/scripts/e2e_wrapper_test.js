const fs = require('fs');
const puppeteer = require('puppeteer-core');

(async () => {
  const outDir = 'docs/ADMIN/frontend/artifact-diffs';
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const consoleErrors = [];
  const networkFailures = [];

  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/chromium',
    args: ['--no-sandbox','--disable-setuid-sandbox'],
    headless: true,
  });

  const page = await browser.newPage();

  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
    }
  });

  page.on('requestfinished', async req => {
    try {
      const res = req.response();
      if (res) {
        const status = res.status();
        if (status >= 400) {
          networkFailures.push(`${status} ${req.url()}`);
        }
      }
    } catch (e) {
      // ignore
    }
  });

  page.on('requestfailed', req => {
    networkFailures.push(`FAILED ${req.url()} ${req.failure() && req.failure().errorText}`);
  });

  const results = {};

  try {
    const base = 'http://127.0.0.1:8086';

    // Root
    let r = await page.goto(base + '/', { waitUntil: 'networkidle2', timeout: 30000 });
    results.rootStatus = r.status();
    await page.screenshot({ path: `${outDir}/screenshot-root.png`, fullPage: true });

    // Login
    r = await page.goto(base + '/login', { waitUntil: 'networkidle2', timeout: 30000 });
    results.loginStatus = r.status();
    await page.screenshot({ path: `${outDir}/screenshot-login.png`, fullPage: true });

    // Missing SPA route
    r = await page.goto(base + '/some/nonexistent/spa/route', { waitUntil: 'networkidle2', timeout: 30000 });
    results.missingStatus = r.status();

    // Assets referenced from index
    const assets = await page.$$eval('link[rel="stylesheet"], script[src]', nodes => nodes.map(n => n.getAttribute('href') || n.getAttribute('src')));
    fs.writeFileSync(`${outDir}/e2e-assets-from-index.txt`, assets.join('\n'));

    // Asset checks
    const assetChecks = [];
    for (const a of assets) {
      try {
        const full = a.startsWith('http') ? a : (base + a);
        const resp = await page.goto(full, { waitUntil: 'networkidle2', timeout: 20000 });
        assetChecks.push(`${resp.status()} ${full}`);
      } catch (e) {
        assetChecks.push(`ERR ${a} ${e.message}`);
      }
    }
    fs.writeFileSync(`${outDir}/e2e-asset-http-checks.txt`, assetChecks.join('\n'));

  } catch (err) {
    fs.appendFileSync(`${outDir}/e2e-wrapper.log`, String(err) + '\n');
    console.error('E2E error', err);
  } finally {
    await browser.close();
    fs.writeFileSync(`${outDir}/e2e-console-errors.txt`, consoleErrors.join('\n'));
    fs.writeFileSync(`${outDir}/e2e-network-failures.txt`, networkFailures.join('\n'));
    const summary = `rootStatus: ${results.rootStatus || 'ERROR'}\nloginStatus: ${results.loginStatus || 'ERROR'}\nmissingStatus: ${results.missingStatus || 'ERROR'}\nconsoleErrors: ${consoleErrors.length}\nnetworkFailures: ${networkFailures.length}\n`;
    fs.writeFileSync(`${outDir}/e2e-summary.md`, summary);
    process.exit(0);
  }
})();
