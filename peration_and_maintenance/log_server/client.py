#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pty
from functools import partial
import socket

def func_read(fd,sock):
    block = os.read(fd,1024)
    sock.send(block) #向服务端发送数据
    return block

if __name__ == '__main__':
#绑定socket
    host = '127.0.0.1'
    port = 12345
    addr = (host,port)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        s.connect(addr) #连接socket
    except socket.error:
        pty.spawn('bin/bash') #如果socket连接失败就进入shell交互
    else:
        myread = partial(func_read,sock=s)
        pty.spawn('bin/bash',master_read=myread)
    s.close()
