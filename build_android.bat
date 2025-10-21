
@echo off
set ANDROID_STUDIO_PATH=D:\b1az
set ANDROID_SDK_PATH=%ANDROID_STUDIO_PATH%\Sdk
set JAVA_HOME=%ANDROID_STUDIO_PATH%\jbr

REM 设置环境变量
echo 使用Android Studio路径: %ANDROID_STUDIO_PATH%
echo 使用Android SDK路径: %ANDROID_SDK_PATH%
echo 使用Java路径: %JAVA_HOME%

REM 添加SDK工具到PATH
set PATH=%PATH%;%ANDROID_SDK_PATH%\platform-tools;%ANDROID_SDK_PATH%\cmdline-tools\latest\bin;%JAVA_HOME%\bin

cls
echo ===================================================
echo PokeMMO自动化 - Android打包脚本
echo ===================================================
echo.
echo 注意：这是一个Python/Kivy项目，有两种打包方式：
echo 1. 使用Buildozer（推荐）
echo 2. 手动集成到Android Studio

echo.
echo 【推荐方法】使用Buildozer：
echo ---------------------------------------------------
echo 由于这是一个Kivy项目，Buildozer是官方推荐的打包工具
echo 您可以按照以下步骤操作：
echo 1. 确保已安装Python 3.7+
echo 2. 在命令提示符中运行：pip install buildozer
echo 3. 运行：buildozer android debug
echo 4. 打包文件将生成在bin目录中
echo.
echo 【Android Studio方法】需要以下步骤：
echo ---------------------------------------------------
echo 1. 打开Android Studio (%ANDROID_STUDIO_PATH%)
echo 2. 创建新项目或导入现有项目
echo 3. 安装Chaquopy插件以支持Python代码
echo 4. 将Python文件（pokemmo_automation_android.py等）添加到项目
echo 5. 配置Python依赖项

echo.
echo 详细步骤请参考项目中的"云服务打包指南.md"
echo 特别是Google Colab和GitHub Actions的免费打包方案
echo.
echo 按任意键继续...
pause
echo.
echo 正在启动Android Studio...
start "Android Studio" "%ANDROID_STUDIO_PATH%\bin\studio64.exe"

pause
