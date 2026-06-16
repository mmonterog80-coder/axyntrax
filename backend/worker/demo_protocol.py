import sys
import os
import uuid
import time
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"C:\AXYNTRAX\.env")

sys.path.append(os.path.abspath(r"C:\AXYNTRAX\backend\jarvis_orchestrator"))
try:
    from plan_generator import generate_plan
except ImportError:
    print("Error importando plan_generator")
    sys.exit(1)

LOG_FILE = r"C:\AXYNTRAX\logs\worker.log"
def log_msg(msg):
    print(msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")
    except:
        pass

def demo():
    log_msg("[SISTEMA] Activando Protocolo COORDINACIÓN OFICIAL CON DEEPSEEK...")
    time.sleep(1)
    
    prompt_supervisor = "Eres DeepSeek, el Arquitecto Supervisor de AXYNTRAX. ¿Cuál es la primera tarea prioritaria para mejorar AXYNTRAX hoy? Responde con una sola instrucción concreta, breve y directa (ej. 'Crea la estructura del agente RESTAURANTE')."
    instruccion = generate_plan(prompt_supervisor, module="scheduler", phase=1, session_id=str(uuid.uuid4()))
    
    log_msg(f"[DeepSeek] Instrucción: {instruccion[:150].strip()}...")
    time.sleep(1)
    
    log_msg("[JARVIS] Ejecutando: Procesando estructura y generando código según directiva de DeepSeek...")
    
    prompt_ejecucion = f"Eres JARVIS, el ejecutor. DeepSeek ordenó: '{instruccion}'. Ejecútalo y redacta el informe o código resultante."
    resultado = generate_plan(prompt_ejecucion, module="scheduler", phase=2, session_id=str(uuid.uuid4()))
    time.sleep(1)
    
    log_msg("[JARVIS] Tarea completada. Informe enviado a DeepSeek.")
    
    path = f"C:\\AXYNTRAX\\workspace\\informe_auto_{os.urandom(2).hex()}.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"INSTRUCCIÓN DE DEEPSEEK:\n{instruccion}\n\nRESULTADO DE JARVIS:\n{resultado}")
    log_msg(f"[JARVIS] Evidencia física generada en: {path}")

if __name__ == "__main__":
    demo()
