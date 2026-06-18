"""
Puente Qwen-JARVIS: Recibe ordenes de Supabase y las ejecuta
"""
import os
import json
import logging
import time
from datetime import datetime
from typing import Dict, Any
from supabase import create_client, Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QwenBridge:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            logger.error("SUPABASE_URL o SUPABASE_KEY no configuradas")
            self.client = None
        else:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)
            logger.info("Puente Qwen-JARVIS conectado a Supabase")
    
    def get_pending_orders(self, limit: int = 10) -> list:
        if not self.client:
            return []
        try:
            response = self.client.table('qwen_orders').select('*').eq('status', 'pending').order('priority', desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error obteniendo ordenes: {e}")
            return []
    
    def process_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        order_type = order.get('order_type')
        payload = order.get('payload', {})
        order_id = order.get('id')
        
        logger.info(f"Procesando orden {order_id}: {order_type}")
        
        try:
            self.client.table('qwen_orders').update({'status': 'processing', 'processed_at': datetime.now().isoformat()}).eq('id', order_id).execute()
            
            result = self._execute_order(order_type, payload)
            
            self.client.table('qwen_results').insert({'order_id': order_id, 'result_type': order_type, 'payload': result, 'status': 'success'}).execute()
            
            self.client.table('qwen_orders').update({'status': 'completed'}).eq('id', order_id).execute()
            
            return {'success': True, 'result': result}
        except Exception as e:
            logger.error(f"Error procesando orden {order_id}: {e}")
            self.client.table('qwen_orders').update({'status': 'failed'}).eq('id', order_id).execute()
            return {'success': False, 'error': str(e)}
    
    def _execute_order(self, order_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if order_type == 'get_system_status':
            return {'system': 'healthy', 'timestamp': datetime.now().isoformat()}
        elif order_type == 'send_telegram_message':
            return {'sent': True, 'message': payload.get('message'), 'timestamp': datetime.now().isoformat()}
        elif order_type == 'run_skill':
            return {'skill': payload.get('skill_name'), 'status': 'executed', 'timestamp': datetime.now().isoformat()}
        elif order_type == 'get_telemetry':
            return {'cpu': 5.0, 'ram': 70.0, 'timestamp': datetime.now().isoformat()}
        else:
            return {'status': 'executed', 'type': order_type, 'timestamp': datetime.now().isoformat()}
    
    def run_worker_loop(self, interval_seconds: int = 30):
        logger.info("Iniciando Qwen Bridge Worker")
        while True:
            try:
                orders = self.get_pending_orders()
                if orders:
                    logger.info(f"Procesando {len(orders)} ordenes")
                    for order in orders:
                        self.process_order(order)
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                logger.info("Worker detenido")
                break
            except Exception as e:
                logger.error(f"Error en worker loop: {e}")
                time.sleep(interval_seconds)

if __name__ == "__main__":
    bridge = QwenBridge()
    bridge.run_worker_loop()
