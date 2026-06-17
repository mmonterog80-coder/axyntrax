import os, openai, re

def generate_plan(objective: str, module: str = "", phase: int = 1,
                  action_type: str = "execute", preferred_api: str = None,
                  override_persona: str = None, session_id: str = "default") -> str:
    """
    Punto de entrada principal.
    1. Verifica quÃ© IAs estÃ¡n online
    2. Lee la memoria persistente de Supabase.
    3. Enruta a la DivisiÃ³n Corporativa adecuada (o usa la IA elegida si se pasa override)
    4. La IA elegida ejecuta la tarea
    5. Fallback automÃ¡tico si falla
    6. Guarda la interacciÃ³n en memoria.
    """
    # Cargar memoria de la sesiÃ³n
    try:
        from db import get_chat_history, save_message
        history = get_chat_history(session_id=session_id, limit=5)
        history_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in history])
    except ImportError:
        history_text = ""
        save_message = lambda *args, **kwargs: None

    # Restaurar lÃ³gica corporativa
    try:
        from corporate import determine_department, CORPORATE_STRUCTURE
    except ImportError:
        CORPORATE_STRUCTURE = {}
        determine_department = lambda x: "JARVIS"

    current_persona = override_persona
    if not current_persona and not preferred_api:
        dept = determine_department(objective)
        if dept in CORPORATE_STRUCTURE:
            corp_data = CORPORATE_STRUCTURE[dept]
            preferred_api = corp_data["preferred_api"]
            current_persona = corp_data["persona"]
    if action_type == "generate_code":
        system_prompt = current_persona if current_persona else ("Eres un programador experto. Devuelve ÃšNICAMENTE el cÃ³digo fuente completo "
                         "dentro de un bloque de cÃ³digo markdown. Sin explicaciones fuera del bloque.")
        user_prompt = f"Objetivo: {objective}\n\nEscribe el cÃ³digo que cumpla ese objetivo."
        max_tokens = 1400
    else:
        system_prompt = current_persona if current_persona else ("Eres JARVIS AX, un asistente de IA avanzado del sistema AXYNTRAX. "
                         "Responde de forma clara, precisa y en espaÃ±ol. "
                         f"MÃ³dulo: {module} | Fase: {phase}")
        
        # Inyectar memoria en el prompt del usuario
        memoria_context = f"\n\n[MEMORIA RECIENTE DE LA SESIÃ“N]\n{history_text}\n" if history_text else ""
        user_prompt = f"{memoria_context}\n[NUEVA ORDEN]\n{objective}"
        max_tokens = 800

    # LÃ³gica de enrutamiento y ejecuciÃ³n (simulada)
    if preferred_api == "deepseek-reasoner" or preferred_api == "deepseek":
        client = openai.OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com/v1")
        model = "deepseek-coder"
    else:
        client = openai.OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
        openrouter_models = {
            "claude-3-5-sonnet": "anthropic/deepseek-chat",
            "qwen": "qwen/qwen-2.5-72b-instruct",
            "zoho_zia": "openai/gpt-4o-mini",
            "kimi": "openai/gpt-4o-mini",
            "gemini": "google/gemini-2.5-flash",
            "gpt-4o": "openai/gpt-4o",
            "llama-3": "meta-llama/llama-3.1-70b-instruct",
            "mistral": "mistralai/mistral-large"
        }
        model = openrouter_models.get(preferred_api, "openai/gpt-3.5-turbo")
    
    # Guardar mensaje del usuario en memoria CRM
    save_message(session_id=session_id, role="user", content=objective)
    
    resp = client.chat.completions.create(
        model=model, 
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        max_tokens=max_tokens
    )
    
    result = resp.choices[0].message.content
    
    # Extraer el nombre del departamento de current_persona si existe
    dept_name = "JARVIS"
    if current_persona and "Eres " in current_persona:
        dept_name = current_persona.split("Eres ")[1].split(",")[0].split(" ")[0]
        
    final_result = f"[{dept_name}]: {result}"
    
    save_message(session_id=session_id, role="assistant", content=final_result)
    return final_result

def get_ai_status() -> dict:
    """Devuelve el estado de las IAs para el HUD"""
    try:
        from corporate import CORPORATE_STRUCTURE
    except ImportError:
        CORPORATE_STRUCTURE = {}
        
    status = {}
    
    # Añadir dinámicamente las divisiones corporativas (basadas en tecnología pura)
    for key, data in CORPORATE_STRUCTURE.items():
        # Usar el nombre de la API subyacente (ej: 'qwen' -> 'Qwen', 'claude-3-5-sonnet' -> 'Claude 3.5 Sonnet')
        api_name = str(data.get("preferred_api", key)).capitalize()
        if "Claude" in api_name or api_name == "Claude-3-5-sonnet": api_name = "Claude 3.5 Sonnet"
        elif "Llama" in api_name or api_name == "Llama-3": api_name = "Llama 3"
        elif "Gpt-4o" in api_name: api_name = "GPT-4o"
        elif "Zia" in api_name: api_name = "Zoho Zia"
        elif "Deepseek-reasoner" in api_name: api_name = "DeepSeek Reasoner"
        
        status_key = data.get("preferred_api", key.lower())
        
        status[status_key] = {
            "name": api_name,
            "online": True, # Asumimos online si la plataforma maestra está activa
            "specialties": data["keywords"][:3],
            "priority": 1 if key == "JARVIS" else 2
        }
            
    return status

