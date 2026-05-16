#!/bin/bash

# 🔱 SCRIPT DE AUTO-SETUP
# Este script hace TODO lo que puede hacer automáticamente

echo "🔱 NEXUS AUTO-SETUP"
echo "=================="
echo ""

cd /home/user/improved-parakeet

# Generar config de Claude Desktop
echo "📝 Generando configuración de Claude Desktop..."

python3 << 'PYTHON_SCRIPT'
import json
from pathlib import Path

base = Path("/home/user/improved-parakeet")

config = {
    "mcpServers": {
        "google_drive": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-gdrive"]
        }
    }
}

# Dropbox
dropbox_env = base / "mcp-servers/dropbox/.env"
if dropbox_env.exists():
    print("✅ Dropbox configurado")
    with open(dropbox_env) as f:
        for line in f:
            if "TOKEN" in line:
                token = line.split('=')[1].strip()
                config["mcpServers"]["nexus_dropbox"] = {
                    "command": "node",
                    "args": [str(base / "mcp-servers/dropbox/index.js")],
                    "env": {"DROPBOX_ACCESS_TOKEN": token, "NEXUS_WORKSPACE": "/Nexus"}
                }
else:
    print("⚠️  Dropbox no configurado (falta .env)")

# OneDrive
onedrive_env = base / "mcp-servers/onedrive/.env"
if onedrive_env.exists():
    print("✅ OneDrive configurado")
    with open(onedrive_env) as f:
        lines = f.readlines()
        try:
            client_id = [l.split('=')[1].strip() for l in lines if 'CLIENT_ID' in l][0]
            client_secret = [l.split('=')[1].strip() for l in lines if 'SECRET' in l][0]
            config["mcpServers"]["nexus_onedrive"] = {
                "command": "node",
                "args": [str(base / "mcp-servers/onedrive/index.js")],
                "env": {
                    "ONEDRIVE_CLIENT_ID": client_id,
                    "ONEDRIVE_CLIENT_SECRET": client_secret,
                    "ONEDRIVE_TENANT_ID": "common",
                    "NEXUS_WORKSPACE": "/Nexus"
                }
            }
        except:
            print("⚠️  OneDrive .env incompleto")
else:
    print("⚠️  OneDrive no configurado (opcional)")

# Guardar
with open("claude_desktop_config_READY.json", 'w') as f:
    json.dump(config, f, indent=2)

print("\n✅ CONFIG GENERADA: claude_desktop_config_READY.json")
print("\n📋 CONTENIDO:")
print(json.dumps(config, indent=2))
PYTHON_SCRIPT

echo ""
echo "✅ Setup automático completado"
echo ""
echo "📝 SIGUIENTE PASO:"
echo "   Copia el contenido de claude_desktop_config_READY.json"
echo "   a tu archivo de configuración de Claude Desktop"
echo ""
echo "📂 Ubicaciones:"
echo "   Windows: %APPDATA%\Claude\claude_desktop_config.json"
echo "   macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   Linux: ~/.config/Claude/claude_desktop_config.json"
echo ""
