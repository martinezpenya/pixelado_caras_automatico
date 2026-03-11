#!/bin/bash
# ==============================================================================
# activar_entorno_webcam.sh
# Si el entorno virtual ~/pixelado_webcam no existe, lo crea e instala
# las dependencias. Luego activa el entorno y lanza pixelado_webcam.py.
#
# Uso:
#   source activar_entorno_webcam.sh          → activa el entorno en la shell actual
#   bash activar_entorno_webcam.sh            → lanza directamente pixelado_webcam.py
# ==============================================================================

VENV_DIR="$HOME/pixelado_webcam"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"
WEBCAM_SCRIPT="$SCRIPT_DIR/pixelado_webcam.py"

echo "========================================================================"
echo "  Pixelado de caras en tiempo real - Webcam"
echo "========================================================================"

# --- Verificar que existe requirements.txt ---
if [ ! -f "$REQUIREMENTS" ]; then
    echo "[ERROR] No se encontró requirements.txt en: $SCRIPT_DIR"
    exit 1
fi

# --- Crear e instalar entorno si no existe ---
if [ ! -d "$VENV_DIR" ]; then
    echo "[INFO]  El entorno virtual no existe. Creando en: $VENV_DIR"
    python3 -m venv "$VENV_DIR"
    echo "[OK]    Entorno virtual creado."

    echo "[INFO]  Instalando dependencias desde requirements.txt..."
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip --quiet
    pip install -r "$REQUIREMENTS"
    echo "[OK]    Dependencias instaladas."
else
    echo "[INFO]  Entorno virtual encontrado en: $VENV_DIR"
    source "$VENV_DIR/bin/activate"

    # Comprobar si las dependencias están instaladas (cv2 como indicador)
    if ! python -c "import cv2" &>/dev/null; then
        echo "[INFO]  Faltan dependencias. Instalando desde requirements.txt..."
        pip install --upgrade pip --quiet
        pip install -r "$REQUIREMENTS"
        echo "[OK]    Dependencias instaladas."
    fi
fi

echo "[OK]    Entorno activado: $VENV_DIR"
echo "========================================================================"

# --- Lanzar el script si se ejecuta directamente (no con source) ---
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "[INFO]  Lanzando pixelado_webcam.py..."
    python "$WEBCAM_SCRIPT" "$@"
fi
