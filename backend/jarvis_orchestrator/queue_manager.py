import os
import json

def push_task(task_type: str, payload: dict, queue_name: str = "axyntrax_tasks"):
    """
    Encola una tarea en memoria para que el worker local la consulte via HTTP.
    """
    try:
        from tasks import memory_queue
        task_data = {
            "type": task_type,
            "payload": payload
        }
        memory_queue.append(task_data)
        print(f"[+] Tarea '{task_type}' encolada en memoria RAM.")
        return True
    except Exception as e:
        print(f"[!] Error al encolar en RAM: {e}")
        return False

def pop_task(queue_name: str = "axyntrax_tasks", timeout: int = 5):
    """
    Saca una tarea de la memoria. (Uso interno).
    """
    try:
        from tasks import memory_queue
        if memory_queue:
            return memory_queue.pop(0)
        return None
    except Exception as e:
        print(f"[!] Error leyendo RAM: {e}")
        return None
