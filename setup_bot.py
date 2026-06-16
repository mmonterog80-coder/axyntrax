import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# Cargar credenciales
load_dotenv(r"C:\AXYNTRAX\job_hunter.env")
STATE_FILE = r"C:\AXYNTRAX\computrabajo_state.json"

async def run_computrabajo():
    print("Iniciando Motor Playwright (Modo Visible)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50, channel="chrome")
        
        # Cargar sesion guardada si existe
        if os.path.exists(STATE_FILE):
            print("Cargando sesión previa...")
            context = await browser.new_context(storage_state=STATE_FILE, viewport={"width": 1280, "height": 720})
        else:
            context = await browser.new_context(viewport={"width": 1280, "height": 720})
        
        page = await context.new_page()
        
        stealth = Stealth()
        await stealth.apply_stealth_async(page)
        
        # ==========================================
        # COMPUTRABAJO
        # ==========================================
        print("Navegando a Computrabajo Perú...")
        await page.goto("https://pe.computrabajo.com/")
        
        is_logged_in = False
        try:
            await page.wait_for_selector("a:has-text('Entrar'), a:has-text('Ingresa')", timeout=5000)
        except:
            is_logged_in = True
            
        if not is_logged_in:
            print("\n========================================================")
            print("⚠️ ATENCIÓN: Por favor, inicia sesión en Computrabajo.")
            print("El bot está pausado. Hazlo en la ventana que se acaba de abrir.")
            print("========================================================\n")
            
            await asyncio.to_thread(input, "👉 VUELVE A ESTA CONSOLA Y PRESIONA 'ENTER' SOLO CUANDO HAYAS INICIADO SESIÓN EN COMPUTRABAJO...")
            
            print("✅ Computrabajo: Guardando sesión...")
            await context.storage_state(path=STATE_FILE)
        else:
            print("✅ Computrabajo: Sesión ya activa.")
            
        # ==========================================
        # LINKEDIN
        # ==========================================
        LINKEDIN_STATE_FILE = r"C:\AXYNTRAX\linkedin_state.json"
        print("\nNavegando a LinkedIn...")
        await page.goto("https://www.linkedin.com/")
        
        is_li_logged_in = False
        try:
            # Si pide el formulario de login, no estamos logueados
            await page.wait_for_selector("input[id='session_key'], a[data-tracking-control-name='guest_homepage-basic_nav-header-signin']", timeout=5000)
        except:
            is_li_logged_in = True
            
        if not is_li_logged_in:
            print("\n========================================================")
            print("⚠️ ATENCIÓN: Por favor, ahora inicia sesión en LinkedIn.")
            print("El bot está pausado esperando tu login.")
            print("========================================================\n")
            
            await asyncio.to_thread(input, "👉 VUELVE A ESTA CONSOLA Y PRESIONA 'ENTER' SOLO CUANDO HAYAS INICIADO SESIÓN EN LINKEDIN...")
            
            print("✅ LinkedIn: Guardando sesión...")
            await context.storage_state(path=LINKEDIN_STATE_FILE)
        else:
            print("✅ LinkedIn: Sesión ya activa.")

        print("\n¡Todo listo! Sesiones capturadas. Cerrando navegador...")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_computrabajo())
