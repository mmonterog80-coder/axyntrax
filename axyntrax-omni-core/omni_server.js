require('dotenv').config({ path: 'C:/AXYNTRAX/AXYNTRAX_VAULT/master_keys.env' });
const fastify = require('fastify')({ logger: true });
const { Server } = require('socket.io');
const { Telegraf } = require('telegraf');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const { GoogleGenAI } = require('@google/genai');
const { processOmniMessage } = require('./ai_router');

// Inicializar Servidores de Escucha y Motores IA
const telegramBot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN || 'dummy_token');
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
// MÓDULO DE VOZ J.A.R.V.I.S (FISH AUDIO)
// ==========================================
const generateJarvisVoice = async (text) => {
    const fishApiKey = process.env.FISH_AUDIO_API_KEY || process.env.ELEVENLABS_API_KEY;
    if (!fishApiKey) return null;
    
    try {
        const ttsResponse = await axios({
            method: 'post',
            url: 'https://api.fish.audio/v1/tts',
            headers: {
                'Authorization': `Bearer ${fishApiKey}`,
                'Content-Type': 'application/json'
            },
            data: {
                text: text,
                format: 'mp3',
                sample_rate: 44100
            },
            responseType: 'arraybuffer' // Necesitamos el buffer crudo para enviarlo a Telegram
        });
        return ttsResponse.data;
    } catch (error) {
        let errorMsg = error.message;
        if (error.response && error.response.data) {
            try {
                errorMsg = Buffer.from(error.response.data).toString('utf8');
            } catch(e) {}
        }
        console.error("❌ Fallo en síntesis TTS Fish Audio:", errorMsg);
        return null;
    }
};

const sendVoiceReply = async (ctx, aiResponse) => {
    try {
        await ctx.telegram.sendChatAction(ctx.chat.id, 'record_voice');
        const textToSpeech = aiResponse.text || "La matriz neuronal no pudo generar una respuesta.";
        const audioBuffer = await generateJarvisVoice(textToSpeech);
        
        if (audioBuffer) {
            // Enviar como Nota de Voz
            await ctx.replyWithVoice({ source: Buffer.from(audioBuffer) });
        } else {
            await ctx.reply("⚠️ [ALERTA L99] El sistema de Voz de J.A.R.V.I.S falló (Llave Inválida o Sin Créditos en Fish Audio). Verifique sus credenciales en master_keys.env.\n\nRespuesta de texto: " + textToSpeech); // Fallback si falla la voz
        }
    } catch (error) {
        console.error("❌ Falla crítica en sendVoiceReply:", error);
        await ctx.reply("⚠️ Error interno al intentar comunicar con los servidores de voz o texto.");
    }
};

// ==========================================
// CANALES DE ENTRADA (TELEGRAM MULTIMODAL)
// ==========================================

// 1. MANEJO DE TEXTO
telegramBot.on('text', async (ctx) => {
    await ctx.telegram.sendChatAction(ctx.chat.id, 'typing');
    const aiResponse = await processOmniMessage(ctx.message.text, 'TELEGRAM', ctx.from.id);
    await sendVoiceReply(ctx, aiResponse);
    broadcastLog('TEXTO', ctx.from.id, ctx.message.text, aiResponse);
});

// 2. MANEJO DE AUDIO (NATIVO CON GEMINI MULTIMODAL)
telegramBot.on('voice', async (ctx) => {
    try {
        await ctx.reply("🎙️ Analizando frecuencia de audio...");
        const fileLink = await ctx.telegram.getFileLink(ctx.message.voice.file_id);
        const response = await axios({ url: fileLink.href, responseType: 'arraybuffer' });
        
        const audioBase64 = Buffer.from(response.data).toString('base64');

        // Usamos Gemini 1.5 Flash para escuchar directamente el audio sin Groq
        const geminiResponse = await gemini.models.generateContent({
            model: 'gemini-1.5-flash',
            contents: [
                {
                    role: 'user',
                    parts: [
                        { inlineData: { data: audioBase64, mimeType: "audio/ogg" } },
                        { text: "Transcribe el contenido de este audio de la manera más fiel posible. Responde SOLAMENTE con la transcripción, sin saludos ni comentarios." }
                    ]
                }
            ]
        });

        const transcription = geminiResponse.text;

        // Enviar el texto transcrito al Cerebro Orquestador
        const aiResponse = await processOmniMessage(`[AUDIO TRANSCRITO DEL USUARIO]: ${transcription}`, 'TELEGRAM', ctx.from.id);
        
        await sendVoiceReply(ctx, aiResponse);
        broadcastLog('VOICE', ctx.from.id, `(🎙️ Audio Transcrito) "${transcription}"`, aiResponse, 'Gemini-Audio');
    } catch (e) {
        console.error("Error en módulo de Audio:", e);
        ctx.reply("❌ Error al procesar su nota de voz. Intente nuevamente o use texto.");
    }
});

// 3. MANEJO DE IMÁGENES (GEMINI VISION OCR)
telegramBot.on('photo', async (ctx) => {
    try {
        await ctx.reply("📷 Escaneando estructura de imagen...");
        const photo = ctx.message.photo[ctx.message.photo.length - 1];
        const fileLink = await ctx.telegram.getFileLink(photo.file_id);
        const response = await axios({ url: fileLink.href, responseType: 'arraybuffer' });
        
        const imageBase64 = Buffer.from(response.data).toString('base64');

        // Conectar con Gemini Vision para OCR
        const geminiResponse = await gemini.models.generateContent({
            model: 'gemini-1.5-flash',
            contents: [
                {
                    role: 'user',
                    parts: [
                        { inlineData: { data: imageBase64, mimeType: "image/jpeg" } },
                        { text: "Analiza esta imagen y describe todos sus detalles. Si es un documento o ticket, extrae el texto (OCR) y resume los datos clave." }
                    ]
                }
            ]
        });

        const imageAnalysis = geminiResponse.text;

        const aiResponse = await processOmniMessage(`[SISTEMA DE VISIÓN]: El usuario acaba de enviar una imagen. Análisis visual extraído:\n\n${imageAnalysis}\n\nRespondele al usuario en base a esto.`, 'TELEGRAM', ctx.from.id);
        
        await sendVoiceReply(ctx, aiResponse);
        broadcastLog('PHOTO', ctx.from.id, `[🖼️ Análisis de Imagen]`, aiResponse, 'Gemini-Vision');
    } catch (e) {
        console.error("Error en módulo de Imagen:", e);
        ctx.reply("❌ Falla en los sensores ópticos. No pude escanear la imagen.");
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
                console.warn(`[CRITICAL] Telegram rechazó el Token (Error: ${tgError.message}).`);
            }
        } else {
            console.warn('[OMNI-CORE] ALERTA: Falta TELEGRAM_BOT_TOKEN.');
        }
        await fastify.listen({ port: 3005, host: '0.0.0.0' });
        console.log('[OMNI-CORE] Servidor Multimodal activo en el puerto 3005.');
    } catch (err) {
        fastify.log.error(err);
        process.exit(1);
    }
};

start();
process.once('SIGINT', () => telegramBot.stop('SIGINT'));
process.once('SIGTERM', () => telegramBot.stop('SIGTERM'));
