import pyautogui
import time
import subprocess
import os

pyautogui.FAILSAFE = False

LOG_FILE = r"C:\AXYNTRAX\logs\worker.log"
def log_to_visor(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")
    except:
        pass

log_to_visor("[JARVIS] Ejecutando orden directa visible (Apertura de Notepad y Mouse)...")

# 1. Abre el Bloc de notas
subprocess.Popen("notepad.exe")
time.sleep(1.5)

# 2. Escribe
texto = f"Ordenes del CEO ejecutadas por JARVIS AX. Fecha y hora: {time.ctime()}"
pyautogui.write(texto)
time.sleep(0.5)

# 3. Guarda el archivo como C:\AXYNTRAX\ORDEN_EJECUTADA.txt
pyautogui.hotkey('ctrl', 's')
time.sleep(1.5)
pyautogui.write(r"C:\AXYNTRAX\ORDEN_EJECUTADA.txt")
time.sleep(0.5)
pyautogui.press('enter')
time.sleep(1)
pyautogui.press('enter') # Confirmar sobreescritura si existe
time.sleep(1)

# 4. Cierra el Bloc de notas.
pyautogui.hotkey('alt', 'f4')
time.sleep(0.5)

# 5. Mueve el mouse lentamente hasta la esquina inferior derecha
width, height = pyautogui.size()
pyautogui.moveTo(width - 50, height - 50, duration=2.0)
time.sleep(0.5)
# Vuelve al centro
pyautogui.moveTo(width // 2, height // 2, duration=2.0)

# 6. Publica en la ventana flotante
log_to_visor("[JARVIS] Ordenes del CEO completadas. Esperando siguiente directiva.")
