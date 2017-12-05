#!/usr/bin/env python
# coding:utf8

import logging
import os
import argparse
import threading
import socket
import time
import logging
from package import load_shell
from package import get_ip_list
from package import connect
from package import logging

# touch log file
if not os.path.isdir('./log/run_log/'):os.makedirs('./log/run_log/')
# log format
logname='./log/run_log/device_file-%s.log' % time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

logging = logging.log(logname)

print("log output in {}".format(logname))

# init 
action_list = []
ip_list = get_ip_list.get_ip_list()

# down file to local
def pull(ip, src, dst):
    s = load_shell.shell('adb -s {}:5555 pull {} {}'.format(ip, src, dst))
    if s[0] == 0:
        logging.info("{} {} file pull ok".format(ip, src))
    else:
        logging.error("{} {} file pull error".format(ip, src))

# push file to device
def push(ip, src, dst):
    s = load_shell.shell('adb -s {}:5555 push  {} {}'.format(ip, src, dst))
    if s[0] == 0:
        logging.info("{} {} file push ok".format(ip, src))
    else:
        logging.error("{} {} file push error".format(ip, src))

# run main
def main(mode, src, dst):
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
            if mode == "pull":
                pull(ip, src, dst)
            elif mode == "push":
                push(ip, src, dst)
            else:
                print("Args error!")
                os._exit(1)
            connect.disconnect(ip)
        except Exception as e:
            logging.warning([ip,e])
            continue

    

if __name__ == "__main__":
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1",44453))
    except Exception as e:
        logging.error(e)
        os._exit(1)

    arg = argparse.ArgumentParser()
    arg.add_argument('-m','--mode',help='pull or push file')
    arg.add_argument('-s','--src',help='src file path')
    arg.add_argument('-d','--dst',help='dst file path')
    argd = arg.parse_args()
    if argd.mode is None or argd.src is None or argd.dst is None:
        print(arg.print_help()) 
        os._exit(1)
     
    thread_num=10
    lock=threading.Lock()
    thread_pool=[]
    for a in range(thread_num):
        t = threading.Thread(target=main,args=(argd.mode, argd.src, argd.dst),name='t{}'.format(a))
        t.start()
        thread_pool.append(t)
        time.sleep(2)
    for t in thread_pool:
        t.join()

logging.info("END!!")
