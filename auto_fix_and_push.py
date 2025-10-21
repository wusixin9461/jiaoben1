#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动修复和推送脚本
用于自动设置Git配置并推送更改到GitHub仓库
"""

import os
import subprocess
import sys
import time

# 定义颜色常量用于输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# 执行命令并返回结果
def run_command(command, cwd=None, timeout=30):
    """执行命令并返回结果"""
    try:
        print(f"{Colors.OKBLUE}执行: {command}{Colors.ENDC}")
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            timeout=timeout
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"{Colors.FAIL}命令执行超时: {command}{Colors.ENDC}")
        return None
    except Exception as e:
        print(f"{Colors.FAIL}命令执行失败: {e}{Colors.ENDC}")
        return None

# 重试函数
def retry(func, max_retries=3, delay=5):
    """重试执行函数"""
    retries = 0
    while retries < max_retries:
        result = func()
        if result is not None and result.returncode == 0:
            return result
        retries += 1
        print(f"{Colors.WARNING}第{retries}次重试...{Colors.ENDC}")
        time.sleep(delay)
    return None

# 主函数
def main():
    # 1. 设置Git配置为HTTP/1.1
    print(f"\n{Colors.HEADER}=== 步骤1: 设置Git配置 ==={Colors.ENDC}")
    config_cmd = "git config --global http.version HTTP/1.1"
    config_result = run_command(config_cmd)
    if config_result and config_result.returncode == 0:
        print(f"{Colors.OKGREEN}✓ Git HTTP版本设置成功{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}✗ Git HTTP版本设置失败{Colors.ENDC}")
        # 继续执行，不在这里中断
    
    # 2. 设置连接超时
    print(f"\n{Colors.HEADER}=== 步骤2: 设置Git超时配置 ==={Colors.ENDC}")
    timeout_cmd = "git config --global http.postBuffer 524288000"
    timeout_result = run_command(timeout_cmd)
    if timeout_result and timeout_result.returncode == 0:
        print(f"{Colors.OKGREEN}✓ Git postBuffer设置成功{Colors.ENDC}")
    
    # 3. 尝试推送更改
    print(f"\n{Colors.HEADER}=== 步骤3: 推送更改到GitHub ==={Colors.ENDC}")
    push_cmd = "git push -u origin main"
    
    def push_func():
        return run_command(push_cmd, timeout=60)
    
    push_result = retry(push_func, max_retries=3, delay=10)
    
    if push_result and push_result.returncode == 0:
        print(f"\n{Colors.OKGREEN}🎉 推送成功！{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✓ 更改已成功推送到GitHub仓库{Colors.ENDC}")
        
        # 4. 提示用户下一步操作
        print(f"\n{Colors.HEADER}=== 下一步操作 ==={Colors.ENDC}")
        print(f"1. 打开GitHub仓库页面: https://github.com/wusixin9461/jiaoben1.git")
        print(f"2. 点击顶部的 'Actions' 标签")
        print(f"3. 找到 'Build Android APK' workflow")
        print(f"4. 点击 'Run workflow' 按钮")
        print(f"5. 等待构建完成，下载APK文件")
        print(f"\n{Colors.WARNING}注意: APK文件将保存在 E:\\#9#531\\APP 文件夹中{Colors.ENDC}")
        
        return True
    else:
        print(f"\n{Colors.FAIL}✗ 推送失败！{Colors.ENDC}")
        print(f"{Colors.WARNING}可能的原因: {Colors.ENDC}")
        print(f"1. 网络连接问题")
        print(f"2. GitHub服务器暂时不可用")
        print(f"3. 仓库权限问题")
        
        # 提供更多诊断信息
        print(f"\n{Colors.HEADER}=== 诊断信息 ==={Colors.ENDC}")
        # 检查仓库状态
        status_cmd = "git status"
        status_result = run_command(status_cmd)
        if status_result:
            print(f"{Colors.OKBLUE}Git状态:{Colors.ENDC}")
            print(status_result.stdout)
        
        # 检查远程配置
        remote_cmd = "git remote -v"
        remote_result = run_command(remote_cmd)
        if remote_result:
            print(f"{Colors.OKBLUE}远程仓库配置:{Colors.ENDC}")
            print(remote_result.stdout)
        
        return False

# 自动启动APK下载工具
def start_apk_tool():
    """启动APK下载和复制工具"""
    try:
        apk_tool_path = os.path.join(os.getcwd(), "auto_download_and_copy_apk.py")
        if os.path.exists(apk_tool_path):
            print(f"\n{Colors.HEADER}=== 启动APK下载和复制工具 ==={Colors.ENDC}")
            subprocess.Popen([sys.executable, apk_tool_path])
            print(f"{Colors.OKGREEN}✓ APK下载工具已启动{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}✗ 无法启动APK下载工具: {e}{Colors.ENDC}")

if __name__ == "__main__":
    print(f"{Colors.BOLD}PokeMMO自动化 - 自动修复和推送工具{Colors.ENDC}")
    print("=" * 50)
    
    success = main()
    
    # 无论推送是否成功，都启动APK工具
    start_apk_tool()
    
    print(f"\n{Colors.OKBLUE}按Enter键退出...{Colors.ENDC}")
    input()