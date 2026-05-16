#!/usr/bin/env python3
"""
🔱 NEXUS CLAUDE WORKFLOW
Workflow automatizado específicamente diseñado para ejecutarse con Claude Desktop

Este script puede ser invocado directamente desde Claude Desktop usando:
"Ejecuta nexus_claude_workflow.py con modo [reconstruction|sync|full]"

Autor: Israel Realivazquez
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path


class ClaudeWorkflow:
    """Workflow optimizado para Claude Desktop"""

    def __init__(self, mode: str = "full"):
        self.mode = mode
        self.workspace = Path("./nexus_workspace")
        self.workspace.mkdir(exist_ok=True)

    def generate_claude_instructions(self) -> str:
        """
        Genera instrucciones específicas para que Claude ejecute vía MCP
        """
        instructions = {
            "workflow_id": f"nexus_{self.mode}_{int(datetime.now().timestamp())}",
            "mode": self.mode,
            "timestamp": datetime.now().isoformat(),
            "steps": []
        }

        if self.mode in ["reconstruction", "full"]:
            instructions["steps"].extend([
                {
                    "step": 1,
                    "action": "list_dropbox_exports",
                    "tool": "dropbox_list_files",
                    "args": {"path": "/Nexus/exports", "recursive": True},
                    "description": "Listar todos los archivos de export en Dropbox"
                },
                {
                    "step": 2,
                    "action": "list_onedrive_exports",
                    "tool": "onedrive_list_files",
                    "args": {"path": "/Nexus/exports", "recursive": True},
                    "description": "Listar todos los archivos de export en OneDrive"
                },
                {
                    "step": 3,
                    "action": "reconstruct_each_file",
                    "description": "Para cada archivo encontrado, ejecutar reconstruction con el ai_type correcto",
                    "tools": [
                        "dropbox_reconstruct_conversations",
                        "onedrive_reconstruct_conversations"
                    ]
                }
            ])

        if self.mode in ["corpus", "full"]:
            instructions["steps"].extend([
                {
                    "step": 4,
                    "action": "create_dropbox_corpus",
                    "tool": "dropbox_create_corpus",
                    "args": {
                        "source_paths": ["<todos los archivos reconstructed de Dropbox>"],
                        "output_path": "/Nexus/corpus_dropbox.json"
                    },
                    "description": "Crear corpus unificado de Dropbox"
                },
                {
                    "step": 5,
                    "action": "create_onedrive_corpus",
                    "tool": "onedrive_create_corpus",
                    "args": {
                        "source_paths": ["<todos los archivos reconstructed de OneDrive>"],
                        "output_path": "/Nexus/corpus_onedrive.json"
                    },
                    "description": "Crear corpus unificado de OneDrive"
                }
            ])

        if self.mode in ["sync", "full"]:
            instructions["steps"].extend([
                {
                    "step": 6,
                    "action": "download_corpus_files",
                    "description": "Descargar corpus_dropbox.json y corpus_onedrive.json a local",
                    "tools": ["dropbox_read_file", "onedrive_read_file"]
                },
                {
                    "step": 7,
                    "action": "unify_corpus_locally",
                    "command": "python scripts/nexus_corpus_unifier.py",
                    "description": "Ejecutar unificador para crear corpus maestro"
                },
                {
                    "step": 8,
                    "action": "convert_to_google_docs",
                    "command": "python scripts/nexus_to_gdocs.py",
                    "description": "Convertir corpus unificado a Google Docs"
                }
            ])

        return json.dumps(instructions, indent=2, ensure_ascii=False)

    def save_instructions(self) -> str:
        """Guarda instrucciones en archivo para que Claude las lea"""
        instructions = self.generate_claude_instructions()
        output_path = self.workspace / f"claude_instructions_{self.mode}.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(instructions)

        return str(output_path)

    def generate_human_readable_guide(self) -> str:
        """Genera guía legible para humanos"""
        guide = f"""
🔱 NEXUS WORKFLOW - GUÍA PASO A PASO
═══════════════════════════════════════════════════════════════

Modo: {self.mode.upper()}
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

═══════════════════════════════════════════════════════════════
INSTRUCCIONES PARA CLAUDE DESKTOP
═══════════════════════════════════════════════════════════════

Copia y pega lo siguiente en Claude Desktop:

---

Necesito que ejecutes el siguiente workflow de sincronización Nexus:

"""

        if self.mode in ["reconstruction", "full"]:
            guide += """
**FASE 1: RECONSTRUCCIÓN DE CONVERSACIONES**

1. Lista todos los archivos en Dropbox:
   ```
   Usa dropbox_list_files con path="/Nexus/exports" y recursive=true
   ```

2. Lista todos los archivos en OneDrive:
   ```
   Usa onedrive_list_files con path="/Nexus/exports" y recursive=true
   ```

3. Para CADA archivo encontrado, identifica el tipo de IA:
   - Si contiene "chatgpt" → ai_type="chatgpt"
   - Si contiene "claude" → ai_type="claude"
   - Si contiene "gemini" → ai_type="gemini"
   - Si contiene "notebooklm" → ai_type="notebooklm"
   - Si contiene "antigravity" → ai_type="antigravity"
   - Si contiene "codex" → ai_type="codex"

4. Reconstruye cada archivo:
   ```
   Para archivos de Dropbox:
   Usa dropbox_reconstruct_conversations con:
   - source_path: [ruta del archivo]
   - ai_type: [tipo identificado]
   - output_path: /Nexus/reconstructed/[nombre]_reconstructed.json

   Para archivos de OneDrive:
   Usa onedrive_reconstruct_conversations con los mismos parámetros
   ```

"""

        if self.mode in ["corpus", "full"]:
            guide += """
**FASE 2: CREACIÓN DE CORPUS POR PLATAFORMA**

5. Crea corpus de Dropbox:
   ```
   Usa dropbox_create_corpus con:
   - source_paths: [array de TODOS los archivos reconstructed de Dropbox]
   - output_path: /Nexus/corpus_dropbox.json
   ```

6. Crea corpus de OneDrive:
   ```
   Usa onedrive_create_corpus con:
   - source_paths: [array de TODOS los archivos reconstructed de OneDrive]
   - output_path: /Nexus/corpus_onedrive.json
   ```

"""

        if self.mode in ["sync", "full"]:
            guide += """
**FASE 3: UNIFICACIÓN Y SINCRONIZACIÓN A GOOGLE DOCS**

7. Descarga corpus de Dropbox:
   ```
   Usa dropbox_read_file con path="/Nexus/corpus_dropbox.json"
   Guarda el contenido en: ./nexus_workspace/corpus_dropbox.json
   ```

8. Descarga corpus de OneDrive:
   ```
   Usa onedrive_read_file con path="/Nexus/corpus_onedrive.json"
   Guarda el contenido en: ./nexus_workspace/corpus_onedrive.json
   ```

9. Descarga corpus de Google Drive (si existe):
   ```
   Lista archivos en Google Drive en carpeta "Nexus"
   Si existe corpus_gdrive.json, descárgalo a ./nexus_workspace/
   ```

10. Ejecuta unificador de corpus:
    ```
    Ejecuta este comando bash:
    python scripts/nexus_corpus_unifier.py
    ```

11. Ejecuta conversor a Google Docs:
    ```
    Ejecuta este comando bash:
    python scripts/nexus_to_gdocs.py
    ```

"""

        guide += """
**FASE FINAL: VERIFICACIÓN Y REPORTE**

12. Verifica que se hayan creado los documentos en Google Docs

13. Lee el archivo ./nexus_unified_corpus/google_docs_links.json

14. Genera un reporte con:
    - Total de conversaciones procesadas
    - Total de mensajes
    - Distribución por IA
    - Enlaces a todos los documentos creados
    - Link al documento maestro índice

═══════════════════════════════════════════════════════════════

DESPUÉS DE COMPLETAR:

Por favor genera un resumen ejecutivo que incluya:
- ✅ Pasos completados
- 📊 Estadísticas (conversaciones, mensajes, documentos)
- 🔗 Enlaces a Google Docs
- 📋 Link al documento maestro
- ⚠️  Cualquier error o advertencia

═══════════════════════════════════════════════════════════════
"""

        return guide

    def run(self):
        """Ejecuta el workflow"""
        print("🔱 NEXUS CLAUDE WORKFLOW")
        print("=" * 80)
        print(f"Modo: {self.mode.upper()}")
        print("=" * 80)

        # Guardar instrucciones JSON
        json_path = self.save_instructions()
        print(f"\n✅ Instrucciones JSON guardadas en: {json_path}")

        # Generar guía legible
        guide = self.generate_human_readable_guide()
        guide_path = self.workspace / f"workflow_guide_{self.mode}.txt"

        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)

        print(f"✅ Guía paso a paso guardada en: {guide_path}")

        # Mostrar guía
        print("\n" + "=" * 80)
        print("GUÍA GENERADA:")
        print("=" * 80)
        print(guide)

        print("\n" + "=" * 80)
        print("SIGUIENTE PASO:")
        print("=" * 80)
        print("\n1. Abre Claude Desktop")
        print(f"2. Copia el contenido de: {guide_path}")
        print("3. Pégalo en una conversación con Claude")
        print("4. Claude ejecutará automáticamente todos los pasos usando MCP")
        print("\n" + "=" * 80)


def main():
    """Función principal"""
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        print("🔱 NEXUS CLAUDE WORKFLOW")
        print("\nModos disponibles:")
        print("  reconstruction - Solo reconstruir conversaciones")
        print("  corpus - Solo crear corpus por plataforma")
        print("  sync - Solo unificar y convertir a Google Docs")
        print("  full - Workflow completo (recomendado)")
        print("\nUso: python nexus_claude_workflow.py [mode]")

        mode = input("\nSelecciona modo (full): ").strip() or "full"

    if mode not in ["reconstruction", "corpus", "sync", "full"]:
        print(f"❌ Modo inválido: {mode}")
        print("Usa: reconstruction, corpus, sync, o full")
        sys.exit(1)

    workflow = ClaudeWorkflow(mode)
    workflow.run()


if __name__ == "__main__":
    main()
