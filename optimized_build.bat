@echo off
cls
echo ===================================================
echo PokeMMO自动化 - 优化版构建脚本
===================================================
echo.
echo 此脚本将帮助您准备构建环境并提供构建选项
 echo.

REM 设置环境变量以防止超时
set P4A_TIMEOUT=1800
set ANDROID_SDK_HOME=%LOCALAPPDATA%\Android\Sdk

REM 检查Python环境
echo 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python环境
    echo 请确保Python 3.7+已正确安装
    pause
    exit /b 1
)

REM 检查pip
echo.
echo 检查pip...
pip --version
if errorlevel 1 (
    echo 警告: pip可能未正确配置
)

REM 安装必要的依赖
echo.
echo 安装/更新必要的依赖...
pip install --upgrade pip
pip install buildozer

REM 创建必要的目录
if not exist "%~dp0in" mkdir "%~dp0in"
if not exist "E:\#9#531\APP" mkdir "E:\#9#531\APP"

echo.
echo ===================================================
echo 构建选项
echo ===================================================
echo 注意: 在Windows上直接使用buildozer构建Android可能会失败
 echo buildozer官方推荐在Linux环境中运行
 echo.
 echo 推荐选项:
 echo 1. 使用Google Colab (最简单的免费方案)
 echo 2. 使用GitHub Actions (自动化构建)
 echo.
echo 3. 尝试本地构建 (不推荐，可能失败)
 echo 4. 退出
 echo ===================================================

echo.
set /p choice="请选择构建方式 (1-4): "

if "%choice%" == "1" (
    echo.
    echo 打开Google Colab...
    start https://colab.research.google.com/
    echo 请上传项目文件并使用optimized_colab_script.ipynb中的命令
    echo 别忘了在浏览器控制台运行防超时脚本
)

if "%choice%" == "2" (
    echo.
    echo 打开GitHub...
    start https://github.com/
    echo 请创建仓库并上传项目文件，包括.github/workflows目录
    echo workflow文件会自动触发构建
)

if "%choice%" == "3" (
    echo.
    echo 警告: 本地Windows构建可能会失败
    echo 按任意键继续尝试...
    pause
    
    echo.
    echo 尝试本地构建...
    buildozer android debug
    
    if exist "%~dp0in\*.apk" (
        echo.
        echo 构建成功！
        dir "%~dp0in\*.apk"
        echo.
        echo 正在复制APK到输出目录...
        copy "%~dp0in\*.apk" "E:\#9#531\APP" /Y
        echo 复制完成！
    ) else (
        echo.
        echo 构建失败或未找到APK文件
        echo 推荐使用云服务构建方案
    )
)

echo.
echo 操作完成！
pause
