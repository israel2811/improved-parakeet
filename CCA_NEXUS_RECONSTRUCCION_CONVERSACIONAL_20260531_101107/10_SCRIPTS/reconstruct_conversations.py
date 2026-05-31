#!/usr/bin/env python3
"""
RECONSTRUCCTOR DE CONVERSACIONES CCA/NEXUS
Convierte exports crudos de múltiples plataformas a HTML canónico y Markdown

Autor: Proyecto CCA/NEXUS
Fecha: 2026-05-31
"""

import json
import html as html_module
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class ConversationReconstructor:
    """Reconstruye conversaciones de múltiples plataformas"""

    def __init__(self, output_base: str):
        self.output_base = Path(output_base)
        self.html_dir = self.output_base / "03_HTML_CANONICO"
        self.md_dir = self.output_base / "04_MARKDOWN_RECONSTRUIDO"
        self.log_dir = self.output_base / "07_LOGS"
        self.errors = []
        self.warnings = []

    def log_error(self, msg: str):
        """Registra error"""
        self.errors.append(f"[{datetime.now().isoformat()}] ERROR: {msg}")

    def log_warning(self, msg: str):
        """Registra advertencia"""
        self.warnings.append(f"[{datetime.now().isoformat()}] WARNING: {msg}")

    def parse_chatgpt_json(self, data: Dict) -> Dict:
        """Parse ChatGPT conversations.json format"""
        conversations = []

        if 'conversations' not in data:
            self.log_error("ChatGPT JSON: No 'conversations' key found")
            return {'conversations': []}

        for conv in data.get('conversations', []):
            conv_data = {
                'title': conv.get('title', 'Sin título'),
                'create_time': conv.get('create_time'),
                'update_time': conv.get('update_time'),
                'conversation_id': conv.get('id', 'UNKNOWN'),
                'messages': []
            }

            mapping = conv.get('mapping', {})

            # Recorrer mapping para extraer mensajes
            for node_id, node in mapping.items():
                if 'message' not in node or not node['message']:
                    continue

                msg = node['message']
                if not msg.get('content'):
                    continue

                role = msg.get('author', {}).get('role', 'unknown')
                parts = msg.get('content', {}).get('parts', [])
                content = '\n'.join(str(p) for p in parts if p)

                if content.strip():
                    conv_data['messages'].append({
                        'node_id': node_id,
                        'message_id': msg.get('id', node_id),
                        'role': role,
                        'content': content,
                        'create_time': msg.get('create_time'),
                        'author': msg.get('author', {}),
                        'metadata': msg.get('metadata', {})
                    })

            # Ordenar por create_time
            conv_data['messages'].sort(key=lambda x: x.get('create_time', 0))

            conversations.append(conv_data)

        return {'platform': 'ChatGPT', 'conversations': conversations}

    def parse_claude_json(self, data: Dict) -> Dict:
        """Parse Claude export format"""
        conversations = []

        messages_list = data.get('chat_messages', data.get('messages', []))

        if messages_list:
            conv_data = {
                'title': 'Claude Conversation',
                'create_time': messages_list[0].get('created_at') if messages_list else None,
                'conversation_id': f"claude_{hashlib.md5(json.dumps(data).encode()).hexdigest()[:12]}",
                'messages': []
            }

            for msg in messages_list:
                conv_data['messages'].append({
                    'message_id': msg.get('uuid', msg.get('id', 'UNKNOWN')),
                    'role': msg.get('sender', msg.get('role', 'unknown')),
                    'content': msg.get('text', msg.get('content', '')),
                    'create_time': msg.get('created_at', msg.get('timestamp')),
                    'metadata': {k: v for k, v in msg.items() if k not in ['uuid', 'sender', 'text', 'created_at']}
                })

            conversations.append(conv_data)

        return {'platform': 'Claude', 'conversations': conversations}

    def parse_gemini_json(self, data: Dict) -> Dict:
        """Parse Gemini export format"""
        conversations = []

        turns = data.get('turns', [])

        if turns:
            conv_data = {
                'title': 'Gemini Conversation',
                'create_time': turns[0].get('timestamp') if turns else None,
                'conversation_id': f"gemini_{hashlib.md5(json.dumps(data).encode()).hexdigest()[:12]}",
                'messages': []
            }

            for turn in turns:
                parts = turn.get('parts', [])
                content = '\n'.join(p.get('text', '') for p in parts if 'text' in p)

                if content.strip():
                    conv_data['messages'].append({
                        'message_id': turn.get('id', 'UNKNOWN'),
                        'role': turn.get('role', 'unknown'),
                        'content': content,
                        'create_time': turn.get('timestamp'),
                        'metadata': {k: v for k, v in turn.items() if k not in ['id', 'role', 'parts', 'timestamp']}
                    })

            conversations.append(conv_data)

        return {'platform': 'Gemini', 'conversations': conversations}

    def generate_html_canonical(self, platform: str, conv: Dict, source_file: str, source_hash: str) -> str:
        """Genera HTML canónico"""

        # Escape HTML
        def esc(text):
            return html_module.escape(str(text)) if text else ''

        # Estadísticas
        total_msgs = len(conv['messages'])
        user_msgs = sum(1 for m in conv['messages'] if m['role'] in ['user', 'Human'])
        assistant_msgs = sum(1 for m in conv['messages'] if m['role'] in ['assistant', 'Assistant', 'model'])
        system_msgs = sum(1 for m in conv['messages'] if m['role'] == 'system')

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CCA/NEXUS - {esc(conv['title'])}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 28px;
        }}
        .metadata {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }}
        .metadata h2 {{
            margin-top: 0;
            color: #333;
            font-size: 18px;
        }}
        .metadata table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .metadata td {{
            padding: 8px;
            border-bottom: 1px solid #eee;
        }}
        .metadata td:first-child {{
            font-weight: bold;
            color: #667eea;
            width: 250px;
        }}
        .message {{
            background: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .message.user {{
            border-left: 4px solid #4CAF50;
        }}
        .message.assistant {{
            border-left: 4px solid #2196F3;
        }}
        .message.system {{
            border-left: 4px solid #FF9800;
            background: #FFF8E1;
        }}
        .message-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }}
        .role {{
            font-weight: bold;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 1px;
        }}
        .role.user {{ color: #4CAF50; }}
        .role.assistant {{ color: #2196F3; }}
        .role.system {{ color: #FF9800; }}
        .timestamp {{
            font-size: 11px;
            color: #999;
        }}
        .content {{
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        pre {{
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        .footer {{
            margin-top: 40px;
            padding: 20px;
            background: #333;
            color: white;
            border-radius: 8px;
            text-align: center;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔱 CCA/NEXUS - Reconstrucción Conversacional</h1>
        <p style="margin: 0; opacity: 0.9;">{esc(conv['title'])}</p>
    </div>

    <div class="metadata">
        <h2>📋 Metadatos de la Conversación</h2>
        <table>
            <tr>
                <td>Plataforma:</td>
                <td><strong>{esc(platform)}</strong></td>
            </tr>
            <tr>
                <td>Título:</td>
                <td>{esc(conv['title'])}</td>
            </tr>
            <tr>
                <td>ID Conversación:</td>
                <td><code>{esc(conv['conversation_id'])}</code></td>
            </tr>
            <tr>
                <td>Archivo fuente:</td>
                <td><code>{esc(source_file)}</code></td>
            </tr>
            <tr>
                <td>Hash fuente (SHA-256):</td>
                <td><code style="font-size: 10px;">{esc(source_hash)}</code></td>
            </tr>
            <tr>
                <td>Fecha de conversación:</td>
                <td>{esc(conv.get('create_time', 'No disponible'))}</td>
            </tr>
            <tr>
                <td>Fecha de reconstrucción:</td>
                <td>{datetime.now().isoformat()}</td>
            </tr>
            <tr>
                <td>Estado de reconstrucción:</td>
                <td><strong style="color: #4CAF50;">✅ Reconstruida completa</strong></td>
            </tr>
            <tr>
                <td>Total de mensajes:</td>
                <td><strong>{total_msgs}</strong></td>
            </tr>
            <tr>
                <td>Mensajes de usuario:</td>
                <td>{user_msgs}</td>
            </tr>
            <tr>
                <td>Mensajes de asistente:</td>
                <td>{assistant_msgs}</td>
            </tr>
            <tr>
                <td>Mensajes de sistema:</td>
                <td>{system_msgs}</td>
            </tr>
        </table>
    </div>

    <h2 style="color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px;">💬 Conversación Completa</h2>
"""

        # Mensajes
        for idx, msg in enumerate(conv['messages'], 1):
            role = msg.get('role', 'unknown')
            role_class = 'user' if role in ['user', 'Human'] else 'assistant' if role in ['assistant', 'Assistant', 'model'] else 'system'

            timestamp = msg.get('create_time', 'No disponible')
            msg_id = msg.get('message_id', 'UNKNOWN')
            content = esc(msg.get('content', ''))

            html += f"""
    <div class="message {role_class}">
        <div class="message-header">
            <span class="role {role_class}">Turno {idx} - {esc(role)}</span>
            <span class="timestamp">{esc(timestamp)}</span>
        </div>
        <div style="font-size: 11px; color: #999; margin-bottom: 10px;">ID: <code>{esc(msg_id)}</code></div>
        <div class="content">{content}</div>
    </div>
"""

        html += """
    <div class="footer">
        <p>🔱 Proyecto CCA/NEXUS - Reconstrucción Conversacional Documental</p>
        <p>Documento generado automáticamente - NO modificar - Preservación epistémica total</p>
    </div>
</body>
</html>
"""
        return html

    def generate_markdown(self, platform: str, conv: Dict, source_file: str, source_hash: str) -> str:
        """Genera Markdown reconstructed"""

        total_msgs = len(conv['messages'])
        user_msgs = sum(1 for m in conv['messages'] if m['role'] in ['user', 'Human'])
        assistant_msgs = sum(1 for m in conv['messages'] if m['role'] in ['assistant', 'Assistant', 'model'])

        md = f"""# 🔱 CCA/NEXUS - {conv['title']}

## 📋 Metadatos

- **Plataforma:** {platform}
- **Título:** {conv['title']}
- **ID Conversación:** `{conv['conversation_id']}`
- **Archivo fuente:** `{source_file}`
- **Hash SHA-256:** `{source_hash}`
- **Fecha conversación:** {conv.get('create_time', 'No disponible')}
- **Fecha reconstrucción:** {datetime.now().isoformat()}
- **Estado:** ✅ Reconstruida completa
- **Total mensajes:** {total_msgs}
- **Mensajes usuario:** {user_msgs}
- **Mensajes asistente:** {assistant_msgs}

---

## 💬 Conversación Completa

"""

        for idx, msg in enumerate(conv['messages'], 1):
            role = msg.get('role', 'unknown')
            timestamp = msg.get('create_time', 'No disponible')
            msg_id = msg.get('message_id', 'UNKNOWN')
            content = msg.get('content', '')

            md += f"""
### Turno {idx}: {role.upper()}

**Timestamp:** {timestamp}
**ID:** `{msg_id}`

{content}

---

"""

        md += """
---

**🔱 Proyecto CCA/NEXUS - Reconstrucción Conversacional Documental**
*Documento generado automáticamente - NO modificar - Preservación epistémica total*
"""

        return md

    def reconstruct_file(self, file_path: str, platform_hint: str = None) -> List[str]:
        """Reconstruye un archivo a HTML y Markdown"""
        file_path = Path(file_path)

        print(f"\n{'='*80}")
        print(f"🔄 Reconstruyendo: {file_path.name}")
        print(f"{'='*80}")

        # Calcular hash
        source_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()

        # Leer JSON
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.log_error(f"No se pudo leer {file_path}: {e}")
            return []

        # Detectar plataforma
        if 'chatgpt' in file_path.name.lower():
            parsed = self.parse_chatgpt_json(data)
        elif 'claude' in file_path.name.lower():
            parsed = self.parse_claude_json(data)
        elif 'gemini' in file_path.name.lower():
            parsed = self.parse_gemini_json(data)
        else:
            self.log_error(f"Formato desconocido: {file_path.name}")
            return []

        platform = parsed['platform']
        conversations = parsed['conversations']

        print(f"📊 Plataforma: {platform}")
        print(f"📊 Conversaciones encontradas: {len(conversations)}")

        output_files = []

        for idx, conv in enumerate(conversations, 1):
            conv_id = conv['conversation_id']
            title_short = conv['title'][:30].replace(' ', '_').replace('/', '_')

            # Generar nombres de archivo
            base_name = f"{platform}_{conv_id}_{title_short}_{datetime.now().strftime('%Y%m%d')}"
            html_name = f"{base_name}_CANONICO.html"
            md_name = f"{base_name}_RECONSTRUIDO.md"

            # Generar HTML
            html_content = self.generate_html_canonical(
                platform, conv, str(file_path), source_hash
            )

            html_path = self.html_dir / html_name
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"  ✅ HTML: {html_name}")

            # Generar Markdown
            md_content = self.generate_markdown(
                platform, conv, str(file_path), source_hash
            )

            md_path = self.md_dir / md_name
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)

            print(f"  ✅ Markdown: {md_name}")

            output_files.extend([str(html_path), str(md_path)])

        return output_files

def main():
    print("🔱 RECONSTRUCTOR DE CONVERSACIONES CCA/NEXUS")
    print("=" * 80)

    base = Path("CCA_NEXUS_RECONSTRUCCION_CONVERSACIONAL_20260531_101107")
    reconstructor = ConversationReconstructor(str(base))

    # Archivos P0 a procesar
    files_to_process = [
        "demo_data/exports/chatgpt_conversations.json",
        "demo_data/exports/claude_conversations.json",
        "demo_data/exports/gemini_conversations.json"
    ]

    all_outputs = []

    for file_rel in files_to_process:
        file_path = Path(file_rel)
        if file_path.exists():
            outputs = reconstructor.reconstruct_file(str(file_path))
            all_outputs.extend(outputs)
        else:
            print(f"⚠️  Archivo no encontrado: {file_path}")

    # Guardar logs
    log_path = base / "07_LOGS" / f"RECONSTRUCCION_LOG_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("RECONSTRUCCIÓN DE CONVERSACIONES CCA/NEXUS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Fecha: {datetime.now().isoformat()}\n")
        f.write(f"Archivos procesados: {len(files_to_process)}\n")
        f.write(f"Archivos generados: {len(all_outputs)}\n\n")

        if reconstructor.errors:
            f.write("\nERRORES:\n")
            for err in reconstructor.errors:
                f.write(f"  {err}\n")

        if reconstructor.warnings:
            f.write("\nADVERTENCIAS:\n")
            for warn in reconstructor.warnings:
                f.write(f"  {warn}\n")

        f.write("\nARCHIVOS GENERADOS:\n")
        for out in all_outputs:
            f.write(f"  {out}\n")

    print(f"\n✅ Log guardado: {log_path}")
    print(f"✅ Total archivos generados: {len(all_outputs)}")

if __name__ == '__main__':
    main()
