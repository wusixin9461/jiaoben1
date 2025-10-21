#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub Actions构建助手 - 用于在无法访问Google Colab时使用"""

import os
import subprocess
import webbrowser
import time
import shutil
from pathlib import Path

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """打印标题"""
    print("=" * 60)
    print("PokeMMO自动化 - GitHub Actions构建助手")
    print("由于Google Colab无法访问，此脚本将指导您使用GitHub Actions构建APK")
    print("=" * 60)
    print()

def check_git_installed():
    """检查Git是否已安装"""
    try:
        subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def generate_git_commands_guide():
    """生成Git命令指南"""
    guide = """
=== GitHub Actions构建步骤 ===

1. 创建GitHub账号（如果没有）：
   访问 https://github.com/join

2. 安装Git（如果未安装）：
   Windows用户：访问 https://git-scm.com/download/win 下载安装
   安装时使用默认设置即可

3. 配置Git（首次使用）：
   打开命令提示符（CMD）或PowerShell，执行以下命令：
   git config --global user.name "您的用户名"
   git config --global user.email "您的邮箱"

4. 在GitHub上创建新仓库：
   - 登录GitHub后，点击右上角的"+"号，选择"New repository"
   - 输入仓库名称（如"pokemmo-automation"）
   - 选择Public（公开）
   - 不要勾选"Initialize this repository with a README"
   - 点击"Create repository"

5. 上传项目文件：
   复制以下命令到命令提示符（CMD）或PowerShell中执行：
   cd E:\#9#531\2414
   git init
   git add .
   git commit -m "首次提交 - PokeMMO自动化项目"
   git branch -M main
   git remote add origin https://github.com/您的用户名/pokemmo-automation.git
   git push -u origin main

6. 触发GitHub Actions构建：
   - 上传完成后，在GitHub仓库页面点击"Actions"标签
   - 点击"Build Android APK" workflow
   - 点击"Run workflow"按钮，然后点击"Run workflow"

7. 下载APK文件：
   - 构建完成后，在Actions页面找到构建记录
   - 滚动到页面底部，在"Artifacts"部分下载"pokemmo-automation-apk"
   - 解压后即可得到APK文件

注意事项：
- 构建过程可能需要30-60分钟，请耐心等待
- 如果构建失败，请查看日志了解具体原因
- 确保.github/workflows目录和build-apk.yml文件已正确上传
    """
    return guide

def create_batch_upload_script():
    """创建批量上传脚本"""
    batch_content = """@echo off
cls
echo 正在准备上传项目到GitHub...
echo 请确保您已在GitHub上创建了仓库并安装了Git
echo.

set /p username="请输入您的GitHub用户名: "
set /p repo_name="请输入您的仓库名称 (默认为pokemmo-automation): "

if "%repo_name%" == "" set repo_name=pokemmo-automation

echo.
echo 正在初始化Git仓库...
git init
if errorlevel 1 (
    echo 错误: Git初始化失败，请确保Git已正确安装
    pause
    exit /b 1
)

echo 正在添加文件...
git add .
echo 正在创建提交...
git commit -m "首次提交 - PokeMMO自动化项目"
echo 正在设置分支...
git branch -M main
echo 正在添加远程仓库...
git remote add origin https://github.com/%username%/%repo_name%.git
echo 正在推送代码...
git push -u origin main

if errorlevel 1 (
    echo.
    echo 错误: 推送失败，请检查您的GitHub用户名和仓库名称是否正确
    echo 或者您可能需要先在GitHub上创建仓库
    echo 请手动执行以上步骤或重试
    pause
    exit /b 1
)

echo.
echo 上传成功！请在GitHub上的Actions标签页触发构建
pause
"""
    
    batch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload_to_github.bat')
    with open(batch_path, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    return batch_path

def check_workflow_file():
    """检查workflow文件是否存在"""
    workflow_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.github', 'workflows', 'build-apk.yml')
    if os.path.exists(workflow_path):
        print(f"✓ GitHub Actions工作流文件已存在: {workflow_path}")
        return True
    else:
        print(f"✗ 未找到工作流文件: {workflow_path}")
        return False

def create_missing_workflow():
    """创建缺失的workflow文件"""
    workflow_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.github', 'workflows')
    os.makedirs(workflow_dir, exist_ok=True)
    
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
        path: bin/*.apk'''
    
    workflow_path = os.path.join(workflow_dir, 'build-apk.yml')
    with open(workflow_path, 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    
    print(f"✓ 已创建GitHub Actions工作流文件: {workflow_path}")
    return workflow_path

def main():
    """主函数"""
    clear_screen()
    print_header()
    
    # 检查workflow文件
    if not check_workflow_file():
        create_missing_workflow()
    
    # 检查Git是否安装
    if check_git_installed():
        print("✓ Git已安装，可以使用命令行上传")
    else:
        print("✗ Git未安装，请先安装Git或使用批量上传脚本")
    
    # 创建批量上传脚本
    batch_path = create_batch_upload_script()
    print(f"✓ 已创建批量上传脚本: {batch_path}")
    
    print("\n" + "=" * 60)
    print("构建选项:")
    print("1. 查看详细的GitHub Actions构建指南")
    print("2. 打开GitHub官网创建仓库")
    print("3. 运行批量上传脚本")
    print("4. 退出")
    
    while True:
        choice = input("\n请选择 (1-4): ").strip()
        
        if choice == '1':
            print(generate_git_commands_guide())
            input("按Enter键继续...")
            clear_screen()
            print_header()
        elif choice == '2':
            print("正在打开GitHub官网...")
            webbrowser.open('https://github.com/new')
            print("请创建新仓库，不要初始化README文件")
            input("仓库创建完成后按Enter键继续...")
            clear_screen()
            print_header()
        elif choice == '3':
            print(f"正在运行批量上传脚本: {batch_path}")
            try:
                subprocess.run([batch_path], shell=True)
            except Exception as e:
                print(f"运行脚本时出错: {e}")
            input("按Enter键继续...")
            clear_screen()
            print_header()
        elif choice == '4':
            print("\n感谢使用！再见！")
            break
        else:
            print("无效的选择，请重新输入")

if __name__ == "__main__":
    main()