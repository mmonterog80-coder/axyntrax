# -*- coding: utf-8 -*-
import asyncio
import os
import json
import datetime
import sys
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from openai import OpenAI
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from supabase import create_client, Client

# --- Configuración y Notificaciones ---
from config_env import (
    DEEPSEEK_API_KEY, SUPABASE_URL, SUPABASE_KEY, 
    CV_PATH, CV_TEXT_PATH, MIGUEL_EMAIL, MIGUEL_TELEFONO, MIGUEL_LINKEDIN_URL
)
import jarvis_notifier

# Inicializar clientes
try:
    openai_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
except:
    openai_client = None

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"⚠️ Error conectando a Supabase: {e}")

try:
    with open(CV_TEXT_PATH, "r", encoding="utf-8") as f:
        CV_TEXT = f.read()
except:
    CV_TEXT = ""

MAX_JOBS_PER_PORTAL = 5

# --- Lista Maestra de Portales ---
PORTALS = {
    # == NACIONALES ==
    "linkedin_pe": {
        "name": "LinkedIn Perú",
        "state_file": r"C:\AXYNTRAX\linkedin_state.json",
        "search_url": "https://www.linkedin.com/jobs/search/?f_WT=2&keywords=Supply%20Chain%20Manager&location=Peru",
        "job_link_selector": "a.job-card-list__title",
        "job_link_prefix": "https://www.linkedin.com",
        "title_selector": "h1.job-details-jobs-unified-top-card__job-title, h1, h2.t-24",
        "company_selector": ".job-details-jobs-unified-top-card__company-name",
        "desc_selector": "div.jobs-description__container, article",
        "apply_selector": "button.jobs-apply-button",
        "salary_selector": ".job-details-jobs-unified-top-card__job-insight",
        "ciclo": 2
    },
    "computrabajo_pe": {
        "name": "Computrabajo Perú",
        "state_file": r"C:\AXYNTRAX\computrabajo_state.json",
        "search_url": "https://pe.computrabajo.com/trabajo-de-supply-chain?q=supply+chain+logistica&pubdate=7",
        "job_link_selector": "a.js-o-link",
        "job_link_prefix": "https://pe.computrabajo.com",
        "title_selector": "h1",
        "company_selector": "p.fs16, a.fs16",
        "desc_selector": ".fs16.t_word_wrap, .box_detail, article.box_detail",
        "apply_selector": "a:has-text('Postularme'), button#btn-apply, a#btn-apply",
        "salary_selector": ".salary, .fs16.fc_base2",
        "ciclo": 2
    },
    "bumeran_pe": {
        "name": "Bumeran",
        "state_file": r"C:\AXYNTRAX\bumeran_state.json",
        "search_url": "https://www.bumeran.com.pe/empleos-supply-chain.html",
        "job_link_selector": "a[data-qa='posting-title-link']",
        "job_link_prefix": "https://www.bumeran.com.pe",
        "title_selector": "h1[data-qa='posting-title']",
        "company_selector": "a[data-qa='company-name']",
        "desc_selector": "[data-qa='posting-description'], .description",
        "apply_selector": "button[data-qa='apply-btn'], a:has-text('Postularme')",
        "salary_selector": "[data-qa='posting-salary']",
        "ciclo": 2
    },
    "aptitus_pe": {
        "name": "Aptitus",
        "state_file": r"C:\AXYNTRAX\aptitus_state.json",
        "search_url": "https://aptitus.com/empleos/?k=supply+chain+logistica&remote=1",
        "job_link_selector": "a.job-name",
        "job_link_prefix": "https://aptitus.com",
        "title_selector": "h1.title",
        "company_selector": ".company-name",
        "desc_selector": ".description",
        "apply_selector": "button:has-text('Postular')",
        "salary_selector": ".salary",
        "ciclo": 2
    },
    "trabajando_pe": {
        "name": "Trabajando.pe",
        "state_file": r"C:\AXYNTRAX\trabajando_state.json",
        "search_url": "https://www.trabajando.pe/empleos/supply-chain-logistica",
        "job_link_selector": "a.job-title",
        "job_link_prefix": "https://www.trabajando.pe",
        "title_selector": "h1",
        "company_selector": ".company-name",
        "desc_selector": ".description",
        "apply_selector": "button:has-text('Postular')",
        "salary_selector": ".salary",
        "ciclo": 3
    },
    "jobted_pe": {
        "name": "Jobted Perú",
        "state_file": r"C:\AXYNTRAX\jobted_state.json",
        "search_url": "https://www.jobted.com.pe/trabajo/remoto/logistica",
        "job_link_selector": "a.job-card",
        "job_link_prefix": "https://www.jobted.com.pe",
        "title_selector": "h1",
        "company_selector": ".company",
        "desc_selector": ".desc",
        "apply_selector": ".apply",
        "salary_selector": ".salary",
        "ciclo": 3
    },
    "indeed_pe": {
        "name": "Indeed Perú",
        "state_file": r"C:\AXYNTRAX\indeed_state.json",
        "search_url": "https://pe.indeed.com/jobs?q=supply+chain+logistica&l=Per%C3%BA&remotejob=1",
        "job_link_selector": "a.jcs-JobTitle",
        "job_link_prefix": "https://pe.indeed.com",
        "title_selector": "h1.jobsearch-JobInfoHeader-title",
        "company_selector": ".jobsearch-InlineCompanyRating a",
        "desc_selector": "#jobDescriptionText",
        "apply_selector": "button.ia-IndeedApplyButton",
        "salary_selector": ".jobsearch-JobMetadataHeader-salaryText",
        "ciclo": 3
    },
    
    # == INTERNACIONALES ==
    "infojobs_es": {
        "name": "InfoJobs España",
        "state_file": r"C:\AXYNTRAX\infojobs_state.json",
        "search_url": "https://www.infojobs.net/ofertas-trabajo/teletrabajo/supply-chain",
        "job_link_selector": "a.ij-OfferCardContent-description-title-link",
        "job_link_prefix": "https://www.infojobs.net",
        "title_selector": "h1.title",
        "company_selector": "a.link",
        "desc_selector": "#offer-description",
        "apply_selector": "button#btn-inscripcion",
        "salary_selector": "li.salary",
        "ciclo": 1
    },
    "computrabajo_mx": {
        "name": "Computrabajo México/España",
        "state_file": r"C:\AXYNTRAX\computrabajo_int_state.json",
        "search_url": "https://mx.computrabajo.com/trabajo-de-supply-chain-modalidad-teletrabajo",
        "job_link_selector": "a.js-o-link",
        "job_link_prefix": "https://mx.computrabajo.com",
        "title_selector": "h1",
        "company_selector": "p.fs16",
        "desc_selector": "article.box_detail",
        "apply_selector": "a#btn-apply",
        "salary_selector": ".salary",
        "ciclo": 1
    },
    "manfred": {
        "name": "Manfred",
        "state_file": r"C:\AXYNTRAX\manfred_state.json",
        "search_url": "https://www.getmanfred.com/ofertas-empleo?remote=true&q=supply+chain",
        "job_link_selector": "a.job-card",
        "job_link_prefix": "https://www.getmanfred.com",
        "title_selector": "h1",
        "company_selector": ".company",
        "desc_selector": ".description",
        "apply_selector": "button:has-text('Aplicar')",
        "salary_selector": ".salary",
        "ciclo": 4
    },
    "remoteok": {
        "name": "RemoteOK",
        "state_file": r"C:\AXYNTRAX\remoteok_state.json",
        "search_url": "https://remoteok.com/remote-operations-jobs",
        "job_link_selector": "a.preventLink",
        "job_link_prefix": "https://remoteok.com",
        "title_selector": "h1",
        "company_selector": "h3",
        "desc_selector": ".description",
        "apply_selector": "a.apply",
        "salary_selector": ".salary",
        "ciclo": 4
    }
}

# --- Inteligencia ---
def evaluar_oferta(title, description, empresa="", salary_text=""):
    if not openai_client: return {"apply": True, "reason": "No IA"}
    prompt = f"""Eres CHAU CHAMBA, el Asistente de Empleo autónomo de Miguel Montero.
Miguel es Líder Senior de Supply Chain (SCM) y Logística con +25 años de experiencia.

REGLAS DE ORO (NUNCA VIOLAR):
1. NUNCA postular a cargos de ventas, telemercadeo, comercial o call center. RECHAZO AUTOMÁTICO.
2. Modalidad obligatoria: 100% Remoto / Teletrabajo / Home Office.
3. Salario: S/ 3,200 o más. (Si el monto es menor y está explícito, rechazar. Si no dice o dice "a convenir", aceptar).
4. El puesto DEBE ser relacionado a SCM, Logística, Procurement, Operaciones o Proyectos.

DATOS DE LA OFERTA:
Empresa: {empresa}
Título: {title}
Salario: {salary_text}
Descripción: {description[:2500]}

Evalúa estrictamente y responde SOLO con JSON: {{"apply": true/false, "reason": "Breve justificación"}}"""
    try:
        res = openai_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        ).choices[0].message.content.strip()
        if res.startswith("```json"): res = res[7:-3]
        elif res.startswith("```"): res = res[3:-3]
        return json.loads(res.strip())
    except Exception as e:
        print(f"  ⚠️ Error IA: {e}")
        return {"apply": False, "reason": "Error en API"}

# --- Base de Datos (Supabase Fallback) ---
def ya_postulado(enlace):
    if supabase:
        try:
            res = supabase.table("postulaciones").select("id").eq("url_oferta", enlace).execute()
            return len(res.data) > 0
        except:
            return False
    return False

def registrar_postulacion(portal, titulo, empresa, enlace, estado, salario, cv_version, notas):
    if supabase:
        try:
            data = {
                "portal": portal,
                "empresa": empresa,
                "cargo": titulo,
                "url_oferta": enlace,
                "salario_ofrecido": salario,
                "fecha_postulacion": datetime.datetime.now().isoformat(),
                "estado": estado,
                "cv_version": cv_version,
                "notas": notas
            }
            supabase.table("postulaciones").insert(data).execute()
        except Exception as e:
            print(f"  ⚠️ Error guardando en Supabase: {e}")

# --- Manejo de Formularios ---
async def detectar_captcha(page):
    # Detecta iframes de recaptcha o textos
    try:
        html = await page.content()
        html_lower = html.lower()
        if "recaptcha" in html_lower or "hcaptcha" in html_lower or "turnstile" in html_lower:
            return True
        return False
    except:
        return False

async def pausar_por_captcha(portal, url, page):
    print(f"\n🚨 CAPTCHA DETECTADO en {portal}")
    jarvis_notifier.notify_alert("CAPTCHA detectado", portal, "Resuélvelo para continuar", url)
    print("⏳ Esperando 60 segundos para resolución manual (ampliable en modo interactivo)...")
    await page.wait_for_timeout(60000) # En producción se puede usar un bucle que revise
    print("▶️ Reanudando ejecución...")

async def procesar_formulario(page):
    try:
        await page.wait_for_timeout(3000)
        
        # Rellenar campos estáticos (Email, telefono, etc) basado en name/id/placeholder
        inputs = await page.query_selector_all("input[type='text'], input[type='email'], input[type='tel']")
        for el in inputs:
            p = (await el.get_attribute("placeholder") or "").lower()
            n = (await el.get_attribute("name") or "").lower()
            i = (await el.get_attribute("id") or "").lower()
            context = f"{p} {n} {i}"
            
            if "mail" in context: await el.fill(MIGUEL_EMAIL)
            elif "phone" in context or "tel" in context: await el.fill(MIGUEL_TELEFONO)
            elif "name" in context or "nombre" in context: await el.fill("Miguel")
            elif "last" in context or "apellido" in context: await el.fill("Montero")
            elif "linkedin" in context: await el.fill(MIGUEL_LINKEDIN_URL)

        file_input = await page.query_selector("input[type='file']")
        if file_input:
            await file_input.set_input_files(CV_PATH)
            await page.wait_for_timeout(1500)

        btn = await page.query_selector("button[type='submit'], button:has-text('Enviar'), button:has-text('Submit'), button:has-text('Postularme')")
        if btn:
            await btn.click()
            await page.wait_for_timeout(4000)
            return True
        return False
    except Exception as e:
        print(f"  ⚠️ Error en formulario: {e}")
        return False

# --- Core Scraper ---
async def cazar_portal(p_key, portal, context, stealth):
    nombre = portal["name"]
    print(f"\n{'='*60}\n🌐 ESCANEANDO: {nombre.upper()}\n{'='*60}")
    
    page = await context.new_page()
    await stealth.apply_stealth_async(page)
    
    postuladas = 0
    
    try:
        await page.goto(portal["search_url"], timeout=45000)
        await page.wait_for_timeout(5000)
        
        if await detectar_captcha(page):
            await pausar_por_captcha(nombre, portal["search_url"], page)

        links_elements = await page.query_selector_all(portal["job_link_selector"])
        urls = []
        for el in links_elements[:MAX_JOBS_PER_PORTAL]:
            href = await el.get_attribute("href")
            if href:
                if href.startswith("http"): urls.append(href)
                else: urls.append(portal["job_link_prefix"] + href)

        print(f"  📋 {len(urls)} ofertas extraídas para evaluación inicial.")

        for url in urls:
            if ya_postulado(url):
                print(f"  ⏭️ Saltando (ya postulado): {url[:50]}")
                continue

            await page.goto(url, timeout=40000)
            await page.wait_for_timeout(3000)
            
            if await detectar_captcha(page):
                await pausar_por_captcha(nombre, url, page)

            try:
                title_el = await page.query_selector(portal["title_selector"])
                title = (await title_el.inner_text()).strip() if title_el else "Desconocido"

                company_el = await page.query_selector(portal["company_selector"])
                empresa = (await company_el.inner_text()).strip() if company_el else "Desconocida"

                desc_el = await page.query_selector(portal["desc_selector"])
                description = (await desc_el.inner_text()).strip() if desc_el else ""

                salary_el = await page.query_selector(portal["salary_selector"])
                salary = (await salary_el.inner_text()).strip() if salary_el else "No especificado"

                if not description or "Desconocido" in title: continue

                print(f"\n  🔎 IA Evaluando: '{title[:50]}' @ {empresa[:20]}")
                decision = evaluar_oferta(title, description, empresa, salary)

                if decision.get("apply"):
                    print(f"  ✅ IA APRUEBA: {decision.get('reason')}")
                    
                    btn_apply = await page.query_selector(portal["apply_selector"])
                    if btn_apply:
                        await btn_apply.click()
                        await page.wait_for_timeout(3000)
                        exito = await procesar_formulario(page)
                        
                        if exito:
                            print("  🚀 ¡Postulación Enviada!")
                            registrar_postulacion(nombre, title, empresa, url, "ENVIADO", salary, "v2_adaptado_SCM", decision.get("reason"))
                            jarvis_notifier.notify_success(nombre, empresa, title, salary, url)
                            postuladas += 1
                        else:
                            print("  ⚠️ No se pudo completar formulario automáticamente.")
                            registrar_postulacion(nombre, title, empresa, url, "PENDIENTE", salary, "N/A", "Formulario complejo")
                    else:
                        print("  ⚠️ Botón de apply externo o no encontrado.")
                else:
                    print(f"  ❌ IA RECHAZA: {decision.get('reason')}")

            except Exception as e:
                print(f"  ⚠️ Error oferta: {e}")

    except Exception as e:
        print(f"  💥 Error portal {nombre}: {e}")
    finally:
        await page.close()

# --- Bucle Principal 24/7 ---
async def chau_chamba_loop():
    print("\n" + "🤖 CHAU CHAMBA INICIADO (Operación 24/7) ".center(60, "═"))
    stealth = Stealth()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=50, channel="chrome")
        
        while True:
            hora_actual = datetime.datetime.now().hour
            if 0 <= hora_actual < 6: ciclo_actual = 1
            elif 6 <= hora_actual < 12: ciclo_actual = 2
            elif 12 <= hora_actual < 18: ciclo_actual = 3
            else: ciclo_actual = 4

            print(f"\n🕒 HORA: {datetime.datetime.now().strftime('%H:%M:%S')} | EJECUTANDO CICLO {ciclo_actual}")
            
            # Enviar reporte diario a las 8 AM
            if hora_actual == 8 and datetime.datetime.now().minute < 15:
                # Simular lectura de dashboard
                jarvis_notifier.notify_daily_report(5, 120, 45, 2, 5, 20, 0, "Supply Chain Manager @ Orica - S/ 15,000")
                await asyncio.sleep(900) # Prevenir múltiples envíos en esos 15 mins

            portales_ciclo = {k: v for k, v in PORTALS.items() if v["ciclo"] == ciclo_actual}
            
            for p_key, portal in portales_ciclo.items():
                state_file = portal["state_file"]
                if not os.path.exists(state_file):
                    print(f"⚠️ Sin sesión configurada para {portal['name']}. Saltando...")
                    continue
                
                context = await browser.new_context(
                    storage_state=state_file,
                    viewport={"width": 1366, "height": 768},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                )
                await cazar_portal(p_key, portal, context, stealth)
                await context.close()
                
            print("\n💤 Ciclo completado. Pausando por 30 minutos antes del próximo escaneo...")
            await asyncio.sleep(1800) # Pausa de 30 minutos entre rondas de ciclo
            
if __name__ == "__main__":
    try:
        asyncio.run(chau_chamba_loop())
    except KeyboardInterrupt:
        print("\n🛑 CHAU CHAMBA detenido manualmente.")
