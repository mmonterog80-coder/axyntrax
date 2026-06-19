import os
from supabase import create_client, Client
from datetime import datetime, timedelta

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
WHATSAPP_NUMBER = os.environ.get("MIGUEL_WHATSAPP_NUMBER", "")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
except Exception as e:
    print("Error conectando a Supabase:", e)
    exit(1)

def alert_whatsapp(message: str):
    print(f"[REPORTE WHATSAPP A {WHATSAPP_NUMBER}]: {message}")

def weekly_digest():
    print("Iniciando generación de Weekly Digest de Seguridad...")
    # Calcular hace 7 días
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    # Obtener logs de la última semana
    # En Supabase gte significa >= 
    res = supabase.table("audit_log").select("*").gte("timestamp", seven_days_ago.isoformat()).execute()
    
    logs = res.data
    total_requests = len(logs)
    denied_requests = [log for log in logs if log["action"] in ("access_denied", "auth_failed")]
    
    reporte = (
        "🛡️ J.A.R.V.I.S. ZERO-TRUST - WEEKLY DIGEST\n"
        "====================================\n"
        f"Total accesos al Vault: {total_requests}\n"
        f"Accesos denegados/fallidos: {len(denied_requests)}\n\n"
    )
    
    if denied_requests:
        reporte += "Intento Sospechosos Destacados:\n"
        for dr in denied_requests[:5]: # Top 5
            reporte += f"- Agente [{dr['agent_id']}] falló en [{dr['secret_name']}] ({dr['action']})\n"
    else:
        reporte += "Sin actividad anómala. Escudo íntegro.\n"
        
    alert_whatsapp(reporte)

if __name__ == "__main__":
    weekly_digest()
