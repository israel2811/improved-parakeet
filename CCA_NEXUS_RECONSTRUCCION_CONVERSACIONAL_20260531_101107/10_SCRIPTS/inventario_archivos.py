#!/usr/bin/env python3
"""
SCRIPT DE INVENTARIO DE ARCHIVOS CONVERSACIONALES
Proyecto: CCA/NEXUS - Reconstrucción Conversacional
Fecha: 2026-05-31
"""

import os
import json
import csv
import hashlib
from pathlib import Path
from datetime import datetime

# Patrones de búsqueda
PATTERNS = {
    'keywords': [
        'takeout', 'google', 'conversations', 'conversation', 'chat', 'chats',
        'export', 'exported', 'claude', 'chatgpt', 'gemini', 'notebooklm',
        'codex', 'antigravity', 'nexus', 'cca', 'raw', 'corpus', 'conversaciones',
        'vol02', 'vol04', 'anthropic', 'openai', 'notebook', 'drive', 'dropbox', 'onedrive'
    ],
    'extensions': [
        '.json', '.jsonl', '.html', '.htm', '.txt', '.md', '.docx',
        '.csv', '.xlsx', '.zip', '.tgz', '.tar.gz', '.tar', '.rtf', '.odt'
    ]
}

def get_file_hash(filepath, hash_type='sha256'):
    """Calcula hash del archivo"""
    try:
        h = hashlib.new(hash_type)
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                h.update(chunk)
        return h.hexdigest()
    except:
        return "ERROR"

def detect_probable_platform(filename, path):
    """Detecta plataforma probable"""
    fn_lower = filename.lower()
    path_lower = str(path).lower()

    if 'chatgpt' in fn_lower or 'openai' in fn_lower:
        return 'ChatGPT'
    elif 'claude' in fn_lower or 'anthropic' in fn_lower:
        return 'Claude'
    elif 'gemini' in fn_lower or 'bard' in fn_lower:
        return 'Gemini'
    elif 'notebooklm' in fn_lower or 'notebook' in fn_lower:
        return 'NotebookLM'
    elif 'codex' in fn_lower:
        return 'Codex'
    elif 'antigravity' in fn_lower:
        return 'Antigravity'
    elif 'takeout' in path_lower:
        return 'Google Takeout'
    else:
        return 'Desconocida'

def detect_export_type(filepath, filename):
    """Detecta tipo de export"""
    ext = Path(filename).suffix.lower()
    fn_lower = filename.lower()

    if ext == '.json':
        if 'conversation' in fn_lower:
            return 'Export conversacional JSON'
        elif 'reconstructed' in fn_lower:
            return 'Conversación ya reconstruida'
        elif 'corpus' in fn_lower:
            return 'Corpus unificado'
        else:
            return 'JSON (tipo por determinar)'
    elif ext in ['.html', '.htm']:
        return 'Export HTML conversacional'
    elif ext in ['.txt', '.md']:
        return 'Export textual conversacional'
    elif ext == '.docx':
        return 'Documento Word conversacional'
    elif ext in ['.zip', '.tgz', '.tar.gz', '.tar']:
        return 'Archivo comprimido'
    else:
        return 'Formato no estándar'

def calculate_priority(filename, path, size):
    """Calcula prioridad P0-P5"""
    fn_lower = filename.lower()
    path_lower = str(path).lower()

    # P0 - Export crudo conversacional crítico
    if 'conversations.json' in fn_lower and 'reconstructed' not in fn_lower:
        return 'P0'
    if 'export' in fn_lower and any(x in fn_lower for x in ['chatgpt', 'claude', 'gemini']) and size > 1000:
        return 'P0'

    # P1 - Conversación reconstruible importante
    if 'chat' in fn_lower or 'conversation' in fn_lower:
        if 'reconstructed' not in fn_lower and size > 500:
            return 'P1'

    # P2 - Ya procesado
    if 'reconstructed' in fn_lower or 'canonical' in fn_lower:
        return 'P2'

    # P3 - Índice/referencia
    if any(x in fn_lower for x in ['index', 'indice', 'inventario', 'manifest']):
        return 'P3'

    # P4 - Infraestructura
    if any(x in fn_lower for x in ['script', 'config', 'setup']):
        return 'P4'

    # P5 - Dudoso
    return 'P5'

def scan_directory(base_path):
    """Escanea directorio en busca de archivos conversacionales"""
    findings = []
    base_path = Path(base_path)

    for item in base_path.rglob('*'):
        if not item.is_file():
            continue

        filename = item.name
        ext = item.suffix.lower()

        # Filtrar por extensión
        if ext not in PATTERNS['extensions']:
            continue

        # Filtrar por keywords
        if not any(kw in str(item).lower() for kw in PATTERNS['keywords']):
            continue

        # Recopilar información
        try:
            size = item.stat().st_size
            mtime = datetime.fromtimestamp(item.stat().st_mtime).isoformat()
        except:
            size = 0
            mtime = "ERROR"

        platform = detect_probable_platform(filename, item)
        export_type = detect_export_type(item, filename)
        priority = calculate_priority(filename, item, size)

        findings.append({
            'ruta': str(item),
            'nombre': filename,
            'extension': ext,
            'tamaño_bytes': size,
            'fecha_modificacion': mtime,
            'formato_probable': export_type,
            'plataforma_probable': platform,
            'prioridad': priority,
            'hash_sha256': get_file_hash(item) if size < 100_000_000 else 'ARCHIVO_MUY_GRANDE'
        })

    return findings

def main():
    print("🔍 ESCANEANDO ARCHIVOS CONVERSACIONALES...")
    print("=" * 80)

    base = Path('/home/user/improved-parakeet')
    findings = scan_directory(base)

    findings.sort(key=lambda x: (x['prioridad'], -x['tamaño_bytes']))

    # Generar ID
    for idx, item in enumerate(findings, 1):
        item['id'] = f"FILE_{idx:04d}"

    # Guardar CSV
    csv_path = 'CCA_NEXUS_RECONSTRUCCION_CONVERSACIONAL_20260531_101107/01_INVENTARIO/INVENTARIO_EXPORTS_CONVERSACIONALES_CCA_NEXUS_20260531.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        if findings:
            writer = csv.DictWriter(f, fieldnames=findings[0].keys())
            writer.writeheader()
            writer.writerows(findings)

    print(f"✅ CSV guardado: {csv_path}")
    print(f"📊 Archivos encontrados: {len(findings)}")

    # Resumen por prioridad
    from collections import Counter
    priority_counts = Counter(f['prioridad'] for f in findings)
    print("\n📈 RESUMEN POR PRIORIDAD:")
    for p in ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']:
        count = priority_counts.get(p, 0)
        if count > 0:
            print(f"   {p}: {count} archivos")

    # Guardar JSON
    json_path = csv_path.replace('.csv', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON guardado: {json_path}")

    return findings

if __name__ == '__main__':
    findings = main()
