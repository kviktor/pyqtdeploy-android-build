# PyQt5 applications with pyqtdeploy on Android

This a small guide that explains how to deploy PyQt5 application to Android using pyqtdeploy.
Keep in mind that this is not a Python/Qt/PyQt5 tutorial.

# Reading list

Before doing anything read these docs, they get you up to speed how PyQt/Qt/Android works.

- Qt
  - https://doc.qt.io/qt-5/android-getting-started.html
  - https://doc.qt.io/qt-5/deployment-android.html

- PyQt
  - https://www.riverbankcomputing.com/static/Docs/pyqtdeploy/ (this is the most useful one)
  - https://www.riverbankcomputing.com/static/Docs/PyQt5/index.html


# Setting up the environment

This guide was written using `Ubuntu 20.04` however there is nothing platform specific here
so it should work on almost any Linux-based system.


## Install required dependencies

These are the required dependencies to build and deploy the example application to Android.

The following package versions are used in the guide
- Python 3.7.7
- Qt 5.13.2
- PyQt 5.15.1
- sip 4.9.24
- pyqtdeploy 2.5.1
- Android NDK r20b


Note: it's recommended to always use the latest PyQt5 source, it's compatible with older version.

### System packages


```
sudo apt-get install clang make zlib1g zlib1g-dev libbz2-dev libssl-dev openjdk-8-jdk build-essential git
```

### Qt

Download the online installer from https://www.qt.io/download-qt-installer and install it under `~/Qt`.
After the installation is completed there should be a `MaintenanceTool` binary in the Qt folder, run it.

Here you should install Qt `5.13.2` and only the Android related packages.

Note: a Qt account might be required.

### Android SDK/NDK

Unfortunatelly things don't seem to work with the command line tool only so we need to download Android Studio from https://developer.android.com/studio and intall it to `~/Android`.

After the installation is done run the following commands to update the Android SDK list and install the Android 29 platform.

```
~/Android/tools/tools/bin/sdkmanager --update
~/Android/tools/tools/bin/sdkmanager "platforms;android-28"
```

We also need to install an Android NDK, to do this go to https://developer.android.com/ndk/downloads/older_releases and download `android-ndk-r20b` and exract it to `~/Android`.

The command `cat ~/Android/android-ndk-r20b/source.properties` should run successfully and show some data.

### pip/pyqtdeploy

We need to have the latest pip and pyqtdeploy installed.
You can install them in a virtualenv or not, up to you.

```
pip install -U pip
pip install pyqtdeploy==2.5.1 pyqt5
```

Note: the latest pyqtdeploy (3 and above) had some major changes, this guide will be updated to follow up with those.

## Download source packages

For building the Android sysroot we will need the source packages of the libraries.
Download the following files and put them in `example/sources/` (the tar.gz/tgz versions)

- sip 4.19.24 https://www.riverbankcomputing.com/software/sip/download
- PyQt5 5.15.1 https://www.riverbankcomputing.com/software/pyqt/download5 or https://pypi.org/project/PyQt5/5.15.1/#files
- Python 3.7.7 https://www.python.org/downloads/source/
- openssl 1.0.2r https://www.openssl.org/source/old/1.0.2/

## Set environment variables

For pyqtdeploy to work properly we need to have some environment variables set

```
# required for pyqtdeploy
export ANDROID_SDK_ROOT=$HOME/Android/tools
export ANDROID_NDK_ROOT=$HOME/Android/android-ndk-r20b
export ANDROID_NDK_PLATFORM=android-29

# useful later, need to specify Qt dir while building sysroot
export QT_DIR=$HOME/Qt/5.13.2

# change this to point to the git repo
# useful for pyqtdeploy to know the example app's directory
export APP_DIR=$HOME/path-to/example/app

# for adb and androiddeployqt
export PATH=$HOME/Android/tools/platform-tools:$PATH
export PATH=$HOME/Qt/5.13.2/android_arm64_v8a/bin:$PATH
```


# Building Android sysroot

Go to `example/` directory and run the following command

```
pyqtdeploy-sysroot --target android-64 --source-dir sources/ --source-dir $QT_DIR --verbose sysroot.json
```

# Building the application

```
pyqtdeploy-build  --target android-64 --verbose --no-clean app.pdy
cd build-android-64
qmake
make -j2
make install INSTALL_ROOT=app
# 29 as in android-29, libmain comes from the entrypoint name in the .pdy file
androiddeployqt --gradle --android-platform 29 --input android-libmain.so-deployment-settings.json --output app
```

To install it to your device run (might need to enable developer mode and USB debugging on your phone, after that it works via USB or over TCP too)
```
adb devices
adb install app/build/outputs/apk/debug/app-debug.apk
```

# Adding Android specific things

In order to customize our application (name, logo, custom permissions) we need to create our
own `AndroidManifest.xml` and also in the long term it's better to have our own custom
Activity inheried from QtActivity.

To create these custom files we need to specifiy `ANDROID_PACKAGE_SOURCE_DIR` (https://doc.qt.io/qt-5/deployment-android.html#android-specific-qmake-variables) in qmake variables (the .pdy file has a separate tab for it). 

First copy `$QT_DIR/android_arm64_v8a/src/android/templates/AndroidManifest.xml` to `example/android_source/`.

Then create `ExampleActivity.java` in `example/android_source/src/org/kviktor/example/` with the following content

```java
package org.kviktor.example;


public class ExampleActivity extends org.qtproject.qt5.android.bindings.QtActivity
{
    private static ExampleActivity m_instance;

    public ExampleActivity()
    {
        m_instance = this;
    }
}
```

This one just extends the original `QtActivity` class and saves a reference to itself in a static variable (this will come in handy later).

In `AndroidManifest.xml` change `org.qtproject.qt5.android.bindings.QtActivity` to
`org.kviktor.example.ExampleActivity`.
