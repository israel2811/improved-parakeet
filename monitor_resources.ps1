$processes = Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 -Property Name, @{Name='RAM(MB)';Expression={[math]::Round($_.WorkingSet64 / 1MB, 2)}}
$disks = Get-CimInstance Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 } | Select-Object DeviceID, @{Name='Free(GB)';Expression={[math]::Round($_.FreeSpace / 1GB, 2)}}, @{Name='Size(GB)';Expression={[math]::Round($_.Size / 1GB, 2)}}
$mem = Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory
$totalRAM = [math]::Round($mem.TotalVisibleMemorySize / 1MB, 2)
$freeRAM = [math]::Round($mem.FreePhysicalMemory / 1MB, 2)
$usedRAM = $totalRAM - $freeRAM

"--- SYSTEM STATUS REPORT ---"
"RAM Usage: $usedRAM GB / $totalRAM GB"
"FREE RAM: $freeRAM GB"
""
"TOP 10 RAM PROCESSES:"
$processes | Format-Table -AutoSize
""
"DISK USAGE:"
$disks | Format-Table -AutoSize
