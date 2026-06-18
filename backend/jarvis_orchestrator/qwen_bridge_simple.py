import os
import httpx
from supabase import create_client, Client
from datetime import datetime

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración de Qwen (ajusta según tu proveedor)
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_API_URL = os.getenv("QWEN_API_URL", "https://api.openai.com/v1/chat/completions")  # Compatible con OpenAI

async def ask_qwen(prompt: str, user_id: str = "anonymous") -> str:
    """Envía un prompt a Qwen y guarda el historial en Supabase."""
    headers = {"Authorization": f"Bearer {QWEN_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "qwen-turbo", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(QWEN_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            ai_response = data['choices'][0]['message']['content']
            supabase.table("chat_history").insert({
                "user_id": user_id,
                "prompt": prompt,
                "response": ai_response,
                "created_at": datetime.utcnow().isoformat()
            }).execute()
            return ai_response
    except Exception as e:
        print(f"Error conectando con Qwen: {e}")
        return "Lo siento, estoy experimentando problemas técnicos en este momento."
