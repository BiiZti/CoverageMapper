@echo off
chcp 65001 >nul
title 信号覆盖地图分析器启动器

echo.
echo ========================================
echo 🗺️ 信号覆盖地图分析器 v2.1
echo ========================================
echo.
echo 正在启动GUI程序...

REM 切换到项目根目录
cd /d "%~dp0\.."

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未安装Python或Python未添加到PATH
    echo 请从 https://python.org 下载并安装Python 3.7+
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

pip show psutil >nul 2>&1
if errorlevel 1 (
    echo 📦 安装依赖包：psutil
    pip install psutil
)

echo.
echo ✅ 环境检查完成，启动程序...

REM 启动GUI程序（最小化终端窗口）
start /min "" python src/signal_mapper_gui.py

REM 等待2秒确保程序启动
timeout /t 2 /nobreak >nul

echo.
echo 🎉 程序正在启动中...
echo 💡 如果没有看到GUI窗口，请检查任务栏或稍等片刻
echo.
echo 按任意键关闭此窗口...
pause >nul 