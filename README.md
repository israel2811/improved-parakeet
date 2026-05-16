# 🔱 NEXUS OMEGA

**Arquitectura de Conocimiento Distribuido para Investigación Doctoral**

Sistema completo de orquestación multi-plataforma que unifica conversaciones de IA desde Dropbox, OneDrive y Google Drive, las reconstruye en formato académico, y las sincroniza a Google Docs para análisis profundo con Claude Desktop.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

---

## 🎯 ¿Qué hace Nexus Omega?

Nexus Omega te permite:

1. **Exportar** conversaciones de ChatGPT, Claude, Gemini, NotebookLM, Antigravity y Codex
2. **Subir** a Dropbox/OneDrive automáticamente
3. **Reconstruir** en formato unificado con servidores MCP
4. **Unificar** en un corpus maestro multi-plataforma
5. **Sincronizar** a Google Docs con formato APA 7
6. **Analizar** todo con Claude Desktop

### Caso de Uso Principal

**Tesis Doctoral:** Compila 5+ años de investigación dispersa en múltiples IAs, unifícala en un corpus coherente, y genera estructura de tesis automáticamente.

---

## ⚡ Quickstart (30 minutos)

### 1. Instalar

```bash
git clone https://github.com/israel2811/improved-parakeet.git
cd improved-parakeet

# Instalar servidores MCP
./install_mcp_servers.sh        # Linux/macOS
.\install_mcp_servers.ps1       # Windows

# Instalar Google integration
./install_google_integration.sh  # Linux/macOS
```

### 2. Configurar

#### Credenciales Cloud

- **Dropbox:** Edita `mcp-servers/dropbox/.env`
- **OneDrive:** Edita `mcp-servers/onedrive/.env`
- **Google:** Descarga `credentials.json` desde Google Cloud Console

#### Claude Desktop

Edita tu `claude_desktop_config.json` usando `claude_desktop_config_full.json` como referencia.

**Ubicación:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

### 3. Sincronizar

```bash
# Generar workflow
python scripts/nexus_claude_workflow.py full

# Copiar instrucciones a Claude Desktop
# Claude ejecutará todo automáticamente
```

**Ver guía completa:** [QUICKSTART.md](QUICKSTART.md)

---

## 📚 Documentación

- **[QUICKSTART.md](QUICKSTART.md)** - Guía rápida (30 min)
- **[WORKFLOW_COMPLETO.md](WORKFLOW_COMPLETO.md)** - Workflow detallado paso a paso
- **[MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)** - Guía completa de MCP
- **[README_MCP.md](README_MCP.md)** - Documentación de servidores MCP

---

## 🛠️ Herramientas

### Servidores MCP
- **Dropbox MCP** - 6 herramientas de gestión de archivos y reconstrucción
- **OneDrive MCP** - 7 herramientas incluyendo sincronización con Google Drive
- **Google Drive MCP** - Servidor oficial de Google

### Scripts Python
- `nexus_corpus_unifier.py` - Unificador multi-plataforma
- `nexus_to_gdocs.py` - Conversor a Google Docs APA 7
- `nexus_sync_orchestrator.py` - Orquestador maestro
- `nexus_claude_workflow.py` - Generador de workflows

---

## 📊 IAs Soportadas

✅ ChatGPT • Claude • Gemini • NotebookLM • Antigravity • OpenAI Codex

---

## 🎓 Caso de Uso: Tesis Doctoral

**Contexto:** PhD en Neuroanatomía y Comunicación Auditiva con 5+ años de conversaciones dispersas

**Resultado:** 150+ conversaciones reconstructed → Corpus unificado → Google Docs APA 7 → Estructura de tesis

**Tiempo ahorrado:** ~200 horas de compilación manual

---

## 👨‍🎓 Autor

**Israel Realivazquez** • PhD Candidate  
Neuroanatomía • Comunicación Auditiva • Vocología  
📧 israel.realivazquez@gmail.com

---

## 📄 Licencia

Apache 2.0 - Ver [LICENSE](LICENSE)

---

**🔱 NEXUS OMEGA - Arquitectura de Conocimiento Distribuido**

*"Del caos digital, conocimiento estructurado."*