#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PokeMMO自动化 - Android打包完整指南

本脚本提供了将Kivy应用打包为Android APK的多种方法，
由于Windows环境限制，推荐使用云服务构建方案。
"""

import os
import sys
import webbrowser
import subprocess
import time

# 确保中文显示正常
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def print_header():
    """打印标题和介绍"""
    print("=" * 80)
    print("           PokeMMO自动化 - Android APK打包指南           ")
    print("=" * 80)
    print("\n本程序提供多种方法将您的Kivy应用打包为Android APK文件")
    print("由于Windows环境限制，直接在本地使用Buildozer可能会失败")
    print("强烈推荐使用云服务构建方案，如Google Colab或GitHub Actions")
    print()

def check_local_files():
    """检查必要的项目文件是否存在"""
    print("\n[✓] 检查项目文件...")
    required_files = [
        "pokemmo_automation_android.py",
        "buildozer.spec",
        "requirements_kivy.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  - 找到 {file}")
        else:
            print(f"  - 缺少 {file} ❌")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n警告: 缺少以下必要文件: {', '.join(missing_files)}")
        print("请确保这些文件存在于当前目录中")
    else:
        print("  - 所有必要文件检查通过 ✅")
    
    return len(missing_files) == 0

def show_google_colab_guide():
    """显示Google Colab构建指南"""
    print("\n" + "=" * 50)
    print("方法一: 使用Google Colab (推荐)")
    print("=" * 50)
    print("\n步骤:")
    print("1. 准备项目文件")
    print("   - 确保包含: pokemmo_automation_android.py, buildozer.spec, requirements_kivy.txt")
    print("\n2. 上传文件到Google Drive")
    print("   - 访问: https://drive.google.com")
    print("   - 创建文件夹: 'PokeMMOAutomation'")
    print("   - 上传上述文件")
    print("\n3. 打开Google Colab")
    print("   - 访问: https://colab.research.google.com/")
    print("   - 创建新笔记本")
    print("\n4. 依次运行以下代码块:")
    
    code_blocks = [
        ["步骤1: 挂载Google Drive", 
         "from google.colab import drive\ndrive.mount('/content/drive')"],
        ["步骤2: 进入项目文件夹", 
         "%cd /content/drive/MyDrive/PokeMMOAutomation"],
        ["步骤3: 安装工具和依赖", 
         "!pip install buildozer\n!apt-get update\n!apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev"],
        ["步骤4: 开始打包", 
         "!buildozer -v android debug"]
    ]
    
    for title, code in code_blocks:
        print(f"\n   {title}:")
        print("   " + "-" * 30)
        print("   " + code.replace("\n", "\n   "))
    
    print("\n5. 等待打包完成 (首次约30-60分钟)")
    print("6. 从bin文件夹下载生成的APK文件")
    print("\n提示: 可使用以下代码防止Colab超时:")
    print("   function ClickConnect(){console.log('Working'); document.querySelector('colab-toolbar-button#connect').click();}")
    print("   setInterval(ClickConnect, 60000)")
    
    if input("\n是否立即打开Google Colab? (y/n): ").lower() == 'y':
        webbrowser.open('https://colab.research.google.com/')

def show_github_actions_guide():
    """显示GitHub Actions构建指南"""
    print("\n" + "=" * 50)
    print("方法二: 使用GitHub Actions")
    print("=" * 50)
    print("\n步骤:")
    print("1. 创建GitHub账户")
    print("   - 访问: https://github.com/join")
    print("\n2. 创建新仓库")
    print("   - 仓库名称: pokemmo-automation")
    print("   - 设置为Public")
    print("\n3. 上传项目文件")
    print("   - 上传: pokemmo_automation_android.py, buildozer.spec, requirements_kivy.txt")
    print("\n4. 创建GitHub Actions工作流文件")
    print("   - 文件名: .github/workflows/build-apk.yml")
    print("   - 内容:")
    
    workflow_yaml = '''name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # 允许手动触发

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

    - name: Build APK
      run: buildozer -v android debug

    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: pokemmo-automation-apk
        path: bin/*.apk'''
    
    print("   " + workflow_yaml.replace("\n", "\n   "))
    print("\n5. 手动触发构建")
    print("   - 进入Actions标签页")
    print("   - 点击'Build Android APK'")
    print("   - 点击'Run workflow'")
    print("\n6. 构建完成后从Artifacts下载APK")
    
    if input("\n是否立即打开GitHub? (y/n): ").lower() == 'y':
        webbrowser.open('https://github.com/join')

def show_android_studio_guide():
    """显示Android Studio构建指南"""
    print("\n" + "=" * 50)
    print("方法三: 使用Android Studio (需要Chaquopy)")
    print("=" * 50)
    print("\n步骤:")
    print("1. 安装Android Studio")
    print("   - 访问: https://developer.android.com/studio")
    print("\n2. 安装Chaquopy插件")
    print("   - 在Android Studio中，进入File > Settings > Plugins")
    print("   - 搜索并安装'Chaquopy'")
    print("   - 重启Android Studio")
    print("\n3. 创建新Android项目")
    print("   - 选择'Empty Activity'")
    print("\n4. 配置Chaquopy")
    print("   - 在app/build.gradle文件中添加Chaquopy配置")
    print("   - 参考Chaquopy文档配置Python代码和依赖")
    print("\n5. 添加Python代码")
    print("   - 将您的Python代码放在app/src/main/python目录下")
    print("\n6. 配置依赖")
    print("   - 在build.gradle中添加必要的Python包依赖")
    print("\n7. 构建APK")
    print("   - 选择Build > Generate Signed Bundle / APK")
    print("   - 按照向导完成构建")
    print("\n注意: 此方法配置较为复杂，适合有Android开发经验的用户")

def run_local_buildozer_test():
    """运行本地Buildozer测试"""
    print("\n" + "=" * 50)
    print("方法四: 本地Windows Buildozer测试 (可能失败)")
    print("=" * 50)
    print("\n警告: Buildozer官方推荐在Linux环境运行")
    print("在Windows上直接运行Buildozer通常会失败")
    
    if input("\n确定要继续测试吗? (y/n): ").lower() != 'y':
        return
    
    print("\n正在尝试运行buildozer android debug...")
    print("这只是测试，不保证成功...")
    
    try:
        process = subprocess.Popen(
            ["buildozer", "android", "debug"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 读取并显示输出
        while True:
            stdout_line = process.stdout.readline()
            stderr_line = process.stderr.readline()
            
            if stdout_line:
                print(stdout_line.strip())
            if stderr_line:
                print(f"错误: {stderr_line.strip()}")
            
            if process.poll() is not None:
                # 读取剩余输出
                for line in process.stdout:
                    print(line.strip())
                for line in process.stderr:
                    print(f"错误: {line.strip()}")
                break
            
            time.sleep(0.1)
        
        print("\n测试完成，如预期，在Windows上Buildozer构建通常会失败")
        print("请使用推荐的云服务构建方案")
        
    except Exception as e:
        print(f"\n执行出错: {e}")
        print("Buildozer在Windows上不可用，建议使用云服务")

def create_github_actions_file():
    """创建GitHub Actions工作流文件"""
    if input("\n是否创建GitHub Actions工作流文件? (y/n): ").lower() != 'y':
        return
    
    workflow_dir = os.path.join(".github", "workflows")
    workflow_file = os.path.join(workflow_dir, "build-apk.yml")
    
    # 创建目录
    if not os.path.exists(workflow_dir):
        os.makedirs(workflow_dir)
        print(f"已创建目录: {workflow_dir}")
    
    # 创建文件内容
    workflow_yaml = '''name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # 允许手动触发

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

    - name: Build APK
      run: buildozer -v android debug

    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: pokemmo-automation-apk
        path: bin/*.apk'''
    
    # 写入文件
    with open(workflow_file, "w", encoding="utf-8") as f:
        f.write(workflow_yaml)
    
    print(f"已创建GitHub Actions工作流文件: {workflow_file}")
    print("您可以将此文件和项目文件一起上传到GitHub仓库")

def main():
    """主函数"""
    print_header()
    
    # 检查项目文件
    files_ready = check_local_files()
    
    if not files_ready:
        print("\n请先准备好所有必要的项目文件")
        time.sleep(2)
    
    while True:
        print("\n" + "=" * 80)
        print("           请选择构建方法           ")
        print("=" * 80)
        print("1. Google Colab 构建 (推荐，免费，简单)")
        print("2. GitHub Actions 构建 (免费，自动化)")
        print("3. Android Studio + Chaquopy (需要更多配置)")
        print("4. 本地Windows Buildozer测试 (不推荐，可能失败)")
        print("5. 创建GitHub Actions工作流文件")
        print("6. 退出")
        print("=" * 80)
        
        choice = input("\n请输入选择 (1-6): ")
        
        if choice == "1":
            show_google_colab_guide()
        elif choice == "2":
            show_github_actions_guide()
        elif choice == "3":
            show_android_studio_guide()
        elif choice == "4":
            run_local_buildozer_test()
        elif choice == "5":
            create_github_actions_file()
        elif choice == "6":
            print("\n感谢使用PokeMMO自动化Android打包指南！")
            print("祝您构建顺利！")
            break
        else:
            print("\n无效选择，请重新输入")

if __name__ == "__main__":
    main()