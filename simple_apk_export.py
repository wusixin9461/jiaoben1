import os
import subprocess
import time
import sys
import shutil

# 确保中文显示正常
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def start_android_studio():
    """启动Android Studio并打开项目"""
    print("\n正在准备启动Android Studio...")
    
    # 定义Android Studio路径和项目路径
    android_studio_path = "D:\\b1az\\bin\\studio64.exe"
    project_path = "E:\\#9#531\\2414\\android_project"
    
    print(f"Android Studio路径: {android_studio_path}")
    print(f"项目路径: {project_path}")
    
    # 检查Android Studio是否存在
    if not os.path.exists(android_studio_path):
        print(f"错误: 找不到Android Studio: {android_studio_path}")
        print("请手动启动Android Studio并打开项目")
        return False
    
    # 检查项目文件夹是否存在
    if not os.path.exists(project_path):
        print(f"错误: 找不到项目文件夹: {project_path}")
        print("请检查项目路径是否正确")
        return False
    
    try:
        print("正在启动Android Studio...")
        # 启动Android Studio并打开项目
        subprocess.Popen([android_studio_path, project_path])
        print("Android Studio已启动，请等待项目加载完成")
        print("这可能需要几分钟时间")
        
        # 等待一段时间让Android Studio启动
        print("\n请确认Android Studio是否已成功启动")
        return True
    except Exception as e:
        print(f"启动Android Studio时出错: {e}")
        print("请手动启动Android Studio并打开项目")
        return False

def create_detailed_guide():
    """创建详细的APK导出指南"""
    guide_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apk_export_guide.txt")
    guide_content = '''
=====================================================
              POKEMMO自动化 - APK导出指南
=====================================================

一、准备工作
------------------------------------------
1. 确保Android Studio已成功启动并加载项目
2. 确保项目构建没有错误
3. 确保您有足够的磁盘空间

二、导出APK步骤
------------------------------------------
1. 在Android Studio顶部菜单栏中，点击 "Build"
2. 从下拉菜单中选择 "Generate Signed Bundle / APK..."
3. 在弹出的对话框中：
   - 选择 "APK"
   - 点击 "Next"

三、创建或使用密钥库
------------------------------------------
1. 如果您没有密钥库（第一次导出）：
   - 点击 "Create new..."
   - 密钥库路径建议：E:\#9#531\APP\keystore.jks
   - 密钥库密码：设置一个安全的密码并记住它
   - 密钥别名：建议使用 "release"
   - 密钥密码：可以与密钥库密码相同
   - 有效期：建议设置为25年
   - 其他信息：填写相关组织和地区信息

2. 如果您已有密钥库：
   - 点击 "Choose existing..."
   - 浏览并选择您的密钥库文件
   - 输入密钥库密码和密钥密码

四、选择构建选项
------------------------------------------
1. 在 "Build Variants" 部分，确保选择 "release"
2. 在 "Signature Versions" 部分：
   - 同时勾选 "V1 (Jar Signature)" 和 "V2 (Full APK Signature)"
3. 点击 "Finish" 开始构建APK

五、等待构建完成
------------------------------------------
- 构建过程可能需要几分钟时间
- 您可以在Android Studio底部的状态栏查看构建进度
- 构建成功后，会显示一个通知

六、复制APK文件
------------------------------------------
构建完成后，请运行以下命令将APK复制到APP文件夹：

1. 打开命令提示符
2. 导航到项目目录：cd E:\#9#531\2414
3. 运行：python -m copy_apk_to_app

或者直接双击运行：copy_apk_to_app.bat

=====================================================
                   重要提示
=====================================================
- 请妥善保存您的密钥库文件和密码
- 丢失密钥将导致无法更新您的应用
- 建议定期备份密钥库文件
- 导出的APK文件最终将保存在：E:\#9#531\APP\
'''
    
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"\n已创建详细导出指南: {guide_path}")
    return guide_path

def create_immediate_copy_script():
    """创建一个立即运行的APK复制脚本"""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "copy_apk_now.py")
    script_content = '''
import os
import shutil
import time
import sys

# 确保中文显示正常
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def copy_apk_to_app_folder():
    # 设置源目录和目标目录
    source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "android_project", "app", "build", "outputs", "apk", "release")
    target_dir = "E:\\#9#531\\APP"
    
    print(f"\n正在检查APK文件位置: {source_dir}")
    print(f"目标文件夹: {target_dir}")
    
    # 确保目标文件夹存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"已创建目标文件夹: {target_dir}")
    
    # 检查源目录是否存在
    if not os.path.exists(source_dir):
        print(f"错误: APK源目录不存在: {source_dir}")
        print("请确保已在Android Studio中完成APK导出操作")
        print("导出步骤请参考 apk_export_guide.txt 文件")
        return False
    
    # 查找APK文件
    apk_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.apk')]
    
    if not apk_files:
        print(f"错误: 在 {source_dir} 目录中未找到APK文件")
        print("请确保已在Android Studio中完成APK导出操作")
        print("导出步骤请参考 apk_export_guide.txt 文件")
        return False
    
    print(f"找到 {len(apk_files)} 个APK文件，正在复制...")
    
    try:
        for apk_file in apk_files:
            source_path = os.path.join(source_dir, apk_file)
            target_path = os.path.join(target_dir, apk_file)
            
            # 检查文件是否可访问
            try:
                with open(source_path, 'rb') as f:
                    pass
            except Exception as e:
                print(f"警告: 无法访问文件 {apk_file}: {e}")
                print("文件可能正在被写入，请稍后再试")
                continue
            
            # 如果目标文件已存在，添加时间戳
            if os.path.exists(target_path):
                timestamp = time.strftime("_%Y%m%d_%H%M%S")
                name_without_ext = os.path.splitext(apk_file)[0]
                ext = os.path.splitext(apk_file)[1]
                target_path = os.path.join(target_dir, f"{name_without_ext}{timestamp}{ext}")
            
            # 复制文件
            shutil.copy2(source_path, target_path)
            print(f"✓ 已成功复制: {apk_file} -> {os.path.basename(target_path)}")
        
        print(f"\n所有APK文件已成功复制到: {target_dir}")
        print("\n您现在可以在APP文件夹中找到导出的APK安装包")
        return True
    except Exception as e:
        print(f"复制APK文件时出错: {e}")
        print("请尝试以管理员身份运行此脚本")
        return False

if __name__ == "__main__":
    print("=== PokeMMO自动化 - APK复制工具 ===")
    copy_apk_to_app_folder()
    print("\n按任意键退出...")
    input()
'''
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"已创建APK复制工具: {script_path}")
    return script_path

def main():
    print("=== PokeMMO自动化 - APK导出助手 ===")
    print("此工具将帮助您通过Android Studio导出APK并复制到指定文件夹")
    
    # 创建详细指南
    guide_path = create_detailed_guide()
    
    # 创建复制工具
    copy_script_path = create_immediate_copy_script()
    
    # 启动Android Studio
    android_studio_started = start_android_studio()
    
    print("\n=== 操作步骤总结 ===")
    print("1. 请等待Android Studio完全加载项目")
    print("2. 按照 'apk_export_guide.txt' 中的详细步骤导出APK")
    print("3. 导出完成后，运行 'copy_apk_now.py' 将APK复制到APP文件夹")
    
    if android_studio_started:
        print("\nAndroid Studio已启动，请按照指南操作")
    else:
        print("\n请手动启动Android Studio并按照指南操作")
    
    print("\nAPK导出完成后，您的安装包将保存在: E:\\#9#531\\APP\\")
    print("\n操作完成！")
    
    # 提示用户是否现在就运行复制工具（用于已导出的情况）
    user_input = input("\n如果您已经完成了APK导出，是否现在就运行复制工具？(y/n): ")
    if user_input.lower() == 'y':
        print("\n正在运行APK复制工具...")
        subprocess.run([sys.executable, copy_script_path])

if __name__ == "__main__":
    main()