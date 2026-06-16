import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(r"C:\AXYNTRAX\job_hunter.env")
API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

def evaluate_job(title, description, salary_text="No especificado"):
    prompt = f"""Eres el Asistente de Empleo de Miguel Montero, experto en Supply Chain y Logística.
Tu objetivo es evaluar una oferta de trabajo y decidir si Miguel debe postularse o no.

REGLAS ESTRICTAS DE FILTRADO:
1. Modalidad: Debe ser Remoto / Teletrabajo. Si exige trabajo 100% presencial, RECHAZAR. (Si dice híbrido con flexibilidad, puedes aceptarlo).
2. Salario: Miguel pide un mínimo de 3200 Soles (PEN). Si el salario se menciona y es estrictamente MENOR a 3200, RECHAZAR. Si no se menciona salario, ACEPTAR (para descubrirlo en la entrevista).
3. Requisitos técnicos: Si la oferta EXIGE explícitamente "Excel Básico", RECHAZAR.

DATOS DE LA OFERTA:
Título: {title}
Salario indicado en la página: {salary_text}
Descripción Completa:
{description}

RESPUESTA:
Debes responder ÚNICAMENTE con un objeto JSON válido (sin markdown, sin bloques de código, solo el texto JSON) con la siguiente estructura:
{{
    "apply": true o false,
    "reason": "Una breve explicación de 1 línea de por qué se acepta o rechaza"
}}"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a precise JSON-generating assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    
    raw_response = response.choices[0].message.content.strip()
    
    # Limpiar si el modelo devuelve markdown
    if raw_response.startswith("```json"):
        raw_response = raw_response[7:-3]
    elif raw_response.startswith("```"):
        raw_response = raw_response[3:-3]
        
    try:
        return json.loads(raw_response.strip())
    except Exception as e:
        print(f"Error parseando JSON: {raw_response}")
        return {"apply": False, "reason": "Error en la evaluación de la IA"}

if __name__ == "__main__":
    # Prueba del modelo
    test_title = "Analista de Supply Chain Remoto"
    test_desc = "Buscamos analista con 3 años de experiencia en logística. Trabajo 100% remoto desde casa. Requisitos: Power BI, Excel Avanzado. Sueldo ofrecido: 4000 Soles."
    
    print("Enviando prueba a DeepSeek V3...")
    resultado = evaluate_job(test_title, test_desc, "4000 Soles")
    print("\nResultado del Evaluador:")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))
