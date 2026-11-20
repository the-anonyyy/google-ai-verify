@echo off
chcp 65001 >nul
title Pro +6 months Step 3 - Google Ai Kit™
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================
echo   Google Ai Kit™ - Pro 5TB add 6 months (Step 3)
echo   Run ONLY after Step 2 succeeded.
echo ============================================
python ultra0.py --account "current@device" --no-add --force --stack --plan pro6b
echo.
pause