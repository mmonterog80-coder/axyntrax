import sqlite3
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

DB_PATH = "checkpoints.sqlite"

def init_db():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pipeline_checkpoints (
                    task_id TEXT PRIMARY KEY,
                    state_data TEXT NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    except Exception as e:
        logger.error(f"Error inicializando checkpoints DB: {e}")

def save_checkpoint(task_id: str, state_data: dict):
    """Guarda el estado actual del pipeline para no perder progreso (Paso 8 - Master Plan)."""
    init_db()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            json_data = json.dumps(state_data)
            now = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO pipeline_checkpoints (task_id, state_data, last_updated)
                VALUES (?, ?, ?)
                ON CONFLICT(task_id) DO UPDATE SET
                    state_data=excluded.state_data,
                    last_updated=excluded.last_updated
            ''', (task_id, json_data, now))
            conn.commit()
            logger.info(f"Checkpoint guardado: {task_id}")
    except Exception as e:
        logger.error(f"Error guardando checkpoint: {e}")

def load_checkpoint(task_id: str) -> dict:
    """Recupera el estado de una tarea pausada o caída por tokens."""
    init_db()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT state_data FROM pipeline_checkpoints WHERE task_id=?", (task_id,))
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
    except Exception as e:
        logger.error(f"Error cargando checkpoint: {e}")
    return {}
