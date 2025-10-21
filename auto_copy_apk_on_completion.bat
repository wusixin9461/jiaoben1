@echo off
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
    target_dir = 'E:\#9#531\APP'
    
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
        print(f'
APK文件已成功复制到: {target_dir}')
    
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
    echo APK文件已成功复制到 E:\#9#531\APP 文件夹
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
