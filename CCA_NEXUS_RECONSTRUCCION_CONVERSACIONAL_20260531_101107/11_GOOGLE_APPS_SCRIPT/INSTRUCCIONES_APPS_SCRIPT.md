# 📱 INSTRUCCIONES: Google Apps Script (MÉTODO MÁS FÁCIL)

## ✨ VENTAJAS:
- ✅ NO requiere instalar nada
- ✅ Funciona desde el navegador (celular o computadora)
- ✅ NO necesitas Python
- ✅ Sube y convierte TODO automáticamente

## 📋 PASOS:

### 1. Abrir Google Apps Script
Ve a: https://script.google.com/

### 2. Crear nuevo proyecto
- Haz clic en **"Nuevo proyecto"** (+ o botón azul)
- Pon nombre: `CCA_NEXUS_Auto_Upload`

### 3. Pegar el código
- Abre el archivo: `11_GOOGLE_APPS_SCRIPT/auto_upload.gs`
- Copia TODO el contenido
- Pégalo en el editor de Apps Script (reemplaza todo)

### 4. Ejecutar
- Haz clic en el botón **▶️ Ejecutar** (arriba)
- Primera vez: te pedirá autorización
  - Haz clic en **"Revisar permisos"**
  - Selecciona tu cuenta de Google
  - **IMPORTANTE:** Dirá "Esta app no está verificada"
    - Haz clic en **"Configuración avanzada"**
    - Haz clic en **"Ir a CCA_NEXUS_Auto_Upload (no seguro)"**
    - Haz clic en **"Permitir"**

### 5. Ver resultados
- Ve a **Ver → Registros** (o Ctrl+Enter)
- Verás las URLs de cada Google Doc creado
- También se creará un archivo `INDICE_URLS_GOOGLE_DOCS.txt` en la carpeta

### 6. Abrir carpeta
Ve a Google Drive y busca:
```
CCA_NEXUS_CONVERSACIONES_RECONSTRUIDAS_20260531
```

¡Listo! Todas tus conversaciones están ahora en Google Docs.

---

## 🔍 VERIFICACIÓN:

Deberías ver 4 Google Docs:
1. ChatGPT_UNKNOWN_Investigación_Doctoral_-_Hipót_20260531
2. ChatGPT_UNKNOWN_Neuroanatomía_del_Sistema_Audi_20260531
3. Claude_claude_03da8f807f1f_Claude_Conversation_20260531
4. Gemini_gemini_f73a7db5303b_Gemini_Conversation_20260531

---

## ⚠️ SOLUCIÓN DE PROBLEMAS:

**"ReferenceError: Drive is not defined"**
→ Habilita "Google Drive API" en el proyecto Apps Script:
  - Configuración (⚙️) → Servicios
  - Busca "Drive API v2"
  - Agrega

**"No veo los logs"**
→ Ve a: Ver → Registros de ejecución

**"Error de autorización"**
→ Ve a: Configuración → Mostrar archivo de manifiesto appsscript.json
→ Agrega:
```json
{
  "oauthScopes": [
    "https://www.googleapis.com/auth/drive.file"
  ]
}
```

---

**🔱 CCA/NEXUS - Reconstrucción Conversacional Automatizada**
