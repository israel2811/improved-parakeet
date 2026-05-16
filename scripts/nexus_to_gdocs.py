#!/usr/bin/env python3
"""
🔱 NEXUS TO GOOGLE DOCS CONVERTER
Convierte corpus unificado a documentos de Google Docs con formato APA 7
Preserva estructura, metadatos y facilita análisis académico

Autor: Israel Realivazquez
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import pickle
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    print("⚠️  google-auth y google-api-python-client no instalados")
    print("   Instala con: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")


# Scopes necesarios
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file'
]


class NexusToGoogleDocs:
    """Conversor de corpus Nexus a Google Docs"""

    def __init__(self, credentials_path: str = 'credentials.json'):
        if not GOOGLE_AVAILABLE:
            raise ImportError("Librerías de Google no disponibles")

        self.credentials_path = credentials_path
        self.creds = None
        self.docs_service = None
        self.drive_service = None
        self.authenticate()

    def authenticate(self):
        """Autenticación con Google"""
        token_path = 'token.pickle'

        # Cargar credenciales existentes
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)

        # Si no hay credenciales válidas, autenticar
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Guardar credenciales
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)

        # Crear servicios
        self.docs_service = build('docs', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)

        print("✅ Autenticado con Google exitosamente")

    def create_folder(self, folder_name: str, parent_id: str = None) -> str:
        """Crea una carpeta en Google Drive"""
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        if parent_id:
            file_metadata['parents'] = [parent_id]

        try:
            folder = self.drive_service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            return folder.get('id')
        except HttpError as error:
            print(f"Error creando carpeta: {error}")
            return None

    def create_document(self, title: str, folder_id: str = None) -> str:
        """Crea un documento de Google Docs"""
        try:
            # Crear documento
            doc = self.docs_service.documents().create(body={'title': title}).execute()
            doc_id = doc.get('documentId')

            # Mover a carpeta si se especificó
            if folder_id:
                file = self.drive_service.files().get(
                    fileId=doc_id,
                    fields='parents'
                ).execute()

                previous_parents = ",".join(file.get('parents', []))
                self.drive_service.files().update(
                    fileId=doc_id,
                    addParents=folder_id,
                    removeParents=previous_parents,
                    fields='id, parents'
                ).execute()

            return doc_id

        except HttpError as error:
            print(f"Error creando documento: {error}")
            return None

    def format_conversation_to_requests(self, conversation: Dict) -> List[Dict]:
        """Convierte una conversación a requests de formato de Google Docs"""
        requests = []

        # Título de la conversación
        ai_type = conversation.get('metadata', {}).get('ai_type', 'Unknown')
        source = conversation.get('metadata', {}).get('source_platform', 'Unknown')

        title_text = f"Conversación: {ai_type.upper()} ({source})\n\n"
        requests.append({
            'insertText': {
                'location': {'index': 1},
                'text': title_text
            }
        })

        # Estilo del título
        requests.append({
            'updateParagraphStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': len(title_text)
                },
                'paragraphStyle': {
                    'namedStyleType': 'HEADING_1',
                    'alignment': 'CENTER'
                },
                'fields': 'namedStyleType,alignment'
            }
        })

        current_index = len(title_text) + 1

        # Metadatos
        metadata_text = f"Fuente: {source}\n"
        metadata_text += f"Tipo de IA: {ai_type}\n"
        metadata_text += f"Fecha de reconstrucción: {conversation.get('metadata', {}).get('reconstructed_at', 'N/A')}\n"
        metadata_text += f"Total de mensajes: {len(conversation.get('messages', []))}\n\n"
        metadata_text += "─" * 80 + "\n\n"

        requests.append({
            'insertText': {
                'location': {'index': current_index},
                'text': metadata_text
            }
        })

        current_index += len(metadata_text)

        # Mensajes
        for idx, message in enumerate(conversation.get('messages', []), 1):
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            timestamp = message.get('timestamp', 'N/A')

            # Header del mensaje
            message_header = f"\n[{idx}] {role.upper()}"
            if timestamp and timestamp != 'N/A':
                message_header += f" • {timestamp}"
            message_header += "\n"

            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': message_header
                }
            })

            # Estilo del header (negrita)
            requests.append({
                'updateTextStyle': {
                    'range': {
                        'startIndex': current_index,
                        'endIndex': current_index + len(message_header)
                    },
                    'textStyle': {
                        'bold': True,
                        'foregroundColor': {
                            'color': {
                                'rgbColor': {
                                    'red': 0.0 if role == 'user' else 0.2,
                                    'green': 0.5 if role == 'user' else 0.4,
                                    'blue': 0.8
                                }
                            }
                        }
                    },
                    'fields': 'bold,foregroundColor'
                }
            })

            current_index += len(message_header)

            # Contenido del mensaje
            message_content = content + "\n\n"
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': message_content
                }
            })

            current_index += len(message_content)

        return requests

    def convert_conversation(self, conversation: Dict, folder_id: str = None) -> str:
        """Convierte una conversación individual a Google Doc"""
        ai_type = conversation.get('metadata', {}).get('ai_type', 'unknown')
        source = conversation.get('metadata', {}).get('source_platform', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        title = f"Nexus_{ai_type}_{source}_{timestamp}"

        # Crear documento
        doc_id = self.create_document(title, folder_id)
        if not doc_id:
            return None

        # Obtener requests de formato
        requests = self.format_conversation_to_requests(conversation)

        # Aplicar formato
        try:
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()

            print(f"  ✅ Conversación convertida: {title}")
            return doc_id

        except HttpError as error:
            print(f"  ❌ Error formateando documento: {error}")
            return None

    def convert_corpus_to_docs(self, corpus_path: str, parent_folder_name: str = "Nexus Corpus") -> Dict[str, str]:
        """Convierte el corpus completo a múltiples Google Docs organizados"""
        print(f"\n🔱 Convirtiendo corpus a Google Docs...")
        print(f"📂 Archivo: {corpus_path}")

        # Leer corpus
        with open(corpus_path, 'r', encoding='utf-8') as f:
            corpus = json.load(f)

        total_conversations = len(corpus.get('conversations', []))
        print(f"📊 Total de conversaciones: {total_conversations}")

        # Crear carpeta principal
        parent_folder_id = self.create_folder(parent_folder_name)
        if not parent_folder_id:
            print("❌ No se pudo crear carpeta principal")
            return {}

        print(f"✅ Carpeta principal creada: {parent_folder_name}")

        # Crear subcarpetas por tipo de IA
        ai_types = {}
        for conv in corpus.get('conversations', []):
            ai_type = conv.get('metadata', {}).get('ai_type', 'unknown')
            if ai_type not in ai_types:
                folder_id = self.create_folder(f"AI_{ai_type.upper()}", parent_folder_id)
                ai_types[ai_type] = folder_id
                print(f"  📁 Subcarpeta creada: AI_{ai_type.upper()}")

        # Convertir conversaciones
        converted_docs = {}
        for idx, conv in enumerate(corpus.get('conversations', []), 1):
            print(f"\n[{idx}/{total_conversations}] Convirtiendo conversación...")

            ai_type = conv.get('metadata', {}).get('ai_type', 'unknown')
            folder_id = ai_types.get(ai_type, parent_folder_id)

            doc_id = self.convert_conversation(conv, folder_id)
            if doc_id:
                doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
                converted_docs[f"conversation_{idx}"] = doc_url

        # Crear documento maestro de índice
        print(f"\n📋 Creando documento índice maestro...")
        index_doc_id = self.create_master_index(
            corpus,
            converted_docs,
            parent_folder_id
        )

        if index_doc_id:
            converted_docs['master_index'] = f"https://docs.google.com/document/d/{index_doc_id}/edit"

        return converted_docs

    def create_master_index(self, corpus: Dict, doc_urls: Dict, folder_id: str) -> str:
        """Crea documento índice maestro con estadísticas y enlaces"""
        title = f"NEXUS CORPUS - ÍNDICE MAESTRO - {datetime.now().strftime('%Y-%m-%d')}"

        doc_id = self.create_document(title, folder_id)
        if not doc_id:
            return None

        # Construir contenido del índice
        stats = corpus.get('statistics', {})

        content = f"""NEXUS OMEGA - CORPUS UNIFICADO
Archivo Maestro de Investigación Doctoral
Israel Realivazquez

═══════════════════════════════════════════════════════════════

📊 ESTADÍSTICAS GENERALES

Total de Conversaciones: {stats.get('total_conversations', 0)}
Total de Mensajes: {stats.get('total_messages', 0)}
Fuentes Integradas: {stats.get('total_sources', 0)}
Fecha de Creación: {corpus.get('created_at', 'N/A')}

═══════════════════════════════════════════════════════════════

🤖 DISTRIBUCIÓN POR IA

"""

        for ai_type, count in stats.get('ai_types', {}).items():
            content += f"• {ai_type.upper()}: {count} conversaciones\n"

        content += f"""

═══════════════════════════════════════════════════════════════

📁 FUENTES

"""

        for source, data in corpus.get('sources', {}).items():
            if data:
                content += f"\n{source.upper()}:\n"
                for file_info in data:
                    content += f"  • {file_info.get('file', 'N/A')} - {file_info.get('conversations', 0)} conversaciones\n"

        content += f"""

═══════════════════════════════════════════════════════════════

🔗 ENLACES A DOCUMENTOS

"""

        for doc_name, doc_url in doc_urls.items():
            if doc_name != 'master_index':
                content += f"\n{doc_name}: {doc_url}\n"

        content += f"""

═══════════════════════════════════════════════════════════════

📚 METADATOS DE ANÁLISIS

Recomendación de Análisis: {corpus.get('analysis_metadata', {}).get('recommended_approach', 'N/A')}
Estado: {corpus.get('analysis_metadata', {}).get('claude_analysis_ready', False)}

Prompts de Análisis Sugeridos:
"""

        for prompt in corpus.get('analysis_metadata', {}).get('analysis_prompts', []):
            content += f"• {prompt}\n"

        content += "\n\n═══════════════════════════════════════════════════════════════\n"
        content += "🔱 NEXUS OMEGA - Arquitectura de Conocimiento Distribuido\n"

        # Insertar contenido
        try:
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={
                    'requests': [{
                        'insertText': {
                            'location': {'index': 1},
                            'text': content
                        }
                    }]
                }
            ).execute()

            print("✅ Documento índice maestro creado")
            return doc_id

        except HttpError as error:
            print(f"❌ Error creando índice: {error}")
            return None


def main():
    """Función principal"""
    print("🔱 NEXUS TO GOOGLE DOCS CONVERTER")
    print("=" * 80)

    if not GOOGLE_AVAILABLE:
        print("\n❌ ERROR: Librerías de Google no disponibles")
        print("\nInstala con:")
        print("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return

    # Verificar archivo de credenciales
    if not os.path.exists('credentials.json'):
        print("\n❌ ERROR: credentials.json no encontrado")
        print("\nPara obtener credenciales:")
        print("1. Ve a https://console.cloud.google.com/")
        print("2. Crea un proyecto nuevo")
        print("3. Habilita Google Docs API y Google Drive API")
        print("4. Crea credenciales OAuth 2.0")
        print("5. Descarga como 'credentials.json' en este directorio")
        return

    # Inicializar conversor
    try:
        converter = NexusToGoogleDocs()
    except Exception as e:
        print(f"❌ Error inicializando: {e}")
        return

    # Buscar corpus unificado
    corpus_path = "./nexus_unified_corpus/corpus_unified.json"

    if not os.path.exists(corpus_path):
        print(f"\n❌ Corpus no encontrado: {corpus_path}")
        print("\nPrimero ejecuta: python nexus_corpus_unifier.py")
        return

    # Convertir corpus
    try:
        doc_urls = converter.convert_corpus_to_docs(corpus_path)

        print("\n" + "=" * 80)
        print("✅ CONVERSIÓN COMPLETADA")
        print("=" * 80)
        print(f"\n📄 Documentos creados: {len(doc_urls)}")
        print("\n🔗 ENLACES:")
        for name, url in doc_urls.items():
            print(f"  • {name}: {url}")

        # Guardar enlaces
        links_path = "./nexus_unified_corpus/google_docs_links.json"
        with open(links_path, 'w', encoding='utf-8') as f:
            json.dump(doc_urls, f, indent=2)

        print(f"\n💾 Enlaces guardados en: {links_path}")

        # Mostrar documento maestro
        if 'master_index' in doc_urls:
            print("\n" + "=" * 80)
            print("📋 DOCUMENTO MAESTRO:")
            print(doc_urls['master_index'])
            print("=" * 80)

    except Exception as e:
        print(f"\n❌ Error durante conversión: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
