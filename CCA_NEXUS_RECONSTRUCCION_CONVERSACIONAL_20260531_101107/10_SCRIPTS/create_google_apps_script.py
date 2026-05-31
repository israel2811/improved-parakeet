#!/usr/bin/env python3
"""
MÉTODO 3: Generar Google Apps Script para subida automática
Este método funciona 100% desde el navegador, sin instalar nada
"""

import json
from pathlib import Path

def generate_apps_script():
    """Genera un Google Apps Script que sube los archivos"""

    # Leer archivos HTML
    html_dir = Path('05_GOOGLE_DOCS_READY')
    if not html_dir.exists():
        html_dir = Path('../05_GOOGLE_DOCS_READY')

    html_files = sorted(html_dir.glob('*_CANONICO.html'))

    # Leer contenido de cada archivo
    files_data = []
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Escapar comillas para JavaScript
            content_escaped = content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
            files_data.append({
                'name': html_file.stem.replace('_CANONICO', ''),
                'content': content_escaped
            })

    # Generar Apps Script
    script = f'''/**
 * CCA/NEXUS - Auto-subida a Google Docs
 *
 * INSTRUCCIONES:
 * 1. Ve a: https://script.google.com/
 * 2. Crea un nuevo proyecto
 * 3. Pega TODO este código
 * 4. Haz clic en "Ejecutar" (▶️)
 * 5. Autoriza el script (primera vez)
 * 6. Revisa los logs para ver las URLs
 */

function uploadConversationsToGoogleDocs() {{

  // Crear carpeta en Google Drive
  var folderName = 'CCA_NEXUS_CONVERSACIONES_RECONSTRUIDAS_20260531';
  var folders = DriveApp.getFoldersByName(folderName);
  var folder;

  if (folders.hasNext()) {{
    folder = folders.next();
    Logger.log('📁 Carpeta ya existe: ' + folderName);
  }} else {{
    folder = DriveApp.createFolder(folderName);
    Logger.log('📁 Carpeta creada: ' + folderName);
  }}

  // Archivos HTML a subir
  var files = {json.dumps(files_data, indent=2, ensure_ascii=False)};

  var results = [];

  // Subir cada archivo
  for (var i = 0; i < files.length; i++) {{
    var fileData = files[i];

    Logger.log('');
    Logger.log('📄 [' + (i+1) + '/' + files.length + '] Procesando: ' + fileData.name);

    try {{
      // Crear Google Doc desde HTML
      var blob = Utilities.newBlob(fileData.content, 'text/html', fileData.name + '.html');
      var doc = {{
        title: fileData.name,
        mimeType: MimeType.GOOGLE_DOCS,
        parents: [{{id: folder.getId()}}]
      }};

      // Subir archivo
      var file = Drive.Files.insert(doc, blob, {{convert: true}});

      var url = 'https://docs.google.com/document/d/' + file.id + '/edit';

      results.push({{
        name: fileData.name,
        id: file.id,
        url: url
      }});

      Logger.log('✅ Google Doc creado: ' + fileData.name);
      Logger.log('🔗 URL: ' + url);

    }} catch (e) {{
      Logger.log('❌ Error: ' + e.message);
    }}
  }}

  // Resumen final
  Logger.log('');
  Logger.log('='.repeat(60));
  Logger.log('✅ SUBIDA COMPLETA!');
  Logger.log('📁 Carpeta: ' + folderName);
  Logger.log('📄 Archivos creados: ' + results.length);
  Logger.log('');
  Logger.log('🔗 URLs de Google Docs:');
  for (var i = 0; i < results.length; i++) {{
    Logger.log('   ' + (i+1) + '. ' + results[i].name);
    Logger.log('      ' + results[i].url);
  }}
  Logger.log('='.repeat(60));

  // Crear archivo índice con URLs
  var indexContent = '# 🔗 URLs de Google Docs - CCA/NEXUS\\n\\n';
  indexContent += 'Fecha: ' + new Date().toISOString() + '\\n\\n';
  for (var i = 0; i < results.length; i++) {{
    indexContent += (i+1) + '. **' + results[i].name + '**\\n';
    indexContent += '   ' + results[i].url + '\\n\\n';
  }}

  var indexFile = folder.createFile('INDICE_URLS_GOOGLE_DOCS.txt', indexContent);
  Logger.log('');
  Logger.log('📋 Índice de URLs creado en la carpeta');

  return results;
}}

/**
 * Función auxiliar: ver URLs directamente
 */
function showURLs() {{
  var results = uploadConversationsToGoogleDocs();
  var ui = SpreadsheetApp.getUi(); // Solo funciona si se ejecuta desde Sheets
  var message = 'URLs creadas:\\n\\n';
  for (var i = 0; i < results.length; i++) {{
    message += results[i].name + ':\\n' + results[i].url + '\\n\\n';
  }}
  ui.alert('Google Docs URLs', message, ui.ButtonSet.OK);
}}
'''

    return script

def main():
    print("🔱 CCA/NEXUS - MÉTODO 3: Google Apps Script")
    print("=" * 70)

    print("\n📝 Generando Google Apps Script...")
    script = generate_apps_script()

    # Guardar script
    output_file = Path('11_GOOGLE_APPS_SCRIPT/auto_upload.gs')
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script)

    print(f"✅ Script generado: {output_file}")

    # Crear instrucciones
    instructions = """# 📱 INSTRUCCIONES: Google Apps Script (MÉTODO MÁS FÁCIL)

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
"""

    inst_file = Path('11_GOOGLE_APPS_SCRIPT/INSTRUCCIONES_APPS_SCRIPT.md')
    with open(inst_file, 'w', encoding='utf-8') as f:
        f.write(instructions)

    print(f"✅ Instrucciones: {inst_file}")

    print("\n" + "=" * 70)
    print("✅ MÉTODO 3 LISTO!")
    print("\n📁 Archivos creados:")
    print(f"   - {output_file}")
    print(f"   - {inst_file}")
    print("\n💡 ESTE ES EL MÉTODO MÁS FÁCIL - funciona desde el navegador")
    print("=" * 70)

if __name__ == '__main__':
    main()
