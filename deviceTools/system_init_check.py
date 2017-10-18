#!/usr/bin/env python
# coding:utf8

import os
import time
import socket
import shutil
import logging
import argparse
import threading
import subprocess
from package import get_apk_info
from package import get_ip_list
from package import load_shell
from package import connect
from package import logging
from package import directory_hash_check

# touch  log file
if not os.path.isdir('./log/check_log/'):os.makedirs('./log/check_log/')
# Log format
logname='./log/check_log/check-%s.log' % time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
logging = logging.log(logname)

print("log output in {}".format(logname))

# init 
action_list = []
ip_list = get_ip_list.get_ip_list()
package_list = get_apk_info.get_all_apk()
tempdir = './log/check_log/temp'

# check apk install status
def apk_check_install(ip, packagelist):
    for package in packagelist:
        cmdline = 'adb -s {}:5555 shell pm list packages |grep -w {}|wc -l'.format(ip,package)
        status, stdout = load_shell.shell(cmdline)
        if int(stdout[0])  != 1:
            print(ip +"       "+get_apk_info.get_apk_filename(package))
            logging.error("{} {} not install ".format(ip, package))

# check apk version
def check_version(ip, packagelist):
    for package in packagelist:
        cmdline = 'adb -s {}:5555 shell dumpsys package {} |grep "versionName"'.format(ip, package)
        status, stdout = shell(cmdline)
        if len(stdout) == 0:
            logging.error("{} not install {}".format(ip, get_apk_info.get_apk_filename(package)))
            return
        newapkversion = get_apk_info.get_apk_version(package)
        apkversion = str(stdout[0].strip()).split("=")[1].strip("\'")
        if apkversion != newapkversion:
            print(ip +"       "+get_apk_info.get_apk_filename(package))
            logging.error("{} {} version not nows,the version is {}".format(ip,get_apk_info.get_apk_filename(package),apkversion))

# directory check verified
def dir_push_check(ip):
     cmdline = 'adb -s {}:5555 shell ls /sdcard/gs-android | wc -l '.format(ip)
     status,stdout = load_shell.shell(cmdline)
     if stdout[0]  == "1":
         print(ip +"       "+ "/sdcard/gs-android")       
         logging.error("{} directory not exist".format(ip))


# Directory integrity check
def dir_hash_check(ip):
     if not os.path.isdir('./log/check_log/temp'):os.makedirs('./log/check_log/temp')
 
     remdir = tempdir + "/" + ip
     loaddir = "/home/deploy-pags/gs-android/"

     cmdline = 'adb -s {}:5555 pull  /sdcard/gs-android  {} '.format(ip,remdir)
     result = load_shell.shell(cmdline)
     shutil.rmtree(remdir+"/"+"log")
     if result[0] != 0:
         logging.error("{} /sdcard/gs-android download error".format(ip))
     loaddirmd5 = directory_hash_check.md5(loaddir)
     remdirmd5 = directory_hash_check.md5(remdir)
     if loaddirmd5 != remdirmd5:
         print(ip +"       "+ "/sdcard/gs-android")
         logging.error("{} gs-android hash check error".format(ip))
     shutil.rmtree(remdir)

def shell(cmdline,wait=0):
    # Execute the shell
    a = subprocess.Popen(cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # Wait for 120 seconds after the command is executed
    if wait == 0:
        status=a.wait(timeout=60*20)
    else:
        time.sleep(wait)
        status=a.kill()
    # Output the command execution result
    stdout=a.stdout.readlines()
    # Write errors and write errors after command execution fails
    return(status,stdout)

# check disable_system_app.sh and enable_system_app.sh
def system_init_app_check(ip):
   with open("./conf.d/init_disabled","r") as f:
       disabled_list = f.readlines()

   for package in disabled_list:
       cmd = "adb -s {}:5555 shell pm list package -e | grep -w {}".format(ip, package)
       dis = shell(cmd)
       if dis[0] == 0:
           print(ip +"       "+ package.strip())  
           logging.error("{} {} not disable".format(ip, package))

def system_init_config_check(ip):
    # check port
    port = shell("adb -s {}:5555 shell getprop {}".format(ip, "persist.adb.tcp.port"))
    if port[1][0].strip() != b"5555":
        print(ip +"       "+ "listen port not 5555")
        logging.error("{} listen port not 5555".format(ip))

    # check timezone
    timezone = shell("adb -s {}:5555 shell getprop {}".format(ip, "persist.sys.timezone"))
    if timezone[1][0].strip() != b"Asia/Shanghai":
        print(ip +"       "+ "timezone not Asia/Shanghai")
        logging.error("{} timezone not Asia/Shanghai".format(ip)) 

    # check country
    country = shell("adb -s {}:5555 shell getprop {}".format(ip, "persist.sys.country"))
    if country[1][0].strip() != b"CN":
        print(ip +"       "+ "country not CN")
        logging.error("{} country not CN".format(ip))
  
    # check language
    language = shell("adb -s {}:5555 shell getprop {}".format(ip, "persist.sys.language"))
    if language[1][0].strip() != b"zh":
        print(ip +"       "+ "language not zh")
        logging.error("{} language not zh".format(ip))

    # check Notice
    notice = shell("adb -s {}:5555 shell settings get global {}".format(ip, "heads_up_notifications_enabled"))
    if notice[1][0].strip() != b"0":
        print(ip +"       "+ "heads_up_notifications_enabled not 0")
        logging.error("{} heads_up_notifications_enabled not 0".format(ip))
    
    # check warning notice
    warn = shell("adb -s {}:5555 shell settings get global {}".format(ip, "package_verifier_enable"))
    if warn[1][0].strip() != b"0":
        print(ip +"       "+ "package_verifier_enable not 0")
        logging.error("{} package_verifier_enable not 0".format(ip))
         
    # check Input
    inputd = shell("adb -s {}:5555 shell settings get secure {}".format(ip, "default_input_method"))
    if inputd[1][0].strip() != b"com.google.android.inputmethod.pinyin/.PinyinIME":
        print(ip +"       "+ "default_input_method error")
        logging.error("{} default_input_method error".format(ip))
    
    # check wm size
    wm_size = shell("adb -s {}:5555 shell wm size | grep 1280x720 | wc -l".format(ip))
    if wm_size[1][0].strip() != b"1":
        print(ip +"       "+ "wm size not 1280x720")
        logging.error("{} wm size not 1280x720")


# user input
def argp(mode, ip):
    if mode == "install":
        apk_check_install(ip, package_list
)
    elif mode == "version":
        check_version(ip, package_list)    
   
    elif mode == "dir":
        dir_push_check(ip)
        dir_hash_check(ip)

    elif mode == "init":
        system_init_app_check(ip)
        system_init_config_check(ip)


def main(mode):
    for ip in ip_list:
        try:
            try:
                lock.acquire()
                if ip in action_list:
                    continue
                else:
                    action_list.append(ip)
                    s = connect.connect(ip)
                    if s != 0:
                        logging.warning('{} not connect !!!'.format(ip))
                        continue

                    if connect.check(ip) != 0:
                        logging.warning('{} check err !!!'.format(ip))
                        continue
            finally:
                lock.release()
            argp(mode, ip)
            connect.disconnect(ip)
        except Exception as e:
            logging.warning([ip,e])
            continue    

if __name__ == "__main__":
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1",44459))
    except Exception as e:
        logging.error(e)
        os._exit(1)

    arg = argparse.ArgumentParser()
    arg.add_argument('-m','--mode',help='install or version or dir or init')
    argd = arg.parse_args()
    if argd.mode is None:
        print(arg.print_help())
        os._exit(1)
    if argd.mode == "version" or argd.mode == "install" or argd.mode == "dir" or argd.mode == "init":
        print("ip                 package")

    thread_num=10
    lock=threading.Lock()
    thread_pool=[]
    for a in range(thread_num):
        t = threading.Thread(target=main,args=(argd.mode,),name='t{}'.format(a))
        t.start()
        thread_pool.append(t)
        time.sleep(2)
    for t in thread_pool:
        t.join()
logging.info('end!!')
