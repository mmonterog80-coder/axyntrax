import os
import openai

def _get_client(api_key, base_url):
    return openai.OpenAI(api_key=api_key, base_url=base_url)

def _get_deepseek_client():
    return _get_client(os.getenv("DEEPSEEK_API_KEY"), "https://api.deepseek.com/v1")

def _get_kimi_client():
    return _get_client(os.getenv("KIMI_API_KEY"), "https://api.moonshot.cn/v1")

def _get_qwen_client():
    return _get_client(os.getenv("DASHSCOPE_API_KEY"), "https://dashscope.aliyuncs.com/compatible-mode/v1")

def _get_zia_client():
    return _get_client(os.getenv("ZIA_API_KEY"), os.getenv("ZIA_BASE_URL", "https://api.zia.ai/v1"))

def _get_openrouter_client():
    return _get_client(os.getenv("OPENROUTER_API_KEY"), "https://openrouter.ai/api/v1")

def _generate(client, model, system_prompt, user_prompt, max_tokens=1000, temperature=0.3):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# ========== PLANES POR TIPO DE TAREA ==========

def generate_plan_deepseek(objective, module, phase, action_type):
    model = os.getenv("DEEPSEEK_PRO_MODEL", "deepseek-coder")
    client = _get_deepseek_client()
    if action_type == "generate_code":
        system_prompt = "Eres un programador experto en C++. Devuelve ÚNICAMENTE el código fuente completo dentro de un bloque de código markdown (```cpp ... ```). No incluyas explicaciones ni comentarios fuera del bloque."
        user_prompt = f"Objetivo: {objective}\n\nEscribe el código C++ completo que cumpla ese objetivo."
        max_tokens = 1200
    else:
        system_prompt = "Eres un arquitecto de software. Diseña un plan detallado de implementación en español."
        user_prompt = f"Objetivo: {objective}\nMódulo: {module}\nFase: {phase}\nDevuelve una lista numerada de pasos."
        max_tokens = 600
    return _generate(client, model, system_prompt, user_prompt, max_tokens=max_tokens)

def generate_plan_kimi(objective, module, phase, action_type):
    model = os.getenv("KIMI_MODEL", "moonshot-v1-8k")
    client = _get_kimi_client()
    if action_type == "generate_code":
        system_prompt = "Eres un programador experto. Devuelve ÚNICAMENTE el código fuente completo dentro de un bloque de código markdown. Sin explicaciones."
        user_prompt = f"Objetivo: {objective}\n\nEscribe el código que cumpla ese objetivo."
        max_tokens = 1000
    else:
        system_prompt = "Eres un asistente de ingeniería eficiente. Genera un plan de ejecución breve."
        user_prompt = f"Objetivo: {objective}\nMódulo: {module}\nFase: {phase}\nResponde con pasos numerados."
        max_tokens = 300
    return _generate(client, model, system_prompt, user_prompt, max_tokens=max_tokens)

def generate_plan_qwen(objective, module, phase, action_type):
    model = os.getenv("QWEN_MODEL", "qwen3-max")
    client = _get_qwen_client()
    if action_type == "generate_code":
        system_prompt = "Eres un programador experto. Devuelve ÚNICAMENTE el código fuente completo dentro de un bloque de código markdown. Sin explicaciones."
        user_prompt = f"Objetivo: {objective}\n\nEscribe el código que cumpla ese objetivo."
        max_tokens = 1000
    else:
        system_prompt = "Eres un asistente eficiente. Convierte este objetivo en pasos breves."
        user_prompt = f"Objetivo: {objective}\nMódulo: {module}\nFase: {phase}\nSolo responde con la lista numerada."
        max_tokens = 300
    return _generate(client, model, system_prompt, user_prompt, max_tokens=max_tokens)

def generate_plan_zia(objective, module, phase, action_type):
    model = os.getenv("ZIA_MODEL", "zia-model")
    client = _get_zia_client()
    if action_type == "generate_code":
        system_prompt = "Eres un programador experto. Devuelve ÚNICAMENTE el código fuente completo dentro de un bloque de código markdown. Sin explicaciones."
        user_prompt = f"Objetivo: {objective}\n\nEscribe el código que cumpla ese objetivo."
        max_tokens = 1000
    else:
        system_prompt = "Eres un ingeniero de software. Genera un plan de ejecución."
        user_prompt = f"Objetivo: {objective}\nMódulo: {module}\nFase: {phase}"
        max_tokens = 400
    return _generate(client, model, system_prompt, user_prompt, max_tokens=max_tokens)

def generate_plan_openrouter(objective, module, phase, action_type, provider="yi"):
    client = _get_openrouter_client()
    if provider == "yi":
        model = os.getenv("OPENROUTER_YI_MODEL", "yi-34b-chat")
    elif provider == "baidu":
        model = os.getenv("OPENROUTER_BAIDU_MODEL", "baidu/ernie-4.0")
    else:
        model = "openai/gpt-3.5-turbo"
    if action_type == "generate_code":
        system_prompt = "Eres un programador experto. Devuelve ÚNICAMENTE el código fuente completo dentro de un bloque de código markdown. Sin explicaciones."
        user_prompt = f"Objetivo: {objective}\n\nEscribe el código que cumpla ese objetivo."
        max_tokens = 1000
    else:
        system_prompt = "Eres un asistente de ingeniería. Genera un plan de ejecución detallado."
        user_prompt = f"Objetivo: {objective}\nMódulo: {module}\nFase: {phase}"
        max_tokens = 500
    return _generate(client, model, system_prompt, user_prompt, max_tokens=max_tokens)

# ========== ORQUESTADOR DE MODELOS ==========
def generate_plan(objective, module, phase, action_type="execute", preferred_api=None):
    if preferred_api:
        api = preferred_api
    elif action_type in ("generate_code", "architect"):
        api = "deepseek"
    elif action_type == "fix_error":
        api = "kimi"
    elif action_type == "creative":
        api = "zia"
    else:
        api = "qwen"

    if api == "deepseek":
        return generate_plan_deepseek(objective, module, phase, action_type)
    elif api == "kimi":
        return generate_plan_kimi(objective, module, phase, action_type)
    elif api == "qwen":
        return generate_plan_qwen(objective, module, phase, action_type)
    elif api == "zia":
        result = generate_plan_zia(objective, module, phase, action_type)
        if result.startswith("Error"):
            return generate_plan_openrouter(objective, module, phase, action_type, "yi")
        return result
    elif api == "openrouter":
        return generate_plan_openrouter(objective, module, phase, action_type, "yi")
    else:
        return generate_plan_qwen(objective, module, phase, action_type)
