#!/usr/bin/env python
# coding:utf8

import logging
import os
import sys
import time
import socket
import argparse
import threading
from package import get_ip_list
from package import connect
from package import load_shell
from package import get_apk_info
from package import file_hash_check
from package import logging


# touch  log file
if not os.path.isdir('./log/install_log/'):os.makedirs('./log/install_log/')
# Log format
logname='./log/install_log/install-%s.log' % time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

logging = logging.log(logname)

print("log output in {}".format(logname))

# init 
action_list = []
ip_list = get_ip_list.get_ip_list()
package_list = get_apk_info.get_all_apk()

# start run apk
def package_start(ip, packagelist):
    for package in packagelist:
        s = load_shell.shell('adb -s {}:5555 shell am start -n {}/{}.MainActivity'.format(ip, package, package))
        if s[0] == 0:
            logging.info("{} {}  start run ok".format(ip, package))
        else:
            logging.error("{} {} start run error".format(ip, package))

# stop run apk
def package_stop(ip, packagelist):
    for package in packagelist:
        s = load_shell.shell('adb -s {}:5555 shell am force-stop {}'.format(ip, package))
        if s[0] == 0:
            logging.info("{} {}  stop run ok".format(ip, package))
        else:
            logging.error("{} {} stop run error".format(ip, package))

# install apk file
def install(ip, packagelist):
    if "com.ledou.mhhy" in packagelist:
        load_shell.shell('adb -s {}:5555 shell su -c sh {}'.format(ip, "/sdcard/gs-android/game/Q8L_3288_100948_GAMES/18.MengHuanHuaYuan/ArchiveFile.sh"))
    for package in packagelist:
        code =  file_hash_check.hash_check(package)
        if code == "1":
            logging.error("{} {} hash check error".format(ip, package))  
            return
        
        packagepath = get_apk_info.get_apk_filepath(package)
        cmdline = 'adb -s {}:5555 install {}'.format(ip,packagepath)
        s = load_shell.shell(cmdline)
        if s[0] == 0:
            logging.info("{} {}  install ok".format(ip, package))
        else:
            logging.error("{} {} install error".format(ip, package))
    check_install(ip, packagelist)


# uninstall apk file
def uninstall(ip, packagelist):
    for package in packagelist:
        package_stop(ip, package.split())
        time.sleep(1) 
        cmdline = 'adb -s {}:5555 uninstall {}'.format(ip, package)
        s = load_shell.shell(cmdline)
        if s[0] == 0:
            logging.info("{} {}  uninstall ok".format(ip, package))
        else:
            logging.error("{} {} uninstall error".format(ip, package))

# reinstall apk file
def reinstall(ip, packagelist):
   uninstall(ip, packagelist)
   time.sleep(1)
   install(ip, packagelist)

# init apk
def init(ip, packagelist):
    for package in packagelist:
        package_stop(ip, package.split())
        time.sleep(1) 
        s2 = load_shell.shell('adb -s {}:5555 shell pm clear {}'.format(ip,package))
        if s2[0] == 0:
            logging.info("{} {}  init ok".format(ip, package))
        else:
            logging.error("{} {} init error".format(ip, package))
        time.sleep(1)
        package_start(ip, package.split())

# check apk install status
def check_install(ip, packagelist):
    for package in packagelist:
        cmdline = 'adb -s {}:5555 shell pm list packages |grep -w {}|wc -l'.format(ip,package)
        status, stdout = load_shell.shell(cmdline)
        if int(stdout[0]) != 1:
            logging.error("{} {} check install error ".format(ip, package))

def update_gs(ip, spath):
	zipname = os.path.split(spath.rstrip('/'))[1:]
	s1 = load_shell.shell('adb -s {}:5555 push {} /sdcard/'.format(ip, spath))
	if s1[0] != 0:
		logging.error("{} zip update error".format(ip))
		return
	else:
		logging.info("{} zip update Success".format(ip))
		
	s2 = load_shell.shell('adb -s {}:5555 shell su -c /data/unzip /sdcard/{} /sdcard/'.format(ip, zipname[0]))
	if s2[1][0].strip() != b"0":
		logging.error("{} {}".format(ip, s2[1]))
		return
	else:
		logging.info("{} unzip Success".format(ip))

# user input
def argp(mode, package, ip):
    if mode == "install":
        if package == "all":
            install(ip, package_list)
        else:
            install(ip, package.split())
    elif mode == "uninstall":
        if package == "all":
            uninstall(ip, package_list)
        else:
            uninstall(ip, package.split())
       
    elif mode == "reinstall":
         if package == "all":
             reinstall(ip, package_list)
         else:
             reinstall(ip, package.split())

    elif mode == "init":
         if package == "all":
            init(ip, package_list)
         else:
            init(ip, package.split())

    elif mode == "check":
         if package == "all":
             check_install(ip, package_list)
         else:
             check_install(ip, package.split())

    elif mode == "start":
         if package == "all":
             package_start(ip, package_list)
         else:
             package_start(ip, package.split())

    elif mode == "stop":
         if package == "all":
             package_stop(ip, package_list)
         else:
             package_stop(ip, package.split())
    elif mode == "update":
        update_gs(ip, package)
    else:
        print("input errror")
        os._exit(1)
        
# run main
def main(mode, package):
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
            argp(mode, package, ip)
            connect.disconnect(ip)
        except Exception as e:
            logging.warning([ip,e])
            continue

if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1",44451))
    except Exception as e:
        logging.error(e)
        os._exit(1)

    arg = argparse.ArgumentParser()
    arg.add_argument('-m','--mode',help='install or uninstall or reinstall or init or status or start or stop or update')
    arg.add_argument('-p','--package',help='select package')
    argd = arg.parse_args()
    if argd.mode is None or argd.package is None:
        print(arg.print_help())
        os._exit(1)

    thread_num=10
    lock=threading.Lock()
    thread_pool=[]
    for a in range(thread_num):
        t = threading.Thread(target=main,args=(argd.mode,argd.package),name='t{}'.format(a))
        t.start()
        thread_pool.append(t)
        time.sleep(2)
    for t in thread_pool:
        t.join()

logging.info("END!!")
