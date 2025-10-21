@echo off
cls
echo ===================================================
echo PokeMMO自动化 - APK复制工具
echo ===================================================
echo 此脚本将把Android Studio导出的APK文件复制到E:\#9#531\APP文件夹

python -c "
import os
import shutil
import time
import sys

def copy_apk_to_app_folder():
    # 设置源目录和目标目录
    source_dir = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'android_project', 'app', 'build', 'outputs', 'apk', 'release')
    target_dir = 'E:\\#9#531\\APP'
    
    print(f'\n正在检查APK文件位置: {source_dir}')
    
    if not os.path.exists(source_dir):
        print(f'错误: APK源目录不存在: {source_dir}')
        print('请确保已在Android Studio中完成APK导出操作')
        return False
    
    # 查找所有APK文件
    apk_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.apk')]
    
    if not apk_files:
        print(f'错误: 在 {source_dir} 目录中未找到APK文件')
        print('请确保已在Android Studio中完成APK导出操作')
        return False
    
    print(f'找到 {len(apk_files)} 个APK文件，正在复制到APP文件夹...')
    
    try:
        for apk_file in apk_files:
            source_path = os.path.join(source_dir, apk_file)
            target_path = os.path.join(target_dir, apk_file)
            
            # 如果目标文件已存在，添加时间戳以避免覆盖
            if os.path.exists(target_path):
                timestamp = time.strftime('_%Y%m%d_%H%M%S')
                name_without_ext = os.path.splitext(apk_file)[0]
                ext = os.path.splitext(apk_file)[1]
                target_path = os.path.join(target_dir, f'{name_without_ext}{timestamp}{ext}')
            
            shutil.copy2(source_path, target_path)
            print(f'✓ 已复制: {apk_file} -> {os.path.basename(target_path)}')
        
        print(f'\n所有APK文件已成功复制到: {target_dir}')
        return True
    except Exception as e:
        print(f'复制APK文件时出错: {e}')
        return False

# 执行复制操作
if copy_apk_to_app_folder():
    sys.exit(0)
else:
    sys.exit(1)
"

if %errorlevel% equ 0 (
    echo.
    echo ===================================================
    echo 复制完成！您可以在 E:\#9#531\APP 文件夹中找到您的APK文件
    echo ===================================================
) else (
    echo.
    echo ===================================================
    echo 复制过程中出现错误，请检查上面的错误信息
    echo ===================================================
)

pause