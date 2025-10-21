
@echo off
cls
echo ===================================================
echo PokeMMO自动化 - APK安装脚本
echo ===================================================

echo 请确保您的Android设备已连接并启用USB调试模式
echo 按任意键开始安装...
pause

REM 检查ADB是否可用
adb version
if %errorlevel% neq 0 (
    echo 错误: 未找到ADB。请确保Android SDK已正确安装。
    echo 或者在以下提示中输入APK文件的完整路径。
)

set APK_PATH=
set /p APK_PATH=请输入APK文件路径（默认为app-release.apk）: 

if "%APK_PATH%"=="" (
    set APK_PATH=app-release.apk
)

echo 正在安装 %APK_PATH%
adb install -r "%APK_PATH%"

if %errorlevel% equ 0 (
    echo 安装成功！
    echo 正在启动应用...
    adb shell monkey -p com.example.pokemmoautomation 1
) else (
    echo 安装失败。请检查设备连接和APK文件。
)

pause
