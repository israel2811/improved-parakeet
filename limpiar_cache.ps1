# Script de Limpieza Segura de Temporales
# NO borra archivos del usuario, solo archivos de sistema que se pueden recrear.

Write-Host "Iniciando limpieza de archivos temporales..." -ForegroundColor Cyan

# 1. Limpiar carpeta TEMP del usuario
$userTemp = $env:TEMP
if (Test-Path $userTemp) {
    Write-Host "Limpiando temp de usuario ($userTemp)..."
    Get-ChildItem -Path $userTemp -Recurse -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

# 2. Limpiar carpeta TEMP del sistema
$sysTemp = "C:\Windows\Temp"
if (Test-Path $sysTemp) {
    Write-Host "Limpiando temp del sistema ($sysTemp)..."
    Get-ChildItem -Path $sysTemp -Recurse -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

# 3. Limpiar logs de VS Code (opcional pero ahorra espacio)
$vscodeLogs = "$env:APPDATA\Code\logs"
if (Test-Path $vscodeLogs) {
    Write-Host "Limpiando logs de VS Code..."
    Get-ChildItem -Path $vscodeLogs -Recurse -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

# 4. Forzar recolección de basura en el sistema
[System.GC]::Collect()

Write-Host "Limpieza completada. Revisa el espacio en disco ahora." -ForegroundColor Green
