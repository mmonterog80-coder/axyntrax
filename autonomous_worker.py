import os
import time
import requests
from datetime import datetime
from supabase import create_client, Client
from openai import OpenAI

print("🤖 Worker Autónomo JARVIS v2 - Iniciando...")

SUPABASE_URL = os.getenv('SUPABASE_URL', '').rstrip('/rest/v1/').rstrip('/')
SUPABASE_KEY = (
    os.getenv('SUPABASE_KEY') or
    os.getenv('SUPABASE_SERVICE_ROLE_KEY') or
    os.getenv('SUPABASE_ANON_KEY')
)
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', os.getenv('TELEGRAM_ALLOWED_CHAT_ID', ''))

if not SUPABASE_URL or not SUPABASE_KEY:
    print(f"❌ Faltan credenciales Supabase. URL={bool(SUPABASE_URL)} KEY={bool(SUPABASE_KEY)}")
    exit(1)

print(f"📡 Conectando a Supabase: {SUPABASE_URL[:40]}...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("✅ Supabase conectado")

deepseek = None
if DEEPSEEK_API_KEY:
    deepseek = OpenAI(api_key=DEEPSEEK_API_KEY, base_url='https://api.deepseek.com')
    print("✅ DeepSeek conectado")

def send_telegram(message):
    if not TELEGRAM_CHAT_ID or not TELEGRAM_TOKEN:
        print(f"📱 [Sin Telegram] {message[:100]}")
        return
    try:
        requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
            json={'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'Markdown'},
            timeout=10
        )
    except Exception as e:
        print(f"Error Telegram: {e}")

def execute_order(order):
    """Ejecuta una orden según su tipo"""
    order_type = order['order_type']
    payload = order.get('payload', {})
    
    print(f"⚙️ Ejecutando: {order_type}")
    
    if order_type == 'test_ping':
        return {
            'status': 'success',
            'message': 'JARVIS responde: estoy vivo y leyendo órdenes',
            'timestamp': datetime.now().isoformat(),
            'from': 'JARVIS'
        }
    
    elif order_type == 'analyze_web':
        url = payload.get('url', 'https://www.axyntrax-automation.net')
        return {
            'status': 'analyzed',
            'url': url,
            'timestamp': datetime.now().isoformat()
        }
    
    elif order_type == 'generate_report':
        topic = payload.get('topic', 'general')
        if deepseek:
            try:
                response = deepseek.chat.completions.create(
                    model='deepseek-chat',
                    messages=[{'role': 'user', 'content': f'Genera un reporte ejecutivo sobre: {topic}'}],
                    max_tokens=500
                )
                return {
                    'status': 'success',
                    'report': response.choices[0].message.content,
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                return {'status': 'error', 'error': str(e)}
        return {'status': 'error', 'error': 'DeepSeek no disponible'}
    
    elif order_type == 'send_telegram':
        message = payload.get('message', 'Mensaje desde JARVIS')
        send_telegram(message)
        return {'status': 'sent', 'timestamp': datetime.now().isoformat()}
    
    else:
        return {
            'status': 'executed',
            'order_type': order_type,
            'timestamp': datetime.now().isoformat()
        }

def process_pending_orders():
    """Procesa todas las órdenes pendientes"""
    try:
        response = supabase.table('qwen_orders').select('*').eq('status', 'pending').order('priority', desc=True).limit(10).execute()
        orders = response.data
        
        if not orders:
            return 0
        
        print(f"📋 {len(orders)} órdenes pendientes")
        
        for order in orders:
            order_id = order['id']
            
            # Marcar como procesando
            supabase.table('qwen_orders').update({'status': 'processing'}).eq('id', order_id).execute()
            
            try:
                result = execute_order(order)
                
                # Guardar resultado
                supabase.table('qwen_results').insert({
                    'order_id': order_id,
                    'result_type': order['order_type'],
                    'payload': result,
                    'status': 'success'
                }).execute()
                
                # Marcar como completado
                supabase.table('qwen_orders').update({'status': 'completed'}).eq('id', order_id).execute()
                
                print(f"✅ Orden {order_id} completada")
                
                # Notificar por Telegram
                send_telegram(f"✅ Orden ejecutada: {order['order_type']}")
                
            except Exception as e:
                supabase.table('qwen_orders').update({'status': 'failed'}).eq('id', order_id).execute()
                print(f"❌ Orden {order_id} falló: {e}")
        
        return len(orders)
    except Exception as e:
        print(f"Error procesando órdenes: {e}")
        return 0

def main():
    print("🌙 Worker Autónomo v2 - Modo Nocturno")
    # Removido el mensaje de inicio para no hacer spam en caso de crash-loops
    
    last_report = time.time()
    total_processed = 0
    
    while True:
        try:
            processed = process_pending_orders()
            total_processed += processed
            
            # Reporte cada 6 horas
            if time.time() - last_report > 21600:
                send_telegram(f"📊 Reporte Worker: {total_processed} órdenes procesadas en las últimas 6h")
                last_report = time.time()
                total_processed = 0
            
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("Worker detenido")
            break
        except Exception as e:
            print(f"Error en loop: {e}")
            time.sleep(30)

if __name__ == '__main__':
    main()
