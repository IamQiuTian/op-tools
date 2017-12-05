#!/bin/python
import threading
import socket
import os
from package import get_ip_list
from package import connect


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
                        print(ip+ "    "  +"down")
                        continue

                    if connect.check(ip) != 0:
                        print(ip+ "    " +"not connect")
                        continue
            finally:
                lock.release()
            connect.disconnect(ip)
        except Exception as e:
            print(ip+ "    " +"not connect")
            continue

if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1",44466))
    except Exception as e:
        print("The port has been monitoring")
        os._exit(1)

    print("ip              status")

    action_list = []
    ip_list = get_ip_list.get_ip_list()
    thread_num = 50 
    lock=threading.Lock()
    thread_pool=[]
    for a in range(thread_num):
        t = threading.Thread(target=main,name='t{}'.format(a))
        t.start()
        thread_pool.append(t)
    for t in thread_pool:
        t.join()
