# 🧹 NEXUS DISK PURGE (V2.0 - PhD Hardened)
# Emergency cleanup for low-disk systems (PhD Edition)

Write-Host "[*] Starting AGGRESSIVE Emergency Disk Purge..." -ForegroundColor Yellow

# 1. Clean Temporary Files & Caches
$PurgeTargets = @(
    "$env:TEMP\*",
    "$env:SystemRoot\Temp\*",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache\*",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Profile 6\Cache\*",
    "$env:LOCALAPPDATA\pip\cache\*",
    "$env:AppData\npm-cache\*",
    "$env:LOCALAPPDATA\Microsoft\TypeScript\*",
    "$env:LOCALAPPDATA\Microsoft\VisualStudio\*\Designer\Cache\*",
    "$env:LOCALAPPDATA\nvm\cache\*"
)

foreach ($target in $PurgeTargets) {
    if (Test-Path $target) {
        Write-Host "[*] Purging: $target" -ForegroundColor Cyan
        Remove-Item -Path $target -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# 2. Clean Windows Update Cache
Write-Host "[*] Clearing Windows Update cache..." -ForegroundColor Cyan
Remove-Item -Path "$env:SystemRoot\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue

# 3. System Cleanup
Write-Host "[*] Clearing Prefetch & Logs..." -ForegroundColor Cyan
Remove-Item -Path "$env:SystemRoot\Prefetch\*" -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "$env:SystemRoot\Logs" -Recurse | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-1) } | Remove-Item -Force -ErrorAction SilentlyContinue

# 4. Git Housekeeping (Critical)
# This will prune unreachable objects in current repo.
Write-Host "[*] Running Git Prune (Current Repo)..." -ForegroundColor Magenta
git prune 2>$null
git gc --prune=now --aggressive 2>$null

# 5. Check Free Space
$C = Get-PSDrive C
$FreeGB = [math]::Round($C.Free / 1GB, 2)
Write-Host "[OK] Aggressive Purge Complete. Free Space on C: $FreeGB GB" -ForegroundColor Green

if ($FreeGB -lt 1.0) {
    Write-Host "[!] WARNING: Still critically low on space. Consider deleting C:\Users\Lenovo\.git (4GB junk)." -ForegroundColor Red
}
