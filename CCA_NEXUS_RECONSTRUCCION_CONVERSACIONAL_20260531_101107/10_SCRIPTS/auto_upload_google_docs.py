#!/usr/bin/env python3
"""
AUTO-SUBIDA A GOOGLE DOCS - MÉTODO 1: OAuth Interactivo
Ejecuta este script desde tu celular/computadora con Python 3
"""

import os
import json
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scopes necesarios
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    """Autenticación OAuth"""
    creds = None
    token_path = 'token.pickle'

    # Cargar credenciales guardadas
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # Si no hay credenciales válidas, autenticar
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Necesitas crear credentials.json en Google Cloud Console
            if not os.path.exists('credentials.json'):
                print("\n❌ FALTA: credentials.json")
                print("\n📋 INSTRUCCIONES PARA CREAR credentials.json:")
                print("1. Ve a https://console.cloud.google.com/")
                print("2. Crea un proyecto nuevo o usa uno existente")
                print("3. Habilita Google Drive API")
                print("4. Ve a 'Credenciales' → 'Crear credenciales' → 'ID de cliente de OAuth'")
                print("5. Tipo: 'Aplicación de escritorio'")
                print("6. Descarga el archivo JSON como 'credentials.json'")
                print("7. Ponlo en la misma carpeta que este script")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Guardar credenciales
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def upload_and_convert_to_gdocs(service, file_path, folder_id=None):
    """Sube HTML y lo convierte a Google Docs"""

    file_name = os.path.basename(file_path)

    # Metadata del archivo
    file_metadata = {
        'name': file_name.replace('_CANONICO.html', ''),
        'mimeType': 'application/vnd.google-apps.document'  # Convierte a Google Docs
    }

    if folder_id:
        file_metadata['parents'] = [folder_id]

    # Subir archivo
    media = MediaFileUpload(file_path, mimetype='text/html', resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()

    return file

def create_folder(service, folder_name):
    """Crea carpeta en Google Drive"""

    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    folder = service.files().create(
        body=file_metadata,
        fields='id, name'
    ).execute()

    return folder

def main():
    print("🔱 CCA/NEXUS - AUTO-SUBIDA A GOOGLE DOCS")
    print("=" * 60)

    # Autenticar
    print("\n1️⃣ Autenticando con Google...")
    creds = authenticate()

    if not creds:
        print("\n❌ Autenticación fallida. Sigue las instrucciones arriba.")
        return

    print("✅ Autenticación exitosa!")

    # Crear servicio de Drive
    service = build('drive', 'v3', credentials=creds)

    # Crear carpeta
    print("\n2️⃣ Creando carpeta en Google Drive...")
    folder_name = 'CCA_NEXUS_CONVERSACIONES_RECONSTRUIDAS_20260531'
    folder = create_folder(service, folder_name)
    folder_id = folder['id']
    print(f"✅ Carpeta creada: {folder_name}")

    # Buscar archivos HTML
    html_dir = Path('05_GOOGLE_DOCS_READY')
    if not html_dir.exists():
        html_dir = Path('../05_GOOGLE_DOCS_READY')

    html_files = sorted(html_dir.glob('*_CANONICO.html'))

    print(f"\n3️⃣ Subiendo {len(html_files)} archivos HTML...")

    results = []
    for i, html_file in enumerate(html_files, 1):
        print(f"\n   [{i}/{len(html_files)}] Subiendo: {html_file.name}")
        try:
            file_info = upload_and_convert_to_gdocs(service, str(html_file), folder_id)
            results.append({
                'filename': html_file.name,
                'gdoc_id': file_info['id'],
                'gdoc_name': file_info['name'],
                'url': file_info['webViewLink']
            })
            print(f"   ✅ Convertido a Google Docs: {file_info['name']}")
            print(f"   🔗 URL: {file_info['webViewLink']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    # Guardar URLs
    print("\n4️⃣ Guardando URLs...")
    urls_file = Path('06_INDICES/GOOGLE_DOCS_URLS.json')
    if not urls_file.parent.exists():
        urls_file = Path('../06_INDICES/GOOGLE_DOCS_URLS.json')

    with open(urls_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ URLs guardadas en: {urls_file}")

    # Resumen
    print("\n" + "=" * 60)
    print("✅ SUBIDA COMPLETA!")
    print(f"📁 Carpeta: {folder_name}")
    print(f"📄 Archivos subidos: {len(results)}")
    print("\n🔗 URLs de Google Docs:")
    for result in results:
        print(f"   - {result['gdoc_name']}")
        print(f"     {result['url']}")
    print("=" * 60)

if __name__ == '__main__':
    main()
