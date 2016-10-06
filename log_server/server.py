#!/usr/bin/env python
# -*- coding:utf-8 -*-

#创建数据库： CREATE DATABASE test;
#创建表 ： CREATE TABLE records(id int(16) not null primary key auto_increment,time datetime,host varchar(20),comm varchar(200));

import socket
import threading
import MySQLdb as mysql
import re

class LogServer(object):
    def __init__(self,sock): #创建数据库游标和套接字
        self.sock = sock #获取套接字
        self.conn = mysql.connect(host='localhost',user='root',passwd='',
                                  db='test',charset='utf8')
        self.cursor = self.conn.cursor()  #获取数据库游标

    def write_mysql(self,host,comm): #数据库写入的内容
        sql = "insert into records (time,host,comm) values (Now(), '%s','%s')" % (host,comm)
        self.cursor.execute(sql) #执行sql语句
        self.conn.commit() #提交操作

    def __call__(self):
        alist = [] #数据列表
        host = self.sock.getpeername()[0] #获取客户端主机名
        while True:
            buf = self.sock.recv(1024) #接收数据
            if not buf: #数据为空就退出
                break
            alist.append(buf) #将数据添加到数据列表
            line = ''.join(alist) #将数据列表里的数据拼接起来，避免接收到'd','i','r'之类的单字符
            if '\r\n' in line:
                m = re.search('(]#|]\$)(.+)\r\n',line) #查找列表中以]#、]$开头以回车结尾的字符或者单独的二者之一，例：[root@tengxun-vm /]# ls -l \r\n
                if m: #如果匹配成功
                    comm = m.group(2) #获取命令操作，例如[root@tengxun-vm /]# ls -l \r\n中的ls -l
                    self.write_mysql(host,comm) #将主机名和命令操作写入数据库
                    alist = [] #清空数据列表，进入下一次循环

        self.sock.close() #关闭套接字
        self.cursor.close() #关闭游标
        self.conn.close() #关闭数据库连接



if __name__ == '__main__':
#绑定套接字
    host = ''
    port = 12345
    addr = (host,port)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(addr)
    s.listen(1)

#运行程序
    while True:
        cli_sock,cli_addr = s.accept()
        t = threading.Thread(target=LogServer(cli_sock))
        t.setDaemon(1)
        t.start()
    s.close()