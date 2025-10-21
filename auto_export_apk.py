import os
import subprocess
import time
import sys
import shutil

def find_android_studio_process():
    """检查Android Studio是否在运行"""
    try:
        # 使用tasklist命令检查Android Studio进程
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq studio64.exe', '/NH'],
            capture_output=True,
            text=True
        )
        return 'studio64.exe' in result.stdout
    except Exception as e:
        print(f"检查Android Studio进程时出错: {e}")
        return False

def activate_android_studio():
    """激活已打开的Android Studio窗口"""
    print("正在尝试激活Android Studio窗口...")
    try:
        # 使用PowerShell命令激活窗口
        ps_command = '''
        $app = Get-Process | Where-Object {$_.ProcessName -eq 'studio64'} | Select-Object -First 1
        if ($app) {
            [Microsoft.VisualBasic.Interaction]::AppActivate($app.MainWindowTitle)
            Write-Host "Android Studio窗口已激活"
        } else {
            Write-Host "未找到Android Studio窗口"
        }
        '''
        subprocess.run([
            'powershell', '-Command', ps_command
        ])
        return True
    except Exception as e:
        print(f"激活Android Studio窗口时出错: {e}")
        return False

def copy_apk_to_app_folder():
    """将导出的APK文件复制到APP文件夹"""
    source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "android_project", "app", "build", "outputs", "apk", "release")
    target_dir = "E:\\#9#531\\APP"
    
    print(f"\n正在检查APK文件位置: {source_dir}")
    
    if not os.path.exists(source_dir):
        print(f"警告: APK源目录不存在: {source_dir}")
        print("请先完成Android Studio中的APK导出操作")
        return False
    
    apk_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.apk')]
    
    if not apk_files:
        print(f"警告: 在 {source_dir} 目录中未找到APK文件")
        print("请先完成Android Studio中的APK导出操作")
        return False
    
    print(f"找到 {len(apk_files)} 个APK文件，正在复制到APP文件夹...")
    
    try:
        for apk_file in apk_files:
            source_path = os.path.join(source_dir, apk_file)
            target_path = os.path.join(target_dir, apk_file)
            
            # 如果目标文件已存在，添加时间戳
            if os.path.exists(target_path):
                timestamp = time.strftime("_%Y%m%d_%H%M%S")
                name_without_ext = os.path.splitext(apk_file)[0]
                ext = os.path.splitext(apk_file)[1]
                target_path = os.path.join(target_dir, f"{name_without_ext}{timestamp}{ext}")
            
            shutil.copy2(source_path, target_path)
            print(f"✓ 已复制: {apk_file} -> {os.path.basename(target_path)}")
        
        print(f"\n所有APK文件已成功复制到: {target_dir}")
        return True
    except Exception as e:
        print(f"复制APK文件时出错: {e}")
        return False

def prepare_export_commands():
    """准备导出APK的命令和说明"""
    print("\n=== Android Studio APK导出步骤 ===")
    print("1. 在已激活的Android Studio窗口中:")
    print("   - 点击顶部菜单栏的 'Build'")
    print("   - 选择 'Generate Signed Bundle / APK...'")
    print("2. 在弹出的窗口中:")
    print("   - 选择 'APK'")
    print("   - 点击 'Next'")
    print("3. 配置密钥库:")
    print("   - 如果有现有密钥库，选择 'Choose existing...'")
    print("   - 如果没有，选择 'Create new...' 创建新密钥库")
    print("4. 填写密钥信息:")
    print("   - 密钥库路径: 选择保存位置")
    print("   - 密钥库密码: 设置安全密码")
    print("   - 密钥别名: 例如 'release'")
    print("   - 密钥密码: 与密钥库密码相同或设置新密码")
    print("   - 有效期: 推荐25年")
    print("5. 点击 'Next' 后选择:")
    print("   - Build Variants: 选择 'release'")
    print("   - Signature Versions: 勾选 'V1 (Jar Signature)' 和 'V2 (Full APK Signature)'")
    print("6. 点击 'Finish' 开始构建APK")
    print("\nAPK文件将生成在项目的 'app\\build\\outputs\\apk\\release' 目录中")
    print("然后将自动复制到: E:\\#9#531\\APP 文件夹中")

def create_adb_install_script():
    """创建ADB安装脚本"""
    adb_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "install_apk.bat")
    script_content = '''
@echo off
cls
echo ===================================================
echo PokeMMO自动化 - APK安装脚本
echo ===================================================

echo 请确保您的Android设备已连接并启用USB调试模式
echo 按任意键开始安装...
pause

REM 检查ADB是否可用
adb version
if %errorlevel% neq 0 (
    echo 错误: 未找到ADB。请确保Android SDK已正确安装。
    echo 或者在以下提示中输入APK文件的完整路径。
)

set APK_PATH=
set /p APK_PATH=请输入APK文件路径（默认为app-release.apk）: 

if "%APK_PATH%"=="" (
    set APK_PATH=app-release.apk
)

echo 正在安装 %APK_PATH%
adb install -r "%APK_PATH%"

if %errorlevel% equ 0 (
    echo 安装成功！
    echo 正在启动应用...
    adb shell monkey -p com.example.pokemmoautomation 1
) else (
    echo 安装失败。请检查设备连接和APK文件。
)

pause
'''
    
    with open(adb_script_path, 'w') as f:
        f.write(script_content)
    
    print(f"\n已创建APK安装脚本: {adb_script_path}")
    return adb_script_path

def main():
    print("=== PokeMMO自动化 - APK导出助手 ===")
    
    # 检查Android Studio是否正在运行
    if not find_android_studio_process():
        print("警告: 未检测到Android Studio进程。请确保它已启动。")
    else:
        print("已检测到Android Studio正在运行。")
    
    # 激活Android Studio窗口
    activate_android_studio()
    
    # 显示导出步骤
    prepare_export_commands()
    
    # 创建ADB安装脚本
    create_adb_install_script()
    
    print("\n=== 完成 ===")
    print("1. 按照上述步骤在Android Studio中导出APK")
    print("2. 导出完成后，可以使用生成的install_apk.bat脚本快速安装到设备")
    print("\n提示: 如果遇到权限问题，请以管理员身份运行命令提示符或PowerShell")
    
    # 尝试设置权限（Windows环境中通常不需要特殊权限）
    print("正在设置必要的权限...")
    try:
        # 确保脚本可执行
        subprocess.run(['powershell', '-Command', 'Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force'])
        print("权限设置完成")
    except Exception as e:
        print(f"设置权限时出现警告: {e}")
    
    # 询问用户是否已完成APK导出
    print("\n=== APK复制功能 ===")
    user_input = input("您是否已经完成了Android Studio中的APK导出操作？(y/n): ")
    
    if user_input.lower() == 'y':
        copy_apk_to_app_folder()
    else:
        print("请先在Android Studio中完成APK导出操作，然后可以重新运行此脚本进行复制")
    
    print("\n现在您可以在已激活的Android Studio窗口中继续操作了")

if __name__ == "__main__":
    main()