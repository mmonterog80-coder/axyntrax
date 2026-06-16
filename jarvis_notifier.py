# -*- coding: utf-8 -*-
import datetime
import requests
import sys
from config_env import WHATSAPP_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

def send_whatsapp_message(text):
    """
    Envía un mensaje usando el webhook de transmisión de JARVIS Orquestador
    para que lo envíe por Telegram con su respectivo Audio (Voz de JARVIS).
    """
    try:
        port = os.getenv("PORT", "8000")
        url = f"http://localhost:{port}/webhook/telegram_broadcast"
        payload = {"message": text}
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️ Error enviando a Orquestador: {response.text}")
            print("\n" + "🔔 [FALLBACK CONSOLA] ".ljust(60, "═"))
            print(text)
            print("═" * 60 + "\n")
    except Exception as e:
        print(f"⚠️ Orquestador desconectado o no responde: {e}")
        print("\n" + "🔔 [FALLBACK CONSOLA] ".ljust(60, "═"))
        print(text)
        print("═" * 60 + "\n")
        
    return True

def notify_success(portal, empresa, cargo, salario, url):
    msg = (f"✅ Postulación enviada\n"
           f" 🏢 Empresa: {empresa}\n"
           f" 💼 Cargo: {cargo}\n"
           f" 💰 Salario: {salario}\n"
           f" 🌐 Portal: {portal}\n"
           f" 📎 CV adaptado: Sí\n"
           f" 🔗 Ver oferta: {url}")
    send_whatsapp_message(msg)

def notify_alert(tipo_obstaculo, portal, accion, url):
    msg = (f"⚠️ {tipo_obstaculo} en {portal}\n"
           f" Acción requerida: {accion}\n"
           f" URL: {url}")
    send_whatsapp_message(msg)

def notify_daily_report(totales, acumulado, vistas, entrevistas, en_proceso, rechazadas, pendientes, mejor_oferta):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    msg = (f"📊 CHAU CHAMBA — Reporte Diario {fecha}\n"
           f" ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
           f" ✅ Postulaciones hoy: {totales}\n"
           f" 📋 Total acumulado: {acumulado}\n"
           f" 👁️ CVs vistos por empresas: {vistas}\n"
           f" 📞 Entrevistas agendadas: {entrevistas}\n"
           f" ⏳ En proceso de selección: {en_proceso}\n"
           f" ❌ Rechazadas: {rechazadas}\n"
           f" ⚠️ Pendientes tu acción: {pendientes}\n"
           f" ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
           f" 🏆 Mejor oferta hoy: {mejor_oferta}\n"
           f" 📌 Ver dashboard completo: Supabase Dashboard")
    send_whatsapp_message(msg)

def notify_status_update(empresa, cargo, estado_ant, estado_act, detalle=""):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    msg = (f"🔄 ACTUALIZACIÓN DE POSTULACIÓN\n"
           f" 🏢 {empresa} — {cargo}\n"
           f" 📊 Estado anterior: {estado_ant}\n"
           f" 📊 Estado actual: {estado_act}\n"
           f" 📅 Fecha: {fecha}\n"
           f" 📝 Detalle: {detalle}")
    send_whatsapp_message(msg)

if __name__ == "__main__":
    notify_success("LinkedIn", "Minera Buenaventura", "Supply Chain Manager", "S/ 3,500", "https://linkedin.com/...")
