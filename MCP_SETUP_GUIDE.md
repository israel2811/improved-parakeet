# 🔱 NEXUS MCP SERVERS - GUÍA COMPLETA DE INSTALACIÓN Y USO

## 📋 Índice

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación](#instalación)
4. [Configuración](#configuración)
5. [Uso con Claude Desktop](#uso-con-claude-desktop)
6. [Reconstrucción de Conversaciones](#reconstrucción-de-conversaciones)
7. [Creación de Corpus Unificado](#creación-de-corpus-unificado)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Introducción

Este proyecto proporciona **servidores MCP (Model Context Protocol)** para integrar Dropbox, OneDrive y Google Drive con Claude Desktop, permitiendo:

- ✅ Lectura/escritura de archivos en las tres plataformas
- ✅ Reconstrucción de conversaciones exportadas de ChatGPT, Claude, Gemini, NotebookLM, Antigravity y Codex
- ✅ Conversión a formato unificado para análisis
- ✅ Creación de corpus completo multi-plataforma
- ✅ Análisis profundo por Claude Desktop

### 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE DESKTOP                            │
│                 (Análisis y Comprensión)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │ MCP Protocol
         ┌────────────┼────────────┐
         │            │            │
    ┌────▼───┐   ┌───▼────┐  ┌───▼──────┐
    │ GDrive │   │Dropbox │  │OneDrive  │
    │  MCP   │   │  MCP   │  │   MCP    │
    └────┬───┘   └───┬────┘  └───┬──────┘
         │           │           │
         └───────────┼───────────┘
                     │
         ┌───────────▼───────────┐
         │  Corpus Unifier       │
         │  (Python Script)      │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │ CORPUS UNIFICADO      │
         │ (JSON + HTML Viewer)  │
         └───────────────────────┘
```

---

## 📦 Requisitos Previos

### Software Necesario

- **Node.js** 18+ (para servidores MCP)
- **Python** 3.8+ (para scripts de unificación)
- **Claude Desktop** (última versión)
- **Git** (para clonar el repositorio)

### Cuentas Necesarias

1. **Dropbox**: Cuenta activa + App Token
2. **OneDrive**: Cuenta Microsoft + Azure AD App
3. **Google Drive**: Cuenta Google (configuración via MCP oficial)

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
cd ~
git clone https://github.com/israel2811/improved-parakeet.git
cd improved-parakeet
```

### 2. Instalar Dependencias de Dropbox MCP

```bash
cd mcp-servers/dropbox
npm install
cp .env.example .env
# Editar .env con tu token de Dropbox
```

### 3. Instalar Dependencias de OneDrive MCP

```bash
cd ../onedrive
npm install
cp .env.example .env
# Editar .env con tus credenciales de Azure
```

### 4. Instalar Dependencias de Python (Corpus Unifier)

```bash
cd ../..
pip install -r requirements.txt  # Si existe, o:
pip install python-dotenv
```

---

## ⚙️ Configuración

### 🔑 Obtener Credenciales

#### **DROPBOX**

1. Ve a https://www.dropbox.com/developers/apps
2. Crea una nueva app (Scoped Access)
3. En la pestaña "Permissions", activa:
   - `files.metadata.read`
   - `files.metadata.write`
   - `files.content.read`
   - `files.content.write`
4. Ve a "Settings" → "Generated access token"
5. Copia el token y añádelo a `mcp-servers/dropbox/.env`:

```env
DROPBOX_ACCESS_TOKEN=sl.xxxxxxxxxxxxxxxxxx
NEXUS_WORKSPACE=/Nexus
```

#### **ONEDRIVE**

1. Ve a https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps
2. Crea un nuevo "App registration"
3. En "Certificates & secrets", crea un "Client secret"
4. En "API permissions", añade:
   - `Files.ReadWrite.All`
   - `User.Read`
5. Copia Client ID, Client Secret y Tenant ID
6. Añádelos a `mcp-servers/onedrive/.env`:

```env
ONEDRIVE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
ONEDRIVE_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ONEDRIVE_TENANT_ID=common
NEXUS_WORKSPACE=/Nexus
```

#### **GOOGLE DRIVE**

Ya configurado vía el servidor MCP oficial: `@modelcontextprotocol/server-gdrive`

---

### 📝 Configurar Claude Desktop

#### **Windows**

Edita: `%APPDATA%\Claude\claude_desktop_config.json`

#### **macOS/Linux**

Edita: `~/.config/Claude/claude_desktop_config.json`

#### **Contenido del archivo:**

```json
{
  "mcpServers": {
    "google_drive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"]
    },
    "nexus_dropbox": {
      "command": "node",
      "args": ["C:/ruta/completa/improved-parakeet/mcp-servers/dropbox/index.js"],
      "env": {
        "DROPBOX_ACCESS_TOKEN": "tu_token_aqui",
        "NEXUS_WORKSPACE": "/Nexus"
      }
    },
    "nexus_onedrive": {
      "command": "node",
      "args": ["C:/ruta/completa/improved-parakeet/mcp-servers/onedrive/index.js"],
      "env": {
        "ONEDRIVE_CLIENT_ID": "tu_client_id",
        "ONEDRIVE_CLIENT_SECRET": "tu_secret",
        "ONEDRIVE_TENANT_ID": "common",
        "NEXUS_WORKSPACE": "/Nexus"
      }
    }
  }
}
```

**⚠️ IMPORTANTE**: Usa rutas absolutas, no relativas.

---

## 🎮 Uso con Claude Desktop

### 1. Reiniciar Claude Desktop

Cierra completamente Claude Desktop y vuelve a abrirlo.

### 2. Verificar Conexión

En Claude Desktop, escribe:

```
¿Qué servidores MCP están disponibles?
```

Deberías ver: `google_drive`, `nexus_dropbox`, `nexus_onedrive`

### 3. Listar Archivos

**Dropbox:**
```
Usa la herramienta dropbox_list_files para listar el contenido de /Nexus
```

**OneDrive:**
```
Usa la herramienta onedrive_list_files para listar el contenido de /Nexus
```

**Google Drive:**
```
Lista archivos en Google Drive en la carpeta Nexus
```

---

## 🔄 Reconstrucción de Conversaciones

### Flujo de Trabajo

1. **Exportar conversaciones** desde tus IAs:
   - ChatGPT: Settings → Data Controls → Export
   - Claude: (ya guardadas automáticamente)
   - Gemini: Exportar historial
   - NotebookLM: Descargar proyecto

2. **Subir a una plataforma** (Dropbox/OneDrive/Google Drive):
   ```
   Sube el archivo conversations_chatgpt.json a /Nexus/exports/ en Dropbox
   ```

3. **Reconstruir con Claude Desktop**:
   ```
   Usa dropbox_reconstruct_conversations:
   - source_path: /Nexus/exports/conversations_chatgpt.json
   - ai_type: chatgpt
   - output_path: /Nexus/reconstructed/chatgpt_clean.json
   ```

4. **Repetir para cada IA**:
   - ChatGPT → `chatgpt`
   - Claude → `claude`
   - Gemini → `gemini`
   - NotebookLM → `notebooklm`
   - Antigravity → `antigravity`
   - Codex → `codex`

---

## 🧩 Creación de Corpus Unificado

### Paso 1: Reconstruir en las 3 plataformas

```
1. Reconstruye todas las conversaciones de ChatGPT en Dropbox
2. Reconstruye todas las conversaciones de Claude en OneDrive
3. Reconstruye todas las conversaciones de Gemini en Google Drive
```

### Paso 2: Crear corpus por plataforma

**Dropbox:**
```
Usa dropbox_create_corpus:
- source_paths: [
    "/Nexus/reconstructed/chatgpt_clean.json",
    "/Nexus/reconstructed/claude_clean.json"
  ]
- output_path: /Nexus/corpus_dropbox.json
```

**OneDrive:**
```
Usa onedrive_create_corpus:
- source_paths: [
    "/Nexus/reconstructed/gemini_clean.json",
    "/Nexus/reconstructed/notebooklm_clean.json"
  ]
- output_path: /Nexus/corpus_onedrive.json
```

**Google Drive:**
```
Crea un corpus en Google Drive con las conversaciones de Antigravity y Codex
```

### Paso 3: Unificar con Python

```bash
cd scripts
python nexus_corpus_unifier.py
```

O desde Python:

```python
from nexus_corpus_unifier import NexusCorpusUnifier

unifier = NexusCorpusUnifier(output_dir="./unified_corpus")

# Añadir corpus de cada plataforma
unifier.add_corpus("./corpus_dropbox.json", "dropbox")
unifier.add_corpus("./corpus_onedrive.json", "onedrive")
unifier.add_corpus("./corpus_gdrive.json", "google_drive")

# Generar corpus unificado
unifier.save_unified_corpus()
unifier.generate_html_viewer()
```

### Paso 4: Analizar con Claude Desktop

```
Lee el archivo ./unified_corpus/corpus_unified.json y analízalo completamente.

Extrae:
1. Todas las ideas originales de Israel sobre neuroanatomía
2. Conceptos clave de comunicación auditiva (CCA)
3. Relaciones con anatomía y vocología (AAV)
4. Estructura propuesta para tesis doctoral
```

---

## 📊 Estructura del Corpus Unificado

```json
{
  "version": "1.0.0",
  "created_at": "2026-05-16T...",
  "system": "Nexus Omega",
  "owner": "Israel Realivazquez",
  "sources": {
    "google_drive": [...],
    "dropbox": [...],
    "onedrive": [...]
  },
  "statistics": {
    "total_conversations": 150,
    "total_messages": 5847,
    "total_sources": 3,
    "ai_types": {
      "chatgpt": 45,
      "claude": 38,
      "gemini": 32,
      "notebooklm": 15,
      "antigravity": 12,
      "codex": 8
    }
  },
  "conversations": [
    {
      "metadata": {
        "ai_type": "chatgpt",
        "source_platform": "dropbox",
        "reconstructed_at": "...",
        "original_file": "..."
      },
      "messages": [
        {
          "role": "user",
          "content": "...",
          "timestamp": "...",
          "id": "..."
        },
        {
          "role": "assistant",
          "content": "...",
          "timestamp": "...",
          "id": "..."
        }
      ]
    }
  ],
  "analysis_metadata": {
    "claude_analysis_ready": true,
    "recommended_approach": "sequential_conversation_analysis",
    "chunking_strategy": {...},
    "analysis_prompts": [...]
  }
}
```

---

## 🐛 Troubleshooting

### Error: "MCP server not found"

**Solución:**
1. Verifica que las rutas en `claude_desktop_config.json` sean **absolutas**
2. Verifica que los servidores estén instalados (`npm install` en cada carpeta)
3. Reinicia Claude Desktop completamente

### Error: "DROPBOX_ACCESS_TOKEN not configured"

**Solución:**
1. Verifica que el archivo `.env` existe en `mcp-servers/dropbox/`
2. Verifica que el token es válido (no expirado)
3. Si usas variables de entorno en el config, asegúrate de que estén definidas

### Error: "Authentication failed" (OneDrive)

**Solución:**
1. Verifica que las credenciales en `.env` son correctas
2. Verifica que la app de Azure tiene los permisos correctos
3. Verifica que el Client Secret no ha expirado
4. Intenta usar `ONEDRIVE_TENANT_ID=common` si tienes cuenta personal

### Claude Desktop no muestra herramientas

**Solución:**
1. Ve a Settings → Developer → MCP Servers
2. Verifica que los servidores están "Connected" (verde)
3. Si están en rojo, revisa los logs de Claude Desktop
4. Reinicia Claude Desktop con Ctrl+Shift+R (o Cmd+Shift+R en Mac)

### Error: "Cannot find module @modelcontextprotocol/sdk"

**Solución:**
```bash
cd mcp-servers/dropbox  # o onedrive
rm -rf node_modules package-lock.json
npm install
```

---

## 🎯 Casos de Uso Avanzados

### 1. Sincronización Automática Diaria

Crea un script que:
1. Exporta nuevas conversaciones de cada IA
2. Las sube a las plataformas cloud
3. Ejecuta reconstrucción automática
4. Actualiza el corpus unificado

### 2. Análisis Temático por IA

```python
# Analizar qué IA usaste más para qué temas
for conv in corpus['conversations']:
    ai_type = conv['metadata']['ai_type']
    # Analizar contenido y categorizar
```

### 3. Búsqueda Semántica

Integrar con embeddings de OpenAI o Claude para búsqueda semántica en el corpus.

### 4. Exportación a Obsidian/Notion

Convertir el corpus a formato Markdown para importar en Obsidian o Notion.

---

## 📚 Recursos Adicionales

- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [Dropbox API Docs](https://www.dropbox.com/developers/documentation)
- [Microsoft Graph API Docs](https://docs.microsoft.com/en-us/graph/)
- [Claude Desktop MCP Guide](https://docs.anthropic.com/claude/docs/mcp)

---

## 🔱 Soporte y Contribuciones

**Autor**: Israel Realivazquez  
**Email**: israel.realivazquez@gmail.com  
**Proyecto**: Nexus Omega - PhD Research Orchestrator

Para reportar bugs o sugerir mejoras, abre un issue en el repositorio.

---

## 📄 Licencia

Apache 2.0 License - Ver archivo LICENSE para más detalles.

---

**🔱 NEXUS OMEGA - Arquitectura de Conocimiento Distribuido**
