import pyautogui
import time
import subprocess
import os

pyautogui.FAILSAFE = False

# Asegurar directorio
os.makedirs("C:\\AXYNTRAX", exist_ok=True)

# 1. Mover el mouse
pyautogui.moveTo(500, 300, duration=0.5)
time.sleep(0.5)

# 2. Abrir Bloc de notas
subprocess.Popen("notepad.exe")
time.sleep(1.5)

# 3. Escribir mensaje
pyautogui.write("JARVIS AX controla este PC.")
pyautogui.press('enter')
pyautogui.write(f"Hora: {time.ctime()}")
time.sleep(0.5)

# 4. Guardar (Ctrl+S)
pyautogui.hotkey('ctrl', 's')
time.sleep(1.5)  # Esperar a que aparezca el diálogo

# 5. Escribir la ruta y presionar Enter (FORZAR ENTER DOS VECES)
pyautogui.write("C:\\AXYNTRAX\\prueba_control.txt")
time.sleep(0.5)
pyautogui.press('enter')
time.sleep(1)
pyautogui.press('enter')  # Confirmar si hay otra ventana
time.sleep(1)

# 6. Cerrar Bloc de notas (Alt+F4)
pyautogui.hotkey('alt', 'f4')
time.sleep(0.5)

print("✅ Prueba completada. Archivo guardado en C:\\AXYNTRAX\\prueba_control.txt")
