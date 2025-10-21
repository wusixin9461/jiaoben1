
import os
import shutil
import time
import sys

# 确保中文显示正常
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def copy_apk_to_app_folder():
    # 设置源目录和目标目录 - 使用原始字符串避免转义问题
    source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "android_project", "app", "build", "outputs", "apk", "release")
    target_dir = r"E:\#9#531\APP"
    
    print(f"\n正在检查APK文件位置: {source_dir}")
    print(f"目标文件夹: {target_dir}")
    
    # 确保目标文件夹存在
    if not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir)
            print(f"已创建目标文件夹: {target_dir}")
        except Exception as e:
            print(f"创建目标文件夹时出错: {e}")
            print("请以管理员身份运行此脚本")
            return False
    
    # 检查源目录是否存在
    if not os.path.exists(source_dir):
        print(f"错误: APK源目录不存在: {source_dir}")
        print("请确保已在Android Studio中完成APK导出操作")
        print("导出步骤请参考 APK导出指南.md 文件")
        return False
    
    # 查找APK文件
    try:
        apk_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.apk')]
    except Exception as e:
        print(f"访问源目录时出错: {e}")
        print("请检查是否有足够权限访问此文件夹")
        return False
    
    if not apk_files:
        print(f"错误: 在 {source_dir} 目录中未找到APK文件")
        print("请确保已在Android Studio中完成APK导出操作")
        print("导出步骤请参考 APK导出指南.md 文件")
        return False
    
    print(f"找到 {len(apk_files)} 个APK文件，正在复制...")
    
    success_count = 0
    
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
            
            # 复制文件
            try:
                shutil.copy2(source_path, target_path)
                print(f"✓ 已成功复制: {apk_file} -> {os.path.basename(target_path)}")
                success_count += 1
            except Exception as e:
                print(f"✗ 复制 {apk_file} 时出错: {e}")
                print("请尝试以管理员身份运行此脚本")
        
        if success_count > 0:
            print(f"\n成功复制 {success_count} 个APK文件到: {target_dir}")
            print("\n您现在可以在APP文件夹中找到导出的APK安装包")
            return True
        else:
            print("\n所有APK文件复制失败")
            return False
            
    except Exception as e:
        print(f"执行过程中出错: {e}")
        return False

def main():
    print("=== PokeMMO自动化 - APK复制工具 ===")
    print("此工具将APK文件从Android Studio导出目录复制到指定文件夹")
    
    result = copy_apk_to_app_folder()
    
    print("\n操作完成!")
    print("按任意键退出...")
    input()

if __name__ == "__main__":
    main()
