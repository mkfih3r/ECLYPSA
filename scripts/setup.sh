#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "=========================================="
echo "   ECLYPSA AI - Foundation Environment Setup"
echo "=========================================="

# Check Python Version
if command -v python3 &> /dev/null; then
    PYTHON_VER=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo "[✓] Python detected: v$PYTHON_VER"
else
    echo "[X] Error: Python 3 is required."
    exit 1
fi

# Check Go Version
if command -v go &> /dev/null; then
    GO_VER=$(go version | awk '{print $3}')
    echo "[✓] Go detected: $GO_VER"
else
    echo "[!] Warning: Go not detected. Core engine Go bindings will require Go v1.22+"
fi

# Create Virtual Environment if not exists
if [ ! -d ".venv" ]; then
    echo "[+] Creating Python virtual environment (.venv)..."
    python3 -m venv .venv
fi

# Activate Virtual Environment
source .venv/bin/activate

echo "[+] Upgrading pip..."
pip install --upgrade pip

echo "[+] Installing core development tools..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "=========================================="
echo " [✓] Environment setup successfully completed!"
echo " Activate virtualenv using: source .venv/bin/activate"
echo "=========================================="