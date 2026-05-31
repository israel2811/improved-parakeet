#!/usr/bin/env python3
"""
GENERADOR DE ÍNDICES MAESTROS
Proyecto CCA/NEXUS
"""

import json
import csv
from pathlib import Path
from datetime import datetime

def create_master_index():
    base = Path("CCA_NEXUS_RECONSTRUCCION_CONVERSACIONAL_20260531_101107")

    # Leer archivos HTML para extraer metadatos
    html_dir = base / "03_HTML_CANONICO"
    md_dir = base / "04_MARKDOWN_RECONSTRUIDO"

    records = []

    for html_file in sorted(html_dir.glob("*.html")):
        base_name = html_file.stem.replace('_CANONICO', '')
        md_file = md_dir / f"{base_name}_RECONSTRUIDO.md"

        # Extraer info del nombre
        parts = base_name.split('_')
        platform = parts[0]
        conv_id = parts[1] if len(parts) > 1 else 'UNKNOWN'

        # Intentar leer título del HTML
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
                # Buscar título en el HTML
                import re
                title_match = re.search(r'<title>CCA/NEXUS - (.+?)</title>', html_content)
                title = title_match.group(1) if title_match else 'Sin título'

                # Contar mensajes
                msg_count = html_content.count('<div class="message')
                user_count = html_content.count('class="message user"')
                assistant_count = html_content.count('class="message assistant"')

        except:
            title = 'Error al leer'
            msg_count = 0
            user_count = 0
            assistant_count = 0

        record = {
            'ID_reconstruccion': f"RECON_{len(records)+1:04d}",
            'Plataforma': platform,
            'Titulo_conversacion': title,
            'ID_conversacion': conv_id,
            'Archivo_original': f"demo_data/exports/{platform.lower()}_conversations.json",
            'HTML_reconstruido': str(html_file.name),
            'Markdown_reconstruido': str(md_file.name) if md_file.exists() else 'N/A',
            'Fecha_reconstruccion': datetime.now().isoformat(),
            'Mensajes_totales': msg_count,
            'Mensajes_usuario': user_count,
            'Mensajes_asistente': assistant_count,
            'Estado_reconstruccion': 'Reconstruida completa',
            'Prioridad': 'P0',
            'Google_Doc_URL': 'PENDIENTE_SUBIDA_MANUAL',
            'Notas': 'Archivos listos en 05_GOOGLE_DOCS_READY'
        }

        records.append(record)

    # Guardar CSV
    csv_path = base / "06_INDICES" / "INDICE_CONVERSACIONES_RECONSTRUIDAS_CCA_NEXUS_20260531.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        if records:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)

    print(f"✅ CSV: {csv_path}")

    # Guardar JSON
    json_path = csv_path.with_suffix('.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON: {json_path}")

    # Guardar Markdown
    md_path = csv_path.with_suffix('.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# 📋 ÍNDICE MAESTRO DE CONVERSACIONES RECONSTRUIDAS\n\n")
        f.write(f"**Fecha:** {datetime.now().isoformat()}\n\n")
        f.write(f"**Total conversaciones:** {len(records)}\n\n")
        f.write("---\n\n")

        for rec in records:
            f.write(f"## {rec['ID_reconstruccion']}: {rec['Titulo_conversacion']}\n\n")
            f.write(f"- **Plataforma:** {rec['Plataforma']}\n")
            f.write(f"- **ID Conversación:** `{rec['ID_conversacion']}`\n")
            f.write(f"- **Archivo original:** `{rec['Archivo_original']}`\n")
            f.write(f"- **HTML:** `{rec['HTML_reconstruido']}`\n")
            f.write(f"- **Markdown:** `{rec['Markdown_reconstruido']}`\n")
            f.write(f"- **Mensajes totales:** {rec['Mensajes_totales']}\n")
            f.write(f"- **Estado:** {rec['Estado_reconstruccion']}\n")
            f.write(f"- **Google Docs:** {rec['Google_Doc_URL']}\n\n")
            f.write("---\n\n")

    print(f"✅ Markdown: {md_path}")

    return records

if __name__ == '__main__':
    print("📊 GENERANDO ÍNDICES MAESTROS...")
    records = create_master_index()
    print(f"✅ {len(records)} conversaciones indexadas")
