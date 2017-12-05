#!/usr/bin/env python
# coding:utf8

import time
import os
import socket
import logging
import threading
from package import connect
from package import get_ip_list
from package import load_shell
from package import logging

# init
action_list = []
ip_list = get_ip_list.get_ip_list()

# touch log file
if not os.path.isdir('./log/device_log/'):os.makedirs('./log/device_log/')
# log format
logname='./log/device_log/system_device-%s.log' % time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

logging = logging.log(logname)

print("log output in {}".format(logname))

# device screencap
def screencap(ip):
    logging.info('pull {} screencap'.format(ip))
    load_shell.shell('adb -s {}:5555 shell screencap -p /sdcard/screen.png'.format(ip))
    load_shell.shell('adb -s {}:5555  pull /sdcard/screen.png ./log/device_log/screencap/{}.png'.format(ip,ip))

# device run log
def log(ip):
    logging.info('pull {} log'.format(ip))
    log_dir=os.path.join('./log/device_log/log/',ip)
    load_shell.shell('adb -s {}:5555  pull /sdcard/gs-android/log/ {}'.format(ip,log_dir))


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
                    logging.info("{} connect ok".format(ip))
            finally:
                lock.release()

            screencap(ip)
            log(ip)
            time.sleep(2)
            connect.disconnect(ip)
            logging.info('{} ok!!!'.format(ip))

        except Exception as e:
            logging.warning([ip,e])
            continue


if __name__ == "__main__":
   try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1",44457))
   except Exception as e:
        logging.error(e)
        os._exit(1)

   thread_num = 10
   lock=threading.Lock()
   thread_pool=[]

   for a in range(thread_num):
       t = threading.Thread(target=main,name='t{}'.format(a))
       t.start()
       thread_pool.append(t)
       time.sleep(2)
   for t in thread_pool:
       t.join()

logging.info('end!!')
