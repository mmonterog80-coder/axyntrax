import time
import requests
import os
import subprocess
import pyautogui
from dotenv import load_dotenv

load_dotenv()
HETZNER_URL = "http://178.156.140.78:8080"
LOCAL_QUEUE = r"C:\AXYNTRAX\remote_orders.txt"
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def send_telegram_msg(chat_id, text):
    if not TELEGRAM_TOKEN: return
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
    except: pass

def send_telegram_photo(chat_id, photo_path, caption=""):
    if not TELEGRAM_TOKEN: return
    try:
        with open(photo_path, 'rb') as photo:
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto", data={"chat_id": chat_id, "caption": caption}, files={"photo": photo})
    except: pass

def check_night_report():
    try:
        print("[SYNC] Verificando reportes nocturnos de DeepSeek...")
        response = requests.get(f"{HETZNER_URL}/api/night_report", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("reports"):
                print("\n" + "="*50)
                print("🌙 REPORTE NOCTURNO DE LA FLOTA AXYNTRAX 🌙")
                print("="*50)
                for r in data["reports"]:
                    print(f"- {r}")
                print("="*50 + "\n")
            else:
                print("[SYNC] No hay reportes nocturnos pendientes.")
    except Exception as e:
        print(f"[SYNC] Error obteniendo reporte nocturno: {e}")

def process_local_order(order):
    cmd = order.get("command", "")
    user = order.get("user", "")
    print(f"-> Procesando orden local de Telegram: {cmd}")
    
    if cmd.lower().startswith("/screenshot") or "captura de pantalla" in cmd.lower() or "pantalla" in cmd.lower():
        try:
            shot_path = "local_screen.png"
            pyautogui.screenshot(shot_path)
            send_telegram_photo(user, shot_path, "🖥️ *HUD Local (Antigravity PC)*")
            os.remove(shot_path)
            send_telegram_msg(user, "✅ Captura de PC local enviada con éxito.")
        except Exception as e:
            send_telegram_msg(user, f"❌ Error tomando captura local: {e}")
            
    elif cmd.lower().startswith("/cmd "):
        actual_cmd = cmd[5:]
        try:
            result = subprocess.run(actual_cmd, shell=True, capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
            send_telegram_msg(user, f"💻 *Resultado Local CMD:*\n```\n{output[:3500]}\n```")
        except Exception as e:
            send_telegram_msg(user, f"❌ Error ejecutando CMD local: {e}")
            
    else:
        # Transferir orden a CrewAI local (para la próxima iteración, actualmente se deja en el .txt)
        with open(LOCAL_QUEUE, "a", encoding="utf-8") as f:
            f.write(f"{cmd}\n")
        send_telegram_msg(user, f"📥 Orden registrada en la PC Local para procesamiento interno: `{cmd}`")

def main():
    print("🤖 Agente Local de Escritorio (Antigravity -> Hetzner)")
    check_night_report()
    while True:
        try:
            # 1. Hacemos ping a poll_orders (Esto actualiza last_ping en el servidor)
            resp = requests.get(f"{HETZNER_URL}/api/poll_orders", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                orders = data.get("orders", [])
                if orders:
                    print(f"[{time.strftime('%X')}] Recibidas {len(orders)} órdenes de Telegram.")
                    for order in orders:
                        # Convertir a dict si viene como string
                        if isinstance(order, str):
                            order = {"command": order, "user": ""}
                        process_local_order(order)
        except requests.exceptions.RequestException as e:
            pass
            
        # Dormir 10 segundos antes del próximo ping
        time.sleep(10)

if __name__ == "__main__":
    main()
