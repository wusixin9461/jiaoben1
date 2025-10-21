[app]

# (str) Title of your application
title = pokemmo自动化

# (str) Package name
package.name = pokemmoautomation

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
# Do not exclude hidden files
#source.exclude_patterns = .*\.py[co]

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = python3,kivy==2.2.1,opencv-python==4.8.1.78,numpy==1.24.3,pillow==10.0.0,plyer==2.1.0
requirements = python3,kivy==2.2.1,opencv-python==4.8.1.78,numpy==1.24.3,pillow==10.0.0,plyer==2.1.0

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, portrait)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#
#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 2.2.1

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names: 'red', 'blue', 'green', 'black', 'white', 'gray', 'cyan', 'magenta', 'yellow', 'lightgray', 'darkgray', 'grey', 'lightgrey', 'darkgrey', 'aqua', 'fuchsia', 'lime', 'maroon', 'navy', 'olive', 'purple', 'silver', 'teal'
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format.
# see https://lottiefiles.com/ for examples and https://airbnb.design/lottie/ for general documentation.
# Lottie files can be created using various tools, like Adobe After Effect or Synfig.
#android.presplash_lottie = "path/to/lottie/file.json"

# (str) Adaptive icon of the application (used if Android API level is 26+ at runtime)
#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
#icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

# (list) Permissions
android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 29

# (str) Android NDK version to use
android.ndk = 25.1.8937393

# (int) Android NDK API to use. This is the minimum API your NDK supports, it should usually match android.minapi.
android.ndk_api = 21

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
# use that parameter together with android.entrypoint to set custom Java class instead of PythonActivity
#android.activity_class_name = org.example.package.MainActivity

# (str) Extra xml to write directly inside the <manifest> element of AndroidManifest.xml
# use that parameter to provide a filename from where to load your custom XML code
#android.extra_manifest_xml = ./src/android/extra_manifest.xml

# (str) Extra xml to write directly inside the <manifest><application> tag of AndroidManifest.xml
# use that parameter to provide a filename from where to load your custom XML arguments:
#android.extra_application_manifest_xml = ./src/android/extra_application_manifest.xml

# (str) Full name including package path of the Java class that implements Python Service
# use that parameter to set custom Java class instead of PythonService
#android.service_class_name = org.example.package.MyService

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = '@android:style/Theme.NoTitleBar'

# (list) Pattern to match files to be excluded from the final apk
android.exclude_patterns = __pycache__, *.pyo, *.pyc, .git, .svn, .hg, .DS_Store

# (str) Path to a custom whitelist file
#android.whitelist = %(source.dir)s/whitelist.txt

# (str) Path to a custom blacklist file
#android.blacklist = %(source.dir)s/blacklist.txt

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a
android.archs = armeabi-v7a, arm64-v8a

# (int) overrides automatic versionCode computation (used in build.gradle)
# this is not the same as app version and should only be edited if you know what you're doing
# android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup rules
android.backup_rules = backup_rules.xml

# (str) If you need to insert variables into your AndroidManifest.xml file, you can do so with the manifestPlaceholders property. 
# This property takes a map of key-value pairs. For example, to add a custom metadata entry, you would add:
android.manifestPlaceholders = package_name=${applicationId}

# (str) Path to a custom build.gradle file
#android.gradle_file = %(source.dir)s/custom_build.gradle

# (str) Dependencies from maven repositories
#android.maven_deps = com.squareup.okhttp3:okhttp:4.9.1,com.squareup.okhttp3:logging-interceptor:4.9.1

# (list) Java classes to add as activities to the manifest
#android.add_activities = com.squareup.okhttp3.sample.helloworld.HelloWorldActivity

# (list) Java classes to add as services to the manifest
#android.add_services = com.squareup.okhttp3.sample.helloworld.HelloWorldService

# (list) Java classes to add as receivers to the manifest
#android.add_receivers = com.squareup.okhttp3.sample.helloworld.HelloWorldReceiver

# (list) Java classes to add as providers to the manifest
#android.add_providers = com.squareup.okhttp3.sample.helloworld.HelloWorldProvider

# (str) Path to a custom strings.xml file
#android.custom_strings_xml = %(source.dir)s/custom_strings.xml

# (str) Path to a custom styles.xml file
#android.custom_styles_xml = %(source.dir)s/custom_styles.xml

# (str) Path to a custom colors.xml file
#android.custom_colors_xml = %(source.dir)s/custom_colors.xml

# (str) Path to a custom attrs.xml file
#android.custom_attrs_xml = %(source.dir)s/custom_attrs.xml

# (str) Path to a custom themes.xml file
#android.custom_themes_xml = %(source.dir)s/custom_themes.xml

# (list) List of assets folder to add to the APK
#android.add_assets = source_assets_folder:destination_assets_folder

# (list) Gradle dependencies to add
#android.gradle_dependencies = implementation 'com.squareup.okhttp3:okhttp:4.9.1'

# (str) Path to custom ProGuard rules
#android.proguard_rules = %(source.dir)s/proguard-rules.pro

# (str) Path to the Android SDK
#android.sdk_path = 

# (str) Path to the Android NDK
#android.ndk_path = 

# (str) Path to the Android SDK packages directory
#android.sdk_packages_path = 

# (str) Path to the Android SDK extras directory
#android.sdk_extras_path = 

# (list) Android app modules to disable
#android.disabled_modules = 

# (list) Android app modules to enable
#android.enabled_modules = 

# (str) Android app bundle mode (aab or apk)
android.release_artifact = apk

# (str) Python for android fork to use
#p4a.fork = kivy/python-for-android

# (str) Python for android branch to use
#p4a.branch = master

# (str) Python for android git clone directory (if not empty, the fork/branch parameters are ignored)
#p4a.source_dir = 

# (str) Python for android recipe directory (if not empty, the fork/branch parameters are ignored)
#p4a.recipe_dir = 

# (str) Python for android distribution directory (if not empty, the fork/branch parameters are ignored)
#p4a.dist_dir = 

# (str) Python for android archives directory (if not empty, the fork/branch parameters are ignored)
#p4a.archives_dir = 

# (str) Python for android cache directory (if not empty, the fork/branch parameters are ignored)
#p4a.cache_dir = 

# (bool) Delete the cache of Python for android
#p4a.clear_cache = False

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes = 

# (str) Filename to the hook for p4a
#p4a.hook = 

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port = 

# (bool) The default value of android.hide_keyboard_layout
#android.hide_keyboard_layout = False

# (str) The default value of android.keyboard_layout
#android.keyboard_layout = qwerty

# (bool) Try to use the android.ndk_path even if the p4a.setup_py_toolchain command fails
#android.force_ndk_path = False

# (str) Log level (debug, info, warning, error, critical)
android.log_level = debug

#
# iOS specific
#

# (str) Path to a custom kivy-ios fork
#ios.kivy_ios_dir = ../kivy-ios

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin

# (list) List of table of contents to include
# toc = 

# (list) Options to pass to the C compiler
# android.cflags = 

# (bool) Use --touch-calibration parameter to control calibration
# android.touch_calibration = False

# (bool) Use --auto-rotation parameter to control rotation
# android.auto_rotation = False

# (bool) Use --orientation parameter to control orientation
# android.orientation = portrait

# (bool) Use --android-minapi parameter to set minapi
# android.minapi = 21

# (bool) Use --android-api parameter to set api
# android.api = 33

# (bool) Use --android-sdk parameter to set sdk
# android.sdk = 29

# (bool) Use --android-ndk parameter to set ndk
# android.ndk = 25.1.8937393

# (bool) Use --android-ndk-api parameter to set ndk-api
# android.ndk_api = 21

# (bool) Use --android-entrypoint parameter to set entrypoint
# android.entrypoint = org.kivy.android.PythonActivity

# (bool) Use --android-whitelist parameter to set whitelist
# android.whitelist = 

# (bool) Use --android-blacklist parameter to set blacklist
# android.blacklist = 

# (bool) Use --android-archs parameter to set archs
# android.archs = armeabi-v7a, arm64-v8a

# (bool) Use --android-numeric-version parameter to set numeric-version
# android.numeric_version = 1

# (bool) Use --android-allow-backup parameter to set allow-backup
# android.allow_backup = True

# (bool) Use --android-backup-rules parameter to set backup-rules
# android.backup_rules = backup_rules.xml

# (bool) Use --android-manifest-placeholders parameter to set manifest-placeholders
# android.manifestPlaceholders = package_name=${applicationId}

# (bool) Use --android-gradle-file parameter to set gradle-file
# android.gradle_file = 

# (bool) Use --android-maven-deps parameter to set maven-deps
# android.maven_deps = 

# (bool) Use --android-add-activities parameter to set add-activities
# android.add_activities = 

# (bool) Use --android-add-services parameter to set add-services
# android.add_services = 

# (bool) Use --android-add-receivers parameter to set add-receivers
# android.add_receivers = 

# (bool) Use --android-add-providers parameter to set add-providers
# android.add_providers = 

# (bool) Use --android-custom-strings-xml parameter to set custom-strings-xml
# android.custom_strings_xml = 

# (bool) Use --android-custom-styles-xml parameter to set custom-styles-xml
# android.custom_styles_xml = 

# (bool) Use --android-custom-colors-xml parameter to set custom-colors-xml
# android.custom_colors_xml = 

# (bool) Use --android-custom-attrs-xml parameter to set custom-attrs-xml
# android.custom_attrs_xml = 

# (bool) Use --android-custom-themes-xml parameter to set custom-themes-xml
# android.custom_themes_xml = 

# (bool) Use --android-add-assets parameter to set add-assets
# android.add_assets = 

# (bool) Use --android-gradle-dependencies parameter to set gradle-dependencies
# android.gradle_dependencies = 

# (bool) Use --android-proguard-rules parameter to set proguard-rules
# android.proguard_rules = 

# (bool) Use --android-sdk-path parameter to set sdk-path
# android.sdk_path = 

# (bool) Use --android-ndk-path parameter to set ndk-path
# android.ndk_path = 

# (bool) Use --android-sdk-packages-path parameter to set sdk-packages-path
# android.sdk_packages_path = 

# (bool) Use --android-sdk-extras-path parameter to set sdk-extras-path
# android.sdk_extras_path = 

# (bool) Use --android-disabled-modules parameter to set disabled-modules
# android.disabled_modules = 

# (bool) Use --android-enabled-modules parameter to set enabled-modules
# android.enabled_modules = 

# (bool) Use --android-release-artifact parameter to set release-artifact
# android.release_artifact = apk

# (bool) Use --p4a-fork parameter to set p4a-fork
# p4a.fork = 

# (bool) Use --p4a-branch parameter to set p4a-branch
# p4a.branch = 

# (bool) Use --p4a-source-dir parameter to set p4a-source-dir
# p4a.source_dir = 

# (bool) Use --p4a-recipe-dir parameter to set p4a-recipe-dir
# p4a.recipe_dir = 

# (bool) Use --p4a-dist-dir parameter to set p4a-dist-dir
# p4a.dist_dir = 

# (bool) Use --p4a-archives-dir parameter to set p4a-archives-dir
# p4a.archives_dir = 

# (bool) Use --p4a-cache-dir parameter to set p4a-cache-dir
# p4a.cache_dir = 

# (bool) Use --p4a-clear-cache parameter to set p4a-clear-cache
# p4a.clear_cache = 

# (bool) Use --p4a-local-recipes parameter to set p4a-local-recipes
# p4a.local_recipes = 

# (bool) Use --p4a-hook parameter to set p4a-hook
# p4a.hook = 

# (bool) Use --p4a-bootstrap parameter to set p4a-bootstrap
# p4a.bootstrap = 

# (bool) Use --p4a-port parameter to set p4a-port
# p4a.port = 

# (bool) Use --android-hide-keyboard-layout parameter to set hide-keyboard-layout
# android.hide_keyboard_layout = 

# (bool) Use --android-keyboard-layout parameter to set keyboard-layout
# android.keyboard_layout = 

# (bool) Use --android-force-ndk-path parameter to set force-ndk-path
# android.force_ndk_path = 

# (bool) Use --android-log-level parameter to set log-level
# android.log_level = 

# (bool) Use --ios-kivy-ios-dir parameter to set kivy-ios-dir
# ios.kivy_ios_dir = 

# (bool) Use --ios-codesign-debug parameter to set codesign-debug
# ios.codesign.debug = 

# (bool) Use --ios-codesign-release parameter to set codesign-release
# ios.codesign.release = 

# (list) Search path for build dependencies
# specify, to update dependencies, modify this to point to your custom directory
# search_paths = 

# (int) How many times to retry the build process if it fails
# retry_build_count = 0

# (list) List of strings to replace in the manifest file
# manifest_replace = 

# (bool) Whether to automatically clean the build directory before building
# clean_before_build = True

# (bool) Whether to automatically clean the dependencies directory before building
# clean_before_deps = True

# (bool) Whether to automatically clean the build and dependencies directories before building
# clean_both_before_build = False

# (bool) Whether to automatically clean the entire buildozer directory before building
# clean_entire_buildozer_dir = False

# (bool) Whether to use the --deploy parameter to deploy to a connected device
# deploy = False

# (str) The name of the device to deploy to, use 'all' for all connected devices
# deploy_device = all

# (bool) Whether to use the --sign parameter to sign the apk/ipa
# sign = False

# (str) The name of the keystore file to use for signing
# sign_keystore = 

# (str) The alias of the keystore file to use for signing
# sign_alias = 

# (str) The password of the keystore file to use for signing
# sign_password = 

# (str) The key password of the keystore file to use for signing
# sign_key_password = 

# (bool) Whether to use the --verify parameter to verify the apk/ipa
# verify = False

# (str) The name of the verification tool to use
# verify_tool = 

# (list) List of verification tools to use
# verify_tools = 

# (str) The name of the build tool to use
# build_tool = 

# (list) List of build tools to use
# build_tools = 

# (bool) Whether to use the --prebuild parameter to prebuild the application
# prebuild = False

# (bool) Whether to use the --postbuild parameter to postbuild the application
# postbuild = False

# (str) The command to run before building the application
# prebuild_command = 

# (str) The command to run after building the application
# postbuild_command = 

# (bool) Whether to use the --prebuild-clean parameter to clean before prebuilding
# prebuild_clean = False

# (bool) Whether to use the --postbuild-clean parameter to clean after postbuilding
# postbuild_clean = False

# (bool) Whether to use the --prebuild-only parameter to only prebuild the application
# prebuild_only = False

# (bool) Whether to use the --postbuild-only parameter to only postbuild the application
# postbuild_only = False

# (bool) Whether to use the --build-only parameter to only build the application
# build_only = False

# (bool) Whether to use the --package-only parameter to only package the application
# package_only = False

# (bool) Whether to use the --deploy-only parameter to only deploy the application
# deploy_only = False

# (bool) Whether to use the --sign-only parameter to only sign the application
# sign_only = False

# (bool) Whether to use the --verify-only parameter to only verify the application
# verify_only = False

# (bool) Whether to use the --upload-only parameter to only upload the application
# upload_only = False

# (bool) Whether to use the --download-only parameter to only download the application
# download_only = False

# (bool) Whether to use the --check-only parameter to only check the application
# check_only = False

# (bool) Whether to use the --list-only parameter to only list the application
# list_only = False

# (bool) Whether to use the --info-only parameter to only show info about the application
# info_only = False

# (bool) Whether to use the --help-only parameter to only show help for the application
# help_only = False

# (bool) Whether to use the --version-only parameter to only show version of the application
# version_only = False

# (bool) Whether to use the --debug parameter to build a debug version of the application
# debug = False

# (bool) Whether to use the --release parameter to build a release version of the application
# release = False

# (bool) Whether to use the --sdk parameter to specify the SDK version
# sdk = False

# (bool) Whether to use the --ndk parameter to specify the NDK version
# ndk = False

# (bool) Whether to use the --ndk-api parameter to specify the NDK API version
# ndk_api = False

# (bool) Whether to use the --sdk-api parameter to specify the SDK API version
# sdk_api = False

# (bool) Whether to use the --build-tools parameter to specify the build tools version
# build_tools = False

# (bool) Whether to use the --gradle parameter to specify the gradle version
# gradle = False

# (bool) Whether to use the --ant parameter to specify the ant version
# ant = False

# (bool) Whether to use the --javac parameter to specify the javac version
# javac = False

# (bool) Whether to use the --javac-target parameter to specify the javac target version
# javac_target = False

# (bool) Whether to use the --javac-source parameter to specify the javac source version
# javac_source = False

# (bool) Whether to use the --jarsigner parameter to specify the jarsigner version
# jarsigner = False

# (bool) Whether to use the --keytool parameter to specify the keytool version
# keytool = False

# (bool) Whether to use the --adb parameter to specify the adb version
# adb = False

# (bool) Whether to use the --aapt parameter to specify the aapt version
# aapt = False

# (bool) Whether to use the --aapt2 parameter to specify the aapt2 version
# aapt2 = False

# (bool) Whether to use the --d8 parameter to specify the d8 version
# d8 = False

# (bool) Whether to use the --dx parameter to specify the dx version
# dx = False

# (bool) Whether to use the --zipalign parameter to specify the zipalign version
# zipalign = False

# (bool) Whether to use the --apksigner parameter to specify the apksigner version
# apksigner = False

# (bool) Whether to use the --unzip parameter to specify the unzip version
# unzip = False

# (bool) Whether to use the --zip parameter to specify the zip version
# zip = False

# (bool) Whether to use the --tar parameter to specify the tar version
# tar = False

# (bool) Whether to use the --gzip parameter to specify the gzip version
# gzip = False

# (bool) Whether to use the --bzip2 parameter to specify the bzip2 version
# bzip2 = False

# (bool) Whether to use the --xz parameter to specify the xz version
# xz = False

# (bool) Whether to use the --7z parameter to specify the 7z version
# 7z = False

# (bool) Whether to use the --cp parameter to specify the cp version
# cp = False

# (bool) Whether to use the --mv parameter to specify the mv version
# mv = False

# (bool) Whether to use the --rm parameter to specify the rm version
# rm = False

# (bool) Whether to use the --mkdir parameter to specify the mkdir version
# mkdir = False

# (bool) Whether to use the --rmdir parameter to specify the rmdir version
# rmdir = False

# (bool) Whether to use the --find parameter to specify the find version
# find = False

# (bool) Whether to use the --grep parameter to specify the grep version
# grep = False

# (bool) Whether to use the --sed parameter to specify the sed version
# sed = False

# (bool) Whether to use the --awk parameter to specify the awk version
# awk = False

# (bool) Whether to use the --sort parameter to specify the sort version
# sort = False

# (bool) Whether to use the --uniq parameter to specify the uniq version
# uniq = False

# (bool) Whether to use the --cat parameter to specify the cat version
# cat = False

# (bool) Whether to use the --echo parameter to specify the echo version
# echo = False

# (bool) Whether to use the --printf parameter to specify the printf version
# printf = False

# (bool) Whether to use the --head parameter to specify the head version
# head = False

# (bool) Whether to use the --tail parameter to specify the tail version
# tail = False

# (bool) Whether to use the --cut parameter to specify the cut version
# cut = False

# (bool) Whether to use the --tr parameter to specify the tr version
# tr = False

# (bool) Whether to use the --wc parameter to specify the wc version
# wc = False

# (bool) Whether to use the --ls parameter to specify the ls version
# ls = False

# (bool) Whether to use the --pwd parameter to specify the pwd version
# pwd = False

# (bool) Whether to use the --cd parameter to specify the cd version
# cd = False

# (bool) Whether to use the --chmod parameter to specify the chmod version
# chmod = False

# (bool) Whether to use the --chown parameter to specify the chown version
# chown = False

# (bool) Whether to use the --chgrp parameter to specify the chgrp version
# chgrp = False

# (bool) Whether to use the --stat parameter to specify the stat version
# stat = False

# (bool) Whether to use the --touch parameter to specify the touch version
# touch = False

# (bool) Whether to use the --date parameter to specify the date version
# date = False

# (bool) Whether to use the --time parameter to specify the time version
# time = False

# (bool) Whether to use the --sleep parameter to specify the sleep version
# sleep = False

# (bool) Whether to use the --yes parameter to specify the yes version
# yes = False

# (bool) Whether to use the --no parameter to specify the no version
# no = False

# (bool) Whether to use the --true parameter to specify the true version
# true = False

# (bool) Whether to use the --false parameter to specify the false version
# false = False

# (bool) Whether to use the --test parameter to specify the test version
# test = False

# (bool) Whether to use the --expr parameter to specify the expr version
# expr = False

# (bool) Whether to use the --bc parameter to specify the bc version
# bc = False

# (bool) Whether to use the --dc parameter to specify the dc version
# dc = False

# (bool) Whether to use the --python parameter to specify the python version
# python = False

# (bool) Whether to use the --python2 parameter to specify the python2 version
# python2 = False

# (bool) Whether to use the --python3 parameter to specify the python3 version
# python3 = False

# (bool) Whether to use the --pip parameter to specify the pip version
# pip = False

# (bool) Whether to use the --pip2 parameter to specify the pip2 version
# pip2 = False

# (bool) Whether to use the --pip3 parameter to specify the pip3 version
# pip3 = False

# (bool) Whether to use the --virtualenv parameter to specify the virtualenv version
# virtualenv = False

# (bool) Whether to use the --venv parameter to specify the venv version
# venv = False

# (bool) Whether to use the --conda parameter to specify the conda version
# conda = False

# (bool) Whether to use the --node parameter to specify the node version
# node = False

# (bool) Whether to use the --npm parameter to specify the npm version
# npm = False

# (bool) Whether to use the --yarn parameter to specify the yarn version
# yarn = False

# (bool) Whether to use the --ruby parameter to specify the ruby version
# ruby = False

# (bool) Whether to use the --gem parameter to specify the gem version
# gem = False

# (bool) Whether to use the --perl parameter to specify the perl version
# perl = False

# (bool) Whether to use the --cpan parameter to specify the cpan version
# cpan = False

# (bool) Whether to use the --go parameter to specify the go version
# go = False

# (bool) Whether to use the --rust parameter to specify the rust version
# rust = False

# (bool) Whether to use the --cargo parameter to specify the cargo version
# cargo = False

# (bool) Whether to use the --java parameter to specify the java version
# java = False

# (bool) Whether to use the --javac parameter to specify the javac version
# javac = False

# (bool) Whether to use the --jar parameter to specify the jar version
# jar = False

# (bool) Whether to use the --gradle parameter to specify the gradle version
# gradle = False

# (bool) Whether to use the --mvn parameter to specify the mvn version
# mvn = False

# (bool) Whether to use the --ant parameter to specify the ant version
# ant = False

# (bool) Whether to use the --make parameter to specify the make version
# make = False

# (bool) Whether to use the --cmake parameter to specify the cmake version
# cmake = False

# (bool) Whether to use the --ninja parameter to specify the ninja version
# ninja = False

# (bool) Whether to use the --scons parameter to specify the scons version
# scons = False

# (bool) Whether to use the --autoconf parameter to specify the autoconf version
# autoconf = False

# (bool) Whether to use the --automake parameter to specify the automake version
# automake = False

# (bool) Whether to use the --libtool parameter to specify the libtool version
# libtool = False

# (bool) Whether to use the --pkg-config parameter to specify the pkg-config version
# pkg-config = False

# (bool) Whether to use the --gcc parameter to specify the gcc version
# gcc = False

# (bool) Whether to use the --g++ parameter to specify the g++ version
# g++ = False

# (bool) Whether to use the --clang parameter to specify the clang version
# clang = False

# (bool) Whether to use the --clang++ parameter to specify the clang++ version
# clang++ = False

# (bool) Whether to use the --ld parameter to specify the ld version
# ld = False

# (bool) Whether to use the --ar parameter to specify the ar version
# ar = False

# (bool) Whether to use the --ranlib parameter to specify the ranlib version
# ranlib = False

# (bool) Whether to use the --strip parameter to specify the strip version
# strip = False

# (bool) Whether to use the --objcopy parameter to specify the objcopy version
# objcopy = False

# (bool) Whether to use the --objdump parameter to specify the objdump version
# objdump = False

# (bool) Whether to use the --readelf parameter to specify the readelf version
# readelf = False

# (bool) Whether to use the --size parameter to specify the size version
# size = False

# (bool) Whether to use the --strings parameter to specify the strings version
# strings = False

# (bool) Whether to use the --hexdump parameter to specify the hexdump version
# hexdump = False

# (bool) Whether to use the --xxd parameter to specify the xxd version
# xxd = False

# (bool) Whether to use the --openssl parameter to specify the openssl version
# openssl = False

# (bool) Whether to use the --curl parameter to specify the curl version
# curl = False

# (bool) Whether to use the --wget parameter to specify the wget version
# wget = False

# (bool) Whether to use the --ssh parameter to specify the ssh version
# ssh = False

# (bool) Whether to use the --scp parameter to specify the scp version
# scp = False

# (bool) Whether to use the --sftp parameter to specify the sftp version
# sftp = False

# (bool) Whether to use the --rsync parameter to specify the rsync version
# rsync = False

# (bool) Whether to use the --git parameter to specify the git version
# git = False

# (bool) Whether to use the --svn parameter to specify the svn version
# svn = False

# (bool) Whether to use the --hg parameter to specify the hg version
# hg = False

# (bool) Whether to use the --bzr parameter to specify the bzr version
# bzr = False

# (bool) Whether to use the --cvs parameter to specify the cvs version
# cvs = False

# (bool) Whether to use the --darcs parameter to specify the darcs version
# darcs = False

# (bool) Whether to use the --fossil parameter to specify the fossil version
# fossil = False

# (bool) Whether to use the --mercurial parameter to specify the mercurial version
# mercurial = False

# (bool) Whether to use the --subversion parameter to specify the subversion version
# subversion = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
# bitbucket = False

# (bool) Whether to use the --github parameter to specify the github version
# github = False

# (bool) Whether to use the --gitlab parameter to specify the gitlab version
# gitlab = False

# (bool) Whether to use the --bitbucket parameter to specify the bitbucket version
android.skip_update = True
android.skip_sign = True
android.sdk_update_hook = %(hooks_path)s/android_sdk_update_hook.sh
android.p4a_dir = ~/.local/share/python-for-android