# -*- coding: utf-8 -*-
import asyncio
import os
import json
import sqlite3
import datetime
import sys

# Forzar salida UTF-8 en Windows para evitar errores de codificación
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
from dotenv import load_dotenv
from openai import OpenAI
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# ── Configuración ──────────────────────────────────────────────────────────────
load_dotenv(r"C:\AXYNTRAX\job_hunter.env")
API_KEY = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

CV_PATH = r"C:\Users\YARVIS\Desktop\certificados\CV_MIGUEL_MONTERO_LITE.pdf"
DB_PATH = r"C:\AXYNTRAX\postulaciones.db"

with open(r"C:\AXYNTRAX\cv_text.txt", "r", encoding="utf-8") as f:
    CV_TEXT = f.read()

# ── Configuración de portales ──────────────────────────────────────────────────
PORTALS = [
    {
        "name": "Computrabajo",
        "state_file": r"C:\AXYNTRAX\computrabajo_state.json",
        "search_url": "https://pe.computrabajo.com/trabajo-de-supply-chain?q=supply+chain+logistica",
        "job_link_selector": "a.js-o-link",
        "job_link_prefix": "https://pe.computrabajo.com",
        "title_selector": "h1",
        "company_selector": "p.fs16, a.fs16",
        "desc_selector": ".fs16.t_word_wrap, .box_detail, article.box_detail",
        "apply_selector": "a:has-text('Postularme'), button#btn-apply, a#btn-apply",
        "salary_selector": ".salary, .fs16.fc_base2",
    },
    {
        "name": "Bumeran",
        "state_file": r"C:\AXYNTRAX\bumeran_state.json",
        "search_url": "https://www.bumeran.com.pe/empleos-supply-chain.html?q=supply+chain+logistica",
        "job_link_selector": "a[data-qa='posting-title-link']",
        "job_link_prefix": "",
        "title_selector": "h1[data-qa='posting-title']",
        "company_selector": "a[data-qa='company-name']",
        "desc_selector": "[data-qa='posting-description'], .description",
        "apply_selector": "button[data-qa='apply-btn'], a:has-text('Postularme'), button:has-text('Postularme')",
        "salary_selector": "[data-qa='posting-salary']",
    },
    {
        "name": "Indeed",
        "state_file": r"C:\AXYNTRAX\indeed_state.json",
        "search_url": "https://pe.indeed.com/jobs?q=supply+chain+logistica+remoto&l=Per%C3%BA&remotejob=1",
        "job_link_selector": "a.jcs-JobTitle",
        "job_link_prefix": "https://pe.indeed.com",
        "title_selector": "h1.jobsearch-JobInfoHeader-title",
        "company_selector": ".jobsearch-InlineCompanyRating a, [data-company-name]",
        "desc_selector": "#jobDescriptionText",
        "apply_selector": "button.ia-IndeedApplyButton, a#indeedApplyButton, button:has-text('Apply'), a:has-text('Postularme')",
        "salary_selector": ".jobsearch-JobMetadataHeader-salaryText, #salaryInfoAndJobType span",
    },
    {
        "name": "Aptitus",
        "state_file": r"C:\AXYNTRAX\aptitus_state.json",
        "search_url": "https://aptitus.com/empleos/?k=supply+chain+logistica&remote=1",
        "job_link_selector": "a.job-name, h2 a, .job-title a",
        "job_link_prefix": "",
        "title_selector": "h1.title, h1",
        "company_selector": ".company-name, .employer-name",
        "desc_selector": ".description, .job-description, [class*='description']",
        "apply_selector": "a:has-text('Postular'), button:has-text('Postular'), a:has-text('Aplicar')",
        "salary_selector": ".salary, [class*='salary']",
    },
    {
        "name": "Trabajando.pe",
        "state_file": r"C:\AXYNTRAX\trabajando_state.json",
        "search_url": "https://www.trabajando.pe/empleos/supply-chain-logistica",
        "job_link_selector": "a.job-title, .job-offer a, h2 a",
        "job_link_prefix": "https://www.trabajando.pe",
        "title_selector": "h1, .job-title",
        "company_selector": ".company-name, .employer",
        "desc_selector": ".description, .job-body, [class*='description']",
        "apply_selector": "a:has-text('Postular'), button:has-text('Postular'), a:has-text('Aplicar')",
        "salary_selector": ".salary, [class*='salary']",
    },
]

MAX_JOBS_PER_PORTAL = 5  # Máximo de ofertas a revisar por portal en cada ciclo

# ── Base de datos ──────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS postulaciones
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  fecha TEXT, portal TEXT, titulo TEXT,
                  empresa TEXT, enlace TEXT, estado TEXT)''')
    conn.commit()
    conn.close()

def ya_postulado(enlace):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM postulaciones WHERE enlace=?", (enlace,))
    res = c.fetchone()
    conn.close()
    return res is not None

def log_postulacion(portal, titulo, empresa, enlace, estado):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO postulaciones (fecha, portal, titulo, empresa, enlace, estado) VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), portal, titulo, empresa, enlace, estado)
    )
    conn.commit()
    conn.close()

# ── Evaluación con DeepSeek ────────────────────────────────────────────────────
def evaluar_oferta(title, description, empresa="", salary_text=""):
    prompt = f"""Eres el Asistente de Empleo de Miguel Montero, experto en Supply Chain y Logística.

REGLAS ESTRICTAS DE FILTRADO:
1. Modalidad: Debe ser Remoto / Teletrabajo. Si exige presencial o híbrido estricto, RECHAZAR.
2. Salario: Mínimo 3200 PEN. Si es menor, RECHAZAR. Si no se menciona, ACEPTAR.
3. Requisitos técnicos: Si exige "Excel Básico", RECHAZAR.
4. Tipo de empresa: Solo formales y corporativas. Excluir call centers, ventas, telecom.
5. Solo trabajos profesionales con contrato formal.

DATOS:
Empresa: {empresa}
Título: {title}
Salario: {salary_text or 'No especificado'}
Descripción: {description[:2000]}

Responde SOLO JSON: {{"apply": true/false, "reason": "..."}}"""
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
        print(f"  ⚠️ Error IA: {e}")
        return {"apply": False, "reason": "Error IA"}

def responder_formulario(preguntas):
    if not preguntas:
        return {}
    prompt = f"""Eres Miguel Montero respondiendo preguntas de un formulario de empleo.
Basado en este CV:
{CV_TEXT[:3000]}

Preguntas:
{json.dumps(preguntas, indent=2, ensure_ascii=False)}

Responde SOLO JSON donde la clave es el 'id' y el valor es la respuesta corta.
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

# ── Procesador de formulario de postulación ────────────────────────────────────
async def procesar_formulario(page):
    try:
        await page.wait_for_timeout(2000)
        preguntas = []
        inputs = await page.query_selector_all("input[type='text'], input[type='number'], textarea")
        for i, el in enumerate(inputs):
            id_val = await el.get_attribute("id") or f"input_{i}"
            placeholder = await el.get_attribute("placeholder") or ""
            if placeholder:
                preguntas.append({"id": id_val, "contexto": placeholder})

        if preguntas:
            respuestas = responder_formulario(preguntas)
            for id_val, respuesta in respuestas.items():
                try:
                    await page.fill(f"[id='{id_val}']", str(respuesta))
                except:
                    pass

        # Adjuntar CV si hay input de archivo
        file_input = await page.query_selector("input[type='file']")
        if file_input:
            await file_input.set_input_files(CV_PATH)
            await page.wait_for_timeout(1000)

        # Enviar formulario
        btn = await page.query_selector(
            "button:has-text('Enviar'), button:has-text('Postularme'), "
            "button:has-text('Aplicar'), button[type='submit']"
        )
        if btn:
            await btn.click()
            await page.wait_for_timeout(3000)
            return True
        return False
    except Exception as e:
        print(f"  ⚠️ Error formulario: {e}")
        return False

# ── Función principal de caza por portal ──────────────────────────────────────
async def cazar_portal(portal: dict, context, stealth: Stealth):
    nombre = portal["name"]
    print(f"\n{'='*55}")
    print(f"🌐 ESCANEANDO: {nombre.upper()}")
    print(f"{'='*55}")

    page = await context.new_page()
    await stealth.apply_stealth_async(page)

    try:
        await page.goto(portal["search_url"], timeout=30000)
        await page.wait_for_timeout(4000)

        # Obtener links de ofertas
        links_elements = await page.query_selector_all(portal["job_link_selector"])
        urls = []
        for el in links_elements[:MAX_JOBS_PER_PORTAL]:
            href = await el.get_attribute("href")
            if href:
                if href.startswith("http"):
                    urls.append(href)
                else:
                    urls.append(portal["job_link_prefix"] + href)

        print(f"  📋 {len(urls)} ofertas encontradas.")

        postuladas = 0
        rechazadas = 0

        for url in urls:
            if ya_postulado(url):
                print(f"  ⏭️ Ya postulado: {url[:60]}")
                continue

            await page.goto(url, timeout=30000)
            await page.wait_for_timeout(3000)

            try:
                title_el = await page.query_selector(portal["title_selector"])
                title = (await title_el.inner_text()).strip() if title_el else "Sin título"

                company_el = await page.query_selector(portal["company_selector"])
                empresa = (await company_el.inner_text()).strip() if company_el else "Desconocida"

                desc_el = await page.query_selector(portal["desc_selector"])
                description = (await desc_el.inner_text()).strip() if desc_el else ""

                salary_el = await page.query_selector(portal["salary_selector"])
                salary = (await salary_el.inner_text()).strip() if salary_el else ""

                if not description:
                    print(f"  ❌ Sin descripción: {title[:50]}")
                    continue

                print(f"\n  🔎 Evaluando: '{title[:55]}' @ {empresa[:30]}")
                decision = evaluar_oferta(title, description, empresa, salary)

                if decision.get("apply"):
                    print(f"  ✅ APROBADO: {decision.get('reason')}")

                    btn_apply = await page.query_selector(portal["apply_selector"])
                    if btn_apply:
                        await btn_apply.click()
                        await page.wait_for_timeout(3000)
                        exito = await procesar_formulario(page)
                        estado = "✅ Postulado" if exito else "⚠️ Formulario Pendiente"
                        log_postulacion(nombre, title, empresa, url, estado)
                        postuladas += 1
                        print(f"  🚀 {estado}")
                    else:
                        log_postulacion(nombre, title, empresa, url, "⚠️ Botón no encontrado")
                        print("  ⚠️ Botón de postulación no encontrado.")
                else:
                    print(f"  ❌ RECHAZADO: {decision.get('reason')}")
                    log_postulacion(nombre, title, empresa, url, f"❌ Rechazado: {decision.get('reason')}")
                    rechazadas += 1

                await page.wait_for_timeout(2000)

            except Exception as e:
                print(f"  ⚠️ Error procesando oferta: {e}")

        print(f"\n  📊 Resumen {nombre}: ✅ {postuladas} postuladas | ❌ {rechazadas} rechazadas")

    except Exception as e:
        print(f"  💥 Error general en {nombre}: {e}")
    finally:
        await page.close()

# ── Motor principal ────────────────────────────────────────────────────────────
async def hunter_global():
    init_db()
    print("\n" + "🤖 AXYNTRAX GLOBAL JOB HUNTER INICIADO ".center(60, "═"))
    print(f"   ⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   🎯 Portales activos: {len(PORTALS)}")
    print(f"   📄 CV: {CV_PATH}")
    print("═" * 60 + "\n")

    stealth = Stealth()

    async with async_playwright() as p:
        # Procesamos portal por portal (cada uno con su sesión maestra)
        for portal in PORTALS:
            state_file = portal["state_file"]
            if not os.path.exists(state_file):
                print(f"⚠️ Sin sesión para {portal['name']}. Saltando...")
                continue

            browser = await p.chromium.launch(headless=True, slow_mo=30, channel="chrome")
            context = await browser.new_context(
                storage_state=state_file,
                viewport={"width": 1280, "height": 720},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            )
            await cazar_portal(portal, context, stealth)
            await browser.close()
            await asyncio.sleep(5)  # Pausa entre portales

    # Mostrar resumen final desde la BD
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT portal, estado, COUNT(*) FROM postulaciones GROUP BY portal, estado ORDER BY portal")
    rows = c.fetchall()
    conn.close()

    print("\n" + "📊 RESUMEN FINAL DE POSTULACIONES ".center(60, "═"))
    for portal, estado, count in rows:
        print(f"   {portal:20s} | {estado:30s} | {count} ofertas")
    print("═" * 60)
    print("\n✅ Ciclo completado. Revisa postulaciones.db para el historial completo.")

if __name__ == "__main__":
    asyncio.run(hunter_global())
