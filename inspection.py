#/usr/bin/env python
#coding:utf8

import commands
import random
import string
import time
import re
import os
import sys

class Inspection(object):
    def __init__(self):
        self.mail_log = "/var/log/maillog"
        self.messages_log = "/var/log/messages"
        self.secure_log = "/var/log/secure"
	self.now_time = str(time.strftime('%Y%m%d'))
    
    def Log_Check(self):
	_path = "/root/error_log/" + self.now_time + ".log"
	f = open(_path,"a")
        with open(self.mail_log,'r') as mail:
            for l in mail:
                if "warning" in l or "error" in l:
			f.write("mail --> ")
			f.write(l)

        with open(self.messages_log,'r') as messages:
            for l in messages:
                if "warning" in l or "error" in l or "ERROR" in l or "Failed" in l:
			f.write("messages --> ")
                        f.write(l)

        with open(self.secure_log,'r') as secure:
            for l in secure:
                if "Failed" in l or "error" in l:
			f.write("secure --> ")
                        f.write(l)
	    f.close()

    def Memory_Check(self):
	_cmd = commands.getoutput("free -m")
        _used = re.search('(buffers/cache:\s+)([0-9]+)',_cmd).group(2)
        _total = re.search('(Mem:\s+)([0-9]+)',_cmd).group(2)
	_count = float(_used) / float( _total) * 100
	print "内存使用率为 %s" %_count,"%"	

    def Cpu_Check(self):
        _cmd = commands.getoutput("top -n 1")
	_used = re.search('(\d\.\d%)',_cmd).group(0)
	print "Cpu使用率为",_used
       
    def Disk_Check(self):
        _cmd = commands.getoutput("df -h")
	_gen_used = re.search('(\d+\%) (\/)',_cmd).group(1)
	_home_used = re.search('(\d+\%) (\/home)',_cmd).group(1)
	print "根的磁盘使用率为%s  home的磁盘使用率为%s" %(_gen_used,_home_used)   	
 
    def Backup_Check(self):
	_time_nowadays = str(time.strftime('%Y%m%d'))
	_time_yesterday = int(time.strftime('%Y%m%d')) - 1
	_path_1 = "/home/bak/usms-db%s.dmp" %_time_nowadays
	_path_2 = "/home/bak/usms-db%s.dmp" %str(_time_yesterday)
        _nowadays = os.path.exists(_path_1)
	_yesterday = os.path.exists(_path_2)
	if _nowadays:
            print "今天已经做了数据库备份!"
	else:
	    print "今天还没有做数据库备份,请及时备份!"
	if _yesterday:
	    print "昨天已经做了数据库备份了!"
	else:
	    print "昨天还没有做数据库备份,请及时备份!" 

    def main(self):
        t.Log_Check()
	_path = "/root/error_log/" + self.now_time + ".log"
	print '\033[1;31;40m'
	print "+++++++++++错误日志+++++++++++"
	print "错误日志存放在 %s 请及时查看" %_path
	print
	print "++++++内存、CPU、磁盘信息+++++"
	t.Memory_Check()
	t.Cpu_Check()
	t.Disk_Check()
	print
	print "++++++++数据库备份情况++++++++"
	t.Backup_Check()
	print 

if __name__ == "__main__":
    t = Inspection()
    t.main()
    
    print "当前时间是 %s" %(time.strftime('%Y-%m-%d %H:%m:%S'))
