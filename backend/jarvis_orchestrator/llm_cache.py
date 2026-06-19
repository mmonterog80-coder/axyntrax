import time
import hashlib
import logging

logger = logging.getLogger(__name__)

class SimpleTTLCache:
    def __init__(self, ttl_seconds=3600, max_size=1000):
        self.cache = {}
        self.ttl = ttl_seconds
        self.max_size = max_size

    def _get_key(self, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def get(self, text):
        key = self._get_key(text)
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                logger.info("✅ Respondiendo desde caché (Ahorro de tokens)")
                return entry['value']
            else:
                del self.cache[key]
        return None

    def set(self, text, value):
        if len(self.cache) >= self.max_size:
            # Limpiar expirados
            now = time.time()
            self.cache = {k: v for k, v in self.cache.items() if now - v['timestamp'] < self.ttl}
            if len(self.cache) >= self.max_size:
                self.cache.clear() # Limpieza forzada si sigue lleno
        
        key = self._get_key(text)
        self.cache[key] = {'value': value, 'timestamp': time.time()}

# Instancia global de caché compartida (1 hora de TTL)
llm_response_cache = SimpleTTLCache(ttl_seconds=3600, max_size=500)
