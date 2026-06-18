param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$ComputerName,
    
    [Parameter(Mandatory=$false)]
    [int]$Timeout = 30
)

Write-Host "========================================"
Write-Host "  Script de Conexión - AXYNTRAX"
Write-Host "========================================"
Write-Host "Computer: $ComputerName"
Write-Host "Timeout:  $Timeout segundos"
Write-Host "========================================"
