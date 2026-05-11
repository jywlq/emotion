@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo.
echo  Starting Cosmic Brew...
echo.

pip install rich openai -q 2>nul

python cosmic_brew.py

if %errorlevel% neq 0 (
    echo.
    echo  [Error] Failed to start. Please check if Python is installed.
    echo.
)

pause
