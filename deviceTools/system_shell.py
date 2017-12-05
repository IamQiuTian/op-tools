#!/usr/bin/env pyhton
# coding:utf8

import os
import time
import socket
import logging
import argparse
import threading
import subprocess
from package import load_shell
from package import connect
from package import get_ip_list
from package import logging

# touch file log
if not os.path.isdir('./log/run_log/'):os.makedirs('./log/run_log/')
# log format
logname='./log/run_log/system_tools-%s.log' % time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

logging = logging.log(logname)

print("log output in {}".format(logname))

# init
action_list = []
ip_list = get_ip_list.get_ip_list()

# script shell
def dshell(ip):
    cmd = "su -c pm disable com.android.calculator2"
    cmdline = "adb -s {}:5555 shell {}".format(ip, cmd)
    if cmd == "reboot":
        cmdline = "adb -s {}:5555 {}".format(ip, cmd)
        load_shell.shell(cmdline, wait=2)
        logging.info("{} Restarting".format(ip))
    else:
        stdout = load_shell.shell(cmdline)
        logging.info("{} {} result {}".format(ip, cmd, stdout))


# run main
def main():
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
            dshell(ip)
            connect.disconnect(ip)
        except Exception as e:
            logging.warning([ip,e])
            continue

if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1",44454))
    except Exception as e:
        logging.error(e)
        os._exit(1)

    thread_num=10
    lock=threading.Lock()
    thread_pool=[]
    for a in range(thread_num):
        t = threading.Thread(target=main,name='t{}'.format(a))
        t.start()
        thread_pool.append(t)
        time.sleep(2)
    for t in thread_pool:
        t.join()

logging.info("END!!")
