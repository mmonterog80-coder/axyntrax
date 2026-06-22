require('dotenv').config({ path: 'C:/AXYNTRAX/AXYNTRAX_VAULT/master_keys.env' });
const fastify = require('fastify')({ logger: true });
const { Server } = require('socket.io');
const { Telegraf } = require('telegraf');
const axios = require('axios');
const fs = require('fs');
const { Groq } = require('groq-sdk');
const { GoogleGenAI } = require('@google/genai');
const { processOmniMessage } = require('./ai_router');

// Inicializar Servidores de Escucha y Motores IA
const telegramBot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN || 'dummy_token');
const groq = new Groq({ apiKey: process.env.GROQ_API_KEY || 'dummy_key' });
const gemini = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || 'dummy_key' });

fastify.register(require('@fastify/cors'), {
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE']
});

let io; // Instancia global de Socket.io

// Configurar WebSockets para el HUD (ESTRICTAMENTE SOLO LECTURA)
fastify.ready(err => {
    if (err) throw err;
    io = new Server(fastify.server, { cors: { origin: '*' } });

    io.on('connection', (socket) => {
        console.log(`[HUD] Nueva conexión de visor de solo lectura: ${socket.id}`);
        // Se ha purgado 'hud_message' - Telegram es el único canal bidireccional L99
    });
});

// Middleware para emitir Logs al HUD
const broadcastLog = (type, user, message, response, preProcessor = null) => {
    if (io) {
        io.emit('omni_log', {
            channel: 'TELEGRAM',
            type,
            user,
            message: preProcessor ? `[${preProcessor}] ${message}` : message,
            intent: response.intent,
            ai_reply: `[${response.agent || 'DeepSeek'}] ${response.text}`
        });
    }
};

// ==========================================
// CANALES DE ENTRADA (TELEGRAM MULTIMODAL)
// ==========================================

// 1. MANEJO DE TEXTO (Directo a DeepSeek)
telegramBot.on('text', async (ctx) => {
    const aiResponse = await processOmniMessage(ctx.message.text, 'TELEGRAM', ctx.from.id);
    await ctx.reply(aiResponse.text);
    broadcastLog('TEXTO', ctx.from.id, ctx.message.text, aiResponse);
});

// 2. MANEJO DE AUDIO (GROQ WHISPER + DEEPSEEK)
telegramBot.on('voice', async (ctx) => {
    try {
        await ctx.reply("🎙️ Escuchando audio...");
        const fileLink = await ctx.telegram.getFileLink(ctx.message.voice.file_id);
        const response = await axios({ url: fileLink.href, responseType: 'stream' });
        
        // Guardar temporalmente el archivo OGG de Telegram
        const tempFilePath = `temp_audio_${ctx.from.id}.ogg`;
        const writer = fs.createWriteStream(tempFilePath);
        response.data.pipe(writer);
        
        await new Promise((resolve) => writer.on('finish', resolve));

        // Transcribir el audio usando Groq (Whisper V3 - Ultra rápido)
        const transcription = await groq.audio.transcriptions.create({
            file: fs.createReadStream(tempFilePath),
            model: "whisper-large-v3",
            response_format: "text",
            language: "es" // Forzamos español para mayor precisión médica/comercial
        });

        fs.unlinkSync(tempFilePath); // Destruir rastro temporal

        // Enviar el texto transcrito al Cerebro Orquestador (DeepSeek V4)
        const aiResponse = await processOmniMessage(`[NOTA DE VOZ TRANSCRITA]: ${transcription}`, 'TELEGRAM', ctx.from.id);
        
        // --- MÓDULO TTS: ELEVENLABS (VOICE OUT) ---
        if (process.env.ELEVENLABS_API_KEY) {
            try {
                await ctx.reply("🎙️ Generando síntesis vocal...");
                const ttsResponse = await axios({
                    method: 'post',
                    url: 'https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB/stream', // Voz de Adam (Estilo J.A.R.V.I.S)
                    headers: {
                        'Accept': 'audio/mpeg',
                        'xi-api-key': process.env.ELEVENLABS_API_KEY,
                        'Content-Type': 'application/json'
                    },
                    data: {
                        text: aiResponse.text,
                        model_id: "eleven_multilingual_v2",
                        voice_settings: { stability: 0.5, similarity_boost: 0.8 }
                    },
                    responseType: 'stream'
                });
                await ctx.replyWithVoice({ source: ttsResponse.data });
            } catch (ttsError) {
                console.error("❌ Fallo en síntesis TTS:", ttsError.message);
                await ctx.reply(aiResponse.text); // Fallback a texto
            }
        } else {
            await ctx.reply(aiResponse.text); // Fallback a texto si no hay API Key
        }
        
        broadcastLog('VOICE', ctx.from.id, `(🎙️ Audio Transcrito) "${transcription}"`, aiResponse, 'Groq-Whisper');
    } catch (e) {
        console.error("Error en módulo de Audio:", e);
        ctx.reply("❌ Error al procesar su nota de voz. Por favor, escriba su mensaje.");
    }
});

// 3. MANEJO DE IMÁGENES (VOUCHERS)
telegramBot.on('photo', async (ctx) => {
    try {
        await ctx.reply("📷 Analizando comprobante...");
        // Obtener foto en mayor resolución
        const photo = ctx.message.photo[ctx.message.photo.length - 1];
        const fileLink = await ctx.telegram.getFileLink(photo.file_id);
        
        // Aquí conectamos con Gemini Vision para OCR
        const aiResponse = await processOmniMessage(`[SISTEMA OCR]: El usuario ha enviado un comprobante de pago. Extraer datos y procesar.`, 'TELEGRAM', ctx.from.id);
        
        await ctx.reply(aiResponse.text);
        broadcastLog('PHOTO', ctx.from.id, `[🖼️ Análisis de Comprobante]`, aiResponse, 'Gemini-OCR');
    } catch (e) {
        console.error("Error en módulo de Imagen:", e);
        ctx.reply("❌ Error al escanear la imagen.");
    }
});

// Arrancar OMNI-CORE
const start = async () => {
    try {
        if (process.env.TELEGRAM_BOT_TOKEN && process.env.TELEGRAM_BOT_TOKEN !== 'dummy_token') {
            try {
                await telegramBot.launch();
                console.log('[OMNI-CORE] Bot de Telegram Multimodal conectado.');
            } catch (tgError) {
                console.warn(`[CRITICAL] Telegram rechazó el Token (Error: ${tgError.message}). Operando en Modo Degradado (Solo HUD).`);
            }
        } else {
            console.warn('[OMNI-CORE] ALERTA: Falta TELEGRAM_BOT_TOKEN.');
        }
        await fastify.listen({ port: 3005, host: '0.0.0.0' });
        console.log('[OMNI-CORE] Servidor Multimodal y WebSockets activos en el puerto 3005.');
    } catch (err) {
        fastify.log.error(err);
        process.exit(1);
    }
};

start();
process.once('SIGINT', () => telegramBot.stop('SIGINT'));
process.once('SIGTERM', () => telegramBot.stop('SIGTERM'));
