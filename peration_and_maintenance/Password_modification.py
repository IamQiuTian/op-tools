#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import sys #导入执行执行模块
import paramiko #导入ssh交互模块
import threading #导入多线程模块
 
def remote_comm(host,pwd,comm): 
    ssh = paramiko.SSHClient() #获取客户端对象
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #ssh登录时自动输入YES
    ssh.connect(host,username='root',password=pwd) #设置登录用户和密码
    stdin,stdout,stderr = ssh.exec_command(comm) #执行命令
    print(stdout.read(),) #打印命令执行的结果
    print(stderr.read(),) #打印错误输出
 
if __name__ == '__main__':
    if len(sys,argv) != 4: #如果命令格式不对的话，就打印正确的命令格式信息
        print("Usane:%s ipfile oldpass newpass") %sys.argv[0]
    else: #如果命令格式正确，就进入下一步执行
        ipfile = sys.argv[1] #获取ip文件
        oldpass = sys.argv[2] #获取当前远程服务器的密码
        newpass = sys.argv[3] #获取新的密码也就是要修改的密码
        ch_pwd = 'echo %s | passwd --stdin root' %newpass #执行密码修改的命令
        fobj = open(ipfile) #打开ip文件
        for line in fobj: #遍历ip文件
            ip = line.strip() #获取文件中每行的IP
            t = threading.Thread(target=trmote_comm,args(ip,oldpass,ch_pwd)) #将参数传递进函数，以多线程执行
            t.start #执行程序