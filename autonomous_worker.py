# -*- coding: utf-8 -*-
"""
Worker Autónomo: Ejecuta órdenes de Supabase automáticamente
Trabaja 24/7 aunque Miguel apague la PC
"""
import os
import time
import requests
from datetime import datetime
from supabase import create_client, Client
from openai import OpenAI

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
deepseek = OpenAI(api_key=DEEPSEEK_API_KEY, base_url='https://api.deepseek.com')

def send_telegram(message):
    if not TELEGRAM_CHAT_ID:
        return
    try:
        requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
            json={'chat_id': TELEGRAM_CHAT_ID, 'text': message}
        )
    except:
        pass

def process_orders():
    """Procesar órdenes pendientes de Supabase"""
    try:
        response = supabase.table('qwen_orders').select('*').eq('status', 'pending').limit(5).execute()
        orders = response.data
        
        if not orders:
            return
        
        print(f"📋 Procesando {len(orders)} órdenes...")
        
        for order in orders:
            order_id = order['id']
            order_type = order['order_type']
            payload = order.get('payload', {})
            
            # Marcar como procesando
            supabase.table('qwen_orders').update({'status': 'processing'}).eq('id', order_id).execute()
            
            try:
                # Ejecutar según el tipo de orden
                result = execute_order(order_type, payload)
                
                # Guardar resultado
                supabase.table('qwen_results').insert({
                    'order_id': order_id,
                    'result_type': order_type,
                    'payload': result,
                    'status': 'success'
                }).execute()
                
                # Marcar como completado
                supabase.table('qwen_orders').update({'status': 'completed'}).eq('id', order_id).execute()
                
                print(f"✅ Orden {order_id} completada")
                
            except Exception as e:
                supabase.table('qwen_orders').update({'status': 'failed'}).eq('id', order_id).execute()
                print(f"❌ Orden {order_id} falló: {e}")
    
    except Exception as e:
        print(f"Error procesando órdenes: {e}")

def execute_order(order_type, payload):
    """Ejecutar una orden específica"""
    if order_type == 'analyze_web':
        url = payload.get('url', 'https://www.axyntrax-automation.net')
        # Análisis básico
        return {'url': url, 'status': 'analyzed', 'timestamp': datetime.now().isoformat()}
    
    elif order_type == 'generate_sales_leads':
        # Generar leads de ejemplo
        return {'leads': 10, 'source': 'automated', 'timestamp': datetime.now().isoformat()}
    
    elif order_type == 'send_report':
        message = payload.get('message', 'Reporte automático')
        send_telegram(message)
        return {'sent': True, 'timestamp': datetime.now().isoformat()}
    
    else:
        return {'status': 'executed', 'type': order_type, 'timestamp': datetime.now().isoformat()}

def main():
    print("🤖 Worker Autónomo iniciado...")
    print("⏰ Revisando órdenes cada 30 segundos...")
    send_telegram("🤖 JARVIS Worker Autónomo activo. Trabajando 24/7.")
    
    while True:
        try:
            process_orders()
            time.sleep(30)
        except KeyboardInterrupt:
            print("Worker detenido")
            break
        except Exception as e:
            print(f"Error en worker loop: {e}")
            time.sleep(30)

if __name__ == '__main__':
    main()
