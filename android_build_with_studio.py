import os
import subprocess
import sys
import shutil

# 假设Android Studio安装路径
ANDROID_STUDIO_PATH = r"D:\b1az"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def check_android_studio():
    """检查Android Studio是否存在"""
    if os.path.exists(ANDROID_STUDIO_PATH):
        print(f"找到Android Studio: {ANDROID_STUDIO_PATH}")
        return True
    else:
        print(f"未找到Android Studio: {ANDROID_STUDIO_PATH}")
        return False

def prepare_project():
    """准备Android项目结构"""
    # 创建必要的文件夹结构
    android_project_dir = os.path.join(PROJECT_DIR, "android_project")
    if not os.path.exists(android_project_dir):
        os.makedirs(android_project_dir)
    
    print(f"已创建Android项目目录: {android_project_dir}")
    return android_project_dir

def create_build_script(android_project_dir):
    """创建构建脚本"""
    build_script_path = os.path.join(PROJECT_DIR, "build_android.bat")
    
    script_content = f"""
@echo off
set ANDROID_STUDIO_PATH={ANDROID_STUDIO_PATH.replace('\\', '\\\\')}
set ANDROID_SDK_PATH=%ANDROID_STUDIO_PATH%\\Sdk
set JAVA_HOME=%ANDROID_STUDIO_PATH%\\jbr

REM 设置环境变量
export ANDROID_HOME=%ANDROID_SDK_PATH%
export PATH=%PATH%;%ANDROID_SDK_PATH%\platform-tools;%ANDROID_SDK_PATH%\tools;%JAVA_HOME%\bin

echo 使用Android Studio路径: %ANDROID_STUDIO_PATH%
echo 使用Android SDK路径: %ANDROID_SDK_PATH%
echo 使用Java路径: %JAVA_HOME%

echo 开始构建Android应用...
REM 这里应该是实际的构建命令，根据项目类型可能不同
echo 注意：由于这是一个Python/Kivy项目，推荐使用buildozer进行打包
echo 请参考项目中的云服务打包指南.md文件获取详细打包方法

pause
"""
    
    with open(build_script_path, 'w') as f:
        f.write(script_content)
    
    print(f"已创建构建脚本: {build_script_path}")
    return build_script_path

def copy_necessary_files(android_project_dir):
    """复制必要的文件到Android项目目录"""
    # 复制主要的Python文件
    if os.path.exists("pokemmo_automation_android.py"):
        shutil.copy("pokemmo_automation_android.py", android_project_dir)
        print("已复制主Python文件")
    
    # 复制配置文件
    if os.path.exists("buildozer.spec"):
        shutil.copy("buildozer.spec", android_project_dir)
        print("已复制buildozer配置文件")
    
    if os.path.exists("requirements_kivy.txt"):
        shutil.copy("requirements_kivy.txt", android_project_dir)
        print("已复制依赖配置文件")

def main():
    print("=== PokeMMO自动化 - Android Studio打包准备工具 ===")
    
    # 检查Android Studio
    android_studio_available = check_android_studio()
    
    if not android_studio_available:
        print("警告: 未找到Android Studio。请确认路径是否正确。")
    
    # 准备项目
    android_project_dir = prepare_project()
    
    # 复制必要文件
    copy_necessary_files(android_project_dir)
    
    # 创建构建脚本
    build_script = create_build_script(android_project_dir)
    
    print("\n=== 准备完成 ===")
    print("1. 项目文件已复制到: " + android_project_dir)
    print("2. 构建脚本已创建: " + build_script)
    print("\n重要提示:")
    print("- 对于Python/Kivy项目，使用buildozer是最推荐的打包方式")
    print("- 请参考项目中的'云服务打包指南.md'获取详细的免费打包方法")
    print("- 如果需要使用Android Studio直接打包，您需要先创建一个Android项目并集成Python代码")
    print("  这通常需要使用Chaquopy或Kivy的Android打包功能")

if __name__ == "__main__":
    main()