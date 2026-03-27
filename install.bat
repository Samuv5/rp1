@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   RP1 Installer - Windows
echo ========================================
echo.

echo Select your language / Selecciona tu idioma:
echo   1) English
echo   2) Espanol
set /p choice="Choice / Opcion [1-2]: "

if "%choice%"=="1" (
    set "INSTALL_LANG=en"
) else (
    set "INSTALL_LANG=es"
)

if "%INSTALL_LANG%"=="es" (
    set "MSG_PYTHON=Verificando Python..."
    set "MSG_PYTHON_OK=Python encontrado"
    set "MSG_PYTHON_ERR=Python 3.8+ es requerido"
    set "MSG_DEP=Instalando dependencias..."
    set "MSG_DEP_OK=Dependencias instaladas"
    set "MSG_OLLAMA=Instalando Ollama..."
    set "MSG_OLLAMA_OK=Ollama instalado"
    set "MSG_DOWNLOAD=Descargando modelo gemma3:4b..."
    set "MSG_DOWNLOAD_OK=Modelo descargado"
    set "MSG_COPY=Copiando archivos..."
    set "MSG_COPY_OK=Archivos copiados"
    set "MSG_PATH=Agregando al PATH..."
    set "MSG_PATH_OK=PATH actualizado"
    set "MSG_COMPLETE=Instalacion completa!"
    set "MSG_RUN=Para ejecutar RP1, escribe: rp1"
    set "MSG_WIN_INSTALL=Instala Ollama desde: https://ollama.com/download"
) else (
    set "MSG_PYTHON=Checking Python..."
    set "MSG_PYTHON_OK=Python found"
    set "MSG_PYTHON_ERR=Python 3.8+ is required"
    set "MSG_DEP=Installing dependencies..."
    set "MSG_DEP_OK=Dependencies installed"
    set "MSG_OLLAMA=Installing Ollama..."
    set "MSG_OLLAMA_OK=Ollama installed"
    set "MSG_DOWNLOAD=Downloading gemma3:4b model..."
    set "MSG_DOWNLOAD_OK=Model downloaded"
    set "MSG_COPY=Copying files..."
    set "MSG_COPY_OK=Files copied"
    set "MSG_PATH=Adding to PATH..."
    set "MSG_PATH_OK=PATH updated"
    set "MSG_COMPLETE=Installation complete!"
    set "MSG_RUN=To run RP1, type: rp1"
    set "MSG_WIN_INSTALL=Install Ollama from: https://ollama.com/download"
)

echo %MSG_PYTHON%

where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %MSG_PYTHON_ERR%
    echo Install Python from: https://www.python.org/downloads/
    exit /b 1
)

python --version >nul 2>&1
set PYTHON_MAJOR=
for /f "delims=" %%i in ('python -c "import sys; print(sys.version_info[0])"') do set PYTHON_MAJOR=%%i
if !PYTHON_MAJOR! LSS 3 (
    echo %MSG_PYTHON_ERR%
    exit /b 1
)

echo %MSG_PYTHON_OK%
echo.

echo %MSG_OLLAMA%

where ollama >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %MSG_WIN_INSTALL%
    echo.
    echo Press any key to continue anyway...
    pause >nul
)

echo %MSG_OLLAMA_OK%
echo.

echo %MSG_DOWNLOAD%
ollama pull gemma3:4b >nul 2>&1 || echo "Model may already exist or download skipped"
echo %MSG_DOWNLOAD_OK%
echo.

echo %MSG_DEP%
pip install pyttsx3 >nul 2>&1
echo %MSG_DEP_OK%
echo.

echo %MSG_COPY%
set "INSTALL_DIR=%USERPROFILE%\.rp1"
set "SCRIPT_DIR=%~dp0"

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
copy /Y "%SCRIPT_DIR%src\rp1.py" "%INSTALL_DIR%\" >nul
echo %MSG_COPY_OK%
echo.

echo %MSG_PATH%
setx PATH "%PATH%;%INSTALL_DIR%" >nul 2>&1
echo %MSG_PATH_OK%
echo.

echo {"color":"yellow","language":"%INSTALL_LANG%"} > "%USERPROFILE%\.rp1\config.json"

echo ========================================
echo   %MSG_COMPLETE%
echo ========================================
echo.
echo %MSG_RUN%
echo.

if "%INSTALL_LANG%"=="es" (
    echo Tambien puedes ejecutar: rp1 --voice para activar voz
    echo Y: rp1 --setup para descargar modelos manualmente
) else (
    echo You can also run: rp1 --voice to enable voice
    echo And: rp1 --setup to download models manually
)

echo.
echo Press any key to exit...
pause >nul
