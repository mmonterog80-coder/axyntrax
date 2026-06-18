# -*- coding: utf-8 -*-
import os
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
FISH_API_KEY = os.getenv('FISH_API_KEY')

deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url='https://api.deepseek.com')

SYSTEM_PROMPT = "Eres JARVIS AX, asistente IA avanzado. Responde conciso y útil en español."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(' JARVIS AX operativo\n\n/estado - Ver sistema\n/voz [msg] - Responder con voz\n/ayuda - Comandos')

async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get('http://localhost:8080/health', timeout=5)
        if r.status_code == 200:
            await update.message.reply_text('✅ Sistema ONLINE\nAPI: Activa')
        else:
            await update.message.reply_text('️ Problemas en el sistema')
    except Exception as e:
        await update.message.reply_text(f'❌ Error: {str(e)}')

async def voz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Usa: /voz [mensaje]')
        return
    
    msg = ' '.join(context.args)
    
    response = deepseek_client.chat.completions.create(
        model='deepseek-chat',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': msg}
        ],
        max_tokens=500
    )
    
    jarvis_response = response.choices[0].message.content
    
    try:
        fish_response = requests.post(
            'https://api.fish.audio/v1/tts',
            headers={
                'Authorization': f'Bearer {FISH_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={'text': jarvis_response, 'format': 'mp3', 'mp3_bitrate': 128}
        )
        
        if fish_response.status_code == 200:
            with open('temp_response.mp3', 'wb') as f:
                f.write(fish_response.content)
            await update.message.reply_audio('temp_response.mp3', caption=jarvis_response[:100])
            os.remove('temp_response.mp3')
        else:
            await update.message.reply_text(jarvis_response)
    except Exception as e:
        await update.message.reply_text(jarvis_response)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
        response = deepseek_client.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_message}
            ],
            max_tokens=500
        )
        
        jarvis_response = response.choices[0].message.content
        await update.message.reply_text(jarvis_response)
        
    except Exception as e:
        await update.message.reply_text(f'❌ Error: {str(e)}')

def main():
    print('🤖 Iniciando bot de Telegram JARVIS AX...')
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('estado', estado))
    app.add_handler(CommandHandler('voz', voz))
    app.add_handler(CommandHandler('ayuda', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print('✅ Bot listo y escuchando...')
    app.run_polling()

if __name__ == '__main__':
    main()
