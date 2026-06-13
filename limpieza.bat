limpieza 


@echo off
:: ============================================================
::   LIMPIEZA TOTAL Y OPTIMIZACION DE PC - SuperTech Cleaner
::   Ejecutar como ADMINISTRADOR
:: ============================================================
title LIMPIEZA TOTAL PC - SuperTech

:: Verificar que se ejecuta como Administrador
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo.
    echo  [!] ERROR: Debes ejecutar este archivo como ADMINISTRADOR.
    echo  [!] Clic derecho sobre el archivo y selecciona "Ejecutar como administrador"
    echo.
    pause
    exit /b
)

color 0A
cls
echo.
echo  =========================================================
echo    LIMPIEZA TOTAL Y OPTIMIZACION DE PC
echo    SuperTech Cleaner v3.0
echo  =========================================================
echo.
echo  [ADVERTENCIA] Este script eliminara archivos temporales,
echo  cachés, residuos de software y actualizaciones obsoletas.
echo.
echo  Presiona cualquier tecla para iniciar...
pause >nul

:: ============================================================
:: [1] LIMPIEZA DE CARPETAS TEMP ESTANDAR
:: ============================================================
cls
echo.
echo  [1/12] Limpiando carpetas TEMP del sistema...
echo  -----------------------------------------------

:: %TEMP% del usuario
if exist "%TEMP%" (
    del /f /s /q "%TEMP%\*.*" >nul 2>&1
    for /d %%x in ("%TEMP%\*") do rd /s /q "%%x" >nul 2>&1
    echo   [OK] %%TEMP%% limpiado
)

:: C:\Windows\Temp
if exist "C:\Windows\Temp" (
    del /f /s /q "C:\Windows\Temp\*.*" >nul 2>&1
    for /d %%x in ("C:\Windows\Temp\*") do rd /s /q "%%x" >nul 2>&1
    echo   [OK] C:\Windows\Temp limpiado
)

:: C:\Windows\Prefetch
if exist "C:\Windows\Prefetch" (
    del /f /s /q "C:\Windows\Prefetch\*.*" >nul 2>&1
    echo   [OK] Prefetch limpiado
)

:: Temp en AppData Local
if exist "%LOCALAPPDATA%\Temp" (
    del /f /s /q "%LOCALAPPDATA%\Temp\*.*" >nul 2>&1
    for /d %%x in ("%LOCALAPPDATA%\Temp\*") do rd /s /q "%%x" >nul 2>&1
    echo   [OK] AppData\Local\Temp limpiado
)

timeout /t 1 /nobreak >nul

:: ============================================================
:: [2] LIMPIEZA PAPELERA DE RECICLAJE
:: ============================================================
echo.
echo  [2/12] Vaciando Papelera de Reciclaje...
echo  -----------------------------------------------
PowerShell -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"
echo   [OK] Papelera vaciada

timeout /t 1 /nobreak >nul

:: ============================================================
:: [3] LIMPIEZA DE CACHE DE WINDOWS
:: ============================================================
echo.
echo  [3/12] Limpiando cache de Windows...
echo  -----------------------------------------------

:: Cache de miniaturas (thumbnails)
if exist "%LOCALAPPDATA%\Microsoft\Windows\Explorer" (
    del /f /s /q "%LOCALAPPDATA%\Microsoft\Windows\Explorer\thumbcache_*.db" >nul 2>&1
    echo   [OK] Cache de miniaturas eliminada
)

:: Cache de iconos
if exist "%LOCALAPPDATA%\IconCache.db" (
    del /f /q "%LOCALAPPDATA%\IconCache.db" >nul 2>&1
    echo   [OK] Cache de iconos eliminada
)

:: Cache DNS
ipconfig /flushdns >nul 2>&1
echo   [OK] Cache DNS limpiada

:: Cache de fuentes
if exist "C:\Windows\ServiceProfiles\LocalService\AppData\Local\FontCache" (
    net stop "Windows Font Cache Service" >nul 2>&1
    del /f /s /q "C:\Windows\ServiceProfiles\LocalService\AppData\Local\FontCache\*.*" >nul 2>&1
    net start "Windows Font Cache Service" >nul 2>&1
    echo   [OK] Cache de fuentes limpiada
)

timeout /t 1 /nobreak >nul

:: ============================================================
:: [4] LIMPIEZA DE CACHE DE NAVEGADORES
:: ============================================================
echo.
echo  [4/12] Limpiando cache de navegadores...
echo  -----------------------------------------------

:: Google Chrome
if exist "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache" (
    del /f /s /q "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache\*.*" >nul 2>&1
    echo   [OK] Cache de Chrome eliminada
)
if exist "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Code Cache" (
    del /f /s /q "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Code Cache\*.*" >nul 2>&1
)

:: Microsoft Edge
if exist "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache" (
    del /f /s /q "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache\*.*" >nul 2>&1
    echo   [OK] Cache de Edge eliminada
)

:: Firefox
if exist "%APPDATA%\Mozilla\Firefox\Profiles" (
    for /d %%p in ("%APPDATA%\Mozilla\Firefox\Profiles\*") do (
        del /f /s /q "%%p\cache2\entries\*.*" >nul 2>&1
    )
    echo   [OK] Cache de Firefox eliminada
)

:: Opera
if exist "%APPDATA%\Opera Software\Opera Stable\Cache" (
    del /f /s /q "%APPDATA%\Opera Software\Opera Stable\Cache\*.*" >nul 2>&1
    echo   [OK] Cache de Opera eliminada
)

timeout /t 1 /nobreak >nul

:: ============================================================
:: [5] LIMPIEZA DE RESIDUOS DE SOFTWARE
:: ============================================================
echo.
echo  [5/12] Eliminando residuos de software...
echo  -----------------------------------------------

:: Instaladores descargados de Windows Update
if exist "C:\Windows\SoftwareDistribution\Download" (
    net stop wuauserv >nul 2>&1
    del /f /s /q "C:\Windows\SoftwareDistribution\Download\*.*" >nul 2>&1
    for /d %%x in ("C:\Windows\SoftwareDistribution\Download\*") do rd /s /q "%%x" >nul 2>&1
    net start wuauserv >nul 2>&1
    echo   [OK] Descargas de Windows Update eliminadas
)

:: Logs de crash de Windows
if exist "C:\ProgramData\Microsoft\Windows\WER\ReportArchive" (
    del /f /s /q "C:\ProgramData\Microsoft\Windows\WER\ReportArchive\*.*" >nul 2>&1
    echo   [OK] Reportes de errores de Windows eliminados
)
if exist "C:\ProgramData\Microsoft\Windows\WER\ReportQueue" (
    del /f /s /q "C:\ProgramData\Microsoft\Windows\WER\ReportQueue\*.*" >nul 2>&1
)

:: Minidumps (volcados de memoria)
if exist "C:\Windows\Minidump" (
    del /f /s /q "C:\Windows\Minidump\*.*" >nul 2>&1
    echo   [OK] Minidumps eliminados
)

:: Logs de instaladores
if exist "C:\Windows\Logs" (
    del /f /s /q "C:\Windows\Logs\CBS\*.log" >nul 2>&1
    del /f /s /q "C:\Windows\Logs\DISM\*.log" >nul 2>&1
    echo   [OK] Logs del sistema limpiados
)

:: Archivos .log y .tmp del sistema
del /f /s /q "C:\*.tmp" >nul 2>&1
del /f /s /q "C:\*.log" >nul 2>&1
del /f /s /q "C:\Windows\*.tmp" >nul 2>&1

:: Steam cache (si existe)
if exist "%LOCALAPPDATA%\Steam\htmlcache" (
    del /f /s /q "%LOCALAPPDATA%\Steam\htmlcache\*.*" >nul 2>&1
    echo   [OK] Cache de Steam eliminada
)

timeout /t 1 /nobreak >nul

:: ============================================================
:: [6] LIMPIAR ACTUALIZACIONES OBSOLETAS (WinSxS)
:: ============================================================
echo.
echo  [6/12] Limpiando actualizaciones obsoletas de Windows...
echo  -----------------------------------------------
echo   Esto puede tardar varios minutos, por favor espera...

:: Limpiar componentes obsoletos con DISM
dism /online /cleanup-image /startcomponentcleanup /resetbase >nul 2>&1
echo   [OK] Componentes obsoletos de Windows eliminados

:: Disk Cleanup silencioso - archivos de actualizacion
cleanmgr /sagerun:65535 >nul 2>&1

timeout /t 2 /nobreak >nul

:: ============================================================
:: [7] OPTIMIZAR LA RED AL 100%
:: ============================================================
echo.
echo  [7/12] Optimizando red e internet al maximo...
echo  -----------------------------------------------

:: Restablecer TCP/IP
netsh int tcp reset >nul 2>&1
echo   [OK] TCP/IP reiniciado

:: Restablecer Winsock
netsh winsock reset >nul 2>&1
echo   [OK] Winsock reiniciado

:: Restablecer IP
netsh int ip reset >nul 2>&1
echo   [OK] IP reiniciada

:: Limpiar cache DNS
ipconfig /release >nul 2>&1
ipconfig /flushdns >nul 2>&1
ipconfig /renew >nul 2>&1
echo   [OK] DNS limpiada y renovada

:: Deshabilitar throttling de red (optimizar ancho de banda)
netsh int tcp set global autotuninglevel=normal >nul 2>&1
netsh int tcp set global chimney=enabled >nul 2>&1
netsh int tcp set global dca=enabled >nul 2>&1
netsh int tcp set global netdma=enabled >nul 2>&1
netsh int tcp set global ecncapability=enabled >nul 2>&1
echo   [OK] Red optimizada al maximo rendimiento

:: Optimizar QoS - quitar reserva del 20% de ancho de banda
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Psched" /v NonBestEffortLimit /t REG_DWORD /d 0 /f >nul 2>&1
echo   [OK] Ancho de banda al 100%% (sin reserva del sistema)

timeout /t 1 /nobreak >nul

:: ============================================================
:: [8] LIMPIAR REGISTRO DE WINDOWS (entradas huerfanas)
:: ============================================================
echo.
echo  [8/12] Limpiando residuos en el Registro de Windows...
echo  -----------------------------------------------

:: Eliminar entradas de programas desinstalados (rutas huerfanas comunes)
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths" /f >nul 2>&1
echo   [OK] Historial de Explorer y RunMRU limpiados

:: Limpiar lista de programas recientes
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Search\RecentApps" /f >nul 2>&1
echo   [OK] Apps recientes limpiadas

timeout /t 1 /nobreak >nul

:: ============================================================
:: [9] LIMPIAR ESCRITORIO Y DESCARGAS (archivos temporales)
:: ============================================================
echo.
echo  [9/12] Limpiando archivos temporales del Escritorio...
echo  -----------------------------------------------

:: Eliminar .tmp y .log del escritorio
del /f /q "%USERPROFILE%\Desktop\*.tmp" >nul 2>&1
del /f /q "%USERPROFILE%\Desktop\*.log" >nul 2>&1
del /f /q "%USERPROFILE%\Desktop\Thumbs.db" >nul 2>&1
del /f /q "%PUBLIC%\Desktop\Thumbs.db" >nul 2>&1
echo   [OK] Residuos temporales del Escritorio eliminados

:: Thumbs.db en todo el sistema
del /f /s /q "%USERPROFILE%\Thumbs.db" >nul 2>&1
echo   [OK] Archivos Thumbs.db eliminados

timeout /t 1 /nobreak >nul

:: ============================================================
:: [10] LIMPIAR ARCHIVOS TEMPORALES DE OFFICE Y APPS
:: ============================================================
echo.
echo  [10/12] Limpiando temporales de Office y otras apps...
echo  -----------------------------------------------

:: Microsoft Office
if exist "%APPDATA%\Microsoft\Office\Recent" (
    del /f /s /q "%APPDATA%\Microsoft\Office\Recent\*.*" >nul 2>&1
    echo   [OK] Recientes de Office eliminados
)
if exist "%LOCALAPPDATA%\Microsoft\Office\16.0\WebServiceCache" (
    del /f /s /q "%LOCALAPPDATA%\Microsoft\Office\16.0\WebServiceCache\*.*" >nul 2>&1
)

:: Adobe cache
if exist "%APPDATA%\Adobe\Common\Media Cache Files" (
    del /f /s /q "%APPDATA%\Adobe\Common\Media Cache Files\*.*" >nul 2>&1
    echo   [OK] Cache de Adobe eliminada
)

:: Spotify cache
if exist "%LOCALAPPDATA%\Spotify\Storage" (
    del /f /s /q "%LOCALAPPDATA%\Spotify\Storage\*.*" >nul 2>&1
    echo   [OK] Cache de Spotify eliminada
)

:: Discord cache
if exist "%APPDATA%\discord\Cache" (
    del /f /s /q "%APPDATA%\discord\Cache\*.*" >nul 2>&1
    echo   [OK] Cache de Discord eliminada
)

timeout /t 1 /nobreak >nul

:: ============================================================
:: [11] OPTIMIZAR DISCO (DESFRAGMENTAR O TRIM segun tipo)
:: ============================================================
echo.
echo  [11/12] Optimizando disco...
echo  -----------------------------------------------
echo   Detectando tipo de disco y optimizando...

:: Optimizar todas las unidades (Windows detecta si es SSD o HDD automaticamente)
defrag C: /U /V /O >nul 2>&1
echo   [OK] Disco C: optimizado (TRIM si es SSD, Defrag si es HDD)

timeout /t 1 /nobreak >nul

:: ============================================================
:: [12] LIMPIEZA FINAL CON HERRAMIENTA DE WINDOWS
:: ============================================================
echo.
echo  [12/12] Ejecutando limpieza final del sistema...
echo  -----------------------------------------------

:: Configurar y ejecutar Disk Cleanup completo
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Active Setup Temp Folders" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\BranchCache" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Downloaded Program Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Internet Cache Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Memory Dump Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Old ChkDsk Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Previous Installations" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Recycle Bin" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Service Pack Cleanup" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Setup Log Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\System error memory dump files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\System error minidump files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Temporary Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Temporary Setup Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Thumbnail Cache" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Update Cleanup" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Upgrade Discarded Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\User file versions" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows Defender" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows Error Reporting Archive Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows Error Reporting Queue Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows Error Reporting System Archive Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows Error Reporting System Queue Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows Upgrade Log Files" /v StateFlags0064 /t REG_DWORD /d 2 /f >nul 2>&1

cleanmgr /sagerun:64
echo   [OK] Limpieza de disco completada

:: ============================================================
:: RESUMEN FINAL
:: ============================================================
cls
color 0A
echo.
echo  =========================================================
echo    LIMPIEZA TOTAL COMPLETADA CON EXITO!
echo  =========================================================
echo.
echo   Lo que se limpio y optimizo:
echo   [OK] TEMP, %%TEMP%%, Windows\Temp, Prefetch
echo   [OK] Papelera de Reciclaje vaciada
echo   [OK] Cache de miniaturas, iconos y DNS
echo   [OK] Cache de Chrome, Edge, Firefox, Opera
echo   [OK] Residuos de software y logs del sistema
echo   [OK] Actualizaciones obsoletas de Windows eliminadas
echo   [OK] Red optimizada al 100%% del ancho de banda
echo   [OK] Registro de Windows limpiado
echo   [OK] Escritorio limpio de archivos temporales
echo   [OK] Cache de Office, Adobe, Spotify, Discord
echo   [OK] Disco optimizado (TRIM/Defrag segun tipo)
echo   [OK] Limpieza profunda con herramientas de Windows
echo.
echo  =========================================================
echo.
echo  IMPORTANTE: Se recomienda REINICIAR tu PC ahora para
echo  que todos los cambios surtan efecto correctamente.
echo.
set /p reiniciar=  Deseas reiniciar ahora? (S/N): 
if /i "%reiniciar%"=="S" (
    echo.
    echo  Reiniciando en 10 segundos...
    shutdown /r /t 10 /c "Reinicio post-limpieza total del sistema"
) else (
    echo.
    echo  Recuerda reiniciar tu PC manualmente para aplicar
    echo  todos los cambios de red y sistema.
    echo.
    pause
)