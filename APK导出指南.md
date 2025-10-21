# POKEMMO自动化 - APK导出与安装包管理指南

## 一、导出APK步骤

### 1. 启动Android Studio
- 打开您的Android Studio（请使用您电脑上已安装的Android Studio）
- 通过 "File > Open" 打开项目文件夹：`E:\#9#531\2414\android_project`

### 2. 导出APK文件
1. 在Android Studio顶部菜单栏中，点击 "Build"
2. 从下拉菜单中选择 "Generate App Bundles or APKs"（根据您的Android Studio版本，可能显示为"Generate Signed Bundle / APK..."）
3. 在弹出的对话框中：
   - 选择 "APK"
   - 点击 "Next"

### 3. 密钥库配置
1. **首次导出**:
   - 点击 "Create new..."
   - 密钥库路径：`E:\#9#531\APP\keystore.jks`
   - 设置密钥库密码（请记住这个密码）
   - 密钥别名：`release`
   - 密钥密码：可以与密钥库密码相同
   - 有效期：建议设置为25年
   - 填写其他必要信息

2. **已有密钥库**:
   - 点击 "Choose existing..."
   - 选择您现有的密钥库文件
   - 输入密钥库密码和密钥密码

### 4. 构建选项
- 在 "Build Variants" 部分，选择 "release"
- 在 "Signature Versions" 部分，同时勾选 "V1 (Jar Signature)" 和 "V2 (Full APK Signature)"
- 点击 "Finish" 开始构建

### 5. 等待构建完成
- 构建过程可能需要几分钟
- 构建成功后，Android Studio会显示通知

## 二、安装包管理

### 1. 自动复制APK到指定文件夹
- APK导出完成后，运行以下命令将APK自动复制到`E:\#9#531\APP\`文件夹：

```
python "E:\#9#531\2414\copy_apk_now.py"
```

或者直接双击运行：`E:\#9#531\2414\copy_apk_to_app.bat`

### 2. 手动查找APK文件
- 如果自动复制失败，您可以手动查找APK文件
- APK文件默认位置：`E:\#9#531\2414\android_project\app\build\outputs\apk\release\`
- 请手动将找到的APK文件复制到`E:\#9#531\APP\`文件夹

## 三、重要提示

1. **密钥库管理**:
   - 请妥善保存密钥库文件和密码
   - 丢失密钥将导致无法更新应用
   - 建议定期备份密钥库文件

2. **权限问题**:
   - 如果遇到访问权限错误，请尝试以管理员身份运行复制脚本

3. **安装到设备**:
   - 复制到`E:\#9#531\APP\`文件夹后，您可以通过各种方式将APK安装到Android设备

## 四、常见导出问题解决方案

### 1. 导出功能异常解决办法

#### 1.1 菜单选项不一致
- 如果您看到的是"Generate App Bundles or APKs"而不是"Generate Signed Bundle / APK..."，这是正常的，不同Android Studio版本的菜单项名称可能略有不同
- 请直接点击"Generate App Bundles or APKs"继续操作

#### 1.2 导出过程中出现错误
- **Gradle同步错误**：点击"Sync Project with Gradle Files"按钮（通常在工具栏上）重新同步项目
- **依赖缺失错误**：检查并安装缺少的依赖包，Android Studio通常会提示如何修复
- **构建失败**：查看底部的"Build"输出窗口，分析错误信息并修复

#### 1.3 无法找到或访问密钥库
- 确保密钥库文件路径正确
- 检查文件权限，确保您有读写权限
- 如果是新创建的密钥库，确保路径中的所有文件夹都存在

#### 1.4 APK导出后无法安装
- 确保同时勾选了V1和V2签名选项
- 检查应用的最低API级别是否与目标设备兼容
- 确保应用已正确签名

#### 1.5 导出按钮灰色或不可点击
- 检查项目是否有编译错误（红色错误图标）
- 尝试清理项目：Build > Clean Project
- 然后重新构建：Build > Rebuild Project

#### 1.6 找不到导出的APK文件
- 导出成功后，Android Studio会显示一个通知，点击"locate"按钮可以直接打开APK所在文件夹
- 默认位置通常是：`项目路径/app/build/outputs/apk/release/`
- 如果找不到，请在Android Studio中查看导出完成后的通知信息，其中包含确切路径

#### 1.7 项目加载缓慢或卡住
- 确保您的电脑有足够的内存和磁盘空间
- 关闭不必要的应用程序以释放资源
- 耐心等待Gradle同步和索引完成

祝您导出顺利！如有问题，请按照上述步骤重新操作。