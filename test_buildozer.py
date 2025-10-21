import os
import sys
import subprocess
import time

# 确保中文显示正常
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def run_command(command, description):
    """运行命令并显示输出"""
    print(f"\n{description}")
    print(f"正在执行: {command}")
    
    try:
        # 使用shell=True来执行命令
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 实时显示输出
        while True:
            stdout_line = process.stdout.readline()
            stderr_line = process.stderr.readline()
            
            if stdout_line:
                print(stdout_line.strip())
            if stderr_line:
                print(f"错误: {stderr_line.strip()}")
            
            # 检查进程是否结束
            if process.poll() is not None:
                # 读取剩余输出
                for line in process.stdout:
                    print(line.strip())
                for line in process.stderr:
                    print(f"错误: {line.strip()}")
                break
            
            # 短暂休眠避免CPU占用过高
            time.sleep(0.1)
        
        return process.returncode
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return -1

def main():
    print("=== PokeMMO自动化 - Buildozer构建测试 ===")
    
    # 检查当前目录
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 检查buildozer是否安装
    print("\n检查Buildozer安装状态...")
    ret = run_command("buildozer --version", "显示Buildozer版本")
    
    if ret != 0:
        print("\n警告: Buildozer可能未正确安装或无法运行")
        print("在Windows上运行Buildozer可能需要特殊配置")
        print("推荐使用Linux环境或云服务进行Buildozer构建")
    
    # 检查buildozer.spec文件
    if os.path.exists("buildozer.spec"):
        print("\n找到buildozer.spec文件")
        # 显示文件开头内容
        with open("buildozer.spec", "r", encoding="utf-8") as f:
            print("配置文件前几行:")
            for i, line in enumerate(f):
                if i < 10:  # 只显示前10行
                    print(line.strip())
                else:
                    break
    else:
        print("\n未找到buildozer.spec文件")
    
    print("\n=== 构建选项 ===")
    print("1. 尝试使用buildozer构建调试版本")
    print("2. 显示云服务构建指南")
    print("3. 退出")
    
    choice = input("\n请选择操作 (1-3): ")
    
    if choice == "1":
        print("\n警告: 在Windows上直接使用buildozer可能会失败")
        print("Buildozer官方推荐在Linux环境中运行")
        confirm = input("确定要继续吗? (y/n): ")
        
        if confirm.lower() == "y":
            print("\n开始尝试构建...")
            print("注意: 这可能会失败，这是预期的行为")
            run_command("buildozer android debug", "执行buildozer android debug")
            print("\n构建尝试完成")
            print("由于Windows环境限制，buildozer构建可能失败")
            print("建议查看'云服务打包指南.md'使用在线构建服务")
    
    elif choice == "2":
        print("\n显示云服务构建指南...")
        if os.path.exists("云服务打包指南.md"):
            print("请查看 '云服务打包指南.md' 文件获取详细说明")
            print("该指南包含Google Colab和GitHub Actions的免费打包方案")
        else:
            print("未找到 '云服务打包指南.md' 文件")
    
    print("\n操作完成!")

if __name__ == "__main__":
    main()