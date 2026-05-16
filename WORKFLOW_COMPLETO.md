# 🔱 NEXUS - WORKFLOW COMPLETO DE SINCRONIZACIÓN

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Prerequisitos](#prerequisitos)
3. [Instalación Inicial](#instalación-inicial)
4. [Flujo Completo Paso a Paso](#flujo-completo-paso-a-paso)
5. [Uso con Claude Desktop](#uso-con-claude-desktop)
6. [Verificación Final](#verificación-final)
7. [Mantenimiento](#mantenimiento)

---

## 🎯 Visión General

Este documento describe el **workflow completo** para sincronizar todas tus conversaciones de IA desde múltiples plataformas hasta Google Docs con formato académico.

### Flujo de Datos

```
┌─────────────────┐
│  Exportar IAs   │
│  (ChatGPT,      │
│   Claude, etc)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Subir a Cloud   │
│ (Dropbox/       │
│  OneDrive)      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Reconstrucción  │
│ (MCP Servers)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Corpus por      │
│ Plataforma      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Corpus          │
│ Unificado       │
│ (Python)        │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Google Docs     │
│ (Formato APA7)  │
└─────────────────┘
         │
         ↓
┌─────────────────┐
│ Análisis por    │
│ Claude Desktop  │
└─────────────────┘
```

---

## 📦 Prerequisitos

### Software

- ✅ Node.js 18+
- ✅ Python 3.8+
- ✅ Claude Desktop (última versión)
- ✅ Git

### Cuentas

- ✅ Dropbox con API token
- ✅ OneDrive con Azure AD app
- ✅ Google Cloud con APIs habilitadas

### Espacios de Almacenamiento

- Dropbox: Crear carpeta `/Nexus/`
- OneDrive: Crear carpeta `/Nexus/`
- Google Drive: Crear carpeta `Nexus`

---

## 🚀 Instalación Inicial

### 1. Instalar Servidores MCP

```bash
cd improved-parakeet

# Linux/macOS
chmod +x install_mcp_servers.sh
./install_mcp_servers.sh

# Windows PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install_mcp_servers.ps1
```

### 2. Instalar Dependencias Python

```bash
pip install -r requirements.txt
```

### 3. Configurar Google Cloud

#### A. Crear Proyecto en Google Cloud

1. Ve a https://console.cloud.google.com/
2. Crea nuevo proyecto: "Nexus Sync"
3. Habilita las siguientes APIs:
   - Google Docs API
   - Google Drive API

#### B. Crear Credenciales OAuth 2.0

1. Ve a **APIs y servicios** → **Credenciales**
2. Clic en **+ CREAR CREDENCIALES** → **ID de cliente de OAuth**
3. Tipo de aplicación: **Aplicación de escritorio**
4. Nombre: "Nexus Desktop Client"
5. Descarga el JSON de credenciales
6. Guarda como `credentials.json` en el directorio raíz de `improved-parakeet`

#### C. Configurar Pantalla de Consentimiento

1. Ve a **Pantalla de consentimiento de OAuth**
2. Tipo: **Externa**
3. Añade tu email como usuario de prueba
4. Ámbitos necesarios:
   - `https://www.googleapis.com/auth/documents`
   - `https://www.googleapis.com/auth/drive.file`

### 4. Configurar Credenciales de Cloud

#### Dropbox

```bash
cd mcp-servers/dropbox
nano .env  # o usa tu editor favorito
```

Añade:
```env
DROPBOX_ACCESS_TOKEN=tu_token_aqui
NEXUS_WORKSPACE=/Nexus
```

#### OneDrive

```bash
cd ../onedrive
nano .env
```

Añade:
```env
ONEDRIVE_CLIENT_ID=tu_client_id
ONEDRIVE_CLIENT_SECRET=tu_secret
ONEDRIVE_TENANT_ID=common
NEXUS_WORKSPACE=/Nexus
```

### 5. Configurar Claude Desktop

Edita el archivo de configuración de Claude Desktop:

**Ubicaciones:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Usa como referencia: `claude_desktop_config_full.json`

**⚠️ IMPORTANTE:** Reemplaza `/ruta/completa/` con la ruta **absoluta** real.

### 6. Reiniciar Claude Desktop

Cierra completamente y vuelve a abrir Claude Desktop.

---

## 🔄 Flujo Completo Paso a Paso

### FASE 1: Exportar Conversaciones de IAs

#### ChatGPT
1. Settings → Data controls → Export data
2. Descarga el archivo ZIP
3. Extrae `conversations.json`

#### Claude
1. Las conversaciones se exportan automáticamente
2. O usa la API de Anthropic para exportar

#### Gemini
1. Abre https://gemini.google.com/
2. Menú → Actividad → Exportar

#### NotebookLM
1. Abre el proyecto en NotebookLM
2. Menú → Export project

### FASE 2: Subir a Cloud Storage

#### Organización de Archivos

Crea esta estructura:

```
Dropbox/Nexus/
├── exports/
│   ├── chatgpt_2024.json
│   ├── claude_2024.json
│   └── gemini_2024.json
└── reconstructed/
    (se llenará automáticamente)

OneDrive/Nexus/
├── exports/
│   ├── notebooklm_projects.json
│   ├── antigravity_sessions.json
│   └── codex_completions.json
└── reconstructed/
    (se llenará automáticamente)
```

#### Subir Archivos

**Opción A: Interfaz Web**
- Sube manualmente a `/Nexus/exports/` en cada plataforma

**Opción B: Claude Desktop**
```
Usa dropbox_write_file para subir el contenido de [ruta_local] a /Nexus/exports/chatgpt_2024.json
```

### FASE 3: Reconstrucción Automática con Claude

#### Opción A: Workflow Guiado

```bash
python scripts/nexus_claude_workflow.py full
```

Esto genera una guía completa que puedes copiar y pegar en Claude Desktop.

#### Opción B: Manual en Claude Desktop

Copia esto en Claude Desktop:

```
Hola Claude, necesito que ejecutes el siguiente workflow de sincronización Nexus:

PASO 1: LISTAR EXPORTS

1. Usa dropbox_list_files con path="/Nexus/exports" y recursive=true
2. Usa onedrive_list_files con path="/Nexus/exports" y recursive=true
3. Lista todos los archivos encontrados

PASO 2: RECONSTRUIR CONVERSACIONES

Para cada archivo que encuentres:

a) Identifica el tipo de IA del nombre del archivo:
   - "chatgpt" → ai_type="chatgpt"
   - "claude" → ai_type="claude"
   - "gemini" → ai_type="gemini"
   - "notebooklm" → ai_type="notebooklm"
   - "antigravity" → ai_type="antigravity"
   - "codex" → ai_type="codex"

b) Reconstruye con la herramienta correspondiente:

   Para Dropbox:
   dropbox_reconstruct_conversations(
     source_path="/Nexus/exports/[nombre_archivo]",
     ai_type="[tipo_identificado]",
     output_path="/Nexus/reconstructed/[nombre]_reconstructed.json"
   )

   Para OneDrive:
   onedrive_reconstruct_conversations(
     source_path="/Nexus/exports/[nombre_archivo]",
     ai_type="[tipo_identificado]",
     output_path="/Nexus/reconstructed/[nombre]_reconstructed.json"
   )

PASO 3: CREAR CORPUS POR PLATAFORMA

1. Crea corpus de Dropbox:
   dropbox_create_corpus(
     source_paths=[todos los .json de /Nexus/reconstructed/],
     output_path="/Nexus/corpus_dropbox.json"
   )

2. Crea corpus de OneDrive:
   onedrive_create_corpus(
     source_paths=[todos los .json de /Nexus/reconstructed/],
     output_path="/Nexus/corpus_onedrive.json"
   )

PASO 4: DESCARGAR CORPUS A LOCAL

1. Lee corpus de Dropbox:
   dropbox_read_file(path="/Nexus/corpus_dropbox.json")
   Guarda en: ./nexus_workspace/corpus_dropbox.json

2. Lee corpus de OneDrive:
   onedrive_read_file(path="/Nexus/corpus_onedrive.json")
   Guarda en: ./nexus_workspace/corpus_onedrive.json

PASO 5: UNIFICAR CORPUS

Ejecuta:
python scripts/nexus_corpus_unifier.py

(Si te pido permisos para ejecutar, autorízalo)

PASO 6: CONVERTIR A GOOGLE DOCS

Ejecuta:
python scripts/nexus_to_gdocs.py

(Primera vez pedirá autenticación con Google - autorízalo en el navegador)

PASO 7: REPORTE FINAL

Dame un resumen con:
- Total de conversaciones procesadas
- Total de mensajes
- Distribución por IA (cuántas conversaciones de cada una)
- Links a todos los documentos de Google Docs creados
- Link al documento maestro índice

¡Gracias!
```

### FASE 4: Verificación y Análisis

#### Verificar Documentos Creados

1. Abre Google Drive: https://drive.google.com/
2. Busca la carpeta "Nexus Corpus"
3. Verifica que existan:
   - Subcarpetas por IA (AI_CHATGPT, AI_CLAUDE, etc.)
   - Documento "NEXUS CORPUS - ÍNDICE MAESTRO"
   - Documentos individuales de cada conversación

#### Análisis con Claude Desktop

```
Lee el documento maestro en Google Docs: [URL del índice maestro]

Analiza el corpus completo y:

1. Extrae todas las ideas originales de Israel sobre:
   - Neuroanatomía
   - Comunicación auditiva
   - Vocología sistémica

2. Identifica los puentes conceptuales entre:
   - CCA (Ciencias de la Comunicación Auditiva)
   - AAV (Anatomía, Fisiología y Vocología)
   - Neurociencias

3. Genera una estructura propuesta para tesis doctoral con:
   - Capítulos principales
   - Subcapítulos
   - Conceptos clave por sección

4. Crea una bibliografía preliminar basada en las referencias mencionadas

5. Identifica gaps en el conocimiento que requieren investigación adicional

Presenta el análisis en formato APA 7 listo para incorporar a la tesis.
```

---

## ✅ Verificación Final

### Checklist de Completado

- [ ] Servidores MCP instalados y configurados
- [ ] Claude Desktop reconoce los 3 servidores (dropbox, onedrive, google_drive)
- [ ] Todas las conversaciones exportadas y subidas a cloud
- [ ] Reconstrucción completada sin errores
- [ ] Corpus por plataforma creados
- [ ] Corpus unificado generado
- [ ] Documentos de Google Docs creados
- [ ] Documento maestro índice accesible
- [ ] Visor HTML generado (`corpus_viewer.html`)
- [ ] Análisis inicial completado con Claude

### Archivos Generados

Deberías tener:

```
improved-parakeet/
├── nexus_workspace/
│   ├── corpus_dropbox.json
│   ├── corpus_onedrive.json
│   └── workflow_guide_full.txt
├── nexus_unified_corpus/
│   ├── corpus_unified.json
│   ├── corpus_viewer.html
│   └── google_docs_links.json
└── nexus_sync_logs/
    └── sync_report_*.json
```

---

## 🔄 Mantenimiento

### Sincronización Incremental

Cada vez que tengas nuevas conversaciones:

1. Exporta desde las IAs
2. Sube a `/Nexus/exports/`
3. Ejecuta:
   ```bash
   python scripts/nexus_claude_workflow.py full
   ```
4. O pide a Claude en Desktop: "Ejecuta workflow de sincronización Nexus"

### Backup

Los corpus unificados están automáticamente respaldados en:
- Dropbox: `/Nexus/corpus_dropbox.json`
- OneDrive: `/Nexus/corpus_onedrive.json`
- Google Drive: Carpeta "Nexus Corpus"
- Local: `./nexus_unified_corpus/`

### Actualización de Documentos

Si modificas conversaciones reconstructed:

```bash
# Re-generar corpus unificado
python scripts/nexus_corpus_unifier.py

# Re-generar Google Docs
python scripts/nexus_to_gdocs.py
```

---

## 🆘 Troubleshooting

### Claude Desktop no ve los servidores MCP

**Solución:**
1. Verifica rutas absolutas en `claude_desktop_config.json`
2. Verifica que `.env` existe y tiene credenciales
3. Reinicia Claude Desktop (cierra todo y vuelve a abrir)
4. Verifica en Settings → Developer → MCP Servers

### Error de autenticación Google

**Solución:**
1. Elimina `token.pickle`
2. Vuelve a ejecutar `python scripts/nexus_to_gdocs.py`
3. Autoriza en el navegador cuando se abra

### Corpus vacío

**Solución:**
1. Verifica que los archivos en `/Nexus/exports/` son JSON válidos
2. Verifica que el ai_type es correcto
3. Revisa los logs de reconstrucción

### Conversiones incompletas

**Solución:**
1. Corpus muy grandes pueden tardar (normal hasta 10 min)
2. Verifica cuota de Google API
3. Ejecuta de nuevo, se retomarán conversiones faltantes

---

## 📚 Recursos Adicionales

- **Guía MCP Completa:** [MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)
- **README MCP:** [README_MCP.md](README_MCP.md)
- **Google Cloud Console:** https://console.cloud.google.com/
- **Claude Desktop Docs:** https://docs.anthropic.com/claude/docs/mcp

---

## 🎓 Caso de Uso: Tesis Doctoral

### Objetivo

Compilar y analizar **5+ años de investigación doctoral** dispersa en conversaciones con múltiples IAs, unificarlas en un corpus coherente y generar estructura de tesis.

### Resultados Esperados

- ✅ 100-150 conversaciones reconstructed
- ✅ 5,000-10,000 mensajes unificados
- ✅ Corpus categorizado por IA y tema
- ✅ Documentos Google Docs con formato APA 7
- ✅ Análisis semántico completo por Claude
- ✅ Estructura de tesis propuesta
- ✅ Bibliografía preliminar automatizada

### Tiempo Estimado

- **Setup inicial:** 2-3 horas (una sola vez)
- **Primera sincronización:** 1-2 horas
- **Sincronizaciones incrementales:** 15-30 minutos
- **Análisis con Claude:** 2-4 horas (depende del corpus)

---

**🔱 NEXUS OMEGA - Arquitectura de Conocimiento Distribuido**

*"Del caos digital a la tesis doctoral, un paso a la vez."*

---

**Autor:** Israel Realivazquez  
**Proyecto:** Nexus Omega PhD Research Orchestrator  
**Fecha:** 2026-05-16  
**Versión:** 1.0.0
