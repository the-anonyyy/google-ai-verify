@echo off
chcp 65001 >nul
title Manual Environment Setup - Google Ai Kit By Anony™
cd /d "%~dp0\..\.."
set PYTHONIOENCODING=utf-8
echo ============================================
echo   Google Ai Kit By Anony™ - Manual Setup (Fallback)
echo ============================================
python --version
if %errorlevel% neq 0 (
    echo [!] Python not found. Install Python 3.10+.
    pause
    exit /b
)
python -m pip install frida==16.5.9 textual==8.2.8
echo [OK] Done. Now run Setup_Environment.bat again.
pause