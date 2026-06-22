import os
from supabase import create_client, Client
import pandas as pd
from datetime import datetime, timedelta
# Importamos modelos para MVP predictivo. En prod usaremos XGBoost entrenado.
from sklearn.ensemble import RandomForestClassifier 

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://xyz.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "ey...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_pending_appointments():
    """Obtiene las citas de mañana para evaluar el riesgo de inasistencia."""
    tomorrow = datetime.now() + timedelta(days=1)
    start_date = tomorrow.replace(hour=0, minute=0, second=0).isoformat()
    end_date = tomorrow.replace(hour=23, minute=59, second=59).isoformat()
    
    # Try except temporal por si la BD no está levantada
    try:
        response = supabase.table('appointments') \
            .select('*') \
            .eq('status', 'PENDING') \
            .gte('appointment_date', start_date) \
            .lte('appointment_date', end_date) \
            .execute()
        return response.data
    except Exception as e:
        print("Mocking data due to DB error or setup:", e)
        return [
            {"id": "uuid-1", "client_name": "Juan Perez", "noshow_probability": 0.0},
            {"id": "uuid-2", "client_name": "Maria Gomez", "noshow_probability": 0.0}
        ]

def calculate_noshow_risk(appointment):
    """
    Motor de predicción (MVP).
    En la versión full, XGBoost evaluará:
    - Distancia del cliente al local.
    - Clima pronosticado para mañana.
    - Historial de inasistencias pasadas.
    """
    # Simulamos una inferencia de modelo
    base_risk = 0.15
    if len(appointment.get('client_name', '')) > 10:
        base_risk += 0.70 # Riesgo alto!
        
    return min(base_risk, 0.99)

def get_client_ltv(client_name):
    """Simula una consulta a BD para obtener el Lifetime Value del cliente"""
    # Si el nombre empieza con M (ej. Maria), simulamos que es VIP
    if client_name.startswith('M'):
        return "VIP"
    return "STANDARD"

def run_engine():
    print("[PREDICTIVE-ENGINE] Iniciando análisis de ausencias para mañana...")
    appointments = fetch_pending_appointments()
    
    for app in appointments:
        risk = calculate_noshow_risk(app)
        ltv_status = get_client_ltv(app['client_name'])
        
        print(f"[PREDICTIVE-ENGINE] Evaluando {app['client_name']} (LTV: {ltv_status}) -> Probabilidad Ausencia: {risk*100:.1f}%")
        
        try:
            supabase.table('appointments').update({"noshow_probability": risk}).eq("id", app['id']).execute()
        except:
            pass
        
        if risk >= 0.80:
            if ltv_status == "VIP":
                print(f"⚠️ RIESGO ALTO EN CLIENTE VIP: Disparando protocolo Concierge (Llamada humana). CERO DESCUENTOS.")
                # requests.post(WEBHOOK_CONCIERGE, json={"client": app, "action": "CALL_PREMIUM"})
            else:
                print(f"⚠️ RIESGO CRITICO: Disparando protocolo de retención automática (Descuento Topado 15%) para {app['client_name']}...")
                # requests.post(WEBHOOK_N8N, json={"client": app, "offer": "15% descuento"})

if __name__ == "__main__":
    run_engine()
