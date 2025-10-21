# PokeMMO自动化 - 完全免费的Android打包方案

本文档提供了几种完全免费的方法，将Python/Kivy应用打包为Android APK文件，无需购买任何软件或服务。

## 方案一：使用Docker（推荐初学者）

Docker是最推荐的方法，因为它避免了复杂的环境配置问题。

### 步骤：

1. **安装Docker Desktop**（完全免费）
   - 访问官网：https://www.docker.com/products/docker-desktop
   - 下载并安装适合您系统的版本
   - 安装完成后启动Docker Desktop

2. **打开命令行工具**
   - Windows: 打开PowerShell或命令提示符
   - 进入项目文件夹：
     ```
     cd e:\#9#531\计算机应用技术2414吴思鑫
     ```

3. **运行Docker打包命令**：
   ```
   docker run --rm -v ${PWD}:/home/user/hostcwd -w /home/user/hostcwd kivy/buildozer:latest buildozer -v android debug
   ```

4. **等待打包完成**
   - 首次打包会下载大量依赖，可能需要30分钟到几小时
   - 请确保网络稳定

5. **获取APK文件**
   - 打包成功后，APK文件将位于项目目录下的`bin`文件夹中
   - 文件名为`pokemmo自动化-0.1-debug.apk`

## 方案二：使用Google Colab（免费云服务）

如果您的电脑性能不足或不想安装Docker，可以使用Google Colab的免费云资源。

### 步骤：

1. **准备文件**
   - 确保项目文件夹包含以下文件：
     - `pokemmo_automation_android.py`
     - `buildozer.spec`
     - `requirements_kivy.txt`

2. **上传文件到Google Drive**
   - 将整个项目文件夹上传到您的Google Drive

3. **打开Google Colab**
   - 访问：https://colab.research.google.com/
   - 创建一个新的笔记本

4. **运行以下代码**（每个代码块单独运行）：

   **挂载Google Drive**：
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

   **进入项目文件夹**：
   ```python
   %cd /content/drive/MyDrive/[您的项目文件夹路径]
   ```

   **安装必要工具**：
   ```python
   !pip install buildozer
   !apt-get update
   !apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   ```

   **初始化Buildozer环境**：
   ```python
   !buildozer init
   ```

   **开始打包**：
   ```python
   !buildozer -v android debug
   ```

5. **下载APK**
   - 打包完成后，在左侧文件浏览器中找到`bin`文件夹
   - 右键点击APK文件，选择"下载"

## 方案三：使用GitHub Actions（自动化打包）

如果您熟悉Git和GitHub，可以使用免费的GitHub Actions服务进行自动化打包。

### 步骤：

1. **创建GitHub账户**（如果没有）
   - 访问：https://github.com/join
   - 注册一个免费账户

2. **创建新仓库**
   - 在GitHub上创建一个新的公共仓库
   - 名称可以是"pokemmo-automation-android"

3. **上传项目文件**
   - 使用Git上传您的项目文件，或直接在GitHub网页界面上传
   - 确保上传以下文件：
     - `pokemmo_automation_android.py`
     - `buildozer.spec`
     - `requirements_kivy.txt`

4. **创建GitHub Actions工作流文件**
   - 在仓库中创建`.github/workflows/build-apk.yml`文件
   - 内容如下：

```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # 允许手动触发

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

    - name: Initialize Buildozer
      run: buildozer init

    - name: Build APK
      run: buildozer -v android debug

    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: pokemmo-automation-apk
        path: bin/*.apk
```

5. **触发构建**
   - 提交工作流文件后，GitHub Actions会自动开始构建
   - 您也可以在Actions标签页手动触发构建

6. **下载APK**
   - 构建完成后，在Actions标签页找到对应的运行
   - 下载"Artifacts"中的APK文件

## 方案四：使用Termux（直接在Android设备上打包）

如果您想在Android设备上直接打包，可以使用Termux应用。

### 步骤：

1. **安装Termux**
   - 从F-Droid下载安装Termux：https://f-droid.org/packages/com.termux/
   - 不要从Google Play下载，那里的版本已不再维护

2. **设置Termux**
   ```bash
   pkg update && pkg upgrade -y
   pkg install -y git python openjdk-17 autoconf libtool pkg-config zlib ncurses cmake libffi openssl
   pip install --upgrade pip
   pip install buildozer
   ```

3. **克隆或复制项目文件**
   - 可以使用git克隆或通过文件共享应用复制文件

4. **运行打包命令**
   ```bash
   cd 项目目录
   buildozer -v android debug
   ```

## 打包注意事项

1. **所有方案都是完全免费的**
   - Docker Desktop免费版对个人用户完全免费
   - Google Colab提供免费计算资源（有限制但足够打包）
   - GitHub Actions对公共仓库提供免费CI/CD服务
   - Termux完全免费

2. **首次打包时间较长**
   - 所有方法的首次打包都会下载大量依赖
   - 请耐心等待并确保网络稳定

3. **内存和存储空间**
   - 确保有足够的磁盘空间（至少10GB）
   - Docker需要分配足够的内存（推荐至少4GB）

4. **常见问题解决**
   - 网络超时：尝试更换网络或使用代理
   - 内存不足：在Docker Desktop中增加分配的内存
   - 依赖错误：确保requirements_kivy.txt中的版本正确

## 后续使用

1. **安装APK到手机**
   - 将生成的APK文件传输到您的Android设备
   - 在设置中允许"安装未知来源的应用"
   - 点击APK文件进行安装

2. **运行应用**
   - 安装完成后，在应用列表中找到"pokemmo自动化"
   - 点击打开并按照界面提示使用

3. **保留源代码**
   - 所有方法都不会删除您的源代码
   - 您可以随时修改代码并重新打包