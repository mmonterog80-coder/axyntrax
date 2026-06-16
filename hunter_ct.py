import asyncio
import os
import json
import sqlite3
import datetime
from dotenv import load_dotenv
from openai import OpenAI
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

load_dotenv(r"C:\AXYNTRAX\job_hunter.env")
API_KEY = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

STATE_FILE = r"C:\AXYNTRAX\computrabajo_state.json"
CV_PATH = r"C:\Users\YARVIS\Desktop\certificados\CV_MIGUEL_MONTERO_CLEAN.pdf"
DB_PATH = r"C:\AXYNTRAX\postulaciones.db"

with open(r"C:\AXYNTRAX\cv_text.txt", "r", encoding="utf-8") as f:
    CV_TEXT = f.read()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS postulaciones
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  fecha TEXT,
                  portal TEXT,
                  titulo TEXT,
                  empresa TEXT,
                  enlace TEXT,
                  estado TEXT)''')
    conn.commit()
    conn.close()

def log_postulacion(portal, titulo, empresa, enlace, estado):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO postulaciones (fecha, portal, titulo, empresa, enlace, estado) VALUES (?, ?, ?, ?, ?, ?)",
              (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), portal, titulo, empresa, enlace, estado))
    conn.commit()
    conn.close()

def evaluar_oferta(title, description, empresa=""):
    prompt = f"""Eres el Asistente de Empleo de Miguel Montero, experto en Supply Chain y Logística.
Reglas ESTRICTAS de filtrado:
1. Modalidad: Debe ser Remoto / Teletrabajo. Si exige presencial o híbrido, RECHAZAR.
2. Salario: Mínimo 3200 PEN. Si es MENOR, RECHAZAR. Si no dice, ACEPTAR para negociar.
3. Requisitos técnicos: Si exige explícitamente "Excel Básico", RECHAZAR.
4. Tipo de Empresa: Solo empresas importantes, formales y corporativas.
5. EXCLUIR canales de ventas: RECHAZAR cualquier oferta que sea para call center, canales de venta, vendedores, o empresas de telecomunicaciones como Claro, Entel, Movistar, Bitel o similares.
6. Calidad del Empleo: Solo trabajos profesionales, con contrato laboral formal.

Empresa: {empresa}
Oferta: {title}
Descripción: {description}

Responde SÓLO con JSON: {{"apply": true/false, "reason": "..."}}"""
    try:
        res = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        ).choices[0].message.content.strip()
        if res.startswith("```json"): res = res[7:-3]
        elif res.startswith("```"): res = res[3:-3]
        return json.loads(res.strip())
    except Exception as e:
        print("Error en evaluación IA:", e)
        return {"apply": False, "reason": "Error IA"}

def responder_formulario(preguntas):
    prompt = f"""Eres Miguel Montero respondiendo preguntas de un formulario de empleo.
Basado estrictamente en este CV:
{CV_TEXT}

Preguntas del formulario:
{json.dumps(preguntas, indent=2, ensure_ascii=False)}

Responde SÓLO un objeto JSON donde la clave es el 'id' de la pregunta y el valor es la respuesta en texto corto.
Ejemplo: {{"preg_1": "3 años", "preg_2": "Sí, disponibilidad inmediata"}}"""
    try:
        res = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        ).choices[0].message.content.strip()
        if res.startswith("```json"): res = res[7:-3]
        elif res.startswith("```"): res = res[3:-3]
        return json.loads(res.strip())
    except:
        return {}

async def procesar_formulario_postulacion(page):
    try:
        print("Buscando preguntas adicionales...")
        await page.wait_for_timeout(2000)
        preguntas = []
        labels = await page.query_selector_all("label")
        inputs = await page.query_selector_all("input[type='text'], input[type='number'], textarea")
        
        # Simulación simplificada: si hay textareas o inputs requeridos
        for i, el in enumerate(inputs):
            id_val = await el.get_attribute("id") or f"input_{i}"
            placeholder = await el.get_attribute("placeholder") or ""
            preguntas.append({"id": id_val, "contexto": placeholder})
            
        if preguntas:
            print("Preguntas detectadas, pidiendo a DeepSeek que las responda basado en el CV...")
            respuestas = responder_formulario(preguntas)
            for id_val, respuesta in respuestas.items():
                try:
                    await page.fill(f"[id='{id_val}']", str(respuesta))
                except:
                    pass
                    
        # Buscar botón para adjuntar CV si existe
        file_input = await page.query_selector("input[type='file']")
        if file_input:
            print("Adjuntando CV actualizado...")
            await file_input.set_input_files(CV_PATH)
            
        # Enviar postulación
        btn_submit = await page.query_selector("button:has-text('Enviar'), button:has-text('Postularme'), a#build-btn")
        if btn_submit:
            print("Enviando postulación final...")
            await btn_submit.click()
            await page.wait_for_timeout(3000)
            return True
        return False
    except Exception as e:
        print(f"Error procesando formulario: {e}")
        return False

async def hunter():
    init_db()
    print("Iniciando AXYNTRAX Job Hunter (Computrabajo)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50, channel="chrome")
        context = await browser.new_context(storage_state=STATE_FILE, viewport={"width": 1280, "height": 720})
        page = await context.new_page()
        stealth = Stealth()
        await stealth.apply_stealth_async(page)
        
        print("Buscando ofertas...")
        await page.goto("https://pe.computrabajo.com/trabajo-de-supply-chain?q=supply%20chain")
        await page.wait_for_timeout(5000)
        
        links = await page.query_selector_all("a.js-o-link")
        urls = []
        for link in links[:3]: # Solo 3 para la prueba inicial
            href = await link.get_attribute("href")
            if href: urls.append(f"https://pe.computrabajo.com{href}")
            
        print(f"Se encontraron {len(urls)} ofertas. Iniciando evaluación...")
        
        for url in urls:
            print(f"\nAnalizando: {url}")
            await page.goto(url)
            await page.wait_for_timeout(3000)
            
            try:
                title_el = await page.query_selector("h1")
                title = await title_el.inner_text() if title_el else "Desconocido"
                
                empresa_el = await page.query_selector("p.fs16, a.fs16")
                empresa = await empresa_el.inner_text() if empresa_el else "Desconocida"
                
                desc_el = await page.query_selector(".fs16.t_word_wrap, .box_detail, article")
                description = await desc_el.inner_text() if desc_el else ""
                
                if not description: continue
                
                print(f"Consultando a DeepSeek para: '{title}' en '{empresa}'...")
                evaluacion = evaluar_oferta(title, description, empresa)
                
                if evaluacion.get("apply"):
                    print(f"✅ DeepSeek APROBÓ: {evaluacion.get('reason')}")
                    # Buscar botón de postular
                    btn_postular = await page.query_selector("a:has-text('Postularme'), button#btn-apply")
                    if btn_postular:
                        await btn_postular.click()
                        print("Entrando al formulario de postulación...")
                        exito = await procesar_formulario_postulacion(page)
                        if exito:
                            log_postulacion("Computrabajo", title, "Confidencial", url, "Postulado (Automático)")
                            print("¡Postulación completada!")
                        else:
                            log_postulacion("Computrabajo", title, "Confidencial", url, "Error en Formulario")
                    else:
                        print("Ya estabas postulado o botón no encontrado.")
                        log_postulacion("Computrabajo", title, "Confidencial", url, "Botón No Encontrado")
                else:
                    print(f"❌ DeepSeek RECHAZÓ: {evaluacion.get('reason')}")
                    log_postulacion("Computrabajo", title, "Confidencial", url, f"Rechazado: {evaluacion.get('reason')}")
                    
            except Exception as e:
                print(f"Error procesando oferta: {e}")
                
        print("\nCiclo completado. Revisa postulaciones.db para el historial.")
        await asyncio.to_thread(input, "\n👉 Presiona ENTER aquí para cerrar el navegador y finalizar...")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(hunter())
