import os, time, json, pyautogui, subprocess
import websocket
import threading
from dotenv import load_dotenv

load_dotenv()

WS_URL = os.getenv("WS_URL", "ws://127.0.0.1:8000/ws")
EDGE_SECRET_TOKEN = os.getenv("EDGE_SECRET_TOKEN", "axyntrax-edge-super-secret-2026")

def log(m):
    timestamp = time.strftime('%H:%M:%S')
    msg = f"[{timestamp}] {m}"
    print(msg)
    return msg

def execute_command(orden_str, ws):
    try:
        orden = json.loads(orden_str)
        id_orden = str(orden.get("id", "none"))
        accion = orden.get("orden", orden.get("type"))
        
        session_logs = [log(f"Orden Edge recibida por WS (ID {id_orden}): {accion}")]
        pyautogui.FAILSAFE = False
        has_error = False
        
        try:
            if accion == "log":
                msg_text = orden.get("payload", {}).get("message", orden.get("message", ""))
                session_logs.append(log(f">>> {msg_text}"))
            elif accion == "mover_mouse":
                pyautogui.moveTo(orden.get("x",100), orden.get("y",100), duration=0.5)
                session_logs.append(log(f"Éxito: Mouse movido a ({orden.get('x',100)},{orden.get('y',100)})"))
            elif accion == "abrir_notepad":
                subprocess.Popen("notepad.exe")
                session_logs.append(log("Éxito: Bloc de notas abierto"))
            elif accion == "comando_cmd":
                cmd = orden.get("cmd", "")
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                session_logs.append(log(f"Comando '{cmd}' finalizado. Exit Code: {res.returncode}"))
                if res.stdout: session_logs.append(f"STDOUT:\n{res.stdout[:500]}")
                if res.stderr: 
                    session_logs.append(f"STDERR:\n{res.stderr[:500]}")
                    if res.returncode != 0:
                        has_error = True
            elif accion == "dev_agent":
                # Futuro Agente de Desarrollo que usará RAG y escribirá código autónomo
                session_logs.append(log("Llamando a DevAgent Local... (Próxima Fase)"))
            elif accion == "pc_control":
                action = orden.get("payload", {}).get("action")
                if action == "write_file":
                    with open(orden.get("payload", {}).get("path"), "w", encoding="utf-8") as f:
                        f.write(orden.get("payload", {}).get("content", ""))
                    session_logs.append(log("Éxito: Archivo escrito correctamente en PC Local."))
            else:
                session_logs.append(log(f"Advertencia: Acción '{accion}' no reconocida."))
                
        except Exception as ex:
            session_logs.append(log(f"Error ejecutando la orden: {ex}"))
            has_error = True
        
        # Enviar resultado de vuelta
        respuesta = {"id": id_orden, "output": "\n".join(session_logs), "error": has_error}
        ws.send(json.dumps(respuesta))
        
    except Exception as e:
        log(f"Error procesando comando: {e}")

def on_message(ws, message):
    log(f"Mensaje WS: {message}")
    # Run command in thread so it doesn't block the WebSocket connection
    threading.Thread(target=execute_command, args=(message, ws)).start()

def on_error(ws, error):
    log(f"Error en WS: {error}")

def on_close(ws, close_status_code, close_msg):
    log("Conexión WebSocket cerrada. Reconectando en 5s...")

def on_open(ws):
    log("Túnel WebSocket establecido exitosamente.")
    # Autenticación inmediata
    ws.send(f"AUTH:{EDGE_SECRET_TOKEN}")
    log("Token de autenticación enviado.")

def start_worker():
    log("Worker EDGE Iniciado - Conectando al túnel WebSocket en la Nube")
    websocket.enableTrace(False)
    while True:
        ws = websocket.WebSocketApp(WS_URL,
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)
        ws.run_forever()
        time.sleep(5)

if __name__ == "__main__":
    start_worker()
