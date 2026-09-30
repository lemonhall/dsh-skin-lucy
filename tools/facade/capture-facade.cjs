#!/usr/bin/env node
/**
 * capture-facade — shoot a skin's two market previews through the official
 * facade renderer.
 *
 * The facade is `market/dist` from the dsh-web checkout: `preview.html` plus
 * `official-facade.js` (a desensitised DOM snapshot of the real GUI) and
 * `manifest.js` / `styles.js` carrying the skin data. `scripts/capture-previews`
 * in that repository renders the same page; this is a dependency-light stand-in
 * that reuses the locally installed Chrome instead of downloading Chromium.
 *
 * Usage:
 *   node tools/facade/capture-facade.cjs <facade-dir> <out-dir> [skin-id]
 *
 * Playwright is resolved from PLAYWRIGHT_PATH when set, otherwise from the
 * module path, i.e. a global install works with
 *   PLAYWRIGHT_PATH=<prefix>/node_modules/playwright
 *
 * Output: 1440x900 JPEG q85 at <out-dir>/{light,dark}.jpg, device scale 1 —
 * byte-for-byte the format the market writes.
 */
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');

const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');

const [facadeDir, outDir, skinId = 'lucy-nightsignal'] = process.argv.slice(2);
if (!facadeDir || !outDir) {
  console.error('usage: capture-facade.cjs <facade-dir> <out-dir> [skin-id]');
  process.exit(1);
}

const TYPES = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
};

function serve(root) {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const url = decodeURIComponent((req.url || '/').split('?')[0]);
      const file = path.normalize(path.join(root, url === '/' ? 'preview.html' : url));
      if (!file.startsWith(path.normalize(root))) {
        res.writeHead(403);
        return res.end('forbidden');
      }
      fs.readFile(file, (err, buf) => {
        if (err) {
          res.writeHead(404);
          return res.end('not found');
        }
        res.writeHead(200, { 'content-type': TYPES[path.extname(file)] || 'application/octet-stream' });
        res.end(buf);
      });
    });
    server.listen(0, '127.0.0.1', () => resolve({ server, base: `http://127.0.0.1:${server.address().port}` }));
  });
}

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const { server, base } = await serve(facadeDir);
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });

  for (const theme of ['light', 'dark']) {
    await page.goto(`${base}/preview.html?skin=${skinId}&theme=${theme}&chrome=0`, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForFunction(() => document.documentElement.dataset.dshSkin !== undefined, undefined, { timeout: 20000 });
    await page.waitForFunction(() => {
      const img = document.querySelector('#skin-backdrop img');
      return !img || (img.complete && img.naturalWidth > 0);
    }, undefined, { timeout: 20000 });
    await page.waitForTimeout(500);
    const out = path.join(outDir, `${theme}.jpg`);
    await page.screenshot({ path: out, type: 'jpeg', quality: 85 });
    console.log(`wrote ${out}`);
  }

  await browser.close();
  server.close();
})().catch((err) => {
  console.error('capture failed:', err);
  process.exit(1);
});
