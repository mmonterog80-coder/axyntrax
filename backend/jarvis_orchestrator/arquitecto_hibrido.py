import asyncio
import time
import subprocess
import os
import uuid
import json
from plan_generator import generate_plan
from state_manager import global_state

# Backlog Maestro (Fase Ómega)
BACKLOG_MISIONES = [
    {
        "titulo": "Integración Meta Ads Graph API",
        "descripcion": "Instalar facebook-business SDK, generar script base para publicar anuncios, y dejarlo programado localmente.",
        "prioridad": "ALTA",
        "requiere_pc": True
    },
    {
        "titulo": "SaaS Landing Page Generator",
        "descripcion": "Crear una landing page en HTML/JS/CSS moderna para vender servicios de automatización AI.",
        "prioridad": "MEDIA",
        "requiere_pc": False
    }
]

async def bucle_arquitecto_hibrido():
    print("[ARQUITECTO HÍBRIDO] Iniciando el bucle infinito...")
    await asyncio.sleep(10) # Esperar a que todo inicie
    
    while True:
        try:
            pc_online = global_state.is_pc_online()
            
            # Buscar en el backlog
            mision_actual = None
            for idx, m in enumerate(BACKLOG_MISIONES):
                if m["requiere_pc"] and not pc_online:
                    continue # Saltamos esta si requiere PC y no está online
                mision_actual = BACKLOG_MISIONES.pop(idx)
                break
                
            if mision_actual:
                titulo = mision_actual["titulo"]
                desc = mision_actual["descripcion"]
                global_state.set_activity("JARVIS", f"Asignando misión del Backlog: {titulo}")
                prompt_mision = f"Eres JARVIS. Debes cumplir esta misión: {titulo} - {desc}. Dame las instrucciones de terminal necesarias para crearlo (Linux o Windows CMD dependiendo del entorno). Responde en formato JSON estricto: {{\"objetivo\": \"{titulo}\", \"comandos\": [\"cmd1\", \"cmd2\"]}}"
            else:
                global_state.set_activity("ORACLE", "Buscando tendencias para nueva misión...")
                prompt_mision = "Eres ORACLE. Investiga o propón un micro-proyecto técnico útil de OSINT, Scraping o IA. Dame solo las instrucciones de terminal necesarias para crearlo. Responde en formato JSON estricto: {\"objetivo\": \"...\", \"comandos\": [\"cmd1\", \"cmd2\"]}"
            
            respuesta_json = generate_plan(prompt_mision, module="hybrid", phase=1, session_id=str(uuid.uuid4()))
            
            # Limpiar posible markdown
            if "```json" in respuesta_json:
                respuesta_json = respuesta_json.split("```json")[1].split("```")[0].strip()
            elif "```" in respuesta_json:
                respuesta_json = respuesta_json.split("```")[1].strip()
                
            if respuesta_json.startswith("[") and "]:" in respuesta_json[:30]:
                try: respuesta_json = respuesta_json.split("]:", 1)[1].strip()
                except: pass
                
            try:
                mision = json.loads(respuesta_json)
            except Exception as e:
                print(f"[ARQUITECTO HÍBRIDO] Error parseando JSON de misión: {e}")
                await asyncio.sleep(20)
                continue
                
            objetivo = mision.get("objetivo", "Proyecto aleatorio")
            comandos = mision.get("comandos", [])
            
            global_state.set_activity("CYPHER", f"Auditando código de: {objetivo}")
            
            # Validación real de QA
            prompt_qa = f"Eres CYPHER, Director de QA y Ciberseguridad. Analiza estos comandos de terminal generados para la misión '{objetivo}': {comandos}. Responde ÚNICAMENTE con 'SEGURO' si los comandos no son destructivos (no borran archivos importantes, no exponen claves). Responde 'PELIGRO' si detectas comandos maliciosos, rm -rf, del, formato, etc."
            qa_result = generate_plan(prompt_qa, module="hybrid_qa", phase=2, session_id=str(uuid.uuid4()))
            
            if "PELIGRO" in qa_result.upper():
                print(f"[CYPHER BLOCK] Comandos destructivos detectados para: {objetivo}. Misión abortada.")
                await asyncio.sleep(60)
                continue
                
            global_state.set_activity("VIERNES" if pc_online else "STARK", f"Ejecutando: {objetivo}")
            
            # Crear directorio de workspace en la nube si no existe
            workspace_dir = "/app/workspace"
            if not os.path.exists(workspace_dir):
                try: os.makedirs(workspace_dir)
                except: workspace_dir = "/tmp/workspace"; os.makedirs(workspace_dir, exist_ok=True)
            
            # 2. Ejecutar comandos
            for cmd in comandos:
                if global_state.is_pc_online():
                    # MODO EDGE (PC Encendida)
                    print(f"[EDGE] Enviando comando a PC local: {cmd}")
                    global_state.push_edge_command({"id": str(uuid.uuid4()), "orden": "comando_cmd", "cmd": cmd})
                    
                    # Esperar respuesta de la PC local
                    espera = 0
                    while espera < 60:
                        resp = global_state.get_latest_edge_response()
                        if resp:
                            print(f"[EDGE] Respuesta recibida:\n{resp}")
                            break
                        await asyncio.sleep(2)
                        espera += 2
                else:
                    # MODO CLOUD (PC Apagada)
                    print(f"[CLOUD] Ejecutando localmente en contenedor Linux: {cmd}")
                    try:
                        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=workspace_dir)
                        if res.returncode != 0:
                            print(f"[CLOUD QA FAILURE] Error en comando: {res.stderr}")
                            # TODO: Aquí entraría el bucle de auto-corrección (QA) enviando res.stderr de vuelta a DeepSeek
                    except Exception as e:
                        print(f"[CLOUD] Error al ejecutar: {e}")
                        
                await asyncio.sleep(3)
                
            global_state.set_activity("JARVIS", "Misión completada. Modo Reposo.")
            
        except Exception as e:
            print(f"[ARQUITECTO HÍBRIDO] Error fatal en bucle: {e}")
            
        # Esperar 5 minutos antes del siguiente proyecto autónomo
        await asyncio.sleep(300)

def iniciar_arquitecto_bg():
    loop = asyncio.get_event_loop()
    loop.create_task(bucle_arquitecto_hibrido())
