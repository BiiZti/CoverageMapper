@echo off
chcp 65001 >nul
title 信号覆盖地图分析器启动器

echo.
echo ========================================
echo    🗺️ 信号覆盖地图分析器 v2.0
echo ========================================
echo.
echo 正在启动GUI程序...
echo.

cd /d "%~dp0"

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未检测到Python，请先安装Python
    echo.
    echo 请访问 https://python.org 下载并安装Python
    pause
    exit /b 1
)

REM 检查依赖包
echo 📦 检查依赖包...
pip show pandas >nul 2>&1
if errorlevel 1 (
    echo 📦 安装依赖包：pandas
    pip install pandas
)

pip show openpyxl >nul 2>&1
if errorlevel 1 (
    echo 📦 安装依赖包：openpyxl
    pip install openpyxl
)

echo.
echo ✅ 环境检查完成，启动程序...
echo.

REM 启动GUI程序
python signal_mapper_gui.py

if errorlevel 1 (
    echo.
    echo ❌ 程序启动失败
    pause
) 