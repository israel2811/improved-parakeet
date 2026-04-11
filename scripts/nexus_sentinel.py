import subprocess
import os
import time
import json

# 🔱 NEXUS SENTINEL (V1.2 - BUDGET OPTIMIZED)
# Mantenimiento automático local. La nube se despierta BAJO DEMANDA.

PROJECT_DIR = r"C:\Users\Lenovo\Dropbox\improved-parakeet"
PURGE_SCRIPT = os.path.join(PROJECT_DIR, "scripts", "nexus_disk_purge.ps1")

def run_purge():
    print("[*] Running Disk Purge...")
    try:
        subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", PURGE_SCRIPT], check=True)
    except Exception as e:
        print(f"[!] Purge failed: {e}")

def main():
    while True:
        # Solo purga localmente para mantener el disco sano.
        # No despierta la nube automáticamente para ahorrar créditos (4 cores = 4x consumo).
        run_purge()
        print("[*] Sentinel sleeping for 1 hour...")
        time.sleep(3600)

if __name__ == "__main__":
    main()
