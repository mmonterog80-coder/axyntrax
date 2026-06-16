@echo off
title JARVIS AX - VISOR DE ACTIVIDAD
color 0a
echo =========================================
echo       VISOR DE CONCIENCIA AUTONOMA       
echo =========================================
echo.

:: Asegurar que los archivos existan antes de leerlos
if not exist "C:\AXYNTRAX\logs" mkdir "C:\AXYNTRAX\logs"
if not exist "C:\AXYNTRAX\logs\worker.log" echo [SISTEMA] Iniciando Bitacora de JARVIS... > "C:\AXYNTRAX\logs\worker.log"

:: Matar workers anteriores para evitar duplicados
taskkill /F /IM python.exe /FI "WINDOWTITLE eq worker_local.py" >nul 2>&1

:: Iniciar el Worker local en una ventana minimizada para no estorbar usando el VENV maestro
start "JARVIS Worker" /min cmd /c "cd C:\AXYNTRAX\backend\worker && title worker_local.py && C:\AXYNTRAX\backend\venv\Scripts\python.exe worker_local.py"

echo [*] Brazo robotico (Worker) iniciado en segundo plano.
echo [*] Conectado a la nube de AXYNTRAX (Railway).
echo [*] Mostrando pensamientos y acciones en tiempo real:
echo.

:: Leer el archivo en tiempo real (Tail)
powershell -Command "Get-Content C:\AXYNTRAX\logs\worker.log -Wait -Tail 20"
