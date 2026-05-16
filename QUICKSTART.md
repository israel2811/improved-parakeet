# 🔱 NEXUS - QUICKSTART GUIDE

**Guía rápida para empezar en 30 minutos**

---

## ⚡ Setup Rápido (5 minutos)

### 1. Instalar Todo

```bash
# Clonar repo (si aún no lo has hecho)
git clone https://github.com/israel2811/improved-parakeet.git
cd improved-parakeet

# Instalar servidores MCP
./install_mcp_servers.sh  # Linux/macOS
# o
.\install_mcp_servers.ps1  # Windows

# Instalar integración Google
./install_google_integration.sh  # Linux/macOS
```

### 2. Configurar Credenciales (10 minutos)

#### A. Dropbox (2 min)
1. https://www.dropbox.com/developers/apps → Create app
2. Copiar token a `mcp-servers/dropbox/.env`

#### B. OneDrive (3 min)
1. https://portal.azure.com → App registrations
2. Crear app, obtener client ID y secret
3. Copiar a `mcp-servers/onedrive/.env`

#### C. Google Cloud (5 min)
1. https://console.cloud.google.com/
2. Crear proyecto, habilitar APIs (Docs + Drive)
3. Crear credenciales OAuth 2.0
4. Descargar como `credentials.json`

### 3. Configurar Claude Desktop (5 minutos)

Editar: `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

Copiar de: `claude_desktop_config_full.json`

**⚠️ Cambiar rutas a absolutas**

Reiniciar Claude Desktop.

---

## 🚀 Primera Sincronización (10 minutos)

### Preparar Datos

1. Exporta conversaciones de tus IAs
2. Crea carpetas en Dropbox y OneDrive:
   ```
   /Nexus/exports/
   /Nexus/reconstructed/
   ```
3. Sube archivos a `/Nexus/exports/`

### Ejecutar Workflow

**Opción 1: Automático con Python**

```bash
python scripts/nexus_claude_workflow.py full
```

Esto genera instrucciones. Cópialas a Claude Desktop.

**Opción 2: Directo en Claude Desktop**

Copia esto en Claude Desktop:

```
Ejecuta workflow Nexus:

1. Lista archivos en /Nexus/exports/ en Dropbox y OneDrive
2. Reconstruye cada conversación según su tipo
3. Crea corpus por plataforma
4. Descarga corpus a local
5. Ejecuta: python scripts/nexus_corpus_unifier.py
6. Ejecuta: python scripts/nexus_to_gdocs.py
7. Dame reporte con links a Google Docs
```

---

## ✅ Verificar Resultados

### En Google Drive

1. Abre: https://drive.google.com/
2. Busca carpeta: "Nexus Corpus"
3. Verifica subcarpetas por IA
4. Abre: "NEXUS CORPUS - ÍNDICE MAESTRO"

### En Local

```bash
ls nexus_unified_corpus/
# Debe tener:
# - corpus_unified.json
# - corpus_viewer.html
# - google_docs_links.json
```

---

## 📊 Analizar con Claude

En Claude Desktop:

```
Lee el documento maestro en: [URL del índice]

Analiza el corpus completo y extrae:
1. Ideas de Israel sobre neuroanatomía
2. Conceptos de comunicación auditiva
3. Estructura para tesis doctoral
4. Bibliografía preliminar
```

---

## 🔄 Sincronizaciones Futuras

Cada vez que tengas nuevas conversaciones:

```bash
# 1. Exporta y sube a /Nexus/exports/
# 2. Ejecuta:
python scripts/nexus_claude_workflow.py full

# O pide a Claude Desktop:
# "Ejecuta workflow de sincronización Nexus"
```

---

## 🆘 Problemas Comunes

### Claude no ve servidores MCP
→ Verifica rutas absolutas en config
→ Reinicia Claude Desktop

### Error autenticación Google
→ Elimina `token.pickle`
→ Vuelve a ejecutar scripts

### Corpus vacío
→ Verifica archivos en `/Nexus/exports/`
→ Verifica formato JSON válido

---

## 📚 Más Información

- **Workflow Completo:** [WORKFLOW_COMPLETO.md](WORKFLOW_COMPLETO.md)
- **Guía MCP:** [MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)
- **README MCP:** [README_MCP.md](README_MCP.md)

---

## 🎯 Lo Esencial

1. **Instala** → `install_mcp_servers.sh` + `install_google_integration.sh`
2. **Configura** → Credenciales en `.env` + `credentials.json`
3. **Sube** → Exports a `/Nexus/exports/`
4. **Ejecuta** → Workflow en Claude Desktop
5. **Analiza** → Documentos en Google Docs

**Tiempo total:** ~30 minutos primera vez, ~15 minutos después.

---

**🔱 NEXUS OMEGA**

¿Preguntas? Lee [WORKFLOW_COMPLETO.md](WORKFLOW_COMPLETO.md) para guía detallada.
