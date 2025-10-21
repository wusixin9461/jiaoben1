@echo off
cls
echo 正在准备上传项目到GitHub...
echo 请确保您已在GitHub上创建了仓库并安装了Git
echo.

set /p username="请输入您的GitHub用户名: "
set /p repo_name="请输入您的仓库名称 (默认为pokemmo-automation): "

if "%repo_name%" == "" set repo_name=pokemmo-automation

echo.
echo 正在初始化Git仓库...
git init
if errorlevel 1 (
    echo 错误: Git初始化失败，请确保Git已正确安装
    pause
    exit /b 1
)

echo 正在添加文件...
git add .
echo 正在创建提交...
git commit -m "首次提交 - PokeMMO自动化项目"
echo 正在设置分支...
git branch -M main
echo 正在添加远程仓库...
git remote add origin https://github.com/%username%/%repo_name%.git
echo 正在推送代码...
git push -u origin main

if errorlevel 1 (
    echo.
    echo 错误: 推送失败，请检查您的GitHub用户名和仓库名称是否正确
    echo 或者您可能需要先在GitHub上创建仓库
    echo 请手动执行以上步骤或重试
    pause
    exit /b 1
)

echo.
echo 上传成功！请在GitHub上的Actions标签页触发构建
pause
