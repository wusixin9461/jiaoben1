#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自动上传项目到GitHub并触发Actions构建"""

import os
import subprocess
import sys
import time
import json
from pathlib import Path

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """打印标题"""
    print("=" * 60)
    print("PokeMMO自动化 - GitHub自动上传与构建助手")
    print("=" * 60)
    print()

def check_git_installed():
    """检查Git是否已安装"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True, check=True)
        print(f"✓ Git已安装: {result.stdout.strip()}")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("✗ Git未安装，请先安装Git")
        return False

def setup_git_config():
    """设置Git配置"""
    try:
        # 检查是否已有配置
        user_name = subprocess.run(['git', 'config', '--global', 'user.name'], capture_output=True, text=True).stdout.strip()
        user_email = subprocess.run(['git', 'config', '--global', 'user.email'], capture_output=True, text=True).stdout.strip()
        
        if not user_name:
            user_name = "吴思鑫"
            subprocess.run(['git', 'config', '--global', 'user.name', user_name], check=True)
            print(f"✓ 设置Git用户名: {user_name}")
        else:
            print(f"✓ Git用户名已设置: {user_name}")
        
        if not user_email:
            user_email = "wusixin9641@example.com"
            subprocess.run(['git', 'config', '--global', 'user.email', user_email], check=True)
            print(f"✓ 设置Git邮箱: {user_email}")
        else:
            print(f"✓ Git邮箱已设置: {user_email}")
            
    except subprocess.SubprocessError as e:
        print(f"✗ 设置Git配置失败: {e}")
        return False
    
    return True

def initialize_git_repo():
    """初始化Git仓库"""
    try:
        # 检查是否已有git环境
        if os.path.exists('.git'):
            print("✓ Git仓库已存在，跳过初始化")
            return True
        
        print("正在初始化Git仓库...")
        subprocess.run(['git', 'init'], check=True)
        print("✓ Git仓库初始化成功")
        return True
    except subprocess.SubprocessError as e:
        print(f"✗ 初始化Git仓库失败: {e}")
        return False

def create_gitignore():
    """创建.gitignore文件"""
    gitignore_path = '.gitignore'
    if not os.path.exists(gitignore_path):
        print("正在创建.gitignore文件...")
        gitignore_content = '''# OSX
#
.DS_Store

# Xcode
#
build/
*.pbxuser
!default.pbxuser
*.mode1v3
!default.mode1v3
*.mode2v3
!default.mode2v3
*.perspectivev3
!default.perspectivev3
xcuserdata
*.xccheckout
*.moved-aside
DerivedData
*.hmap
*.ipa
*.xcuserstate
project.xcworkspace

# Android/IntelliJ
#
build/
.idea
.gradle
local.properties
*.iml
*.hprof
.cxx/
*.keystore
!debug.keystore

# node.js
#
node_modules/
npm-debug.log
yarn-error.log

# BUCK
buck-out/
\.buckd/
*.keystore
!debug.keystore

# Bundle artifacts
*.jsbundle

# CocoaPods
/ios/Pods/

# Temporary files created by Metro to check the health of the file watcher
.metro-health-check*

# Expo
.expo/
dist/
web-build/

# Buildozer
.buildozer/
bin/
*.apk
*.aab

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
env3/
ENV/
*.egg-info/
.installed.cfg
*.egg

# Testing
coverage/
.pytest_cache/
.tox/

# Logs
*.log
*.log.*

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Other
.cache/
.tmp/
.temp/'''
        
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print(f"✓ 创建.gitignore文件成功")
    else:
        print("✓ .gitignore文件已存在")

def add_and_commit():
    """添加文件并提交"""
    try:
        print("正在添加所有文件...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        print("正在创建提交...")
        commit_message = f"自动提交 - PokeMMO自动化项目 - {time.strftime('%Y-%m-%d %H:%M:%S')}"
        result = subprocess.run(['git', 'commit', '-m', commit_message], capture_output=True, text=True)
        
        if "nothing to commit" in result.stdout:
            print("✓ 没有需要提交的更改")
        else:
            print(f"✓ 提交成功: {commit_message}")
        
        return True
    except subprocess.SubprocessError as e:
        print(f"✗ 添加或提交失败: {e}")
        return False

def setup_remote(repo_url):
    """设置远程仓库"""
    try:
        # 检查是否已有远程仓库配置
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
        
        if result.returncode == 0:
            current_url = result.stdout.strip()
            if current_url == repo_url:
                print(f"✓ 远程仓库已正确配置: {repo_url}")
            else:
                print(f"正在更新远程仓库URL...")
                subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url], check=True)
                print(f"✓ 远程仓库URL已更新: {repo_url}")
        else:
            print(f"正在添加远程仓库: {repo_url}")
            subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
            print(f"✓ 远程仓库添加成功")
        
        return True
    except subprocess.SubprocessError as e:
        print(f"✗ 设置远程仓库失败: {e}")
        return False

def push_to_github():
    """推送到GitHub"""
    try:
        print("正在推送到GitHub...")
        # 设置分支为main
        subprocess.run(['git', 'branch', '-M', 'main'], check=True)
        
        # 推送代码，设置为跟踪远程分支
        result = subprocess.run(
            ['git', 'push', '-u', 'origin', 'main'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            # 检查是否需要强制推送（如果远程有冲突）
            print(f"推送失败，可能存在冲突: {result.stderr}")
            print("尝试强制推送...")
            subprocess.run(['git', 'push', '-u', 'origin', 'main', '--force'], check=True)
        
        print("✓ 推送到GitHub成功！")
        return True
    except subprocess.SubprocessError as e:
        print(f"✗ 推送到GitHub失败: {e}")
        return False

def check_workflow_file():
    """检查workflow文件是否存在并正确配置"""
    workflow_path = Path('.github/workflows/build-apk.yml')
    
    if not workflow_path.exists():
        print(f"✗ 未找到workflow文件: {workflow_path}")
        return False
    
    print(f"✓ workflow文件存在: {workflow_path}")
    return True

def generate_build_instructions():
    """生成构建说明"""
    instructions = """
============================================================
🎉 项目上传成功！接下来请手动触发GitHub Actions构建：
============================================================

1. 打开GitHub仓库页面：
   https://github.com/wusixin9641/jiaben

2. 点击顶部的 "Actions" 标签

3. 在左侧找到 "Build Android APK" workflow

4. 点击 "Run workflow" 按钮

5. 在弹出的对话框中再次点击 "Run workflow"

6. 构建过程将自动开始，大约需要30-60分钟

7. 构建完成后，在构建记录页面的底部 "Artifacts" 部分
   下载 "pokemmo-automation-apk" 文件

8. 解压后即可得到APK安装包！

============================================================
注意：构建过程可能会因为网络或依赖问题失败，请耐心等待并查看日志
============================================================
    """
    return instructions

def main():
    """主函数"""
    clear_screen()
    print_header()
    
    # 定义仓库URL
    repo_url = "https://github.com/wusixin9641/jiaben.git"
    
    # 获取当前目录作为项目目录（避免硬编码路径问题）
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"当前工作目录: {os.getcwd()}")
    
    # 检查Git安装
    if not check_git_installed():
        print("请先安装Git，然后重试")
        input("按Enter键退出...")
        return
    
    # 设置Git配置
    if not setup_git_config():
        input("按Enter键退出...")
        return
    
    # 检查workflow文件
    if not check_workflow_file():
        print("正在创建workflow文件...")
        # 创建必要的目录
        os.makedirs('.github/workflows', exist_ok=True)
        # 创建workflow文件
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
        
        with open('.github/workflows/build-apk.yml', 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        print("✓ workflow文件创建成功")
    
    # 创建.gitignore
    create_gitignore()
    
    # 初始化仓库
    if not initialize_git_repo():
        input("按Enter键退出...")
        return
    
    # 添加并提交
    if not add_and_commit():
        input("按Enter键退出...")
        return
    
    # 设置远程仓库
    if not setup_remote(repo_url):
        input("按Enter键退出...")
        return
    
    # 推送到GitHub
    if not push_to_github():
        print("\n推送失败，请手动执行以下命令：")
        print(f"git push -u origin main")
        input("按Enter键退出...")
        return
    
    # 显示构建说明
    print(generate_build_instructions())
    
    print("\n自动上传完成！请按照上面的说明触发GitHub Actions构建")
    input("按Enter键退出...")

if __name__ == "__main__":
    main()