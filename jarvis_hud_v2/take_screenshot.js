const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1920, height: 1080 }
  });
  
  try {
    await page.goto('http://localhost:3002', { timeout: 10000, waitUntil: 'networkidle' });
    await page.waitForTimeout(2000); // Wait for animations to settle
    await page.screenshot({ path: 'C:\\Users\\YARVIS\\.gemini\\antigravity\\brain\\1f93d070-3901-4fb5-843f-88e907a0656e\\hud_cian_dense.png' });
    console.log('✅ Screenshot taken: hud_cian_dense.png');
  } catch (error) {
    console.error('❌ Error taking screenshot:', error.message);
  } finally {
    await browser.close();
  }
})();
