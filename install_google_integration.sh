#!/bin/bash

# 🔱 NEXUS - INSTALADOR DE INTEGRACIÓN GOOGLE
# Configura Google Cloud APIs y credenciales para Nexus

set -e

echo "🔱 ========================================"
echo "   NEXUS GOOGLE INTEGRATION SETUP"
echo "========================================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Verificar Python
log_info "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 no está instalado. Instala Python 3.8+ primero."
    exit 1
fi

log_success "Python $(python3 --version) detectado"

# Instalar dependencias
log_info "Instalando dependencias de Google..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    log_success "Dependencias instaladas"
else
    log_error "Error instalando dependencias"
    exit 1
fi

# Verificar credentials.json
echo ""
log_info "Verificando credenciales de Google Cloud..."

if [ ! -f "credentials.json" ]; then
    log_warning "credentials.json NO encontrado"
    echo ""
    echo "${YELLOW}Para obtener credenciales de Google Cloud:${NC}"
    echo ""
    echo "1. Ve a: ${BLUE}https://console.cloud.google.com/${NC}"
    echo ""
    echo "2. ${YELLOW}Crea un proyecto nuevo${NC} o selecciona uno existente"
    echo ""
    echo "3. ${YELLOW}Habilita las siguientes APIs:${NC}"
    echo "   - Google Docs API"
    echo "   - Google Drive API"
    echo ""
    echo "4. Ve a ${YELLOW}'APIs y servicios'${NC} → ${YELLOW}'Credenciales'${NC}"
    echo ""
    echo "5. Clic en ${YELLOW}'+ CREAR CREDENCIALES'${NC} → ${YELLOW}'ID de cliente de OAuth'${NC}"
    echo ""
    echo "6. Tipo de aplicación: ${YELLOW}'Aplicación de escritorio'${NC}"
    echo ""
    echo "7. Nombre: ${BLUE}'Nexus Desktop Client'${NC}"
    echo ""
    echo "8. ${YELLOW}Descarga el JSON${NC} de credenciales"
    echo ""
    echo "9. Guárdalo como ${BLUE}'credentials.json'${NC} en este directorio"
    echo ""
    echo "10. Vuelve a ejecutar este script"
    echo ""
    exit 1
else
    log_success "credentials.json encontrado"
fi

# Verificar estructura de credentials.json
log_info "Validando estructura de credentials.json..."

if python3 -c "import json; json.load(open('credentials.json'))" 2>/dev/null; then
    log_success "credentials.json es válido"
else
    log_error "credentials.json no es un JSON válido"
    exit 1
fi

# Test de autenticación
echo ""
log_info "Probando autenticación con Google..."
log_warning "Se abrirá un navegador para autorizar la aplicación"
log_info "Autoriza el acceso cuando se te solicite"
echo ""

cat > test_google_auth.py << 'EOF'
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file'
]

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

print("✅ Autenticación exitosa")
EOF

if python3 test_google_auth.py; then
    log_success "Autenticación con Google completada"
    rm test_google_auth.py
else
    log_error "Error en autenticación"
    rm test_google_auth.py
    exit 1
fi

# Crear carpeta de workspace
mkdir -p nexus_workspace
mkdir -p nexus_unified_corpus
mkdir -p nexus_sync_logs

log_success "Directorios de trabajo creados"

# Resumen
echo ""
echo "🔱 ========================================"
echo "   INSTALACIÓN COMPLETADA"
echo "========================================"
echo ""
log_success "Integración con Google configurada correctamente"
echo ""
echo "📝 PRÓXIMOS PASOS:"
echo ""
echo "1. ${YELLOW}Verifica que tienes archivos en:${NC}"
echo "   - ${BLUE}Dropbox/Nexus/exports/${NC}"
echo "   - ${BLUE}OneDrive/Nexus/exports/${NC}"
echo ""
echo "2. ${YELLOW}Ejecuta el workflow completo:${NC}"
echo "   ${BLUE}python scripts/nexus_claude_workflow.py full${NC}"
echo ""
echo "3. ${YELLOW}O usa Claude Desktop directamente${NC}"
echo "   (Copia las instrucciones generadas por el workflow)"
echo ""
echo "4. ${YELLOW}Para convertir a Google Docs:${NC}"
echo "   ${BLUE}python scripts/nexus_to_gdocs.py${NC}"
echo ""
echo "📚 Documentación completa: ${BLUE}WORKFLOW_COMPLETO.md${NC}"
echo ""
log_success "¡Todo listo para sincronizar!"
echo ""
