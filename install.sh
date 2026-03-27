#!/bin/bash

set -e

INSTALL_DIR="${HOME}/.rp1"
VENV_DIR="${INSTALL_DIR}/venv"
BIN_DIR="${HOME}/.local/bin"
CONFIG_FILE="${HOME}/.rp1/config.json"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
NC='\033[0m'

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  RP1 Installer - Linux/Mac${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

select_language() {
    echo "Select your language / Selecciona tu idioma:"
    echo "  1) English"
    echo "  2) Espanol"
    read -p "Choice / Opcion [1-2]: " choice
    case $choice in
        1) INSTALL_LANG="en";;
        2) INSTALL_LANG="es";;
        *) INSTALL_LANG="en";;
    esac
}

if [ -f "$CONFIG_FILE" ]; then
    INSTALL_LANG=$(grep -o '"language": "[^"]*"' "$CONFIG_FILE" 2>/dev/null | cut -d'"' -f4)
    if [ -z "$INSTALL_LANG" ]; then
        select_language
    fi
else
    select_language
fi

if [ "$INSTALL_LANG" = "es" ]; then
    MSG_PYTHON="Verificando Python..."
    MSG_PYTHON_OK="Python encontrado"
    MSG_PYTHON_ERR="Python 3.8+ es requerido"
    MSG_VENV="Creando entorno virtual..."
    MSG_VENV_OK="Entorno virtual creado"
    MSG_DEP="Instalando dependencias..."
    MSG_DEP_OK="Dependencias instaladas"
    MSG_OLLAMA="Instalando Ollama..."
    MSG_OLLAMA_OK="Ollama instalado"
    MSG_DOWNLOAD="Descargando modelo gemma3:4b..."
    MSG_DOWNLOAD_OK="Modelo descargado"
    MSG_COPY="Copiando archivos..."
    MSG_COPY_OK="Archivos copiados"
    MSG_PATH="Agregando al PATH..."
    MSG_PATH_OK="PATH actualizado"
    MSG_COMPLETE="Instalacion completa!"
    MSG_RUN="Para ejecutar RP1, escribe: rp1"
else
    MSG_PYTHON="Checking Python..."
    MSG_PYTHON_OK="Python found"
    MSG_PYTHON_ERR="Python 3.8+ is required"
    MSG_VENV="Creating virtual environment..."
    MSG_VENV_OK="Virtual environment created"
    MSG_DEP="Installing dependencies..."
    MSG_DEP_OK="Dependencies installed"
    MSG_OLLAMA="Installing Ollama..."
    MSG_OLLAMA_OK="Ollama installed"
    MSG_DOWNLOAD="Downloading gemma3:4b model..."
    MSG_DOWNLOAD_OK="Model downloaded"
    MSG_COPY="Copying files..."
    MSG_COPY_OK="Files copied"
    MSG_PATH="Adding to PATH..."
    MSG_PATH_OK="PATH updated"
    MSG_COMPLETE="Installation complete!"
    MSG_RUN="To run RP1, type: rp1"
fi

echo -e "${YELLOW}${MSG_PYTHON}${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}${MSG_PYTHON_ERR}${NC}"
    echo "Install Python: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(sys.version_info[1])')
if [ "$PYTHON_VERSION" -lt 8 ]; then
    echo -e "${RED}${MSG_PYTHON_ERR}${NC}"
    exit 1
fi

echo -e "${GREEN}${MSG_PYTHON_OK}${NC}"
echo ""

echo -e "${YELLOW}${MSG_VENV}${NC}"
mkdir -p "$INSTALL_DIR"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
echo -e "${GREEN}${MSG_VENV_OK}${NC}"
echo ""

echo -e "${YELLOW}${MSG_DEP}${NC}"
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install pyttsx3
echo -e "${GREEN}${MSG_DEP_OK}${NC}"
echo ""

echo -e "${YELLOW}${MSG_OLLAMA}${NC}"
if ! command -v ollama &> /dev/null; then
    if [ "$(uname)" = "Darwin" ]; then
        brew install ollama
    else
        curl -fsSL https://ollama.com/install.sh | sh
    fi
fi
if ! pgrep -x "ollama" > /dev/null; then
    nohup ollama serve > /dev/null 2>&1 &
    sleep 2
fi
echo -e "${GREEN}${MSG_OLLAMA_OK}${NC}"
echo ""

echo -e "${YELLOW}${MSG_DOWNLOAD}${NC}"
ollama pull gemma3:4b
echo -e "${GREEN}${MSG_DOWNLOAD_OK}${NC}"
echo ""

echo -e "${YELLOW}${MSG_COPY}${NC}"
mkdir -p "$BIN_DIR"
cp "$(dirname "$0")/src/rp1.py" "$INSTALL_DIR/"
cat > "$BIN_DIR/rp1" << 'RP1SCRIPT'
#!/bin/bash
source "$HOME/.rp1/venv/bin/activate"
python3 "$HOME/.rp1/rp1.py" "$@"
RP1SCRIPT
chmod +x "$BIN_DIR/rp1"
echo -e "${GREEN}${MSG_COPY_OK}${NC}"
echo ""

if [ -f "${HOME}/.bashrc" ]; then
    if ! grep -q "\.local/bin" "${HOME}/.bashrc"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "${HOME}/.bashrc"
    fi
fi
if [ -f "${HOME}/.zshrc" ]; then
    if ! grep -q "\.local/bin" "${HOME}/.zshrc"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "${HOME}/.zshrc"
    fi
fi

echo "{\"color\": \"yellow\", \"language\": \"$INSTALL_LANG\"}" > "$CONFIG_FILE"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ${MSG_COMPLETE}${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${CYAN}${MSG_RUN}${NC}"
echo ""

if [ "$INSTALL_LANG" = "es" ]; then
    echo "Opciones: rp1 --voice para activar voz"
    echo "         rp1 --setup para descargar modelos"
else
    echo "Options: rp1 --voice to enable voice"
    echo "         rp1 --setup to download models"
fi

export PATH="$HOME/.local/bin:$PATH"
echo ""
echo "Source your shell config or restart terminal to use 'rp1' command"
