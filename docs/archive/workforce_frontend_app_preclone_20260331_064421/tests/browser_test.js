const { chromium } = require('playwright');
const fs = require('fs');
(async ()=> {
  const outDir = 'docs/ADMIN/frontend/artifact-diffs';
  const screenshotsDir = `${outDir}/screenshots`;
  fs.mkdirSync(screenshotsDir, { recursive: true });
  const consoleErrors = [];
  const pageErrors = [];
  const failedRequests = [];
  const routeResults = [];
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  page.on('console', msg => {
    if (msg.type && msg.type() === 'error') {
      consoleErrors.push(`${new Date().toISOString()} console.${msg.type()}: ${msg.text()}`);
    }
  });
  page.on('pageerror', err => {
    pageErrors.push(`${new Date().toISOString()} pageerror: ${err.message}`);
  });
  page.on('requestfailed', req => {
    const f = req.failure && req.failure().errorText ? req.failure().errorText : 'unknown';
    failedRequests.push(`${new Date().toISOString()} ${req.method()} ${req.url()} ${f}`);
  });
  const routes = ['/', '/login', '/rooms', '/dashboard'];
  for (const route of routes) {
    const url = `http://127.0.0.1:8001${route}`;
    try {
      const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      const status = resp ? resp.status() : null;
      const content = await page.content();
      const heuristics = {
        hasLoginText: /login|sign in|sign-in/i.test(content),
        hasAppRoot: /id="app"|id="root"|<main|<div class="app"/i.test(content),
      };
      routeResults.push({ route, url, status, heuristics });
      const name = route === '/' ? 'root' : route.replace(/\//g,'').replace(/[^a-z0-9_-]/gi,'') || 'route';
      await page.screenshot({ path: `${screenshotsDir}/${name}.png`, fullPage: true });
    } catch (e) {
      routeResults.push({ route, url, error: e.message });
    }
  }
  // Save outputs
  const ceOut = consoleErrors.concat(pageErrors).join('\n');
  fs.writeFileSync(`${outDir}/browser-console-errors.txt`, ceOut);
  fs.writeFileSync(`${outDir}/failed-network-requests.txt`, failedRequests.join('\n'));
  fs.writeFileSync(`${outDir}/route-validation-summary.md`, routeResults.map(r=>JSON.stringify(r)).join('\n'));
  console.log('Test finished. ConsoleErrors:', consoleErrors.length + pageErrors.length, 'FailedRequests:', failedRequests.length);
  await browser.close();
  process.exit(0);
})().catch(err => { console.error(err); process.exit(2); });
