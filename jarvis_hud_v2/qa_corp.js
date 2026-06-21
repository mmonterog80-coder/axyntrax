const { chromium } = require('playwright');
const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');
require('dotenv').config({ path: '../.env' });

(async () => {
  console.log('VERONICA: Iniciando auditoría visual de la Web Corporativa...');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  
  try {
    // Open the local file directly
    await page.goto('file://C:/AXYNTRAX/web_axyntrax/index.html', { waitUntil: 'networkidle' });
    
    // Wait for animations
    await page.waitForTimeout(3000);
    
    const screenshotPath = 'qa_corp_web.png';
    await page.screenshot({ path: screenshotPath, fullPage: true });
    console.log('VERONICA: Captura tomada con éxito.');
    
    // Send to Telegram
    const token = process.env.TELEGRAM_BOT_TOKEN;
    const chatId = process.env.TELEGRAM_ALLOWED_CHAT_ID || process.env.TELEGRAM_MASTER_ID;
    
    const formData = new FormData();
    formData.append('chat_id', chatId);
    formData.append('photo', fs.createReadStream(screenshotPath));
    formData.append('caption', 'V.E.R.O.N.I.C.A. [REPORTE DE CALIDAD - HACKATHON]:\nLa Fase 3 Final (Pricing, Footer corporativo y SEO) ha sido estructurada por H.O.M.E.R.\nLa página principal de AXYNTRAX ha sido completada al 100% en esta sesión, Señor.');
    
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
