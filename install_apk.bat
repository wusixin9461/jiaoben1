
@echo off
cls
echo ===================================================
echo PokeMMO�Զ��� - APK��װ�ű�
echo ===================================================

echo ��ȷ������Android�豸�����Ӳ�����USB����ģʽ
echo ���������ʼ��װ...
pause

REM ���ADB�Ƿ����
adb version
if %errorlevel% neq 0 (
    echo ����: δ�ҵ�ADB����ȷ��Android SDK����ȷ��װ��
    echo ������������ʾ������APK�ļ�������·����
)

set APK_PATH=
set /p APK_PATH=������APK�ļ�·����Ĭ��Ϊapp-release.apk��: 

if "%APK_PATH%"=="" (
    set APK_PATH=app-release.apk
)

echo ���ڰ�װ %APK_PATH%
adb install -r "%APK_PATH%"

if %errorlevel% equ 0 (
    echo ��װ�ɹ���
    echo ��������Ӧ��...
    adb shell monkey -p com.example.pokemmoautomation 1
) else (
    echo ��װʧ�ܡ������豸���Ӻ�APK�ļ���
)

pause
