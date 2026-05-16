#!/bin/bash

# 🔱 NEXUS MCP SERVERS - INSTALADOR AUTOMÁTICO
# Script de instalación para servidores MCP de Dropbox y OneDrive
# Autor: Israel Realivazquez

set -e

echo "🔱 ========================================"
echo "   NEXUS MCP SERVERS - INSTALADOR"
echo "========================================"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función de log
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

# Verificar Node.js
log_info "Verificando Node.js..."
if ! command -v node &> /dev/null; then
    log_error "Node.js no está instalado. Por favor instala Node.js 18+ desde https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    log_error "Node.js debe ser versión 18 o superior. Versión actual: $(node -v)"
    exit 1
fi

log_success "Node.js $(node -v) detectado"

# Verificar Python
log_info "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    log_warning "Python 3 no está instalado. Algunas funcionalidades no estarán disponibles."
else
    log_success "Python $(python3 --version) detectado"
fi

# Instalar dependencias de Dropbox MCP
log_info "Instalando servidor MCP de Dropbox..."
cd mcp-servers/dropbox
if [ ! -f "package.json" ]; then
    log_error "package.json no encontrado en mcp-servers/dropbox"
    exit 1
fi

npm install
log_success "Dependencias de Dropbox instaladas"

# Crear .env si no existe
if [ ! -f ".env" ]; then
    cp .env.example .env
    log_warning ".env creado desde .env.example - DEBES EDITAR .env con tu token de Dropbox"
else
    log_info ".env ya existe, no se sobrescribió"
fi

cd ../..

# Instalar dependencias de OneDrive MCP
log_info "Instalando servidor MCP de OneDrive..."
cd mcp-servers/onedrive
if [ ! -f "package.json" ]; then
    log_error "package.json no encontrado en mcp-servers/onedrive"
    exit 1
fi

npm install
log_success "Dependencias de OneDrive instaladas"

# Crear .env si no existe
if [ ! -f ".env" ]; then
    cp .env.example .env
    log_warning ".env creado desde .env.example - DEBES EDITAR .env con tus credenciales de Azure"
else
    log_info ".env ya existe, no se sobrescribió"
fi

cd ../..

# Instalar dependencias de Python
if command -v python3 &> /dev/null; then
    log_info "Instalando dependencias de Python..."
    python3 -m pip install python-dotenv --quiet
    log_success "Dependencias de Python instaladas"
fi

# Crear directorio de salida
mkdir -p nexus_unified_corpus
log_success "Directorio de corpus unificado creado"

# Resumen
echo ""
echo "🔱 ========================================"
echo "   INSTALACIÓN COMPLETADA"
echo "========================================"
echo ""
log_success "Servidores MCP instalados correctamente"
echo ""
echo "📝 PRÓXIMOS PASOS:"
echo ""
echo "1. ${YELLOW}Configurar credenciales${NC}:"
echo "   - Edita: ${BLUE}mcp-servers/dropbox/.env${NC}"
echo "   - Edita: ${BLUE}mcp-servers/onedrive/.env${NC}"
echo ""
echo "2. ${YELLOW}Configurar Claude Desktop${NC}:"
echo "   - Lee la guía completa en: ${BLUE}MCP_SETUP_GUIDE.md${NC}"
echo "   - Edita tu claude_desktop_config.json"
echo "   - Usa ${BLUE}claude_desktop_config_full.json${NC} como referencia"
echo ""
echo "3. ${YELLOW}Reiniciar Claude Desktop${NC}"
echo ""
echo "4. ${YELLOW}Verificar conexión${NC}:"
echo "   En Claude Desktop: '¿Qué servidores MCP están disponibles?'"
echo ""
echo "📚 Para más información: ${BLUE}MCP_SETUP_GUIDE.md${NC}"
echo ""
log_success "¡Listo para usar!"
echo ""
