@echo off
cls
echo ===================================================
echo PokeMMO自动化 - Buildozer Android APK构建脚本
echo ===================================================
echo.
echo 正在准备构建环境...
echo.

REM 设置构建目录和输出目录
set PROJECT_DIR=%CD%
set OUTPUT_DIR=%PROJECT_DIR%\bin
set APP_DIR=E:\#9#531\APP

REM 确保APP目录存在
if not exist "%APP_DIR%" (
    echo 创建APP输出目录: %APP_DIR%
    mkdir "%APP_DIR%"
)

REM 检查buildozer.spec文件
if not exist "%PROJECT_DIR%\buildozer.spec" (
    echo 错误: 找不到buildozer.spec文件
    echo 正在尝试初始化buildozer...
    echo.
    buildozer init
    if errorlevel 1 (
        echo 错误: Buildozer初始化失败
        echo 请检查Python环境和依赖安装
        pause
        exit /b 1
    )
    echo 注意: 已创建默认的buildozer.spec文件，请根据需要修改配置
    echo 特别是应用名称、包名和依赖项
    pause
)

REM 安装项目依赖
set KIVY_REQ_FILE=%PROJECT_DIR%\requirements_kivy.txt
if exist "%KIVY_REQ_FILE%" (
    echo 安装Kivy项目依赖...
    pip install -r "%KIVY_REQ_FILE%"
    if errorlevel 1 (
        echo 警告: 依赖安装可能不完整，请检查错误信息
    )
)

echo.
echo ===================================================
echo 开始使用Buildozer构建APK
echo ===================================================
echo 此过程将下载所需的Android SDK、NDK和其他依赖
echo 首次构建可能需要较长时间，请耐心等待
echo 请确保网络连接正常，所有下载请求将被允许

echo.
echo 按任意键开始构建...
pause

REM 开始构建过程
echo.
echo 正在启动Buildozer构建...
echo 这可能需要30分钟到几小时不等，取决于您的网络速度和系统性能

buildozer android debug

REM 检查构建结果
if exist "%OUTPUT_DIR%" (
    echo.
    echo 构建完成！检查输出目录中的APK文件
    dir "%OUTPUT_DIR%"\*.apk
    
    REM 复制APK文件到APP目录
    echo.
    echo 正在将APK文件复制到APP目录...
    for %%f in ("%OUTPUT_DIR%"\*.apk) do (
        if exist "%%f" (
            echo 复制: %%~nxf
            copy "%%f" "%APP_DIR%\" > nul
            if errorlevel 0 (
                echo 成功: %%~nxf 已复制到 %APP_DIR%
            ) else (
                echo 失败: 无法复制 %%~nxf
            )
        )
    )
    
    echo.
    echo 构建和复制完成！
    echo APK文件位置:
    echo - 原始位置: %OUTPUT_DIR%
    echo - 复制位置: %APP_DIR%
    
) else (
    echo.
    echo 构建失败或输出目录不存在
    echo 请检查上面的错误信息
)

echo.
echo ===================================================
echo 构建流程完成
if exist "%APP_DIR%\*.apk" (
    echo 恭喜！您的APK安装包已成功生成并复制到 %APP_DIR%
) else (
    echo 注意: 没有找到生成的APK文件
    echo 可能需要检查Buildozer的配置和错误信息
)
echo.
echo 提示:
if not exist "%OUTPUT_DIR%" (
    echo 1. Buildozer在Windows上构建可能需要特殊配置
    echo 2. 您可以参考"云服务打包指南.md"使用在线构建服务
    echo 3. 或者使用Android Studio直接构建
)
echo.
echo 按任意键退出...
pause