#!/bin/bash
# Google Ai Kit™ - macOS Entrypoint
# Anony · t.me/CracKz_Hubb

echo "============================================================"
echo "  Google Ai Kit™ - Anony Engine VIP"
echo "  Channel: https://t.me/CracKz_Hubb"
echo "============================================================"

if [ ! -f "tui.py" ]; then
    echo "[!] Error: tui.py not found."
    exit 1
fi

PYTHON_CMD="python3"
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "[!] python3 not found. Please install Python 3.10+."
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "[*] Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

python3 tui.py "$@"