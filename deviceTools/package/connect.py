#!/usr/bin/env pyhton 
# coding:utf8

from package import load_shell

def connect(ip):
    status,stdout=load_shell.shell('adb connect {}:5555'.format(ip))
    s=1
    for line in stdout:
        if b"connected to" in line and status == 0:
            s=0
    if s != 0:
        return s
    else:
        return(s)


# Remove the device
def disconnect(ip):
    status,stdout = load_shell.shell('adb disconnect {}:5555'.format(ip))


# Get information about the device
def check(ip):
    status,stdout = load_shell.shell('adb -s {}:5555 shell getprop  |grep ro.build.version.incremental'.format(ip))
    s=1
    if status == 0:
        for line in stdout:
            if b'20170425.143627' in line:
                s=0
    return(s)

