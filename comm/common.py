#encoding=utf-8
import platform
import os

PHONE = 1       # 手机
MAC = 2         # mac
LINUX = 3       # 云服务器


# 返回系统平台
def system():
    if platform.system() == 'Darwin' and platform.machine() == 'x86_64':
        return MAC

    if platform.system() == 'Linux' and platform.machine() in ('aarch64', 'armv7l'):
        return PHONE

    if platform.system() == 'Linux' and platform.machine() == 'x86_64':
        return LINUX


# 重启飞行模式
def restart_fly_mode():
    os.system('settings put global airplane_mode_on 1')
    os.system('settings put global airplane_mode_on 0')


# 重启wifi
def restart_wifi():
    os.system('svc wifi disable')
    os.system('svc wifi enable')