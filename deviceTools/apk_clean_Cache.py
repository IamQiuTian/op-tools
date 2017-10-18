#!/usr/bin/env python

import os
import sys
import time
import threading
import socket
from package import get_ip_list
from package import connect
from package import load_shell
from package import logging


# touch  log file
if not os.path.isdir('./log/install_log/'):os.makedirs('./log/install_log/')
# Log format
logname='./log/install_log/apk_clean_cache-%s.log' % time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

logging = logging.log(logname)

print("log output in {}".format(logname))

# init
action_list = []
ip_list = get_ip_list.get_ip_list()

# stop run apk
def package_stop(ip, package):
    s = load_shell.shell('adb -s {}:5555 shell am force-stop {}/{}.MainActivity'.format(ip, package, package))
    if s[0] == 0:
        logging.info("{} {}  stop run ok".format(ip, package))
    else:
        logging.error("{} {} stop run error".format(ip, package))


# start run apk
def package_start(ip, package):
    s = load_shell.shell('adb -s {}:5555 shell am start -n {}/{}.MainActivity'.format(ip, package, package))
    if s[0] == 0:
        logging.info("{} {}  start run ok".format(ip, package))
    else:
        logging.error("{} {} start run error".format(ip, package))


def package_init(ip, package):
    package_stop(ip, package)
    time.sleep(1)
    s = load_shell.shell('adb -s {}:5555 shell pm clear {}'.format(ip,package))
    if s[0] == 0:
        logging.info("{} {}  init ok".format(ip, package))
    else:
        logging.error("{} {} init error".format(ip, package))
    time.sleep(1)
    package_start(ip, package)



# run main
def main(package):
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
            package_init(ip, package)
            connect.disconnect(ip)
        except Exception as e:
            logging.warning([ip,e])
            continue


if __name__ == "__main__":
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1",44461))
    except Exception as e:
        logging.error(e)
        os._exit(1)

    try:
       package = sys.argv[1]
    except:
       print("input error!")
       os._exit(1)

    thread_num=10
    lock=threading.Lock()
    thread_pool=[]
    for a in range(thread_num):
        t = threading.Thread(target=main,args=(package,),name='t{}'.format(a))
        t.start()
        thread_pool.append(t)
        time.sleep(2)
    for t in thread_pool:
        t.join()

logging.info("END!!")
 
