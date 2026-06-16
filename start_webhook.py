import os
import time
import requests
from pyngrok import ngrok
from dotenv import load_dotenv

load_dotenv("C:/AXYNTRAX/.env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

print("Iniciando túnel ngrok...")
http_tunnel = ngrok.connect(8000)
public_url = http_tunnel.public_url
print(f"URL Pública de ngrok: {public_url}")

webhook_url = f"{public_url}/tasks/telegram/webhook"
api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={webhook_url}"

print("Configurando webhook en Telegram...")
response = requests.get(api_url)
print(response.json())

print("Webhook configurado. Ngrok esta en ejecucion. Esperando mensajes...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Cerrando túnel...")
    ngrok.disconnect(public_url)
    ngrok.kill()
