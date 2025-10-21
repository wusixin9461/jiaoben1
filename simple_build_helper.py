#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单构建助手脚本"""

import os
import subprocess
import webbrowser
import time
from pathlib import Path

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """打印标题"""
    print("=" * 50)
    print("PokeMMO自动化 - 构建助手")
    print("=" * 50)
    print()

def check_environment():
    """检查环境"""
    print("正在检查环境...")
    try:
        # 检查Python版本
        python_version = subprocess.check_output(['python', '--version'], stderr=subprocess.STDOUT).decode().strip()
        print(f"✓ Python: {python_version}")
        
        # 检查pip
        pip_version = subprocess.check_output(['pip', '--version'], stderr=subprocess.STDOUT).decode().strip()
        print(f"✓ pip: {pip_version.split()[0]} {pip_version.split()[1]}")
        
        # 检查buildozer
        try:
            buildozer_version = subprocess.check_output(['buildozer', '--version'], stderr=subprocess.STDOUT).decode().strip()
            print(f"✓ Buildozer: {buildozer_version}")
        except (subprocess.SubprocessError, FileNotFoundError):
            print("✗ Buildozer未安装")
        
        # 检查项目文件
        project_dir = os.path.dirname(os.path.abspath(__file__))
        main_file = os.path.join(project_dir, 'pokemmo_automation_android.py')
        spec_file = os.path.join(project_dir, 'buildozer.spec')
        
        if os.path.exists(main_file):
            print(f"✓ 主程序文件: {os.path.basename(main_file)}")
        else:
            print(f"✗ 未找到主程序文件: {os.path.basename(main_file)}")
        
        if os.path.exists(spec_file):
            print(f"✓ Buildozer配置: {os.path.basename(spec_file)}")
        else:
            print(f"✗ 未找到Buildozer配置文件: {os.path.basename(spec_file)}")
            
    except Exception as e:
        print(f"检查环境时出错: {e}")
    
    print()

def open_colab():
    """打开Google Colab并提供指导"""
    print("正在打开Google Colab...")
    webbrowser.open('https://colab.research.google.com/')
    
    print("\n=== Google Colab构建指南 ===")
    print("1. 将项目文件上传到Google Drive")
    print("2. 在Colab中挂载Google Drive")
    print("3. 运行optimized_colab_script.ipynb中的命令")
    print("4. 重要: 在浏览器控制台运行防超时脚本:")
    print("   function ClickConnect(){console.log(\"Working\"); document.querySelector(\"colab-toolbar-button#connect\").click();}")
    print("   setInterval(ClickConnect, 60000)")
    print("\n构建完成后，APK文件将在项目目录的bin文件夹中")

def open_github():
    """打开GitHub并提供指导"""
    print("正在打开GitHub...")
    webbrowser.open('https://github.com/')
    
    print("\n=== GitHub Actions构建指南 ===")
    print("1. 创建新的GitHub仓库")
    print("2. 上传所有项目文件，包括.github/workflows目录")
    print("3. 进入Actions标签页，手动触发构建")
    print("4. 构建完成后，从Artifacts下载APK文件")

def try_local_build():
    """尝试本地构建"""
    print("警告: 在Windows上直接使用buildozer构建Android可能会失败")
    print("buildozer官方推荐在Linux环境中运行")
    
    if input("是否继续尝试本地构建? (y/n): ").lower() != 'y':
        return
    
    print("\n正在尝试本地构建...")
    print("此过程可能需要很长时间，且在Windows上很可能失败")
    
    try:
        # 设置超时环境变量
        env = os.environ.copy()
        env['P4A_TIMEOUT'] = '1800'
        
        # 执行buildozer命令
        process = subprocess.Popen(
            ['buildozer', 'android', 'debug'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env
        )
        
        # 实时显示输出
        for line in process.stdout:
            print(line.strip())
        
        process.wait()
        
        # 检查结果
        if process.returncode == 0:
            print("\n构建成功！")
            # 查找APK文件
            bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin')
            if os.path.exists(bin_dir):
                apks = [f for f in os.listdir(bin_dir) if f.endswith('.apk')]
                if apks:
                    print(f"找到APK文件: {', '.join(apks)}")
                    # 复制到APP目录
                    app_dir = 'E:\\#9#531\\APP'
                    if not os.path.exists(app_dir):
                        os.makedirs(app_dir)
                    
                    for apk in apks:
                        apk_path = os.path.join(bin_dir, apk)
                        dest_path = os.path.join(app_dir, apk)
                        try:
                            import shutil
                            shutil.copy2(apk_path, dest_path)
                            print(f"已复制到: {dest_path}")
                        except Exception as e:
                            print(f"复制失败: {e}")
                else:
                    print("未找到APK文件")
        else:
            print("\n构建失败")
            print("推荐使用Google Colab或GitHub Actions构建方案")
            
    except subprocess.SubprocessError as e:
        print(f"构建过程中出错: {e}")
    except KeyboardInterrupt:
        print("\n构建已取消")
    except Exception as e:
        print(f"发生未知错误: {e}")

def main():
    """主函数"""
    clear_screen()
    print_header()
    check_environment()
    
    while True:
        print("构建选项:")
        print("1. 使用Google Colab (推荐的免费方案)")
        print("2. 使用GitHub Actions (自动化构建)")
        print("3. 尝试本地构建 (不推荐，可能失败)")
        print("4. 退出")
        
        choice = input("\n请选择 (1-4): ").strip()
        
        if choice == '1':
            open_colab()
        elif choice == '2':
            open_github()
        elif choice == '3':
            try_local_build()
        elif choice == '4':
            print("\n感谢使用！再见！")
            break
        else:
            print("无效的选择，请重新输入")
        
        print("\n按Enter键继续...")
        input()
        clear_screen()
        print_header()

if __name__ == "__main__":
    main()