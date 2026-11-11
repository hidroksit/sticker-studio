@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Studio - Gorsel Editor

python --version >nul 2>&1
if %errorlevel%==0 (
    python server.py
    goto :end
)

py --version >nul 2>&1
if %errorlevel%==0 (
    py server.py
    goto :end
)

echo.
echo Python bulunamadi.
echo Lutfen https://www.python.org/downloads/ adresinden Python kurun
echo ve kurulumda "Add Python to PATH" secenegini isaretleyin.
echo.
pause

:end
