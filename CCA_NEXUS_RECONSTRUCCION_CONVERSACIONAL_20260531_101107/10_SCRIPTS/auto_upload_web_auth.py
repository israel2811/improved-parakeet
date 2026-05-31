#!/usr/bin/env python3
"""
AUTO-SUBIDA A GOOGLE DOCS - MÉTODO 2: Autenticación Web
Este método NO requiere credentials.json - usa tu email directamente
"""

import os
import json
import webbrowser
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import http.server
import socketserver
import urllib.parse

# Cliente ID público (solo para pruebas - crea el tuyo en producción)
CLIENT_CONFIG = {
    "installed": {
        "client_id": "CLIENTE_ID_AQUI",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
}

SCOPES = ['https://www.googleapis.com/auth/drive.file']
REDIRECT_URI = 'http://localhost:8080'

class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    """Handler para recibir el código de autorización"""

    auth_code = None

    def do_GET(self):
        # Extraer código de autorización
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if 'code' in params:
            OAuthHandler.auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1 style="color: green;">✅ Autorizacion Exitosa!</h1>
                    <p>Ya puedes cerrar esta ventana y volver a la terminal.</p>
                </body>
                </html>
            """)
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Silenciar logs

def authenticate_web():
    """Autenticación vía navegador web"""

    print("\n🌐 MÉTODO 2: Autenticación Web Simplificada")
    print("=" * 60)
    print("\n⚠️  NOTA: Este método requiere configuración manual.")
    print("\nPara usar este método necesitas:")
    print("1. Ir a: https://console.cloud.google.com/apis/credentials")
    print("2. Crear un proyecto")
    print("3. Habilitar Google Drive API")
    print("4. Crear credenciales OAuth 2.0")
    print("5. Copiar el Client ID aquí")
    print("\nAlternativamente, usa el MÉTODO 1 (auto_upload_google_docs.py)")
    print("o el MÉTODO 3 (instrucciones manuales desde celular)")
    print("=" * 60)

    return None

def main():
    print("🔱 CCA/NEXUS - AUTO-SUBIDA MÉTODO 2")
    creds = authenticate_web()

    if not creds:
        print("\n💡 RECOMENDACIÓN: Usa uno de estos métodos alternativos:")
        print("\n   MÉTODO 1: auto_upload_google_docs.py (OAuth local)")
        print("   MÉTODO 3: Instrucciones manuales (más simple)")
        print("   MÉTODO 4: Google Apps Script (desde navegador)")

if __name__ == '__main__':
    main()
