import os
import requests
from supabase import create_client, Client
from datetime import datetime, timedelta

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
WHATSAPP_NUMBER = os.environ.get("MIGUEL_WHATSAPP_NUMBER", "")
# Asumimos que tienes una API key de mensajería (ej. Meta) guardada o accesible para notificar
META_GRAPH_TOKEN = os.environ.get("META_GRAPH_TOKEN", "")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
except Exception as e:
    print("Error conectando a Supabase:", e)
    exit(1)

def alert_whatsapp(message: str):
    """Función de utilidad para enviar alertas al admin"""
    print(f"[ALERTA WHATSAPP A {WHATSAPP_NUMBER}]: {message}")
    # Aquí iría el código real de requests.post hacia graph.facebook.com/v19.0/.../messages

def check_rotations():
    print("Iniciando chequeo de rotaciones de secretos...")
    res = supabase.table("secret_rotation_schedule").select("*").execute()
    
    now = datetime.now()
    alerts = []
    
    for row in res.data:
        secret_path = row["secret_path"]
        rotation_days = row["rotation_days"]
        # Convertir ISO 8601 a datetime
        # Supabase devuelve ej: '2026-06-19T00:34:29.123456+00:00'
        # Hacemos parsing básico
        last_rotated_str = row["last_rotated_at"].split('.')[0].replace('T', ' ').replace('+00:00', '')
        last_rotated = datetime.strptime(last_rotated_str, "%Y-%m-%d %H:%M:%S")
        
        days_since_rotation = (now - last_rotated).days
        days_left = rotation_days - days_since_rotation
        
        if days_left <= 3:
            alerts.append(f"⚠️ El secreto {secret_path} expirará en {days_left} días (Rotación cada {rotation_days}d).")
            
    if alerts:
        mensaje_final = "J.A.R.V.I.S. ZERO-TRUST ALERT\n" + "\n".join(alerts)
        alert_whatsapp(mensaje_final)
    else:
        print("Todo en orden. Ningún secreto próximo a rotación.")

if __name__ == "__main__":
    check_rotations()
