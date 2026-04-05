# Script de Vigilancia de RAM
# Monitoreo en vivo de RAM libre

Write-Host "Iniciando vigilancia de memoria física..." -ForegroundColor Cyan
Write-Host "Presiona Ctrl+C para detener."

while($true) {
    $mem = Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory
    $freeMB = [math]::Round($mem.FreePhysicalMemory / 1024, 2)
    
    if ($freeMB -lt 150) {
        Write-Host "ALERTA: Memoria libre por debajo de 150MB ($freeMB MB)!" -ForegroundColor Red
        # Podríamos sonar un beep si el usuario lo permite
        # [System.Console]::Beep(440, 500)
    } elseif ($freeMB -lt 300) {
        Write-Host "PRECAUCIÓN: Memoria libre baja ($freeMB MB)" -ForegroundColor Yellow
    } else {
        Write-Host "Estado: OK ($freeMB MB libres)" -ForegroundColor Green
    }
    
    Start-Sleep -Seconds 10
}
