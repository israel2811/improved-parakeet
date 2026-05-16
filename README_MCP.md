# 🔱 NEXUS MCP SERVERS

**Servidores MCP para integración multi-plataforma con Claude Desktop**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

## 🎯 ¿Qué es esto?

Este proyecto proporciona **servidores MCP (Model Context Protocol)** que permiten a **Claude Desktop** acceder directamente a tus archivos en:

- 📦 **Dropbox**
- ☁️ **OneDrive**
- 📁 **Google Drive**

Además, incluye herramientas para:

- 🔄 **Reconstruir conversaciones** exportadas de ChatGPT, Claude, Gemini, NotebookLM, Antigravity y Codex
- 📊 **Unificar corpus** de múltiples plataformas en un solo archivo analizable
- 🎨 **Visualizar** conversaciones en un visor HTML interactivo
- 🧠 **Analizar** todo tu historial con Claude Desktop

## 🚀 Instalación Rápida

### Opción 1: Script Automático (Recomendado)

**Linux/macOS:**
```bash
cd improved-parakeet
chmod +x install_mcp_servers.sh
./install_mcp_servers.sh
```

**Windows (PowerShell):**
```powershell
cd improved-parakeet
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install_mcp_servers.ps1
```

### Opción 2: Instalación Manual

```bash
# 1. Instalar Dropbox MCP
cd mcp-servers/dropbox
npm install
cp .env.example .env
# Editar .env con tu token

# 2. Instalar OneDrive MCP
cd ../onedrive
npm install
cp .env.example .env
# Editar .env con tus credenciales

# 3. Instalar dependencias Python
cd ../..
pip install python-dotenv
```

## ⚙️ Configuración

### 1. Obtener Credenciales

#### Dropbox
1. Ve a https://www.dropbox.com/developers/apps
2. Crea una app con "Scoped Access"
3. Activa permisos: `files.*`
4. Genera un token de acceso
5. Copia a `mcp-servers/dropbox/.env`

#### OneDrive
1. Ve a https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps
2. Crea un "App registration"
3. Crea un "Client secret"
4. Añade permisos API: `Files.ReadWrite.All`
5. Copia credenciales a `mcp-servers/onedrive/.env`

### 2. Configurar Claude Desktop

**Ubicación del archivo de configuración:**
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

**Añade los servidores:**

```json
{
  "mcpServers": {
    "google_drive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"]
    },
    "nexus_dropbox": {
      "command": "node",
      "args": ["/ruta/completa/improved-parakeet/mcp-servers/dropbox/index.js"],
      "env": {
        "DROPBOX_ACCESS_TOKEN": "tu_token_aqui"
      }
    },
    "nexus_onedrive": {
      "command": "node",
      "args": ["/ruta/completa/improved-parakeet/mcp-servers/onedrive/index.js"],
      "env": {
        "ONEDRIVE_CLIENT_ID": "tu_client_id",
        "ONEDRIVE_CLIENT_SECRET": "tu_secret"
      }
    }
  }
}
```

⚠️ **IMPORTANTE:** Usa rutas **absolutas**, no relativas.

### 3. Reiniciar Claude Desktop

Cierra completamente Claude Desktop y vuelve a abrirlo.

## 📚 Uso

### Comandos Básicos en Claude Desktop

#### Listar Archivos
```
Usa dropbox_list_files para listar archivos en /Nexus
```

#### Leer Archivo
```
Usa dropbox_read_file para leer /Nexus/mi_documento.txt
```

#### Escribir Archivo
```
Usa onedrive_write_file para escribir contenido en /Nexus/nuevo.txt
```

#### Buscar Archivos
```
Usa onedrive_search para buscar archivos que contengan "neuroanatomía"
```

### Reconstrucción de Conversaciones

#### Paso 1: Exportar desde tus IAs

- **ChatGPT:** Settings → Data Controls → Export
- **Claude:** (ya guardadas automáticamente)
- **Gemini:** Exportar historial
- **NotebookLM:** Descargar proyecto

#### Paso 2: Subir a la nube

```
Sube conversations.json a /Nexus/exports/ en Dropbox
```

#### Paso 3: Reconstruir

```
Usa dropbox_reconstruct_conversations:
- source_path: /Nexus/exports/conversations.json
- ai_type: chatgpt
- output_path: /Nexus/reconstructed/chatgpt_clean.json
```

### Crear Corpus Unificado

#### En Claude Desktop:

```
1. Usa dropbox_create_corpus con todos los archivos reconstructed
2. Usa onedrive_create_corpus con los demás archivos
3. Descarga ambos corpus
```

#### Con Python:

```bash
cd scripts
python nexus_corpus_unifier.py
```

O programáticamente:

```python
from nexus_corpus_unifier import NexusCorpusUnifier

unifier = NexusCorpusUnifier()
unifier.add_corpus("corpus_dropbox.json", "dropbox")
unifier.add_corpus("corpus_onedrive.json", "onedrive")
unifier.add_corpus("corpus_gdrive.json", "google_drive")
unifier.save_unified_corpus()
unifier.generate_html_viewer()
```

### Analizar con Claude

```
Lee ./nexus_unified_corpus/corpus_unified.json

Analiza todo el contenido y:
1. Extrae ideas originales de Israel sobre neuroanatomía
2. Identifica conceptos de comunicación auditiva
3. Relaciona con vocología sistémica
4. Propone estructura de tesis doctoral
```

## 📊 Estructura del Proyecto

```
improved-parakeet/
├── mcp-servers/
│   ├── dropbox/
│   │   ├── index.js           # Servidor MCP Dropbox
│   │   ├── package.json
│   │   └── .env.example
│   └── onedrive/
│       ├── index.js           # Servidor MCP OneDrive
│       ├── package.json
│       └── .env.example
├── scripts/
│   ├── nexus_corpus_unifier.py    # Unificador de corpus
│   └── nexus_reconstructor_v3.py  # Reconstructor HTML
├── MCP_SETUP_GUIDE.md             # Guía completa
├── claude_desktop_config_full.json # Config de referencia
├── install_mcp_servers.sh         # Instalador Linux/macOS
├── install_mcp_servers.ps1        # Instalador Windows
└── README_MCP.md                  # Este archivo
```

## 🔧 Herramientas Disponibles

### Dropbox MCP

- `dropbox_list_files` - Listar archivos y carpetas
- `dropbox_read_file` - Leer contenido de archivos
- `dropbox_write_file` - Escribir/actualizar archivos
- `dropbox_search` - Buscar archivos
- `dropbox_reconstruct_conversations` - Reconstruir conversaciones IA
- `dropbox_create_corpus` - Crear corpus unificado

### OneDrive MCP

- `onedrive_list_files` - Listar archivos y carpetas
- `onedrive_read_file` - Leer contenido de archivos
- `onedrive_write_file` - Escribir/actualizar archivos
- `onedrive_search` - Buscar archivos
- `onedrive_reconstruct_conversations` - Reconstruir conversaciones IA
- `onedrive_create_corpus` - Crear corpus unificado
- `onedrive_sync_with_gdrive` - Sincronizar con Google Drive

### Corpus Unifier (Python)

- `add_corpus()` - Añadir corpus de una plataforma
- `save_unified_corpus()` - Guardar corpus unificado
- `generate_html_viewer()` - Generar visor HTML interactivo
- `calculate_statistics()` - Calcular estadísticas

## 🎨 Formatos Soportados

### Conversaciones IA

- ✅ ChatGPT (JSON export)
- ✅ Claude (JSON export)
- ✅ Gemini (JSON export)
- ✅ NotebookLM (project export)
- ✅ Antigravity (custom format)
- ✅ OpenAI Codex (completions)

### Archivos

- ✅ JSON
- ✅ TXT
- ✅ Markdown (MD)
- ✅ HTML
- ✅ DOCX (OneDrive)

## 🐛 Troubleshooting

### "MCP server not found"
- ✅ Verifica rutas **absolutas** en config
- ✅ Ejecuta `npm install` en cada carpeta
- ✅ Reinicia Claude Desktop

### "DROPBOX_ACCESS_TOKEN not configured"
- ✅ Verifica que `.env` existe
- ✅ Verifica que el token no ha expirado
- ✅ Regenera token si es necesario

### "Authentication failed" (OneDrive)
- ✅ Verifica credenciales en `.env`
- ✅ Verifica permisos de la app Azure
- ✅ Verifica que el secret no ha expirado

### Claude Desktop no muestra herramientas
- ✅ Settings → Developer → MCP Servers
- ✅ Verifica que están "Connected" (verde)
- ✅ Reinicia con Ctrl+Shift+R

**Ver guía completa:** [MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)

## 📖 Documentación Adicional

- **[Guía Completa de Instalación](MCP_SETUP_GUIDE.md)** - Instrucciones detalladas paso a paso
- **[MCP Protocol Docs](https://modelcontextprotocol.io/)** - Documentación oficial del protocolo
- **[Dropbox API](https://www.dropbox.com/developers/documentation)** - API de Dropbox
- **[Microsoft Graph](https://docs.microsoft.com/en-us/graph/)** - API de OneDrive

## 🤝 Contribuciones

Este es un proyecto de investigación doctoral. Si encuentras bugs o tienes sugerencias:

1. Abre un issue en el repositorio
2. Describe el problema claramente
3. Incluye logs/screenshots si es posible

## 👨‍🎓 Autor

**Israel Realivazquez**  
PhD Candidate - Neuroanatomía, Comunicación Auditiva, Vocología  
📧 israel.realivazquez@gmail.com

## 📄 Licencia

Apache 2.0 License - Ver [LICENSE](LICENSE) para más detalles.

---

## 🎯 Caso de Uso: Tesis Doctoral

Este proyecto fue creado para:

1. **Recopilar** todas las conversaciones con IAs durante la investigación doctoral
2. **Reconstruir** y unificar 5+ años de diálogos sobre neuroanatomía
3. **Analizar** con Claude Desktop para extraer insights
4. **Sintetizar** en estructura coherente de tesis

### Resultados Esperados

- ✅ Corpus unificado de 100+ conversaciones
- ✅ 5,000+ mensajes reconstructed
- ✅ Análisis semántico completo
- ✅ Estructura de tesis generada
- ✅ Bibliografía APA7 automatizada

---

**🔱 NEXUS OMEGA - Arquitectura de Conocimiento Distribuido**

*"El conocimiento disperso, unificado. La consciencia fragmentada, reconstruida."*
