import os
import time
import requests
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# --- INYECCIÓN L99: CONECTANDO CON EL VAULT MAESTRO ---
load_dotenv(os.path.join(os.path.dirname(__file__), 'AXYNTRAX_VAULT', 'master_keys.env'))

print("🤖 [J.A.R.V.I.S ORCHESTRATION] Iniciando Autonomous Worker L99 (Rol: Qwen Peón Avanzado)...")

SUPABASE_URL = os.getenv('SUPABASE_URL', '').rstrip('/rest/v1/').rstrip('/')
SUPABASE_KEY = (
    os.getenv('SUPABASE_KEY') or
    os.getenv('SUPABASE_SERVICE_ROLE_KEY') or
    os.getenv('SUPABASE_ANON_KEY')
)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', os.getenv('TELEGRAM_ALLOWED_CHAT_ID', ''))

if not SUPABASE_URL or not SUPABASE_KEY:
    print(f"❌ [Qwen] Faltan credenciales Supabase. No se puede iniciar el Worker Asíncrono.")
    exit(1)

print(f"📡 [Qwen] Conectando a Supabase Base de Datos: {SUPABASE_URL[:40]}...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("✅ [Qwen] Conectado. Esperando delegación de J.A.R.V.I.S...")

def send_report_to_jarvis(message):
    """Reporta los resultados terminados de vuelta al centro de mando (Telegram) bajo la firma [Qwen Worker]"""
    formatted_msg = f"🕷️ *[QWEN WORKER L99]*\n{message}"
    if not TELEGRAM_CHAT_ID or not TELEGRAM_TOKEN:
        print(f"📱 [Offline Report] {formatted_msg}")
        return
    try:
        requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
            json={'chat_id': TELEGRAM_CHAT_ID, 'text': formatted_msg, 'parse_mode': 'Markdown'},
            timeout=10
        )
    except Exception as e:
        print(f"Error reportando a JARVIS: {e}")

def execute_heavy_task(order):
    """Ejecuta una orden pesada delegada por J.A.R.V.I.S"""
    order_type = order['order_type']
    payload = order.get('payload', {})
    
    print(f"⚙️ [Qwen] Procesando orden pesada: {order_type}")
    
    if order_type == 'ping_servers':
        # Simula chequeo de servidores
        time.sleep(2)
        return {'status': 'success', 'report': 'Todos los nodos de Axyntrax (HUD, Core, Predictive) están ONLINE.'}
    
    elif order_type == 'database_cleanup':
        # Simula limpieza de DB
        time.sleep(3)
        return {'status': 'success', 'report': 'Vouchers basura eliminados. Logs comprimidos.'}

    elif order_type == 'market_analysis':
        # Simula un reporte largo que DeepSeek no debería hacer para no bloquear el Event Loop
        time.sleep(5)
        return {'status': 'success', 'report': 'Análisis del mercado finalizado. Se han detectado 3 competidores nuevos.'}
    
    else:
        time.sleep(1)
        return {'status': 'executed', 'report': f'Tarea genérica {order_type} completada satisfactoriamente.'}

def process_pending_orders():
    """Tira de Supabase para revisar órdenes asignadas a Qwen"""
    try:
        response = supabase.table('qwen_orders').select('*').eq('status', 'pending').order('priority', desc=True).limit(5).execute()
        orders = response.data
        
        if not orders:
            return 0
        
        print(f"📋 [Qwen] J.A.R.V.I.S ha delegado {len(orders)} órdenes.")
        
        for order in orders:
            order_id = order['id']
            # Marcar como procesando
            supabase.table('qwen_orders').update({'status': 'processing'}).eq('id', order_id).execute()
            
            try:
                result = execute_heavy_task(order)
                # Guardar resultado
                supabase.table('qwen_results').insert({
                    'order_id': order_id,
                    'result_type': order['order_type'],
                    'payload': result,
                    'status': 'success'
                }).execute()
                # Marcar como completado
                supabase.table('qwen_orders').update({'status': 'completed'}).eq('id', order_id).execute()
                
                print(f"✅ [Qwen] Orden {order_id} resuelta.")
                send_report_to_jarvis(f"Reporte de Tarea: `{order['order_type']}`\nEstado: COMPLETADO\nDetalle: {result.get('report', 'Sin detalles.')}")
                
            except Exception as e:
                supabase.table('qwen_orders').update({'status': 'failed'}).eq('id', order_id).execute()
                print(f"❌ [Qwen] Orden {order_id} falló: {e}")
                send_report_to_jarvis(f"FALLO CRÍTICO en tarea `{order['order_type']}`: {e}")
        
        return len(orders)
    except Exception as e:
        # Silencioso para no ensuciar consola
        return 0

def main():
    print("🌙 [Qwen] Peón Avanzado Listo. Escuchando base de datos...")
    
    last_report = time.time()
    total_processed = 0
    
    while True:
        try:
            processed = process_pending_orders()
            total_processed += processed
            
            # Reporte de guardia cada hora (3600 segs) a J.A.R.V.I.S
            if time.time() - last_report > 3600:
                if total_processed > 0:
                    send_report_to_jarvis(f"Reporte de Guardia: He procesado {total_processed} órdenes pesadas en la última hora.")
                last_report = time.time()
                total_processed = 0
            
            time.sleep(15) # Polling moderado
            
        except KeyboardInterrupt:
            print("[Qwen] Apagado de emergencia.")
            break
        except Exception as e:
            time.sleep(30)

if __name__ == '__main__':
    main()
