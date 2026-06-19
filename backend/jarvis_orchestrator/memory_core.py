import os
import logging
from typing import Dict, Any, List
import uuid

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import VectorParams, Distance, PointStruct
except ImportError:
    QdrantClient = None

class MemoryCore:
    def __init__(self):
        self.qdrant_url = os.environ.get("QDRANT_URL", "http://localhost:6333")
        self.qdrant_api_key = os.environ.get("QDRANT_API_KEY", "")
        self.client = None
        self._init_qdrant()

    def _init_qdrant(self):
        if QdrantClient is None:
            logging.warning("[MemoryCore] qdrant_client no está instalado. Ejecutará modo degradado.")
            return
        try:
            self.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)
            logging.info(f"[MemoryCore] Conectado a Qdrant en {self.qdrant_url}")
        except Exception as e:
            logging.error(f"[MemoryCore] Fallo al conectar con Qdrant: {e}")

    def create_collection_if_not_exists(self, collection_name: str, vector_size: int = 1536):
        if not self.client:
            return
        try:
            collections = self.client.get_collections().collections
            if not any(c.name == collection_name for c in collections):
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
                )
                logging.info(f"[MemoryCore] Colección '{collection_name}' creada en Qdrant.")
        except Exception as e:
            logging.error(f"[MemoryCore] Error creando colección {collection_name}: {e}")

    def store_document(self, collection_name: str, text: str, vector: List[float], payload: Dict[str, Any] = None):
        if not self.client:
            return False
        if payload is None:
            payload = {}
        payload["content"] = text
        
        # Generate a unique integer or UUID string for Qdrant
        doc_id = str(uuid.uuid4())
        
        try:
            self.client.upsert(
                collection_name=collection_name,
                points=[PointStruct(id=doc_id, vector=vector, payload=payload)]
            )
            logging.info(f"[MemoryCore] Chunk guardado en {collection_name}")
            return True
        except Exception as e:
            logging.error(f"[MemoryCore] Error guardando chunk: {e}")
            return False

    def search_similar(self, collection_name: str, query_vector: List[float], limit: int = 5):
        if not self.client:
            return []
        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit
            )
            return results
        except Exception as e:
            logging.error(f"[MemoryCore] Error buscando en Qdrant: {e}")
            return []

# Singleton instance
memory_db = MemoryCore()
