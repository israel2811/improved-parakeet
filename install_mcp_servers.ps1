# 🔱 NEXUS MCP SERVERS - INSTALADOR AUTOMÁTICO (PowerShell)
# Script de instalación para servidores MCP de Dropbox y OneDrive
# Autor: Israel Realivazquez

$ErrorActionPreference = "Stop"

Write-Host "🔱 ========================================" -ForegroundColor Cyan
Write-Host "   NEXUS MCP SERVERS - INSTALADOR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Log-Info {
    param([string]$Message)
    Write-Host "[INFO] " -ForegroundColor Blue -NoNewline
    Write-Host $Message
}

function Log-Success {
    param([string]$Message)
    Write-Host "[✓] " -ForegroundColor Green -NoNewline
    Write-Host $Message
}

function Log-Warning {
    param([string]$Message)
    Write-Host "[!] " -ForegroundColor Yellow -NoNewline
    Write-Host $Message
}

function Log-Error {
    param([string]$Message)
    Write-Host "[✗] " -ForegroundColor Red -NoNewline
    Write-Host $Message
}

# Verificar Node.js
Log-Info "Verificando Node.js..."
try {
    $nodeVersion = node -v
    $versionNumber = [int]($nodeVersion -replace 'v(\d+)\..*', '$1')

    if ($versionNumber -lt 18) {
        Log-Error "Node.js debe ser versión 18 o superior. Versión actual: $nodeVersion"
        Log-Info "Descarga desde: https://nodejs.org/"
        exit 1
    }

    Log-Success "Node.js $nodeVersion detectado"
} catch {
    Log-Error "Node.js no está instalado."
    Log-Info "Por favor instala Node.js 18+ desde https://nodejs.org/"
    exit 1
}

# Verificar Python
Log-Info "Verificando Python..."
try {
    $pythonVersion = python --version
    Log-Success "$pythonVersion detectado"
} catch {
    Log-Warning "Python 3 no está instalado. Algunas funcionalidades no estarán disponibles."
}

# Instalar dependencias de Dropbox MCP
Log-Info "Instalando servidor MCP de Dropbox..."
Push-Location mcp-servers\dropbox

if (!(Test-Path "package.json")) {
    Log-Error "package.json no encontrado en mcp-servers\dropbox"
    Pop-Location
    exit 1
}

npm install
Log-Success "Dependencias de Dropbox instaladas"

# Crear .env si no existe
if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Log-Warning ".env creado desde .env.example - DEBES EDITAR .env con tu token de Dropbox"
} else {
    Log-Info ".env ya existe, no se sobrescribió"
}

Pop-Location

# Instalar dependencias de OneDrive MCP
Log-Info "Instalando servidor MCP de OneDrive..."
Push-Location mcp-servers\onedrive

if (!(Test-Path "package.json")) {
    Log-Error "package.json no encontrado en mcp-servers\onedrive"
    Pop-Location
    exit 1
}

npm install
Log-Success "Dependencias de OneDrive instaladas"

# Crear .env si no existe
if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Log-Warning ".env creado desde .env.example - DEBES EDITAR .env con tus credenciales de Azure"
} else {
    Log-Info ".env ya existe, no se sobrescribió"
}

Pop-Location

# Instalar dependencias de Python
try {
    Log-Info "Instalando dependencias de Python..."
    python -m pip install python-dotenv --quiet
    Log-Success "Dependencias de Python instaladas"
} catch {
    Log-Warning "No se pudieron instalar dependencias de Python (opcional)"
}

# Crear directorio de salida
New-Item -ItemType Directory -Force -Path "nexus_unified_corpus" | Out-Null
Log-Success "Directorio de corpus unificado creado"

# Resumen
Write-Host ""
Write-Host "🔱 ========================================" -ForegroundColor Cyan
Write-Host "   INSTALACIÓN COMPLETADA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Log-Success "Servidores MCP instalados correctamente"
Write-Host ""
Write-Host "📝 PRÓXIMOS PASOS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. " -NoNewline
Write-Host "Configurar credenciales:" -ForegroundColor Yellow
Write-Host "   - Edita: " -NoNewline
Write-Host "mcp-servers\dropbox\.env" -ForegroundColor Blue
Write-Host "   - Edita: " -NoNewline
Write-Host "mcp-servers\onedrive\.env" -ForegroundColor Blue
Write-Host ""
Write-Host "2. " -NoNewline
Write-Host "Configurar Claude Desktop:" -ForegroundColor Yellow
Write-Host "   - Lee la guía completa en: " -NoNewline
Write-Host "MCP_SETUP_GUIDE.md" -ForegroundColor Blue
Write-Host "   - Edita tu archivo de configuración:"
Write-Host "     " -NoNewline
Write-Host "$env:APPDATA\Claude\claude_desktop_config.json" -ForegroundColor Blue
Write-Host "   - Usa " -NoNewline
Write-Host "claude_desktop_config_full.json" -ForegroundColor Blue -NoNewline
Write-Host " como referencia"
Write-Host ""
Write-Host "3. " -NoNewline
Write-Host "Reiniciar Claude Desktop" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. " -NoNewline
Write-Host "Verificar conexión:" -ForegroundColor Yellow
Write-Host "   En Claude Desktop: '¿Qué servidores MCP están disponibles?'"
Write-Host ""
Write-Host "📚 Para más información: " -NoNewline
Write-Host "MCP_SETUP_GUIDE.md" -ForegroundColor Blue
Write-Host ""
Log-Success "¡Listo para usar!"
Write-Host ""
