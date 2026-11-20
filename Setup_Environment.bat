@echo off
chcp 65001 >nul
title Setup Environment - Google Ai Kit™
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8

echo ============================================================
echo   Google Ai Kit™ - One-click Environment Setup
echo   Channel: https://t.me/CracKz_Hubb
echo ============================================================
python setup_env.py

echo.
echo ------------------------------------------------------------
echo   Done. If all green, run 2_Pro_12m_Step1.bat to start.
echo ------------------------------------------------------------
pause