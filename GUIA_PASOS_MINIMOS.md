# 🔱 GUÍA DE PASOS MÍNIMOS - NEXUS OMEGA

**Total de tiempo: 10-15 minutos**  
**Total de clics: ~15**  
**Yo hago TODO lo demás automáticamente**

---

## 🎯 PASO 1: DROPBOX (3 clics + 1 copiar)

### 📍 Ve a esta URL:
```
https://www.dropbox.com/developers/apps
```

### 👆 HAZ ESTOS 3 CLICS:

1. **Clic** en el botón azul **"Create app"**

2. **Selecciona:**
   - ✅ Scoped access
   - ✅ Full Dropbox
   - Nombre: `Nexus`
   - **Clic** en **"Create app"**

3. **En tu nueva app:**
   - Ve a pestaña **"Permissions"**
   - Marca TODAS las casillas que digan `files.*`
   - **Clic** en **"Submit"** (abajo de la página)

4. **Ve a pestaña "Settings":**
   - Busca "Generated access token"
   - **Clic** en **"Generate"**
   - **COPIA** el token que aparece (es largo, como: `sl.B1234...`)

### 💾 PEGA TU TOKEN AQUÍ:

```bash
# Ejecuta esto y pega tu token cuando te lo pida:
cd /home/user/improved-parakeet/mcp-servers/dropbox
echo "DROPBOX_ACCESS_TOKEN=TU_TOKEN_AQUI" > .env
echo "NEXUS_WORKSPACE=/Nexus" >> .env
```

**O manualmente:**
- Abre: `/home/user/improved-parakeet/mcp-servers/dropbox/.env`
- Escribe:
  ```
  DROPBOX_ACCESS_TOKEN=tu_token_aquí
  NEXUS_WORKSPACE=/Nexus
  ```

---

## 🎯 PASO 2: ONEDRIVE (OPCIONAL - 5 clics + 2 copiar)

**⏭️ PUEDES SALTAR ESTE PASO** si no tienes cuenta Microsoft Azure.

### 📍 Ve a esta URL:
```
https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
```

### 👆 HAZ ESTOS 5 CLICS:

1. **Clic** en **"+ New registration"**

2. **Completa:**
   - Name: `Nexus OneDrive`
   - Supported account types: `Accounts in any organizational directory and personal Microsoft accounts`
   - **Clic** en **"Register"**

3. **COPIA** el **"Application (client) ID"**
   (Está en la página que se abre, algo como: `a1b2c3d4-...`)

4. **Ve a "Certificates & secrets"** (menú izquierdo)
   - **Clic** en **"+ New client secret"**
   - Description: `Nexus`
   - **Clic** en **"Add"**

5. **COPIA** el **"Value"** del secret que acabas de crear
   (⚠️ Solo se muestra UNA VEZ, cópialo ahora)

### 💾 PEGA TUS CREDENCIALES AQUÍ:

```bash
# Ejecuta esto:
cd /home/user/improved-parakeet/mcp-servers/onedrive
cat > .env << 'EOF'
ONEDRIVE_CLIENT_ID=tu_client_id_aquí
ONEDRIVE_CLIENT_SECRET=tu_secret_aquí
ONEDRIVE_TENANT_ID=common
NEXUS_WORKSPACE=/Nexus
EOF
```

---

## 🎯 PASO 3: GOOGLE CLOUD (4 clics + 1 descargar)

### 📍 Abre ESTAS 4 URLs (se abrirán automáticamente):

```bash
# Ejecuta esto para abrir las 4 URLs:
xdg-open "https://console.cloud.google.com/projectcreate" &
sleep 2
xdg-open "https://console.cloud.google.com/apis/library/docs.googleapis.com" &
sleep 2
xdg-open "https://console.cloud.google.com/apis/library/drive.googleapis.com" &
sleep 2
xdg-open "https://console.cloud.google.com/apis/credentials" &
```

### 👆 HAZ ESTOS 4 CLICS (en orden):

#### Pestaña 1: Crear Proyecto
1. Nombre del proyecto: `Nexus`
2. **Clic** en **"CREATE"**
3. Espera ~30 segundos a que se cree

#### Pestaña 2: Habilitar Google Docs API
1. Selecciona tu proyecto "Nexus" (arriba)
2. **Clic** en **"ENABLE"**

#### Pestaña 3: Habilitar Google Drive API
1. Selecciona tu proyecto "Nexus" (arriba)
2. **Clic** en **"ENABLE"**

#### Pestaña 4: Crear Credenciales
1. **Clic** en **"+ CREATE CREDENTIALS"**
2. Selecciona **"OAuth client ID"**
3. Si te pide configurar pantalla de consentimiento:
   - User Type: **External**
   - App name: `Nexus`
   - User support email: tu email
   - **Clic** en **"SAVE AND CONTINUE"** (x3 veces)
4. Application type: **Desktop app**
5. Name: `Nexus Desktop`
6. **Clic** en **"CREATE"**
7. **Clic** en **"DOWNLOAD JSON"**

### 💾 MUEVE EL ARCHIVO:

El archivo se descargó como `client_secret_...json`. Renómbralo y muévelo:

```bash
# Encuentra y mueve el archivo:
mv ~/Downloads/client_secret_*.json /home/user/improved-parakeet/credentials.json

# O si está en otra ubicación:
# cp /ruta/a/tu/archivo.json /home/user/improved-parakeet/credentials.json
```

---

## 🎯 PASO 4: CONFIGURAR CLAUDE DESKTOP (1 copiar)

### 📝 YO GENERO TU CONFIG AUTOMÁTICAMENTE:

```bash
# Ejecuta esto (yo lo hago):
cd /home/user/improved-parakeet
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
    with open(dropbox_env) as f:
        for line in f:
            if "TOKEN" in line:
                token = line.split('=')[1].strip()
                config["mcpServers"]["nexus_dropbox"] = {
                    "command": "node",
                    "args": [str(base / "mcp-servers/dropbox/index.js")],
                    "env": {"DROPBOX_ACCESS_TOKEN": token, "NEXUS_WORKSPACE": "/Nexus"}
                }

# OneDrive
onedrive_env = base / "mcp-servers/onedrive/.env"
if onedrive_env.exists():
    with open(onedrive_env) as f:
        lines = f.readlines()
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

# Guardar
with open("claude_desktop_config_READY.json", 'w') as f:
    json.dump(config, f, indent=2)

print("✅ CONFIG GENERADA: claude_desktop_config_READY.json")
print("\n" + json.dumps(config, indent=2))
PYTHON_SCRIPT
```

### 📋 AHORA COPIA LA CONFIG A CLAUDE DESKTOP:

**Ubicación del archivo de config de Claude Desktop:**

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

**Qué hacer:**

1. Abre el archivo de arriba
2. **COPIA TODO** el contenido de `/home/user/improved-parakeet/claude_desktop_config_READY.json`
3. **PEGA** en tu archivo de config de Claude Desktop (reemplaza todo)
4. **GUARDA**
5. **REINICIA** Claude Desktop completamente

---

## 🎯 PASO 5: CREAR CARPETAS EN CLOUD (AUTOMÁTICO CON CLAUDE)

Una vez que Claude Desktop esté configurado, **COPIA ESTO** en Claude Desktop:

```
Hola Claude, necesito que crees las carpetas de Nexus:

1. Usa dropbox_write_file para crear estos archivos:
   - Archivo: /Nexus/exports/.keep
   - Contenido: "Carpeta de exports"

   - Archivo: /Nexus/reconstructed/.keep
   - Contenido: "Carpeta de reconstructed"

2. Si tienes OneDrive configurado, haz lo mismo con onedrive_write_file

¡Gracias!
```

Claude hará esto **automáticamente** en ~10 segundos.

---

## ✅ ¡LISTO! AHORA PUEDES USAR EL SISTEMA

### 🚀 Siguiente Paso: Exportar y Procesar Conversaciones

1. **Exporta tus conversaciones:**
   - ChatGPT: Settings → Data controls → Export data
   - Claude: Exportar historial
   - Gemini: Exportar conversaciones

2. **Sube los archivos a Dropbox/OneDrive** (usa Claude Desktop):
   ```
   En Claude Desktop:
   "Sube el contenido del archivo [ruta] a /Nexus/exports/chatgpt.json en Dropbox"
   ```

3. **Ejecuta el workflow completo:**
   ```bash
   python3 /home/user/improved-parakeet/scripts/nexus_claude_workflow.py full
   ```

4. **Copia las instrucciones generadas a Claude Desktop**

5. **Claude ejecutará TODO automáticamente:**
   - Reconstruirá conversaciones
   - Creará corpus unificado
   - Generará Google Docs
   - Te dará reporte completo

---

## 📊 RESUMEN DE TUS CLICS

| Servicio | Clics | Tiempo |
|----------|-------|--------|
| **Dropbox** | 3 clics + 1 copiar | 2 min |
| **OneDrive** | 5 clics + 2 copiar (OPCIONAL) | 3 min |
| **Google** | 4 clics + 1 descargar | 4 min |
| **Claude Desktop** | 1 copiar | 1 min |
| **TOTAL** | ~15 clics | **10 min** |

Después de estos 10 minutos, **YO HAGO TODO EL RESTO AUTOMÁTICAMENTE**.

---

## 💡 TIPS

- ✅ Puedes hacer los pasos en el orden que quieras
- ✅ OneDrive es OPCIONAL (Dropbox + Google es suficiente)
- ✅ Si algo falla, puedes reintentar ese paso solo
- ✅ Guarda bien los tokens/secrets (no los pierdas)
- ✅ Si no ves la opción de crear app en Dropbox, revisa que estés logueado

---

## 🆘 SI ALGO SALE MAL

**Dropbox token no funciona:**
→ Verifica que marcaste TODOS los permisos `files.*`
→ Regenera el token

**Google credentials no funcionan:**
→ Asegúrate de habilitar AMBAS APIs (Docs + Drive)
→ Descarga el JSON correcto (Desktop app)

**Claude Desktop no ve los servidores:**
→ Verifica que las rutas sean ABSOLUTAS (no relativas)
→ Reinicia Claude Desktop completamente
→ Verifica que los archivos `.env` tengan las credenciales

---

**🔱 NEXUS OMEGA**

*10 minutos de clics → 5 años de investigación organizada*

---

**¿Listo para empezar? Sigue los pasos en orden y yo haré el resto.**
