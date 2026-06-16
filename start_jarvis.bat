@echo off
title JARVIS AX - Iniciador Definitivo
color 0b
echo ========================================
echo    INICIANDO JARVIS AX (modo autonomo)
echo ========================================

:: Forzar uso del entorno virtual maestro
set PYTHON_CMD=C:\AXYNTRAX\backend\venv\Scripts\python.exe
if not exist "%PYTHON_CMD%" (
    echo ERROR: El entorno virtual no existe en C:\AXYNTRAX\backend\venv.
    pause
    exit /b 1
)
echo [OK] Usando Python del Entorno Virtual: %PYTHON_CMD%

:: Matar procesos antiguos de uvicorn en el puerto 8000 para evitar choques
echo [INFO] Limpiando procesos en el puerto 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)

:: Iniciar orquestador
echo [OK] Iniciando Orquestador...
start "JARVIS Orquestador" cmd /k "cd /d C:\AXYNTRAX\backend\jarvis_orchestrator && %PYTHON_CMD% -m uvicorn main:app --host 0.0.0.0 --port 8000"

:: Esperar a que el puerto levante
ping 127.0.0.1 -n 4 >nul

:: Iniciar worker
echo [OK] Iniciando Worker...
start "JARVIS Worker" cmd /k "cd /d C:\AXYNTRAX\backend\worker && %PYTHON_CMD% worker_local.py"

echo ========================================
echo JARVIS AX LEVANTADO CORRECTAMENTE
echo El HUD Web reconectara automaticamente
echo ========================================
ping 127.0.0.1 -n 4 >nul
exit
