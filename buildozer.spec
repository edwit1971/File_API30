############################################################
#
# App
#
############################################################

[app]

# (str) Title of your application
title = File_Api30

# (str) Package name
package.name = File_Api30

# (str) Package domain (needed for android/ios packaging)
package.domain = com.handgems

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py, png, atlas, db, ttf, md, yaml, json

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = bin, __pycache__

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3==3.8.6,
               hostpython3==3.8.6,
               kivy==2.0.0,
               kivymd==0.104.2,
               pyjnius==1.2.1,
               pyparsing==2.4.7,
               chardet==4.0.0,
               httplib2==0.19.1,
               idna==2.10,
               oauth2client==4.1.3,
               pillow==8.2.0,
               plyer==2.0.0,
               pyasn1==0.4.8,
               pyasn1-modules==0.2.7,
               pydrive==1.3.1,
               pydrive2==1.10.0,
               pygments==2.9.0,
               pyyaml==5.4.1,
               requests==2.25.1,
               rsa==4.7.2,
               sdl2_ttf==2.0.15,
               six==1.16.0,
               uritemplate==3.0.1,
               urllib3==1.26.5,

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = /home/edwit3/anaconda3/envs/myenv/lib/python3.8/site-packages/kivy/

# (list) Garden requirements
#garden_requirements = matplotlib

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/images/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/images/icon.png

# (str) Supported orientation (one of portrait, landscape, sensorLandscape, or all)
orientation = portrait


############################################################
#
# OSX Specific
#
############################################################

# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 2.0.0


############################################################
#
# Android specific
#
############################################################

# (bool) Indicate if the application should be fullscreen or not
fullscreen = True

# (string) Presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API, should be as high as possible.
# API 28 is AndroidOS 9.0 and has to do with changes made in v10.0 with File Handling
# API 29 is Android 10 and I need to set requestLegacyExternalStorage to True
android.api = 29

# (int) Minimum API your APK will support. 21 = Lollipop v5.0
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 19c

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path = /home/edwit1971/.buildozer/android/platform/android-ndk-r22b/
android.ndk_path = /home/edwit1971/.buildozer/android/platform/android-ndk-r19c/

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = armeabi-v7a

android.add_aars = support-v4-24.0.0-alpha1.aar

############################################################
#
# Python for android (p4a) specific
#
############################################################

# (str) python-for-android fork to use, defaults to upstream (kivy)
# p4a.fork = edwit1971

# (str) python-for-android branch to use, defaults to master
# p4a.branch = develop


############################################################
#
# iOS specific
#
############################################################

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency: ios-deploy
# Uncomment to use a custom checkout
#ios.ios_deploy_dir = ../ios_deploy
# Or specify URL and branch
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s


############################################################
#
# Buildozer
#
############################################################

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

