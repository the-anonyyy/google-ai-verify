<#
.SYNOPSIS
    Google AI Kit - Windows Entrypoint
#>
$ErrorActionPreference = "Stop"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Google Ai Kit™ - Anony Engine VIP" -ForegroundColor Cyan
Write-Host "  Channel: https://t.me/CracKz_Hubb" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

if (!(Test-Path ".\tui.py")) {
    Write-Host "[!] Error: tui.py not found. Make sure all files are extracted." -ForegroundColor Red
    exit
}

$python = "python"
if (!(Get-Command $python -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Python not found. Please install Python 3.10+." -ForegroundColor Red
    exit
}

# Auto-install requirements
if (!(Test-Path ".\.deps_installed")) {
    Write-Host "[*] Installing dependencies..." -ForegroundColor Yellow
    & $python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] Dependency installation failed." -ForegroundColor Red
        exit
    }
    New-Item -ItemType File -Path ".\.deps_installed" | Out-Null
}

# Run the Textual Dashboard
& $python tui.py $args