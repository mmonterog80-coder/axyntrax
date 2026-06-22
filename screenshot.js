const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto('http://localhost:3000', { waitUntil: 'networkidle0', timeout: 60000 });
  await page.screenshot({ path: 'C:\\Users\\YARVIS\\.gemini\\antigravity\\brain\\1f93d070-3901-4fb5-843f-88e907a0656e\\hud_validation_final.png' });
  await browser.close();
})();
