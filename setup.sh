### FILE: setup.sh
```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Google Ai Kit setup"

command -v python3 >/dev/null 2>&1 || { echo "python3 required"; exit 1; }
command -v pip3 >/dev/null 2>&1 || command -v pip >/dev/null 2>&1 || { echo "pip required"; exit 1; }

PIP=$(command -v pip3 || command -v pip)

echo "Installing pinned dependencies..."
$PIP install --user frida==16.5.9 textual==8.2.8 || $PIP install frida==16.5.9 textual==8.2.8

if [[ ! -f .env ]]; then
  cp -n .env.example .env || true
  echo "Copied .env.example to .env"
fi

echo "Setup complete."
echo "Channel : https://t.me/CracKz_Hubb"
echo "Run: sh run-macos.sh   or   .\run-all.ps1 on Windows"