@echo off
chcp 65001 >nul
title 创建桌面快捷方式

echo.
echo ========================================
echo    创建信号覆盖地图分析器桌面快捷方式
echo ========================================
echo.

set "current_dir=%~dp0"
set "desktop=%USERPROFILE%\Desktop"

REM 创建快捷方式的VBS脚本
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\CreateShortcut.vbs"
echo sLinkFile = "%desktop%\信号覆盖地图分析器.lnk" >> "%temp%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\CreateShortcut.vbs"
echo oLink.TargetPath = "%current_dir%start_gui.bat" >> "%temp%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%current_dir%" >> "%temp%\CreateShortcut.vbs"
echo oLink.Description = "信号覆盖地图分析器 - 一键启动版本" >> "%temp%\CreateShortcut.vbs"
echo oLink.IconLocation = "shell32.dll,13" >> "%temp%\CreateShortcut.vbs"
echo oLink.Save >> "%temp%\CreateShortcut.vbs"

REM 执行VBS脚本
cscript //nologo "%temp%\CreateShortcut.vbs"

REM 清理临时文件
del "%temp%\CreateShortcut.vbs"

echo ✅ 桌面快捷方式创建成功！
echo.
echo 📍 快捷方式位置：%desktop%\信号覆盖地图分析器.lnk
echo.
echo 现在您可以：
echo  1. 双击桌面上的"信号覆盖地图分析器"图标
echo  2. 或者双击"start_gui.bat"文件
echo  3. 启动程序后点击"一键启动完整服务"
echo.
pause 