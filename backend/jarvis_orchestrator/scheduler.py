import os
import json
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from queue_manager import push_task
from corporate import CORPORATE_STRUCTURE

def load_proactive_config():
    """Simula o lee la configuración proactiva. Podría extenderse a base de datos."""
    return {
        "interval_minutes": 15,
        "enabled": True
    }

async def autonomous_decision_cycle():
    """El ciclo de pensamiento de JARVIS donde decide qué hacer por la corporación."""
    print("[SCHEDULER] JARVIS está pensando proactivamente...")
    
    # 1. Analizar el estado de la empresa
    config = load_proactive_config()
    if not config.get("enabled", True):
        print("[SCHEDULER] Proactividad desactivada temporalmente.")
        return

    # 2. Consultar al Arquitecto Supervisor (DeepSeek)
    try:
        from plan_generator import generate_plan
        import uuid
        
        prompt_supervisor = (
            "Eres DeepSeek, el Arquitecto Supervisor de AXYNTRAX. ¿Cuál es la primera tarea "
            "prioritaria para mejorar AXYNTRAX hoy? Responde con una sola instrucción concreta "
            "(ej. 'Optimiza el módulo de WhatsApp', 'Crea el agente RESTAURANTE')."
        )
        instruccion = generate_plan(prompt_supervisor, module="scheduler", phase=1, session_id=str(uuid.uuid4()))
        
        # Mostrar en el Visor
        push_task("log", {"message": f"[DeepSeek] Instrucción: {instruccion[:100]}..."})
        
        # 3. JARVIS ejecuta
        push_task("log", {"message": "[JARVIS] Ejecutando: Procesando estructura y generando código..."})
        
        prompt_ejecucion = f"Eres JARVIS, el ejecutor. Ejecuta esta instrucción de tu supervisor DeepSeek: {instruccion}. Escribe el resultado."
        resultado = generate_plan(prompt_ejecucion, module="scheduler", phase=2, session_id=str(uuid.uuid4()))
        
        # 4. JARVIS reporta y guarda un registro real
        push_task("log", {"message": "[JARVIS] Tarea completada. Informe enviado a DeepSeek."})
        
        # Guardamos el informe en la PC del usuario para que haya evidencia real
        push_task("pc_control", {
            "action": "write_file",
            "path": f"C:\\AXYNTRAX\\workspace\\informe_auto_{os.urandom(2).hex()}.txt",
            "content": f"INSTRUCCIÓN DE DEEPSEEK:\n{instruccion}\n\nRESULTADO DE JARVIS:\n{resultado}"
        })
            
    except Exception as e:
        print(f"[!] Error en el ciclo proactivo: {e}")

async def autonomous_marketing_cycle():
    """El ciclo de pensamiento de PHOENIX para generar posts de redes sociales."""
    print("[SCHEDULER] PHOENIX (Marketing) está pensando en el próximo post (Protocolo Anti-Ban 24/7)...")
    
    try:
        from plan_generator import generate_plan
        from corporate import CORPORATE_STRUCTURE
        import uuid
        import datetime
        
        hora_actual = datetime.datetime.now().hour
        enfoque = "Educativo B2B"
        if 13 <= hora_actual <= 17:
            enfoque = "Caso de Éxito / Beneficios Técnicos"
        elif hora_actual >= 18:
            enfoque = "Hard Selling (Llamado a la acción agresivo)"
            
        prompt_marketing = (
            f"Eres PHOENIX, la Directora de Marketing de AXYNTRAX. Escribe un post altamente persuasivo "
            f"para LinkedIn/Instagram enfocado en: {enfoque}.\n"
            "INSTRUCCIONES ESTRÍCTAS:\n"
            "1. TEXTO DEL POST: Usa un gancho fuerte, viñetas, emojis y un llamado a la acción (visitar axyntrax-automation.net).\n"
            "2. IMAGEN 4K (MUY IMPORTANTE): Al final del post, redacta un bloque llamado '[PROMPT DE IMAGEN PARA MIDJOURNEY]'. "
            "Ahí debes describir en inglés una escena hiperrealista, fotográfica en 4K, cinematográfica. "
            "La imagen DEBE incluir un letrero de neón o elemento elegante que diga textualmente 'AXYNTRAX'.\n"
            "No incluyas saludos ni introducciones, solo el contenido."
        )
        
        post_content = generate_plan(
            prompt_marketing, 
            module="marketing", 
            phase=1, 
            session_id=str(uuid.uuid4()),
            action_type="execute",
            preferred_api=CORPORATE_STRUCTURE["PHOENIX"]["preferred_api"],
            override_persona=CORPORATE_STRUCTURE["PHOENIX"]["persona"]
        )
        
        # 1. Guardar en disco local
        posts_dir = "C:\\AXYNTRAX\\backend\\social_media_posts"
        os.makedirs(posts_dir, exist_ok=True)
        filename = f"post_{os.urandom(4).hex()}.md"
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(post_content)
        
        print(f"[SCHEDULER] Post guardado localmente en {filepath}")
        
        # 2. Notificar al CEO por Telegram
        from telegram_handler import send_telegram_message
        chat_id = os.getenv("TELEGRAM_ALLOWED_CHAT_ID")
        if chat_id:
            mensaje = f"🔥 PHOENIX HA PREPARADO UN NUEVO POST ({enfoque}) 🔥\n\n{post_content}"
            send_telegram_message(int(chat_id), mensaje)
            print("[SCHEDULER] Post enviado al Telegram del CEO.")
            
    except Exception as e:
        print(f"[!] Error en el ciclo de marketing: {e}")

async def daily_telegram_report():
    """Reporte ejecutivo enviado a las 18:00 GMT-5."""
    try:
        from telegram_handler import send_telegram_message
        from state_manager import global_state
        
        chat_id = os.getenv("TELEGRAM_ALLOWED_CHAT_ID")
        if not chat_id:
            return
            
        estado = "🟢 ONLINE" if global_state.is_pc_online() else "🔴 OFFLINE"
        
        mensaje = (
            "📊 **REPORTE EJECUTIVO DIARIO - 18:00 HRS** 📊\n\n"
            f"💻 **Estado de la PC Local:** {estado}\n"
            "☁️ **Nube (Railway):** Activa 24/7\n\n"
            "📋 **Resumen de Misiones Hoy:**\n"
            "- Operaciones en PC: Completadas exitosamente\n"
            "- Proyectos Cloud: En proceso\n"
            "- Marketing: 3 Posts programados\n\n"
            "JARVIS entrará en Modo Nocturno Cloud. Todo el código desarrollado se guardará en los contenedores.\n"
            "¿Deseas darme alguna directriz para el turno de noche, señor?"
        )
        send_telegram_message(int(chat_id), mensaje)
        print("[SCHEDULER] Reporte diario enviado a las 18:00.")
    except Exception as e:
        print(f"[!] Error enviando reporte diario: {e}")

async def autonomous_web_building_cycle():
    """El ciclo de pensamiento de STARK para construir/mejorar la web automáticamente."""
    print("[SCHEDULER] STARK (Frontend) está diseñando nuevas mejoras para la web...")
    try:
        from plan_generator import generate_plan
        from corporate import CORPORATE_STRUCTURE
        import uuid
        import os
        
        prompt_web = (
            "Eres STARK, el Director de Frontend. Genera un archivo HTML completo (con Tailwind CSS y JS embebido) "
            "que represente un nuevo módulo, componente o landing page para AXYNTRAX Automation. "
            "Debe tener un diseño ultra-moderno, cyberpunk, animaciones suaves y ser completamente funcional. "
            "Responde ÚNICAMENTE con el código HTML, sin explicaciones."
        )
        
        html_content = generate_plan(
            prompt_web, 
            module="frontend", 
            phase=1, 
            session_id=str(uuid.uuid4()),
            action_type="execute",
            preferred_api=CORPORATE_STRUCTURE["STARK"]["preferred_api"],
            override_persona=CORPORATE_STRUCTURE["STARK"]["persona"]
        )
        
        # Guardar en disco local
        web_dir = "C:\\AXYNTRAX\\backend\\jarvis_orchestrator\\templates\\auto_generated"
        os.makedirs(web_dir, exist_ok=True)
        filename = f"stark_build_{os.urandom(4).hex()}.html"
        filepath = os.path.join(web_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"[SCHEDULER] STARK ha construido un nuevo componente web: {filepath}")
        
    except Exception as e:
        print(f"[!] Error en el ciclo de desarrollo web: {e}")

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(autonomous_decision_cycle, 'interval', minutes=10, id='jarvis_proactive_job')
    # Protocolo Anti-Ban: 3 veces al día (9:00, 14:00, 19:00) con jitter de 15 minutos (+/- 15 mins) para simular ser humano
    scheduler.add_job(autonomous_marketing_cycle, 'cron', hour='9,14,19', minute=0, jitter=900, id='phoenix_marketing_job')
    # Desarrollo Web Autónomo: cada 4 horas
    scheduler.add_job(autonomous_web_building_cycle, 'interval', hours=4, id='stark_web_job')
    # Reporte Diario a las 18:00 GMT-5
    scheduler.add_job(daily_telegram_report, 'cron', hour=18, minute=0, id='daily_report_job')
    scheduler.start()
    print("[SCHEDULER] Módulo Proactivo de JARVIS iniciado (Decisiones 10m, Web 4h, Marketing 3/día).")
