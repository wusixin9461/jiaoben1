import os
import subprocess
import time
import sys
import shutil
import ctypes

# 确保中文显示正常
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def is_admin():
    """检查当前进程是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员权限重启程序"""
    print("需要管理员权限来执行某些操作...")
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        time.sleep(2)
        # 不立即退出，让用户有机会看到后续输出
    except Exception as e:
        print(f"以管理员权限运行时出错: {e}")

def find_android_studio_process():
    """检查Android Studio是否在运行"""
    try:
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq studio64.exe', '/NH'],
            capture_output=True,
            text=True
        )
        return 'studio64.exe' in result.stdout
    except Exception as e:
        print(f"检查Android Studio进程时出错: {e}")
        return False

def start_android_studio():
    """启动Android Studio并打开项目"""
    android_studio_path = "D:\\b1az\\bin\\studio64.exe"
    project_path = "E:\\#9#531\\2414\\android_project"
    
    print(f"正在启动Android Studio: {android_studio_path}")
    print(f"正在打开项目: {project_path}")
    
    try:
        subprocess.Popen([android_studio_path, project_path])
        print("Android Studio已启动，请等待项目加载完成...")
        print("请手动确认项目是否正确加载")
        time.sleep(10)  # 给Android Studio一些启动时间
        return True
    except Exception as e:
        print(f"启动Android Studio时出错: {e}")
        print("请手动启动Android Studio并打开项目")
        return False

def create_key_store_template():
    """创建密钥库模板文件"""
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keystore_template.txt")
    template_content = '''
=== 密钥库创建指南 ===

当您在Android Studio中创建新密钥库时，请使用以下信息作为参考：

密钥库路径建议: E:\\#9#531\\APP\\keystore.jks
密钥库密码: 请设置一个强密码并记住它
密钥别名: release
密钥密码: 建议与密钥库密码相同
有效期: 25年
组织单位: 2414
组织: PokeMMO自动化
城市: 城市名称
省/市: 省份名称
国家/地区代码: CN

重要提示:
- 请妥善保存您的密钥库文件和密码
- 丢失密钥将导致无法更新您的应用
- 建议备份密钥库文件到安全位置
'''
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"已创建密钥库模板: {template_path}")
    return template_path

def prepare_directories():
    """准备必要的目录结构"""
    # 确保APP文件夹存在
    app_folder = "E:\\#9#531\\APP"
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)
        print(f"已创建APP文件夹: {app_folder}")
    
    # 创建临时目录用于存放中间文件
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_apk")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        print(f"已创建临时目录: {temp_dir}")
    
    return app_folder, temp_dir

def show_export_instructions():
    """显示详细的APK导出步骤"""
    print("\n=== Android Studio APK导出详细指南 ===")
    print("1. 等待Android Studio完全加载项目")
    print("2. 点击顶部菜单栏的 'Build'")
    print("3. 选择 'Generate Signed Bundle / APK...'")
    print("4. 在弹出的窗口中:")
    print("   - 选择 'APK'")
    print("   - 点击 'Next'")
    print("5. 密钥库配置:")
    print("   - 如果没有密钥库，点击 'Create new...'")
    print("   - 请参考keystore_template.txt文件中的建议信息")
    print("   - 记住您设置的所有密码信息")
    print("6. 填写完密钥库信息后点击 'Next'")
    print("7. 选择构建选项:")
    print("   - Build Variants: 确保选择 'release'")
    print("   - Signature Versions: 同时勾选 'V1 (Jar Signature)' 和 'V2 (Full APK Signature)'")
    print("8. 点击 'Finish' 开始构建APK")
    print("9. 等待构建完成，这可能需要几分钟时间")
    print("10. 构建完成后，APK文件将自动被复制到 E:\\#9#531\\APP 文件夹")
    
    print("\n重要提示:")
    print("- 整个过程可能需要一些时间，请耐心等待")
    print("- 如果遇到构建错误，请检查Gradle配置和依赖项")
    print("- 请确保您的计算机有足够的内存和磁盘空间")

def create_auto_copy_script():
    """创建自动复制APK的脚本"""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auto_copy_apk_on_completion.bat")
    script_content = '''@echo off
cls
echo ===================================================
echo PokeMMO自动化 - APK自动复制脚本
===================================================
echo 此脚本将监控Android Studio的构建输出目录并自动复制APK文件

:CHECK_FOR_APK
python -c "
import os
import shutil
import time
import sys

def check_and_copy_apk():
    # 设置源目录和目标目录
    source_dir = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'android_project', 'app', 'build', 'outputs', 'apk', 'release')
    target_dir = 'E:\\#9#531\\APP'
    
    print('正在检查APK文件...')
    
    if not os.path.exists(source_dir):
        print(f'源目录不存在: {source_dir}')
        print('Android Studio可能尚未完成构建')
        return False
    
    apk_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.apk')]
    
    if not apk_files:
        print('未找到APK文件，请等待Android Studio完成构建')
        return False
    
    print(f'找到 {len(apk_files)} 个APK文件，开始复制...')
    
    copied = False
    for apk_file in apk_files:
        try:
            source_path = os.path.join(source_dir, apk_file)
            target_path = os.path.join(target_dir, apk_file)
            
            # 检查文件是否正在被写入
            try:
                with open(source_path, 'rb') as f:
                    pass
            except:
                print(f'文件 {apk_file} 正在被写入，请稍后再试')
                continue
            
            # 如果目标文件已存在，添加时间戳
            if os.path.exists(target_path):
                timestamp = time.strftime('_%%Y%%m%%d_%%H%%M%%S')
                name_without_ext = os.path.splitext(apk_file)[0]
                ext = os.path.splitext(apk_file)[1]
                target_path = os.path.join(target_dir, f'{name_without_ext}{timestamp}{ext}')
            
            shutil.copy2(source_path, target_path)
            print(f'✓ 已复制: {apk_file} -> {os.path.basename(target_path)}')
            copied = True
        except Exception as e:
            print(f'复制 {apk_file} 时出错: {e}')
    
    if copied:
        print(f'\nAPK文件已成功复制到: {target_dir}')
    
    return copied

if __name__ == '__main__':
    if check_and_copy_apk():
        sys.exit(0)
    else:
        sys.exit(1)
"

if %errorlevel% equ 0 (
    echo.
    echo ===================================================
    echo APK文件已成功复制到 E:\\#9#531\\APP 文件夹
    echo 操作完成！
    echo ===================================================
    pause
    exit
)

echo.
echo APK文件尚未生成，请继续等待Android Studio完成构建...
echo 10秒后再次尝试检查...
ping 127.0.0.1 -n 11 > nul
goto CHECK_FOR_APK
'''
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"已创建自动复制脚本: {script_path}")
    return script_path

def main():
    print("=== PokeMMO自动化 - 增强版APK导出助手 ===")
    print("正在准备导出环境...")
    
    # 检查并提升权限
    if not is_admin():
        print("建议以管理员权限运行此脚本以避免权限问题")
        print("请考虑手动以管理员身份运行命令提示符，然后执行此脚本")
        # 不再自动提升权限，避免中断流程
    
    # 准备目录结构
    prepare_directories()
    
    # 创建密钥库模板
    create_key_store_template()
    
    # 检查Android Studio是否在运行
    if not find_android_studio_process():
        print("未检测到Android Studio进程")
        if input("是否启动Android Studio？(y/n): ").lower() == 'y':
            start_android_studio()
        else:
            print("请手动启动Android Studio并打开项目")
    else:
        print("已检测到Android Studio正在运行")
    
    # 显示导出指南
    show_export_instructions()
    
    # 创建自动复制脚本
    copy_script = create_auto_copy_script()
    
    print("\n=== 操作准备就绪 ===")
    print("1. 请按照上述步骤在Android Studio中导出APK")
    print("2. 当您开始在Android Studio中构建APK后，请运行以下命令:")
    print(f"   {copy_script}")
    print("3. 该脚本将自动检测并复制生成的APK文件到E:\\#9#531\\APP文件夹")
    print("\n您也可以直接按任意键运行自动复制脚本，它会持续监控并在APK生成后自动复制")
    
    input("按任意键开始监控APK生成...")
    
    # 运行自动复制脚本
    print("\n正在启动自动复制监控脚本...")
    subprocess.run([copy_script], shell=True)
    
    print("\n所有操作已完成！")

if __name__ == "__main__":
    main()