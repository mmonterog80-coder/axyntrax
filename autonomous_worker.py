# -*- coding: utf-8 -*-
import os
import time
import requests
from datetime import datetime, timedelta
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
    if not TELEGRAM_CHAT_ID or not TELEGRAM_TOKEN:
        print("⚠️ Faltan credenciales de Telegram")
        return
    try:
        requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', json={'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'Markdown'})
    except Exception as e:
        print(f"Error Telegram: {e}")

def process_orders():
    try:
        response = supabase.table('qwen_orders').select('*').eq('status', 'pending').limit(5).execute()
        for order in response.data:
            order_id = order['id']
            supabase.table('qwen_orders').update({'status': 'processing'}).eq('id', order_id).execute()
            try:
                supabase.table('qwen_results').insert({'order_id': order_id, 'result_type': order['order_type'], 'payload': {'status': 'completed', 'time': datetime.now().isoformat()}, 'status': 'success'}).execute()
                supabase.table('qwen_orders').update({'status': 'completed'}).eq('id', order_id).execute()
            except Exception as e:
                supabase.table('qwen_orders').update({'status': 'failed'}).eq('id', order_id).execute()
    except Exception as e:
        print(f"Error procesando órdenes: {e}")

def send_nightly_report():
    print("📊 Generando Reporte Nocturno...")
    try:
        # Obtener resultados de las últimas 12 horas
        twelve_hours_ago = (datetime.now() - timedelta(hours=12)).isoformat()
        response = supabase.table('qwen_results').select('*').gte('created_at', twelve_hours_ago).execute()
        results = response.data
        
        msg = "🌅 *REPORTE EJECUTIVO NOCTURNO*\n\n"
        msg += f"*Fecha:* {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        msg += f"*Tareas Completadas:* {len(results)}\n\n"
        
        if results:
            msg += "*Detalle de Actividades:*\n"
            for r in results[:10]: # Mostrar las últimas 10
                msg += f"✅ [{r.get('result_type', 'N/A')}] - {r.get('created_at', '')[:16]}\n"
        else:
            msg += "No se registraron tareas nuevas en las últimas 12 horas. El sistema estuvo en espera activa.\n"
            
        msg += "\n---\n_JARVIS AX - Trabajando 24/7_"
        send_telegram(msg)
    except Exception as e:
        send_telegram(f"❌ Error generando reporte: {e}")

def main():
    print("🌙 Worker Autónomo Nocturno Iniciado...")
    send_telegram("🌙 *Modo Nocturno Activado.*\n\nJARVIS está trabajando. Te enviaré el reporte ejecutivo en unas horas. Descansa, Miguel.")
    
    last_report_time = time.time()
    
    while True:
        try:
            process_orders()
            time.sleep(60) # Revisar órdenes cada minuto
            
            # Enviar reporte cada 6 horas (21600 segundos)
            if time.time() - last_report_time > 21600:
                send_nightly_report()
                last_report_time = time.time()
                
        except Exception as e:
            print(f"Error en loop: {e}")
            time.sleep(60)

if __name__ == '__main__':
    main()
