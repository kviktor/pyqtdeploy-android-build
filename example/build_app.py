import argparse
import os
from os.path import join as opj
import subprocess
import sys

# set variables
# preferably the env vars would be set outside
# but it's nice to have everything in one place

HOME = os.path.expanduser('~')
ANDROID_SDK_ROOT = opj(HOME, 'Android', 'tools')
ANDROID_NDK_PLATFORM = 'android-29'
QT_DIR = opj(HOME, 'Qt', '5.13.2')

os.environ['ANDROID_SDK_ROOT'] = ANDROID_SDK_ROOT
os.environ['ANDROID_NDK_ROOT'] = opj(HOME, 'Android', 'android-ndk-r20b')
os.environ['ANDROID_NDK_PLATFORM'] = ANDROID_NDK_PLATFORM

ADB_PATH = opj(ANDROID_SDK_ROOT, 'platform-tools', 'adb')

TARGET = 'android-64'
SYSROOT_DIR = f'sysroot-{TARGET}'
BUILD_DIR = f'build-{TARGET}'
HOST_BIN_DIR = os.path.abspath(opj(SYSROOT_DIR, 'host', 'bin'))


def run(args):
    print('Running: %s' % ' '.join(args))
    retval = subprocess.call(' '.join(args), shell=True)
    if retval != 0:
        sys.exit(1)


parser = argparse.ArgumentParser()
parser.add_argument('--with-sysroot', help="should we build sysroot too", action='store_true')
parser.add_argument('--install', help="install it", action='store_true')

cmd_args = parser.parse_args()

if cmd_args.with_sysroot:
    args = [
        'pyqtdeploy-sysroot',
        '--target', 'android-64', 
        '--source-dir', 'sources/',
        '--source-dir', QT_DIR,
        '--verbose',
        'sysroot.json'
    ]
    run(args)


args = [
    'pyqtdeploy-build',
    '--target', 'android-64',
    '--verbose',
    '--no-clean',
    'app.pdy',
]
run(args)

os.chdir(BUILD_DIR)
run([os.path.join(HOST_BIN_DIR, 'qmake')])
run(['make', '-j2'])
run(['make', 'INSTALL_ROOT=app', 'install'])
run([
    os.path.join(HOST_BIN_DIR, 'androiddeployqt'),
    '--gradle',
    '--android-platform', ANDROID_NDK_PLATFORM.replace('android-', ''),
    '--input', 'android-libmain.so-deployment-settings.json',
    '--output', 'app'
])

if cmd_args.install:
    run([ADB_PATH, 'devices'])
    run([ADB_PATH, 'install', os.path.join('app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')])
