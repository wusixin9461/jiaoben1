#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动解决Kivy+Buildozer Android构建问题脚本
此脚本将自动配置环境、优化构建设置并提供完整的构建流程
"""

import os
import sys
import subprocess
import time
import json
import webbrowser
import re
import shutil
from pathlib import Path

# 确保中文显示正常
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 项目配置
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join("E:\#9#531", "APP")
LOG_FILE = os.path.join(PROJECT_DIR, "build_automation.log")

# GitHub Actions文件路径
GITHUB_WORKFLOW_DIR = os.path.join(PROJECT_DIR, ".github", "workflows")
GITHUB_WORKFLOW_FILE = os.path.join(GITHUB_WORKFLOW_DIR, "build-apk.yml")

# Google Colab脚本路径
COLAB_SCRIPT_PATH = os.path.join(PROJECT_DIR, "colab_build_script.ipynb")

def log_message(message):
    """记录日志信息"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    print(log_entry.strip())
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

def ensure_directory(path):
    """确保目录存在"""
    if not os.path.exists(path):
        log_message(f"创建目录: {path}")
        os.makedirs(path)

def check_project_files():
    """检查必要的项目文件"""
    log_message("检查项目文件...")
    
    required_files = [
        ("pokemmo_automation_android.py", "主程序文件"),
        ("buildozer.spec", "Buildozer配置文件"),
        ("requirements_kivy.txt", "依赖文件")
    ]
    
    missing_files = []
    for filename, description in required_files:
        filepath = os.path.join(PROJECT_DIR, filename)
        if os.path.exists(filepath):
            log_message(f"✓ 找到 {description}: {filename}")
        else:
            log_message(f"✗ 缺少 {description}: {filename}")
            missing_files.append(filename)
    
    return missing_files

def optimize_buildozer_spec():
    """优化buildozer.spec文件配置"""
    spec_path = os.path.join(PROJECT_DIR, "buildozer.spec")
    
    if not os.path.exists(spec_path):
        log_message("buildozer.spec文件不存在，将创建默认配置")
        create_default_spec()
        return
    
    log_message("优化buildozer.spec配置文件...")
    
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 优化配置项
    optimizations = [
        # 加快构建速度
        (r'#?android.skip_update =.*', 'android.skip_update = True'),
        (r'#?android.skip_sign =.*', 'android.skip_sign = True'),
        # 增加超时设置
        (r'#?android.sdk_update_hook =.*', 'android.sdk_update_hook = %(hooks_path)s/android_sdk_update_hook.sh'),
        # 优化依赖安装
        (r'#?requirements = .*', 'requirements = python3,kivy==2.2.1,opencv-python==4.8.1.78,numpy==1.24.3,pillow==10.0.0,plyer==2.1.0'),
        # 设置更好的API级别
        (r'#?android.api = .*', 'android.api = 33'),
        (r'#?android.minapi = .*', 'android.minapi = 21'),
        (r'#?android.ndk = .*', 'android.ndk = 25.1.8937393'),
        # 增加内存配置
        (r'#?p4a.branch = .*', 'p4a.branch = master'),
        # 设置缓存
        (r'#?android.p4a_dir = .*', 'android.p4a_dir = ~/.local/share/python-for-android'),
    ]
    
    for pattern, replacement in optimizations:
        if not re.search(r'^[^#]*' + pattern.split('#?')[-1].split(' =')[0], content, re.MULTILINE):
            # 如果配置项不存在，则添加到相应部分
            if 'android.' in pattern:
                content += f'\n{replacement}'
        else:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # 确保权限设置正确
    if 'android.permissions =' not in content:
        content += '\nandroid.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET'
    
    # 保存优化后的配置
    with open(spec_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    log_message("✓ buildozer.spec配置优化完成")

def create_default_spec():
    """创建默认的buildozer.spec文件"""
    spec_path = os.path.join(PROJECT_DIR, "buildozer.spec")
    
    default_spec = '''[app]

title = pokemmo自动化

package.name = pokemmoautomation

package.domain = org.example

source.dir = .

source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy==2.2.1,opencv-python==4.8.1.78,numpy==1.24.3,pillow==10.0.0,plyer==2.1.0

orientation = portrait

fullscreen = 0

android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

android.api = 33

android.minapi = 21

android.ndk = 25.1.8937393

android.skip_update = True

android.skip_sign = True

p4a.branch = master

android.p4a_dir = ~/.local/share/python-for-android
'''
    
    with open(spec_path, "w", encoding="utf-8") as f:
        f.write(default_spec)
    
    log_message("✓ 默认buildozer.spec文件创建完成")

def create_github_workflow():
    """创建GitHub Actions工作流文件"""
    ensure_directory(GITHUB_WORKFLOW_DIR)
    
    workflow_content = '''name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # 允许手动触发

jobs:
  build:
    runs-on: ubuntu-latest
    
    # 增加超时时间
    timeout-minutes: 120

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    # 缓存依赖以加快构建速度
    - name: Cache Python dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Cache buildozer
      uses: actions/cache@v3
      with:
        path: |
          ~/.buildozer
          .buildozer
        key: ${{ runner.os }}-buildozer
        restore-keys: |
          ${{ runner.os }}-buildozer

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

    - name: Build APK
      run: |
        # 设置更长的超时时间
        export P4A_TIMEOUT=1800
        buildozer -v android debug

    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: pokemmo-automation-apk
        path: bin/*.apk
'''
    
    with open(GITHUB_WORKFLOW_FILE, "w", encoding="utf-8") as f:
        f.write(workflow_content)
    
    log_message(f"✓ GitHub Actions工作流文件创建完成: {GITHUB_WORKFLOW_FILE}")

def create_colab_script():
    """创建Google Colab构建脚本"""
    colab_content = '''
# Google Colab Kivy应用构建脚本
# 此脚本包含防超时机制和优化的构建配置

# 步骤1: 挂载Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 步骤2: 设置工作目录
%cd /content/drive/MyDrive/PokeMMOAutomation

# 步骤3: 安装必要的工具和依赖
!pip install --upgrade pip
!pip install buildozer
!apt-get update
!apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 步骤4: 创建防超时机制
# 在浏览器控制台运行以下代码防止Colab超时:
"""
function ClickConnect(){console.log("Working"); document.querySelector("colab-toolbar-button#connect").click();}
setInterval(ClickConnect, 60000)
"""

# 步骤5: 增加构建超时设置
import os
os.environ['P4A_TIMEOUT'] = '1800'

# 步骤6: 开始优化构建
print("开始构建APK...")
print("首次构建可能需要30-60分钟，请保持页面打开")
print("如果遇到内存问题，可以切换到High-RAM运行时类型")

!buildozer -v android debug

# 步骤7: 检查构建结果
print("\n检查构建结果:")
!ls -la bin/ 2>/dev/null || echo "构建失败，未找到bin目录"

# 如果构建成功，显示APK信息
!file bin/*.apk 2>/dev/null || echo "构建可能失败，未找到APK文件"

print("\n构建完成！")
print("如果成功，APK文件位于bin目录中")
print("您可以使用左侧文件浏览器下载APK文件")
'''
    
    with open(COLAB_SCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(colab_content)
    
    log_message(f"✓ Google Colab构建脚本创建完成: {COLAB_SCRIPT_PATH}")

def create_skip_update_hook():
    """创建Android SDK更新钩子以跳过不必要的更新"""
    hooks_dir = os.path.join(PROJECT_DIR, "hooks")
    hook_path = os.path.join(hooks_dir, "android_sdk_update_hook.sh")
    
    ensure_directory(hooks_dir)
    
    hook_content = '''#!/bin/bash
# Android SDK更新钩子 - 跳过不必要的更新以加快构建速度
echo "执行自定义SDK更新钩子..."
echo "跳过完整SDK更新，以加快构建速度"

# 确保必要的目录存在
mkdir -p $ANDROID_SDK_HOME/licenses

# 创建必要的许可证文件
echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > $ANDROID_SDK_HOME/licenses/android-sdk-license
echo "d975f751698a77b662f1254ddbeed3901e976f5a" > $ANDROID_SDK_HOME/licenses/android-sdk-preview-license

echo "SDK更新钩子执行完成"
exit 0
'''
    
    with open(hook_path, "w", encoding="utf-8") as f:
        f.write(hook_content)
    
    # 设置执行权限
    try:
        os.chmod(hook_path, 0o755)
    except:
        log_message("警告: 无法设置钩子脚本执行权限(Windows上正常)")
    
    log_message(f"✓ SDK更新钩子创建完成: {hook_path}")

def create_optimized_build_script():
    """创建优化的构建脚本"""
    build_script_path = os.path.join(PROJECT_DIR, "optimized_build.bat")
    
    script_content = '''@echo off
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
if not exist "%~dp0\bin" mkdir "%~dp0\bin"
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
    
    if exist "%~dp0\bin\*.apk" (
        echo.
        echo 构建成功！
        dir "%~dp0\bin\*.apk"
        echo.
        echo 正在复制APK到输出目录...
        copy "%~dp0\bin\*.apk" "E:\#9#531\APP\" /Y
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
'''
    
    with open(build_script_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    
    log_message(f"✓ 优化的构建脚本创建完成: {build_script_path}")

def create_anti_timeout_colab_notebook():
    """创建包含防超时机制的完整Colab笔记本文件"""
    notebook_path = os.path.join(PROJECT_DIR, "optimized_colab_script.ipynb")
    
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# PokeMMO自动化 - Google Colab构建指南\n", "\n", "使用此笔记本将Kivy应用打包为Android APK文件。\n", "此版本包含防超时机制和优化的构建配置。"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# 步骤1: 挂载Google Drive\n", "from google.colab import drive\n", "drive.mount('/content/drive')"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# 步骤2: 设置工作目录\n", "%cd /content/drive/MyDrive/PokeMMOAutomation"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 防超时提示\n", "\n", "请在浏览器控制台运行以下代码防止Colab超时:\n", "```javascript\n", "function ClickConnect(){console.log(\"Working\"); document.querySelector(\"colab-toolbar-button#connect\").click();}\n", "setInterval(ClickConnect, 60000)\n", "```"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# 步骤3: 安装必要的工具和依赖\n", "!pip install --upgrade pip\n", "!pip install buildozer\n", "!apt-get update\n", "!apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# 步骤4: 增加构建超时设置\n", "import os\n", "os.environ['P4A_TIMEOUT'] = '1800'  # 设置30分钟超时"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 内存优化提示\n", "\n", "如果遇到内存不足错误，请执行以下操作:\n", "1. 点击顶部菜单: Runtime -> Change runtime type\n", "2. 选择High-RAM选项\n", "3. 点击Save后重新运行所有代码块"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# 步骤5: 开始构建\n", "print(\"开始构建APK...\")\n", "print(\"首次构建可能需要30-60分钟，请保持页面打开\")\n", "\n", "!buildozer -v android debug"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# 步骤6: 检查构建结果\n", "print(\"\\n检查构建结果:\")\n", "!ls -la bin/ 2>/dev/null || echo \"构建失败，未找到bin目录\"\n", "\n", "# 显示APK信息\n", "!file bin/*.apk 2>/dev/null || echo \"构建可能失败，未找到APK文件\"\n", "\n", "print(\"\\n构建完成！\")\n", "print(\"如果成功，APK文件位于bin目录中\")\n", "print(\"您可以使用左侧文件浏览器下载APK文件\")"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 常见问题解决\n", "\n", "### 如果构建失败:\n", "1. 检查错误信息，通常是依赖问题\n", "2. 尝试修改buildozer.spec中的依赖版本\n", "3. 确保项目文件完整\n", "4. 重新运行构建命令\n", "\n", "### 成功后:\n", "1. 下载APK文件到您的电脑\n", "2. 将APK传输到Android设备\n", "3. 安装并授予必要的权限"]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(notebook_content, f, indent=2, ensure_ascii=False)
    
    log_message(f"✓ 优化的Colab笔记本创建完成: {notebook_path}")

def main():
    """主函数"""
    print("=" * 80)
    print("        PokeMMO自动化 - Android构建问题自动解决方案        ")
    print("=" * 80)
    print("\n此工具将自动解决Kivy+Buildozer Android构建中的超时问题")
    print("正在进行自动配置和优化...")
    
    # 初始化日志
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 构建自动化开始\n")
    
    # 确保APP目录存在
    ensure_directory(APP_DIR)
    
    # 检查项目文件
    missing_files = check_project_files()
    if missing_files:
        log_message("警告: 缺少必要的项目文件，将影响构建结果")
    
    # 优化配置
    optimize_buildozer_spec()
    create_github_workflow()
    create_colab_script()
    create_skip_update_hook()
    create_optimized_build_script()
    create_anti_timeout_colab_notebook()
    
    # 创建快速开始指南
    quick_start_path = os.path.join(PROJECT_DIR, "快速开始构建指南.md")
    with open(quick_start_path, "w", encoding="utf-8") as f:
        f.write('''# 快速开始构建指南

## 推荐构建方法（解决超时问题）

### 方法一：Google Colab（最简单）
1. 打开 `optimized_colab_script.ipynb` 文件查看详细步骤
2. 将项目文件上传到Google Drive的PokeMMOAutomation文件夹
3. 在Google Colab中运行笔记本中的代码
4. **重要**: 在浏览器控制台运行防超时代码:
   ```javascript
   function ClickConnect(){console.log("Working"); document.querySelector("colab-toolbar-button#connect").click();}
   setInterval(ClickConnect, 60000)
   ```

### 方法二：GitHub Actions
1. 创建GitHub仓库并上传项目文件（包括.github/workflows目录）
2. 进入Actions标签页手动触发构建
3. 构建完成后从Artifacts下载APK

## 一键运行
双击运行 `optimized_build.bat` 获取交互式构建选项

## 解决的问题
- ✓ 增加构建超时时间
- ✓ 提供防Colab超时脚本
- ✓ 优化buildozer配置
- ✓ 创建自动化工作流
- ✓ 提供多种构建选项
''')
    
    print("\n" + "=" * 80)
    print("✅ 自动配置完成！")
    print("=" * 80)
    print("\n已解决的问题:")
    print("1. 增加了构建超时时间设置")
    print("2. 创建了防Colab超时机制")
    print("3. 优化了buildozer.spec配置文件")
    print("4. 创建了GitHub Actions自动化工作流")
    print("5. 生成了完整的构建脚本和指南")
    print("\n快速开始:")
    print(f"- 查看详细指南: {quick_start_path}")
    print(f"- 运行一键构建脚本: {os.path.join(PROJECT_DIR, 'optimized_build.bat')}")
    print(f"- 使用优化的Colab笔记本: E:\#9#531\2414\optimized_colab_script.ipynb")
    print("\n所有操作已自动完成，无需额外权限设置！")

if __name__ == "__main__":
    main()