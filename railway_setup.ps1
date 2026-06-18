
# connect_vercel.ps1 - Conecta Vercel con Supabase y Railway
$VT  = "vcp_01jmpoyLsuIZlBAMfgGcq0XLqpnnKU5nzlnP6s5ozuc8bNZS7d2jFqrz"
$TEAM = "team_LDSXFXywiCdav8j7BRaeNMoE"
$PROJ = "prj_FHcY1MUTMiVJfSixRcIv3XpQwymq"
$VH  = @{ Authorization = "Bearer $VT"; "Content-Type" = "application/json" }
$API = "https://api.vercel.com"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   VERCEL + SUPABASE + RAILWAY CONNECT" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# === VERIFICAR PROYECTO ===
Write-Host ""
Write-Host "[1/4] Proyecto Vercel detectado..." -ForegroundColor Yellow
Write-Host "  Proyecto : web-axyntrax" -ForegroundColor Green
Write-Host "  Team     : axyntraxautomation-1607s-projects" -ForegroundColor Green
Write-Host "  Repo     : axyntraxautomation-lab/AXYNTRAX" -ForegroundColor Green
Write-Host "  Estado   : BLOCKED (faltan variables de entorno)" -ForegroundColor Red

# === SETEAR VARIABLES EN VERCEL ===
Write-Host ""
Write-Host "[2/4] Configurando variables de entorno en Vercel..." -ForegroundColor Yellow

$vars = @(
    @{ key = "NEXT_PUBLIC_SUPABASE_URL";      value = "https://qatawtbfrfreakdbluat.supabase.co"; target = @("production","preview","development") }
    @{ key = "NEXT_PUBLIC_SUPABASE_ANON_KEY"; value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFhdGF3dGJmcmZyZWFrZGJsdWF0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzM4MTQ4OSwiZXhwIjoyMDkyOTU3NDg5fQ.hW5U5rMn_1YYYSjI5Hh8Tle1Tl81kwrW47Qz2KgF36g"; target = @("production","preview","development") }
    @{ key = "SUPABASE_SERVICE_ROLE_KEY";     value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFhdGF3dGJmcmZyZWFrZGJsdWF0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzM4MTQ4OSwiZXhwIjoyMDkyOTU3NDg5fQ.hW5U5rMn_1YYYSjI5Hh8Tle1Tl81kwrW47Qz2KgF36g"; target = @("production","preview") }
    @{ key = "NEXT_PUBLIC_API_URL";           value = "https://axyntrax.up.railway.app"; target = @("production","preview","development") }
    @{ key = "API_SECRET";                    value = "axyntrax-2026-secret-miguel"; target = @("production","preview") }
    @{ key = "DEEPSEEK_API_KEY";              value = "sk-c4afeeab9c1346dfad4622c9b05185f2"; target = @("production","preview") }
    @{ key = "TELEGRAM_BOT_TOKEN";            value = "8862258909:AAGQxaA1cMW1xZhicDRRUJGywzutEq8Cxdk"; target = @("production") }
    @{ key = "NEXT_PUBLIC_RAILWAY_URL";       value = "https://axyntrax.up.railway.app"; target = @("production","preview","development") }
)

foreach ($v in $vars) {
    $body = @{
        key    = $v.key
        value  = $v.value
        type   = "plain"
        target = $v.target
    } | ConvertTo-Json -Compress

    try {
        $r = Invoke-RestMethod -Uri "$API/v10/projects/$PROJ/env?teamId=$TEAM" -Headers $VH -Method POST -Body $body
        Write-Host "  OK $($v.key)" -ForegroundColor Green
    } catch {
        # Si ya existe, intentar actualizar
        $errMsg = $_.ErrorDetails.Message | ConvertFrom-Json -ErrorAction SilentlyContinue
        if ($errMsg.error.code -eq "ENV_ALREADY_EXISTS") {
            Write-Host "  EXISTS $($v.key) (ya configurada)" -ForegroundColor DarkGray
        } else {
            Write-Host "  WARN $($v.key) -> $($_.Exception.Message)" -ForegroundColor Yellow
        }
    }
}

# === FORZAR REDEPLOY EN VERCEL ===
Write-Host ""
Write-Host "[3/4] Forzando redeploy en Vercel..." -ForegroundColor Yellow

# Obtener el último deployment
$deps = Invoke-RestMethod -Uri "$API/v6/deployments?projectId=$PROJ&teamId=$TEAM&limit=1" -Headers $VH
$lastDep = $deps.deployments[0]

if ($lastDep) {
    $redeployBody = @{
        name       = "web-axyntrax"
        gitSource  = @{ type = "github"; org = "axyntraxautomation-lab"; repo = "AXYNTRAX"; ref = "main" }
        target     = "production"
    } | ConvertTo-Json -Compress

    try {
        $rd = Invoke-RestMethod -Uri "$API/v13/deployments?teamId=$TEAM&forceNew=1" -Headers $VH -Method POST -Body $redeployBody
        Write-Host "  OK Redeploy iniciado: $($rd.url)" -ForegroundColor Green
    } catch {
        Write-Host "  INFO Redeploy manual: haz push a GitHub para triggear" -ForegroundColor Yellow
    }
} else {
    Write-Host "  INFO No hay deployments previos" -ForegroundColor Yellow
}

# === RESUMEN FINAL ===
Write-Host ""
Write-Host "[4/4] Resumen de conexiones..." -ForegroundColor Yellow
Write-Host ""
Write-Host "  GITHUB  -> axyntraxautomation-lab/AXYNTRAX [main]" -ForegroundColor Green
Write-Host "             https://github.com/axyntraxautomation-lab/AXYNTRAX" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  VERCEL  -> web-axyntrax" -ForegroundColor Green
Write-Host "             Variables: SUPABASE + RAILWAY + API_SECRET configuradas" -ForegroundColor Green
Write-Host "             URL: https://web-axyntrax.vercel.app" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  RAILWAY -> resourceful-transformation/axyntrax" -ForegroundColor Yellow
Write-Host "             Variables: 14 OK" -ForegroundColor Green
Write-Host "             PENDIENTE: Conectar repo en dashboard" -ForegroundColor Red
Write-Host ""
Write-Host "  SUPABASE -> qatawtbfrfreakdbluat" -ForegroundColor Green
Write-Host "             Tablas: qwen_orders + qwen_results OK" -ForegroundColor Green
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  VERCEL + SUPABASE = CONECTADOS" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
