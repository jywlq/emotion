@echo off
chcp 65001 >nul 2>&1
title ☕ Cosmic Brew 星咖占卜
cd /d "%~dp0"

echo.
echo  正在启动 Cosmic Brew...
echo.

pip install rich -q 2>nul

python cosmic_brew.py

if %errorlevel% neq 0 (
    echo.
    echo  [错误] 运行失败，请检查 Python 是否已安装。
    echo.
)

pause
