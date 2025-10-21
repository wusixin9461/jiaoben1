#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动下载GitHub Actions构建的APK并复制到APP文件夹
作者: AI助手
日期: 2024-01-01
"""

import os
import sys
import time
import zipfile
import requests
import subprocess
from pathlib import Path

# 项目配置
GITHUB_USERNAME = "wusixin9461"
GITHUB_REPO_NAME = "jiaoben1"
WORKFLOW_NAME = "Build Android APK"
APP_FOLDER = "E:\\#9#531\\APP"
DOWNLOAD_DIR = "E:\\#9#531\\2414\\temp_apk"

# 确保目录存在
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(APP_FOLDER, exist_ok=True)

def print_color(text, color="green"):
    """彩色输出文本"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    # Windows系统不支持ANSI颜色码
    if os.name == "nt":
        print(text)
    else:
        print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def open_github_actions():
    """打开GitHub Actions页面，让用户手动触发构建"""
    github_url = f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO_NAME}/actions"
    print_color(f"正在打开GitHub Actions页面: {github_url}")
    
    try:
        if os.name == 'nt':  # Windows
            os.startfile(github_url)
        elif os.name == 'posix':  # macOS或Linux
            subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', github_url])
        print_color("✓ 请在浏览器中手动触发GitHub Actions构建")
        print_color("请按照以下步骤操作：")
        print_color("1. 在Actions页面找到'Build Android APK'工作流")
        print_color("2. 点击'Run workflow'按钮")
        print_color("3. 再次点击'Run workflow'确认")
        print_color("构建过程将持续30-60分钟")
    except Exception as e:
        print_color(f"✗ 无法打开浏览器: {e}", "red")
        print_color(f"请手动访问: {github_url}", "yellow")

def wait_for_build_completion():
    """等待用户确认构建完成"""
    print_color("\n请在GitHub Actions构建完成后继续...", "yellow")
    print_color("构建完成后，您可以在Actions页面下载APK文件")
    input("请下载APK文件并按Enter键继续...")

def download_apk_manually():
    """指导用户手动下载APK并提供自动复制功能"""
    print_color("\n请将下载的APK文件（或ZIP压缩包）保存到以下位置:", "yellow")
    print_color(f"{DOWNLOAD_DIR}")
    input("保存完成后按Enter键继续...")
    
    # 查找下载的文件
    apk_files = []
    zip_files = []
    
    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith('.apk'):
            apk_files.append(os.path.join(DOWNLOAD_DIR, file))
        elif file.endswith('.zip'):
            zip_files.append(os.path.join(DOWNLOAD_DIR, file))
    
    return apk_files, zip_files

def extract_zip_files(zip_files):
    """解压ZIP文件并提取APK"""
    extracted_apks = []
    
    for zip_file in zip_files:
        print_color(f"正在解压: {os.path.basename(zip_file)}")
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # 提取所有文件到临时目录
                zip_ref.extractall(DOWNLOAD_DIR)
                # 查找提取的APK文件
                for root, _, files in os.walk(DOWNLOAD_DIR):
                    for file in files:
                        if file.endswith('.apk'):
                            apk_path = os.path.join(root, file)
                            extracted_apks.append(apk_path)
                            print_color(f"✓ 找到APK文件: {file}")
        except Exception as e:
            print_color(f"✗ 解压失败: {e}", "red")
    
    return extracted_apks

def copy_apk_to_app_folder(apk_files):
    """将APK文件复制到APP文件夹"""
    success_count = 0
    
    for apk_path in apk_files:
        apk_name = os.path.basename(apk_path)
        target_path = os.path.join(APP_FOLDER, apk_name)
        
        try:
            # 复制文件
            with open(apk_path, 'rb') as src_file:
                with open(target_path, 'wb') as dst_file:
                    dst_file.write(src_file.read())
            success_count += 1
            print_color(f"✓ 已复制: {apk_name} → {APP_FOLDER}")
        except Exception as e:
            print_color(f"✗ 复制失败 {apk_name}: {e}", "red")
    
    return success_count

def main():
    """主函数"""
    print_color("=" * 60)
    print_color("      APK自动下载与复制工具      ")
    print_color("=" * 60)
    print_color("本工具将指导您完成GitHub Actions构建和APK复制")
    print_color("=" * 60)
    
    # 第1步：打开GitHub Actions页面
    open_github_actions()
    
    # 第2步：等待构建完成
    wait_for_build_completion()
    
    # 第3步：手动下载APK
    apk_files, zip_files = download_apk_manually()
    
    # 第4步：解压ZIP文件
    if zip_files:
        extracted_apks = extract_zip_files(zip_files)
        apk_files.extend(extracted_apks)
    
    # 第5步：复制APK到APP文件夹
    if apk_files:
        print_color("\n正在复制APK文件到APP文件夹...")
        success_count = copy_apk_to_app_folder(apk_files)
        
        print_color("\n" + "=" * 60, "blue")
        print_color(f"      操作完成！      ", "blue")
        print_color("=" * 60, "blue")
        print_color(f"成功复制了 {success_count} 个APK文件到 {APP_FOLDER}", "green")
        print_color("您现在可以从APP文件夹中获取安装包了。", "green")
    else:
        print_color("\n✗ 未找到APK文件，请检查下载位置。", "red")
    
    print_color("\n按Enter键退出...")
    input()


if __name__ == "__main__":
    main()