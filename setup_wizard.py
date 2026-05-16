#!/usr/bin/env python3
"""
🔱 NEXUS SETUP WIZARD - ASISTENTE INTERACTIVO
Te guía paso a paso con los MÍNIMOS clics necesarios
"""

import os
import json
import webbrowser
import time
from pathlib import Path

class NexusSetupWizard:
    """Asistente que hace TODO excepto los clics mínimos necesarios"""

    def __init__(self):
        self.base_dir = Path("/home/user/improved-parakeet")
        self.config = {}

    def print_header(self, text):
        """Imprime encabezado"""
        print("\n" + "="*80)
        print(f"  {text}")
        print("="*80 + "\n")

    def wait_for_enter(self, message="Presiona ENTER cuando hayas terminado"):
        """Espera a que el usuario presione ENTER"""
        input(f"\n⏸️  {message} → ")

    def save_credential(self, service, key, value):
        """Guarda credencial automáticamente"""
        if service not in self.config:
            self.config[service] = {}
        self.config[service][key] = value
        print(f"  ✅ Guardado: {key}")

    def step1_dropbox(self):
        """Paso 1: Dropbox - Solo 3 clics"""
        self.print_header("PASO 1/3: DROPBOX (3 clics)")

        print("🎯 VOY A ABRIR DROPBOX EN TU NAVEGADOR")
        print("   Solo necesitas hacer 3 clics:")
        print()
        print("   1️⃣  Clic en 'Create app'")
        print("   2️⃣  Seleccionar 'Scoped access'")
        print("   3️⃣  Nombre: 'Nexus' → Clic 'Create app'")
        print()
        print("   Luego yo haré el resto...")

        self.wait_for_enter("Presiona ENTER para abrir Dropbox")

        # Abrir URL
        url = "https://www.dropbox.com/developers/apps"
        webbrowser.open(url)
        print(f"\n✅ Abrí: {url}")
        print("\n📍 AHORA HAZ LOS 3 CLICS:")
        print("   1. Create app")
        print("   2. Scoped access")
        print("   3. Nombre: 'Nexus' → Create app")

        self.wait_for_enter("Presiona ENTER después de crear la app")

        print("\n🎯 AHORA EN LA PÁGINA DE TU APP:")
        print("   1️⃣  Ve a la pestaña 'Permissions'")
        print("   2️⃣  Marca TODAS las casillas en 'files.*'")
        print("   3️⃣  Clic en 'Submit' abajo")

        self.wait_for_enter()

        print("\n🎯 ÚLTIMO PASO:")
        print("   1️⃣  Ve a la pestaña 'Settings'")
        print("   2️⃣  En 'Generated access token' → clic 'Generate'")
        print("   3️⃣  COPIA el token que aparece")
        print()

        token = input("📋 Pega aquí tu token de Dropbox: ").strip()

        if token:
            # Guardar automáticamente
            env_path = self.base_dir / "mcp-servers" / "dropbox" / ".env"
            with open(env_path, 'w') as f:
                f.write(f"DROPBOX_ACCESS_TOKEN={token}\n")
                f.write("NEXUS_WORKSPACE=/Nexus\n")

            print("\n✅ TOKEN GUARDADO AUTOMÁTICAMENTE")
            print(f"   Ubicación: {env_path}")
            self.save_credential("dropbox", "token", token)

    def step2_onedrive(self):
        """Paso 2: OneDrive - Solo 5 clics"""
        self.print_header("PASO 2/3: ONEDRIVE (5 clics)")

        print("🎯 VOY A ABRIR AZURE PORTAL EN TU NAVEGADOR")
        print("   Solo necesitas hacer 5 clics:")
        print()
        print("   1️⃣  Clic en '+ New registration'")
        print("   2️⃣  Nombre: 'Nexus OneDrive'")
        print("   3️⃣  Clic 'Register'")
        print("   4️⃣  Copiar 'Application (client) ID'")
        print("   5️⃣  Copiar 'Client Secret' (generarlo si no existe)")
        print()

        self.wait_for_enter("Presiona ENTER para abrir Azure Portal")

        # Abrir URL
        url = "https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade"
        webbrowser.open(url)
        print(f"\n✅ Abrí: {url}")

        print("\n📍 SI NO TIENES CUENTA AZURE:")
        print("   → Puedes SALTAR este paso (presiona ENTER)")
        print("   → OneDrive es OPCIONAL")
        print()
        print("📍 SI TIENES CUENTA:")
        print("   1. Clic en '+ New registration'")
        print("   2. Nombre: 'Nexus OneDrive'")
        print("   3. Accounts: 'Any Azure AD directory - Multitenant'")
        print("   4. Clic 'Register'")

        self.wait_for_enter("Presiona ENTER después de crear la app")

        print("\n🎯 AHORA COPIA TUS CREDENCIALES:")
        print()

        client_id = input("📋 Pega aquí tu 'Application (client) ID' (o ENTER para saltar): ").strip()

        if client_id:
            print("\n🔐 AHORA CREA UN SECRET:")
            print("   1. Ve a 'Certificates & secrets'")
            print("   2. Clic '+ New client secret'")
            print("   3. Description: 'Nexus'")
            print("   4. Clic 'Add'")
            print("   5. COPIA el 'Value' (no el Secret ID)")
            print()

            client_secret = input("📋 Pega aquí tu 'Client secret VALUE': ").strip()

            if client_secret:
                # Guardar automáticamente
                env_path = self.base_dir / "mcp-servers" / "onedrive" / ".env"
                with open(env_path, 'w') as f:
                    f.write(f"ONEDRIVE_CLIENT_ID={client_id}\n")
                    f.write(f"ONEDRIVE_CLIENT_SECRET={client_secret}\n")
                    f.write("ONEDRIVE_TENANT_ID=common\n")
                    f.write("NEXUS_WORKSPACE=/Nexus\n")

                print("\n✅ CREDENCIALES GUARDADAS AUTOMÁTICAMENTE")
                print(f"   Ubicación: {env_path}")
                self.save_credential("onedrive", "client_id", client_id)
                self.save_credential("onedrive", "client_secret", client_secret)
        else:
            print("\n⏭️  OneDrive saltado (opcional)")

    def step3_google(self):
        """Paso 3: Google Cloud - Solo 4 clics"""
        self.print_header("PASO 3/3: GOOGLE CLOUD (4 clics)")

        print("🎯 VOY A ABRIR GOOGLE CLOUD CONSOLE")
        print("   Solo necesitas hacer 4 clics:")
        print()
        print("   1️⃣  Crear proyecto 'Nexus'")
        print("   2️⃣  Habilitar Google Docs API")
        print("   3️⃣  Habilitar Google Drive API")
        print("   4️⃣  Descargar credentials.json")
        print()

        self.wait_for_enter("Presiona ENTER para abrir Google Cloud Console")

        # Abrir URLs automáticamente
        urls = [
            ("Crear Proyecto", "https://console.cloud.google.com/projectcreate"),
            ("Habilitar Docs API", "https://console.cloud.google.com/apis/library/docs.googleapis.com"),
            ("Habilitar Drive API", "https://console.cloud.google.com/apis/library/drive.googleapis.com"),
            ("Crear Credenciales", "https://console.cloud.google.com/apis/credentials")
        ]

        print("\n🚀 Abriendo URLs automáticamente...")
        for name, url in urls:
            print(f"   ✅ {name}: {url}")
            webbrowser.open(url)
            time.sleep(1)

        print("\n📍 PASOS EN ORDEN:")
        print()
        print("1️⃣  CREAR PROYECTO (primera pestaña):")
        print("   → Nombre: 'Nexus'")
        print("   → Clic 'Create'")
        print("   → Espera ~30 segundos")

        self.wait_for_enter()

        print("\n2️⃣  HABILITAR GOOGLE DOCS API (segunda pestaña):")
        print("   → Selecciona tu proyecto 'Nexus'")
        print("   → Clic 'Enable'")

        self.wait_for_enter()

        print("\n3️⃣  HABILITAR GOOGLE DRIVE API (tercera pestaña):")
        print("   → Selecciona tu proyecto 'Nexus'")
        print("   → Clic 'Enable'")

        self.wait_for_enter()

        print("\n4️⃣  CREAR CREDENCIALES (cuarta pestaña):")
        print("   → Clic '+ CREATE CREDENTIALS'")
        print("   → Selecciona 'OAuth client ID'")
        print("   → Application type: 'Desktop app'")
        print("   → Name: 'Nexus Desktop'")
        print("   → Clic 'Create'")
        print("   → Clic 'DOWNLOAD JSON'")
        print("   → Guarda como 'credentials.json'")
        print()
        print("📂 IMPORTANTE: Guarda el archivo en tu carpeta de Descargas")

        self.wait_for_enter("Presiona ENTER cuando hayas descargado credentials.json")

        # Buscar archivo
        possible_paths = [
            Path.home() / "Downloads" / "credentials.json",
            Path.home() / "Descargas" / "credentials.json",
            self.base_dir / "credentials.json"
        ]

        found = False
        for path in possible_paths:
            if path.exists():
                # Copiar automáticamente
                dest = self.base_dir / "credentials.json"
                if path != dest:
                    import shutil
                    shutil.copy(path, dest)
                    print(f"\n✅ COPIÉ AUTOMÁTICAMENTE credentials.json")
                    print(f"   Desde: {path}")
                    print(f"   Hacia: {dest}")
                else:
                    print(f"\n✅ credentials.json ya está en el lugar correcto")
                found = True
                break

        if not found:
            print("\n⚠️  No encontré credentials.json automáticamente")
            manual_path = input("📂 Ingresa la ruta completa del archivo: ").strip()
            if manual_path and Path(manual_path).exists():
                import shutil
                dest = self.base_dir / "credentials.json"
                shutil.copy(manual_path, dest)
                print(f"\n✅ COPIÉ credentials.json a {dest}")

    def step4_claude_desktop_config(self):
        """Paso 4: Configurar Claude Desktop - 1 solo paso"""
        self.print_header("CONFIGURACIÓN DE CLAUDE DESKTOP")

        print("🎯 VOY A GENERAR TU CONFIGURACIÓN COMPLETA")
        print("   Solo necesitas hacer 1 paso:")
        print()
        print("   1️⃣  Copiar y pegar en tu archivo de config")
        print()

        # Generar config con rutas absolutas
        config = {
            "mcpServers": {
                "google_drive": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-gdrive"]
                }
            }
        }

        # Añadir Dropbox si existe
        dropbox_env = self.base_dir / "mcp-servers" / "dropbox" / ".env"
        if dropbox_env.exists():
            with open(dropbox_env) as f:
                token = [l.split('=')[1].strip() for l in f if 'TOKEN' in l][0]

            config["mcpServers"]["nexus_dropbox"] = {
                "command": "node",
                "args": [str(self.base_dir / "mcp-servers" / "dropbox" / "index.js")],
                "env": {
                    "DROPBOX_ACCESS_TOKEN": token,
                    "NEXUS_WORKSPACE": "/Nexus"
                }
            }
            print("   ✅ Dropbox configurado")

        # Añadir OneDrive si existe
        onedrive_env = self.base_dir / "mcp-servers" / "onedrive" / ".env"
        if onedrive_env.exists():
            with open(onedrive_env) as f:
                lines = f.readlines()
                client_id = [l.split('=')[1].strip() for l in lines if 'CLIENT_ID' in l][0]
                client_secret = [l.split('=')[1].strip() for l in lines if 'CLIENT_SECRET' in l][0]

            config["mcpServers"]["nexus_onedrive"] = {
                "command": "node",
                "args": [str(self.base_dir / "mcp-servers" / "onedrive" / "index.js")],
                "env": {
                    "ONEDRIVE_CLIENT_ID": client_id,
                    "ONEDRIVE_CLIENT_SECRET": client_secret,
                    "ONEDRIVE_TENANT_ID": "common",
                    "NEXUS_WORKSPACE": "/Nexus"
                }
            }
            print("   ✅ OneDrive configurado")

        # Guardar config
        config_path = self.base_dir / "claude_desktop_config_READY.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"\n✅ CONFIGURACIÓN GENERADA: {config_path}")
        print("\n📋 TU CONFIG COMPLETA:")
        print(json.dumps(config, indent=2))

        print("\n" + "="*80)
        print("🎯 AHORA COPIA ESTA CONFIG A CLAUDE DESKTOP:")
        print("="*80)
        print()

        # Detectar sistema operativo
        import platform
        system = platform.system()

        if system == "Windows":
            config_location = "%APPDATA%\\Claude\\claude_desktop_config.json"
        elif system == "Darwin":
            config_location = "~/Library/Application Support/Claude/claude_desktop_config.json"
        else:
            config_location = "~/.config/Claude/claude_desktop_config.json"

        print(f"📂 Ubicación: {config_location}")
        print()
        print("📝 CÓMO HACERLO:")
        print("   1. Abre el archivo de arriba")
        print("   2. Copia TODO el contenido de claude_desktop_config_READY.json")
        print("   3. Pégalo en tu archivo")
        print("   4. Guarda")
        print("   5. Reinicia Claude Desktop")
        print()

        print(f"💡 TIP: El contenido está en:")
        print(f"   {config_path}")
        print(f"   (Ya lo imprimí arriba también)")

    def step5_create_folders(self):
        """Paso 5: Crear carpetas en cloud - AUTOMÁTICO"""
        self.print_header("CREANDO ESTRUCTURA DE CARPETAS")

        print("🤖 VOY A CREAR LAS CARPETAS AUTOMÁTICAMENTE")
        print()
        print("   Esto lo haré yo usando los servidores MCP:")
        print("   → /Nexus/exports/")
        print("   → /Nexus/reconstructed/")
        print()
        print("⏳ Esperando que configures Claude Desktop primero...")

        self.wait_for_enter("Presiona ENTER cuando Claude Desktop esté configurado")

        print("\n📝 INSTRUCCIONES PARA CLAUDE DESKTOP:")
        print()
        instructions = """
Copia esto en Claude Desktop:

Hola Claude, necesito que crees las carpetas de Nexus:

1. Usa dropbox_write_file para crear /Nexus/exports/.keep (contenido: "folder")
2. Usa dropbox_write_file para crear /Nexus/reconstructed/.keep (contenido: "folder")
3. Si tienes OneDrive, haz lo mismo:
   - onedrive_write_file para /Nexus/exports/.keep
   - onedrive_write_file para /Nexus/reconstructed/.keep

¡Gracias!
"""
        print(instructions)
        print("\n💾 Guardaré estas instrucciones en un archivo...")

        inst_path = self.base_dir / "nexus_workspace" / "create_folders_instructions.txt"
        with open(inst_path, 'w') as f:
            f.write(instructions)

        print(f"✅ Guardado en: {inst_path}")

    def step6_ready_to_use(self):
        """Paso 6: Sistema listo"""
        self.print_header("🎉 ¡SISTEMA LISTO!")

        print("✅ CONFIGURACIÓN COMPLETADA")
        print()
        print("Ahora puedes:")
        print()
        print("1️⃣  Exportar tus conversaciones reales:")
        print("   → ChatGPT: Settings → Export")
        print("   → Claude: Exportar historial")
        print("   → Gemini: Exportar conversaciones")
        print()
        print("2️⃣  Subir a /Nexus/exports/ (usa Claude Desktop)")
        print()
        print("3️⃣  Ejecutar workflow completo:")
        print("   → python scripts/nexus_claude_workflow.py full")
        print("   → Copiar instrucciones a Claude Desktop")
        print()
        print("4️⃣  Ver resultados en:")
        print("   → nexus_unified_corpus/corpus_viewer.html")
        print("   → Google Docs (creados automáticamente)")
        print()
        print("="*80)
        print("🔱 NEXUS OMEGA CONFIGURADO Y LISTO PARA USAR")
        print("="*80)

    def run(self):
        """Ejecutar wizard completo"""
        print("🔱" + "="*78 + "🔱")
        print("   NEXUS SETUP WIZARD - ASISTENTE INTERACTIVO")
        print("   Yo hago TODO, tú solo haces clics MÍNIMOS")
        print("🔱" + "="*78 + "🔱")

        print("\n📋 VAS A NECESITAR HACER:")
        print("   → Dropbox: 3 clics + copiar 1 token")
        print("   → OneDrive: 5 clics + copiar 2 valores (OPCIONAL)")
        print("   → Google: 4 clics + descargar 1 archivo")
        print("   → Claude Desktop: Copiar 1 config")
        print()
        print("   TOTAL: ~15 clics y 10 minutos")
        print()

        if input("¿Listo para empezar? (s/n): ").lower() != 's':
            print("Ok, cuando estés listo ejecuta de nuevo este script.")
            return

        try:
            # Paso 1: Dropbox
            self.step1_dropbox()

            # Paso 2: OneDrive (opcional)
            print("\n" + "="*80)
            if input("\n¿Quieres configurar OneDrive también? (s/n, recomendado 's'): ").lower() == 's':
                self.step2_onedrive()
            else:
                print("⏭️  OneDrive saltado")

            # Paso 3: Google
            self.step3_google()

            # Paso 4: Claude Desktop Config
            self.step4_claude_desktop_config()

            # Paso 5: Crear carpetas
            self.step5_create_folders()

            # Paso 6: Listo
            self.step6_ready_to_use()

        except KeyboardInterrupt:
            print("\n\n⚠️  Setup cancelado. Puedes continuar después ejecutando de nuevo.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    wizard = NexusSetupWizard()
    wizard.run()
