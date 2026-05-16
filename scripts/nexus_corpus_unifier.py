#!/usr/bin/env python3
"""
🔱 NEXUS CORPUS UNIFIER V1.0
Unifica corpus de conversaciones desde Google Drive, Dropbox y OneDrive
Crea un corpus maestro analizable por Claude Desktop

Autor: Israel Realivazquez
Fecha: 2026-05-16
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class NexusCorpusUnifier:
    """Unificador de corpus multi-plataforma"""

    def __init__(self, output_dir: str = "./unified_corpus"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.unified_corpus = {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "system": "Nexus Omega",
            "owner": "Israel Realivazquez",
            "sources": {
                "google_drive": [],
                "dropbox": [],
                "onedrive": []
            },
            "statistics": {
                "total_conversations": 0,
                "total_messages": 0,
                "total_sources": 0,
                "ai_types": {}
            },
            "conversations": []
        }

    def add_corpus(self, corpus_path: str, source_type: str) -> None:
        """
        Añade un corpus al unificado

        Args:
            corpus_path: Ruta al archivo JSON del corpus
            source_type: 'google_drive', 'dropbox' o 'onedrive'
        """
        print(f"[*] Procesando corpus de {source_type}: {corpus_path}")

        try:
            with open(corpus_path, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)

            # Validar estructura
            if 'conversations' not in corpus_data:
                print(f"[!] Advertencia: Corpus sin campo 'conversations', intentando reconstruir...")
                corpus_data = {'conversations': [corpus_data]}

            # Añadir metadatos de fuente a cada conversación
            for conv in corpus_data['conversations']:
                if 'metadata' not in conv:
                    conv['metadata'] = {}

                conv['metadata']['source_platform'] = source_type
                conv['metadata']['imported_at'] = datetime.now().isoformat()
                conv['metadata']['original_file'] = corpus_path

                # Actualizar estadísticas
                ai_type = conv.get('metadata', {}).get('ai_type', 'unknown')
                self.unified_corpus['statistics']['ai_types'][ai_type] = \
                    self.unified_corpus['statistics']['ai_types'].get(ai_type, 0) + 1

                self.unified_corpus['conversations'].append(conv)

            # Actualizar fuentes
            self.unified_corpus['sources'][source_type].append({
                'file': corpus_path,
                'conversations': len(corpus_data['conversations']),
                'imported_at': datetime.now().isoformat()
            })

            self.unified_corpus['statistics']['total_sources'] += 1

            print(f"[✓] {len(corpus_data['conversations'])} conversaciones añadidas desde {source_type}")

        except Exception as e:
            print(f"[✗] Error procesando {corpus_path}: {e}")

    def calculate_statistics(self) -> None:
        """Calcula estadísticas finales del corpus unificado"""
        total_messages = 0

        for conv in self.unified_corpus['conversations']:
            messages = conv.get('messages', [])
            total_messages += len(messages)

        self.unified_corpus['statistics']['total_conversations'] = len(self.unified_corpus['conversations'])
        self.unified_corpus['statistics']['total_messages'] = total_messages

    def generate_analysis_metadata(self) -> Dict[str, Any]:
        """Genera metadatos para análisis por Claude"""
        return {
            "claude_analysis_ready": True,
            "recommended_approach": "sequential_conversation_analysis",
            "chunking_strategy": {
                "method": "by_conversation",
                "max_tokens_per_chunk": 100000,
                "overlap": False
            },
            "analysis_prompts": [
                "Analiza las ideas originales de Israel sobre neuroanatomía y comunicación auditiva",
                "Extrae conceptos clave relacionados con vocología sistémica",
                "Identifica puentes entre CCA (Comunicación Auditiva) y AAV (Anatomía y Vocología)",
                "Genera estructura de tesis doctoral basada en el corpus completo"
            ],
            "export_formats": {
                "markdown": f"{self.output_dir}/corpus_analysis.md",
                "json": f"{self.output_dir}/corpus_unified.json",
                "html": f"{self.output_dir}/corpus_viewer.html"
            }
        }

    def save_unified_corpus(self) -> str:
        """Guarda el corpus unificado"""
        self.calculate_statistics()
        analysis_metadata = self.generate_analysis_metadata()
        self.unified_corpus['analysis_metadata'] = analysis_metadata

        output_path = self.output_dir / "corpus_unified.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.unified_corpus, f, indent=2, ensure_ascii=False)

        print(f"\n{'='*60}")
        print(f"🔱 CORPUS UNIFICADO GENERADO")
        print(f"{'='*60}")
        print(f"📁 Archivo: {output_path}")
        print(f"💬 Conversaciones totales: {self.unified_corpus['statistics']['total_conversations']}")
        print(f"📨 Mensajes totales: {self.unified_corpus['statistics']['total_messages']}")
        print(f"🤖 IAs representadas: {', '.join(self.unified_corpus['statistics']['ai_types'].keys())}")
        print(f"📊 Fuentes:")
        for source, data in self.unified_corpus['sources'].items():
            if data:
                print(f"   - {source}: {len(data)} archivos")
        print(f"{'='*60}\n")

        return str(output_path)

    def generate_html_viewer(self) -> None:
        """Genera un visor HTML interactivo del corpus"""
        html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔱 Nexus Unified Corpus Viewer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0a0c;
            --bg-secondary: #16161a;
            --bg-tertiary: #1e1e24;
            --text-primary: #e0e0e6;
            --text-secondary: #a0a0a8;
            --accent: #00d2ff;
            --accent-dim: #0099cc;
            --border: #2a2a30;
            --success: #00ff88;
            --warning: #ffaa00;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }

        .header {
            background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
            padding: 2rem;
            text-align: center;
            border-bottom: 2px solid var(--accent);
            box-shadow: 0 4px 20px rgba(0, 210, 255, 0.1);
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: 300;
            letter-spacing: 3px;
            color: var(--accent);
            margin-bottom: 0.5rem;
        }

        .header .subtitle {
            color: var(--text-secondary);
            font-size: 1rem;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .stat-card {
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid var(--border);
            text-align: center;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
            margin-bottom: 0.5rem;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .controls {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem 2rem;
        }

        .search-box {
            width: 100%;
            padding: 1rem;
            background: var(--bg-secondary);
            border: 2px solid var(--border);
            border-radius: 10px;
            color: var(--text-primary);
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }

        .search-box:focus {
            border-color: var(--accent);
        }

        .filters {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }

        .filter-btn {
            padding: 0.5rem 1rem;
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            border-radius: 5px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.3s;
        }

        .filter-btn:hover, .filter-btn.active {
            background: var(--accent-dim);
            color: var(--text-primary);
            border-color: var(--accent);
        }

        .conversations {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem 2rem;
        }

        .conversation-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .conversation-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 210, 255, 0.15);
        }

        .conversation-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }

        .ai-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: var(--accent-dim);
            color: var(--text-primary);
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .source-badge {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        .message {
            margin: 1rem 0;
            padding: 1rem;
            background: var(--bg-tertiary);
            border-left: 3px solid var(--accent);
            border-radius: 5px;
        }

        .message-role {
            font-size: 0.8rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }

        .message-content {
            color: var(--text-primary);
        }

        .hidden { display: none; }

        .load-more {
            text-align: center;
            padding: 2rem;
        }

        .load-more-btn {
            padding: 1rem 2rem;
            background: var(--accent-dim);
            color: var(--text-primary);
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.3s;
        }

        .load-more-btn:hover {
            background: var(--accent);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔱 NEXUS UNIFIED CORPUS</h1>
        <p class="subtitle">Multi-Platform AI Conversations Archive | Israel Realivazquez PhD Research</p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value" id="total-conversations">0</div>
            <div class="stat-label">Conversaciones</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="total-messages">0</div>
            <div class="stat-label">Mensajes</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="total-sources">0</div>
            <div class="stat-label">Fuentes</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="ai-types">0</div>
            <div class="stat-label">Tipos de IA</div>
        </div>
    </div>

    <div class="controls">
        <input type="text" class="search-box" id="search" placeholder="🔍 Buscar en todo el corpus..." />
        <div class="filters" id="filters"></div>
    </div>

    <div class="conversations" id="conversations"></div>

    <div class="load-more">
        <button class="load-more-btn" id="load-more">Cargar más conversaciones</button>
    </div>

    <script>
        // Cargar datos del corpus
        const corpusData = {{CORPUS_DATA}};

        // Renderizar estadísticas
        document.getElementById('total-conversations').textContent = corpusData.statistics.total_conversations;
        document.getElementById('total-messages').textContent = corpusData.statistics.total_messages;
        document.getElementById('total-sources').textContent = corpusData.statistics.total_sources;
        document.getElementById('ai-types').textContent = Object.keys(corpusData.statistics.ai_types).length;

        // Crear filtros
        const filtersContainer = document.getElementById('filters');
        Object.keys(corpusData.statistics.ai_types).forEach(aiType => {
            const btn = document.createElement('button');
            btn.className = 'filter-btn';
            btn.textContent = aiType;
            btn.dataset.aiType = aiType;
            btn.onclick = () => filterByAI(aiType);
            filtersContainer.appendChild(btn);
        });

        // Renderizar conversaciones
        let currentPage = 0;
        const pageSize = 10;

        function renderConversations(start = 0, end = pageSize) {
            const container = document.getElementById('conversations');
            const conversations = corpusData.conversations.slice(start, end);

            conversations.forEach(conv => {
                const card = document.createElement('div');
                card.className = 'conversation-card';
                card.dataset.aiType = conv.metadata?.ai_type || 'unknown';
                card.innerHTML = `
                    <div class="conversation-header">
                        <span class="ai-badge">${conv.metadata?.ai_type || 'Unknown'}</span>
                        <span class="source-badge">📁 ${conv.metadata?.source_platform || 'Unknown'}</span>
                    </div>
                    ${conv.messages.slice(0, 3).map(msg => `
                        <div class="message">
                            <div class="message-role">${msg.role}</div>
                            <div class="message-content">${msg.content.substring(0, 200)}${msg.content.length > 200 ? '...' : ''}</div>
                        </div>
                    `).join('')}
                    ${conv.messages.length > 3 ? `<p style="text-align: center; color: var(--text-secondary);">... y ${conv.messages.length - 3} mensajes more</p>` : ''}
                `;
                container.appendChild(card);
            });

            currentPage = end;
        }

        // Buscar
        document.getElementById('search').addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            document.querySelectorAll('.conversation-card').forEach(card => {
                const content = card.textContent.toLowerCase();
                card.style.display = content.includes(query) ? 'block' : 'none';
            });
        });

        // Filtrar por IA
        function filterByAI(aiType) {
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.aiType === aiType);
            });

            document.querySelectorAll('.conversation-card').forEach(card => {
                card.style.display = card.dataset.aiType === aiType ? 'block' : 'none';
            });
        }

        // Cargar más
        document.getElementById('load-more').addEventListener('click', () => {
            renderConversations(currentPage, currentPage + pageSize);
        });

        // Inicializar
        renderConversations();
    </script>
</body>
</html>
        """

        # Insertar datos del corpus
        corpus_json = json.dumps(self.unified_corpus, ensure_ascii=False)
        html_content = html_template.replace('{{CORPUS_DATA}}', corpus_json)

        output_path = self.output_dir / "corpus_viewer.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"[✓] Visor HTML generado: {output_path}")


def main():
    """Función principal"""
    print("🔱 NEXUS CORPUS UNIFIER V1.0")
    print("=" * 60)

    unifier = NexusCorpusUnifier(output_dir="./nexus_unified_corpus")

    # Aquí añadirías tus corpus reales
    # Ejemplo:
    # unifier.add_corpus("./gdrive_corpus.json", "google_drive")
    # unifier.add_corpus("./dropbox_corpus.json", "dropbox")
    # unifier.add_corpus("./onedrive_corpus.json", "onedrive")

    print("\n[i] INSTRUCCIONES DE USO:")
    print("1. Exporta tus conversaciones usando los servidores MCP")
    print("2. Ejecuta: unifier.add_corpus('ruta/al/corpus.json', 'source_type')")
    print("3. Ejecuta: unifier.save_unified_corpus()")
    print("4. Ejecuta: unifier.generate_html_viewer()")

    output_path = unifier.save_unified_corpus()
    unifier.generate_html_viewer()

    print(f"\n[✓] PROCESO COMPLETADO")
    print(f"[✓] Corpus unificado listo para análisis por Claude Desktop")
    print(f"[✓] Archivo principal: {output_path}")


if __name__ == "__main__":
    main()
