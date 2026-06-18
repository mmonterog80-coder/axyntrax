# -*- coding: utf-8 -*-
import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
FISH_API_KEY = os.getenv('FISH_API_KEY')

deepseek = OpenAI(api_key=DEEPSEEK_API_KEY, base_url='https://api.deepseek.com')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🤖 JARVIS AX Online. Usa /estado o escríbeme.')

async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ Sistema Operativo. CPU y RAM estables.')

async def voz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Usa: /voz [tu mensaje]')
        return
    msg = ' '.join(context.args)
    try:
        res = deepseek.chat.completions.create(model='deepseek-chat', messages=[{'role':'user','content':msg}], max_tokens=300)
        text = res.choices[0].message.content
        await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f'Error: {e}')

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = deepseek.chat.completions.create(model='deepseek-chat', messages=[{'role':'user','content':update.message.text}], max_tokens=300)
        await update.message.reply_text(res.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f'Error: {e}')

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('estado', estado))
    app.add_handler(CommandHandler('voz', voz))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("✅ Bot Telegram escuchando...")
    app.run_polling()

if __name__ == '__main__':
    main()
