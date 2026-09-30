#!/usr/bin/env node
/**
 * diag — print the numbers behind the portrait placement, so a layout argument
 * can be settled with measurements instead of screenshots.
 *
 * Usage:
 *   node tools/facade/diag.cjs <facade-dir> [skin-id]
 *
 * Reports:
 *   - whether the engine supports anchor positioning at all;
 *   - how many elements match each anchor-name carrier, and the rect of the
 *     input card (the anchor owner);
 *   - the computed inset / size / background-image of body::before and
 *     body::after, i.e. where each portrait actually lands.
 */
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');

const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');

const [facadeDir, skinId = 'lucy-nightsignal'] = process.argv.slice(2);
if (!facadeDir) {
  console.error('usage: diag.cjs <facade-dir> [skin-id]');
  process.exit(1);
}

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp' };

function serve(root) {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const url = decodeURIComponent((req.url || '/').split('?')[0]);
      const file = path.normalize(path.join(root, url === '/' ? 'preview.html' : url));
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
  const { server, base } = await serve(facadeDir);
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  await page.goto(`${base}/preview.html?skin=${skinId}&theme=light&chrome=0`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  const report = await page.evaluate(() => {
    const rect = (el) => (el ? el.getBoundingClientRect().toJSON() : null);
    const count = (sel) => document.querySelectorAll(sel).length;
    const before = getComputedStyle(document.body, '::before');
    const after = getComputedStyle(document.body, '::after');
    return {
      supportsAnchor: CSS.supports('left: anchor(--x right, 0px)'),
      counts: {
        card: count('[data-composer-card]'),
        seat: count('[data-composer-seat]'),
        surface: count('[data-dsh-surface="composer"]'),
      },
      card: rect(document.querySelector('[data-composer-card]')),
      before: { left: before.left, right: before.right, width: before.width, height: before.height, z: before.zIndex, bg: before.backgroundImage.slice(0, 50) },
      after: { left: after.left, right: after.right, width: after.width, height: after.height, z: after.zIndex, bg: after.backgroundImage.slice(0, 50) },
    };
  });
  console.log(JSON.stringify(report, null, 2));
  await browser.close();
  server.close();
})().catch((err) => {
  console.error('diag failed:', err);
  process.exit(1);
});
