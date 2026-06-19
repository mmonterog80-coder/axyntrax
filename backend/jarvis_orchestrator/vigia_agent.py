import os
import requests
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

def check_deepseek_health():
    """Realiza un ping mínimo a DeepSeek para verificar si hay error 429."""
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        return "SKIPPED: Sin clave"
    try:
        client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5
        )
        return "OK"
    except Exception as e:
        error_str = str(e).lower()
        if "429" in error_str or "insufficient_quota" in error_str:
            return "ERROR 429: Cuota Excedida"
        return f"ERROR: {e}"

def check_openrouter_health():
    """Realiza un ping mínimo a OpenRouter (Gemini/Qwen) para verificar si hay error 429."""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        return "SKIPPED: Sin clave"
    try:
        client = OpenAI(api_key=key, base_url="https://openrouter.ai/api/v1")
        resp = client.chat.completions.create(
            model="google/gemini-2.5-flash",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5
        )
        return "OK"
    except Exception as e:
        error_str = str(e).lower()
        if "429" in error_str or "insufficient_quota" in error_str:
            return "ERROR 429: Cuota Excedida"
        return f"ERROR: {e}"

def alert_telegram(message: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_ALLOWED_CHAT_ID")
    if not token or not chat_id:
        print("Telegram no configurado para VIGÍA.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": message})
    except Exception as e:
        print(f"Error alertando a Telegram: {e}")

def run_vigia_check():
    """Agente VIGÍA: Monitorea salud de APIs y alerta si se agotan tokens."""
    print("Iniciando escaneo VIGÍA...")
    ds_status = check_deepseek_health()
    or_status = check_openrouter_health()
    
    print(f"DeepSeek: {ds_status}")
    print(f"OpenRouter: {or_status}")
    
    alert_msg = "👁️ *AGENTE VIGÍA: Reporte de Tokens*\n\n"
    alert_msg += f"🔹 DeepSeek: {ds_status}\n"
    alert_msg += f"🔹 OpenRouter (Gemini): {or_status}\n"
    
    if "429" in ds_status or "429" in or_status:
        alert_msg += "\n⚠️ ALERTA: Protocolo Eclipse sugerido. Una o más APIs han agotado sus tokens."
        
    alert_telegram(alert_msg)

if __name__ == "__main__":
    run_vigia_check()
