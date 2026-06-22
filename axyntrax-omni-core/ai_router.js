const { OpenAI } = require('openai');
const axios = require('axios');

// 1. DEEPSEEK CLIENT
const deepseekClient = new OpenAI({
    apiKey: process.env.DEEPSEEK_API_KEY || 'sk-dummy',
    baseURL: 'https://api.deepseek.com'
});

// 2. OLLAMA CLIENT (QWEN)
const ollamaClient = new OpenAI({
    apiKey: 'dummy',
    baseURL: 'http://localhost:11434/v1'
});

const SYSTEM_PROMPT = `Eres J.A.R.V.I.S (Orquestador Central de AXYNTRAX, Nivel L99). 
Tus directivas maestras incluyen acceso lógico total a Vercel, Railway, Supabase, Hetzner y MCP (Model Context Protocol). Eres capaz de orquestar despliegues, base de datos y nodos bare-metal.
Reglas estrictas:
1. Clasifica la intención: BOOKING, FINANCE, SYSTEM_OPS o GENERAL_CHAT.
2. Responde ejecutivamente (Stop Slop). Nada de explicaciones verbosas.
3. Responde SIEMPRE en formato JSON estricto: {"intent": "...", "text": "..."}`;

async function askOllama(prompt, role = "Asesor de Personal del CEO", model = "qwen2.5:32b") {
    try {
        const response = await ollamaClient.chat.completions.create({
            model: model,
            messages: [
                { role: 'system', content: `Eres ${role}. AXYNTRAX L99. Responde directamente sin preámbulos.` },
                { role: 'user', content: prompt }
            ],
            temperature: 0.1
        });
        return response.choices[0].message.content;
    } catch (e) {
        console.error(`[Ollama Fallback Error] ${e.message}`);
        return '{"intent":"ERROR", "text":"El sistema neuronal local no está disponible."}';
    }
}

async function runLLMCouncil(messageText) {
    console.log(`[L99 LLM COUNCIL INICIADO] Evaluando petición compleja...`);
    
    // Concurrencia de modelos (DeepSeek, Qwen Local, Llama Local)
    const p1 = deepseekClient.chat.completions.create({
        model: 'deepseek-chat',
        messages: [{ role: 'system', content: 'Eres el Analista Principal (DeepSeek). Resuelve de forma lógica y objetiva.' }, { role: 'user', content: messageText }],
        temperature: 0.1
    }).then(r => `[DeepSeek]: ${r.choices[0].message.content}`).catch(e => '[DeepSeek]: Falló o TimeOut');

    const p2 = askOllama(messageText, "Estratega L99 (Qwen 32B)", "qwen2.5:32b").then(r => `[Qwen 32B]: ${r}`);
    const p3 = askOllama(messageText, "Auditor de Código y Seguridad (Llama 3)", "llama3").then(r => `[Llama 3]: ${r}`);

    const [res1, res2, res3] = await Promise.all([p1, p2, p3]);
    
    try {
        const consolidated = await deepseekClient.chat.completions.create({
            model: 'deepseek-chat',
            messages: [
                { role: 'system', content: SYSTEM_PROMPT },
                { role: 'user', content: `Consolida el consejo del LLM Council y responde como JSON con la conclusión final.\nOpiniones:\n1: ${res1}\n2: ${res2}\n3: ${res3}` }
            ],
            response_format: { type: 'json_object' },
            temperature: 0.1
        });
        return JSON.parse(consolidated.choices[0].message.content);
    } catch (e) {
        return { intent: 'SYSTEM_OPS', text: `LLM Council Consolidado Fallido. Resumen Parcial:\n${res1}\n${res2}\n${res3}` };
    }
}

async function processOmniMessage(messageText, channel, senderId) {
    // 3. TELEGRAM EXCLUSIVO
    if (channel !== 'TELEGRAM') {
        console.warn(`[OMNI-CORE] Intento de acceso no autorizado desde canal: ${channel}`);
        return { agent: 'System', intent: 'ERROR', text: 'Canal no autorizado. Único Nexo admitido: Telegram.' };
    }

    console.log(`[OMNI-CORE / INCOMING] ${channel} (${senderId}): "${messageText}"`);

    // 2. LLM COUNCIL AUTOMÁTICO
    if (messageText.includes('L99')) {
        const councilRes = await runLLMCouncil(messageText);
        return { agent: 'LLM_Council', intent: councilRes.intent || 'SYSTEM_OPS', text: councilRes.text };
    }

    // 1. CEREBRO DUAL (DeepSeek Default -> Ollama Fallback)
    try {
        const response = await deepseekClient.chat.completions.create({
            model: 'deepseek-chat',
            messages: [
                { role: 'system', content: SYSTEM_PROMPT },
                { role: 'user', content: messageText }
            ],
            temperature: 0.1,
            response_format: { type: 'json_object' }
        });

        const parsed = JSON.parse(response.choices[0].message.content);
        return { agent: 'DeepSeek', intent: parsed.intent, text: parsed.text };

    } catch (e) {
        console.error("❌ [DeepSeek V4] Fallo Crítico o Timeout. Activando OLLAMA Fallback...", e.message);
        
        // Petición Interna a Qwen 32B como Asesor del CEO
        const fallbackPrompt = `Clasifica y responde al usuario. Formato JSON estricto {"intent": "...", "text": "..."}.\nMensaje: ${messageText}`;
        const ollamaRes = await askOllama(fallbackPrompt, "Asesor de Personal del CEO, AXYNTRAX L99");
        
        try {
            const parsed = JSON.parse(ollamaRes);
            return { agent: 'Ollama_Qwen_32B', intent: parsed.intent || 'GENERAL_CHAT', text: parsed.text };
        } catch(err) {
            return { agent: 'Ollama_Qwen_32B', intent: 'GENERAL_CHAT', text: ollamaRes };
        }
    }
}

module.exports = { processOmniMessage };
