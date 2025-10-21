#!/bin/bash
# Android SDK更新钩子 - 跳过不必要的更新以加快构建速度
echo "执行自定义SDK更新钩子..."
echo "跳过完整SDK更新，以加快构建速度"

# 确保必要的目录存在
mkdir -p $ANDROID_SDK_HOME/licenses

# 创建必要的许可证文件
echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > $ANDROID_SDK_HOME/licenses/android-sdk-license
echo "d975f751698a77b662f1254ddbeed3901e976f5a" > $ANDROID_SDK_HOME/licenses/android-sdk-preview-license

echo "SDK更新钩子执行完成"
exit 0
