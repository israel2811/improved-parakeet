# 🚀 MÉTODOS DE SUBIDA AUTOMÁTICA A GOOGLE DOCS

**Proyecto:** CCA/NEXUS - Reconstrucción Conversacional  
**Objetivo:** Subir TODAS las conversaciones reconstruidas a Google Docs automáticamente  
**Fecha:** 2026-05-31

---

## 📊 RESUMEN DE MÉTODOS

| Método | Dificultad | Dónde ejecutar | Requiere instalación | Recomendado |
|--------|-----------|----------------|---------------------|-------------|
| **MÉTODO 1: Apps Script** | ⭐ Fácil | Navegador | ❌ No | ✅ SÍ |
| **MÉTODO 2: Python Local** | ⭐⭐ Media | Computadora | ✅ Python + pip | Alternativa |
| **MÉTODO 3: Manual Celular** | ⭐⭐⭐ Fácil pero manual | Celular | ❌ No | Si otros fallan |

---

# 🥇 MÉTODO 1: Google Apps Script (RECOMENDADO)

## ✨ VENTAJAS:
- ✅ **MÁS FÁCIL** - todo desde el navegador
- ✅ Funciona en celular y computadora
- ✅ NO requiere instalar nada
- ✅ Sube y convierte los 4 archivos automáticamente
- ✅ Genera URLs automáticamente

## 📋 PASOS RÁPIDOS:

### 1. Abre Google Apps Script
```
https://script.google.com/
```

### 2. Nuevo proyecto
- Haz clic en **"+ Nuevo proyecto"**
- Nombre: `CCA_NEXUS_Upload`

### 3. Pega el código
- Abre: `11_GOOGLE_APPS_SCRIPT/auto_upload.gs`
- Copia TODO el código
- Pégalo en Apps Script (reemplaza el código vacío)

### 4. Habilita Drive API
- Haz clic en **⚙️ Configuración del proyecto** (izquierda)
- Baja hasta **"Servicios de Google"**
- Haz clic en **"+ Agregar un servicio"**
- Busca **"Drive API"** → Agregar

### 5. Ejecutar
- Haz clic en **▶️ Ejecutar** (función: uploadConversationsToGoogleDocs)
- **Primera vez:** Autorizar
  - "Revisar permisos"
  - Selecciona tu cuenta
  - "Esta app no está verificada" → **"Configuración avanzada"**
  - **"Ir a CCA_NEXUS_Upload (no seguro)"**
  - **"Permitir"**

### 6. Ver resultados
- **Ver → Registros** (Ctrl+Enter)
- Verás las 4 URLs de Google Docs creados

### 7. Verificar
Ve a Google Drive:
```
📁 CCA_NEXUS_CONVERSACIONES_RECONSTRUIDAS_20260531/
   ├── ✅ ChatGPT_UNKNOWN_Investigación_Doctoral...
   ├── ✅ ChatGPT_UNKNOWN_Neuroanatomía_del_Sistema...
   ├── ✅ Claude_claude_03da8f807f1f_Claude...
   ├── ✅ Gemini_gemini_f73a7db5303b_Gemini...
   └── 📋 INDICE_URLS_GOOGLE_DOCS.txt
```

**¡LISTO! 4 Google Docs creados en ~2 minutos.**

---

# 🥈 MÉTODO 2: Python con OAuth (Alternativa)

## 📋 REQUISITOS:
- Python 3.x instalado
- Acceso a Google Cloud Console
- Terminal/línea de comandos

## 📋 PASOS:

### 1. Crear credenciales OAuth

Ve a: https://console.cloud.google.com/apis/credentials

1. **Crear proyecto nuevo**
   - Nombre: `CCA-NEXUS-Upload`

2. **Habilitar APIs**
   - Ir a "Biblioteca"
   - Buscar "Google Drive API"
   - Habilitar

3. **Crear credenciales**
   - "Credenciales" → "+ Crear credenciales"
   - Tipo: **"ID de cliente de OAuth"**
   - Tipo de aplicación: **"Aplicación de escritorio"**
   - Nombre: `CCA_Upload_Desktop`
   - Descargar JSON

4. **Guardar credenciales**
   - Renombrar archivo a: `credentials.json`
   - Copiarlo a: `10_SCRIPTS/credentials.json`

### 2. Instalar dependencias

```bash
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 3. Ejecutar script

```bash
cd CCA_NEXUS_RECONSTRUCCION_CONVERSACIONAL_20260531_101107/10_SCRIPTS
python3 auto_upload_google_docs.py
```

### 4. Autorizar
- Se abrirá el navegador automáticamente
- Inicia sesión con tu cuenta de Google
- Permite el acceso

### 5. Verificar
El script mostrará las URLs creadas en la terminal.

---

# 🥉 MÉTODO 3: Manual desde Celular (Plan B)

Si los métodos automáticos fallan, sigue las instrucciones en:
```
INSTRUCCIONES_IMPORTACION_GOOGLE_DOCS_DESDE_CELULAR.md
```

**Pasos resumidos:**
1. Subir los 4 HTML a Google Drive
2. Abrir cada HTML con Google Docs
3. Crear copia (se convierte a Google Doc)
4. Copiar URLs manualmente

**Tiempo estimado:** 10-15 minutos

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Apps Script: "Drive is not defined"
**Solución:** Habilita Drive API v2 en servicios del proyecto

### Apps Script: "No veo los registros"
**Solución:** Ver → Registros de ejecución (o Ctrl+Enter)

### Python: "credentials.json not found"
**Solución:** Descarga credentials.json de Google Cloud Console

### Python: "ModuleNotFoundError: google"
**Solución:** 
```bash
pip3 install google-api-python-client google-auth-oauthlib
```

### Manual: "No puedo subir archivos"
**Solución:** Verifica espacio en Google Drive y conexión

---

## ✅ VERIFICACIÓN FINAL

Después de subir, deberías tener:

**En Google Drive:**
```
📁 CCA_NEXUS_CONVERSACIONES_RECONSTRUIDAS_20260531/
   ├── 📄 ChatGPT_UNKNOWN_Investigación_Doctoral_-_Hipót_20260531 (Google Doc)
   ├── 📄 ChatGPT_UNKNOWN_Neuroanatomía_del_Sistema_Audi_20260531 (Google Doc)
   ├── 📄 Claude_claude_03da8f807f1f_Claude_Conversation_20260531 (Google Doc)
   ├── 📄 Gemini_gemini_f73a7db5303b_Gemini_Conversation_20260531 (Google Doc)
   └── 📄 INDICE_URLS_GOOGLE_DOCS.txt (índice de URLs)
```

**Total:** 4 Google Docs + 1 índice

---

## 📞 SIGUIENTE PASO

Una vez que tengas las URLs de Google Docs:

1. **Actualizar índice maestro:**
   - Abre: `06_INDICES/INDICE_CONVERSACIONES_RECONSTRUIDAS_CCA_NEXUS_20260531.csv`
   - Reemplaza "PENDIENTE_SUBIDA_MANUAL" con las URLs reales

2. **Usar con Claude Desktop:**
   ```
   Claude, lee estos Google Docs:
   
   1. [URL doc 1]
   2. [URL doc 2]
   3. [URL doc 3]
   4. [URL doc 4]
   
   Analiza las conversaciones y extrae:
   - Hipótesis doctoral principal
   - Conceptos clave de neuroanatomía auditiva
   - Referencias bibliográficas
   - Estructura de tesis propuesta
   ```

---

## 🎯 RECOMENDACIÓN FINAL

**Para la mayoría de usuarios:**
→ **Usa MÉTODO 1 (Google Apps Script)**
  - Más rápido
  - Más simple
  - Funciona desde celular

**Si tienes experiencia con Python:**
→ **Usa MÉTODO 2 (Python OAuth)**
  - Más control
  - Reutilizable para futuros batches

**Si todo falla:**
→ **Usa MÉTODO 3 (Manual)**
  - Garantizado que funciona
  - Solo toma 10-15 minutos

---

**🔱 NEXUS CCA - Automatización de Subida a Google Docs**

*Elige el método que prefieras y completa la subida en menos de 5 minutos.*
