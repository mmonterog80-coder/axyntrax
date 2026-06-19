<#
.SYNOPSIS
Script para compilar y desplegar el HUD de JARVIS en Railway de manera automática.

.DESCRIPTION
1. Se ubica en el directorio correcto de Vite (jarvis_hud).
2. Ejecuta npm run build para minificar y compilar los assets de React.
3. Añade la carpeta dist/ al control de versiones de forma forzada.
4. Hace commit y push automático a la rama main para triggear Railway.
#>

$ErrorActionPreference = "Stop"
$HUD_DIR = "jarvis_hud"
$DIST_DIR = "$HUD_DIR\dist"

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   J.A.R.V.I.S. C&C - SECUENCIA DE DESPLIEGUE" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# 1. Verificar si estamos en la raíz del proyecto AXYNTRAX
if (-Not (Test-Path $HUD_DIR)) {
    Write-Host "[ERROR] No se encuentra la carpeta $HUD_DIR. Ejecute este script desde la raíz de C:\AXYNTRAX." -ForegroundColor Red
    Exit 1
}

# 2. Compilar el frontend React/Vite
Write-Host "`n[1/3] Compilando recursos ópticos (React/Vite)..." -ForegroundColor Yellow
Set-Location $HUD_DIR
try {
    npm run build
} catch {
    Write-Host "[ERROR] Fallo en la compilación de npm. Abortando despliegue." -ForegroundColor Red
    Set-Location ..
    Exit 1
}
Set-Location ..

# 3. Validar existencia del build
if (-Not (Test-Path $DIST_DIR)) {
    Write-Host "[ERROR] La carpeta $DIST_DIR no se generó." -ForegroundColor Red
    Exit 1
}

# 4. Git Add, Commit y Push
Write-Host "`n[2/3] Empaquetando y subiendo a la red orbital (GitHub -> Railway)..." -ForegroundColor Yellow
git add $DIST_DIR
git add start_cloud.sh
git add backend/jarvis_orchestrator/main.py

$commitMsg = "Automated HUD Deployment: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
git commit -m $commitMsg

Write-Host "`n[3/3] Ejecutando inserción en el clúster remoto..." -ForegroundColor Yellow
git push origin main

Write-Host "`n=============================================" -ForegroundColor Green
Write-Host " [OK] SECUENCIA COMPLETADA. RAILWAY EN PROCESO." -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host "El satélite estará actualizado en aproximadamente 60 segundos." -ForegroundColor Gray
Write-Host "Ruta: https://jarvis-ax-cloud-production.up.railway.app/index.html`n" -ForegroundColor Gray
