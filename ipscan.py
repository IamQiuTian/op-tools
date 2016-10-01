#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os #导入系统命令执行模块
import threading #导入多线程模块
def ping(ip): #设置ping命令操作，传递ip参数
    res = os.system('ping -c2 %s &> /dev/null' %ip) #执行ping传递来的ip参数
    if res: #如果返回值为1，就表示主机非存活状态
        print('%s:down') %ip
    else: #否则主机存活
        print('%s:up') %ip
		
for i in range(1,255):
    ipaddr = '10.141.50.%s' %ip #使用for循环补齐10.141.50.1-255
    t = threading.Thread(target=ping,args=(ipaddr)) #调用多线程，将ipaddr传递进函数参数中
    t.start() #执行程序
