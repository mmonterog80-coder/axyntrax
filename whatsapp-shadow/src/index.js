require('dotenv').config();
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

console.log('[WHATSAPP-SHADOW] Inicializando cliente...');

const client = new Client({
    authStrategy: new LocalAuth({ clientId: "shadow-client" }),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

client.on('qr', (qr) => {
    console.log('[WHATSAPP-SHADOW] Escanea el siguiente QR para iniciar sesión:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('[WHATSAPP-SHADOW] Cliente está listo y conectado!');
});

client.on('message', async msg => {
    console.log(`[WHATSAPP-SHADOW] Mensaje recibido de ${msg.from}: ${msg.body}`);
    
    // Enviar al CORE_API (Audit Logs)
    try {
        await axios.post(`${process.env.CORE_API_URL}/whatsapp/webhook`, {
            from: msg.from,
            body: msg.body,
            timestamp: msg.timestamp
        });
    } catch (error) {
        console.error(`[WHATSAPP-SHADOW] Error enviando al CORE_API: ${error.message}`);
    }

    if(msg.body === '!ping') {
        msg.reply('pong');
    }
});

client.initialize();
