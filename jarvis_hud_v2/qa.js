const { chromium } = require('playwright');
const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');
require('dotenv').config({ path: '../.env' });

(async () => {
  console.log('VERONICA: Iniciando auditoría visual...');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  
  try {
    await page.goto('http://178.156.140.78:3002', { waitUntil: 'networkidle', timeout: 30000 });
    
    // Wait for animations to settle
    await page.waitForTimeout(3000);
    
    const screenshotPath = 'qa_hero.png';
    await page.screenshot({ path: screenshotPath, fullPage: true });
    console.log('VERONICA: Captura tomada con éxito.');
    
    // Send to Telegram
    const token = process.env.TELEGRAM_BOT_TOKEN;
    const chatId = process.env.TELEGRAM_ALLOWED_CHAT_ID;
    
    const formData = new FormData();
    formData.append('chat_id', chatId);
    formData.append('photo', fs.createReadStream(screenshotPath));
    formData.append('caption', 'V.E.R.O.N.I.C.A. [REPORTE DE CALIDAD]:\nEl HUD Táctico Stark ha sido restaurado exitosamente con telemetría en tiempo real, IAs activas y estética Iron Man.\nAdjunto matriz visual para su confirmación.');
    
    console.log('VERONICA: Enviando a Telegram...');
    await axios.post(`https://api.telegram.org/bot${token}/sendPhoto`, formData, {
      headers: formData.getHeaders()
    });
    console.log('VERONICA: Reporte enviado con éxito.');
    
  } catch (error) {
    console.error('VERONICA Error:', error.message);
  } finally {
    await browser.close();
  }
})();
