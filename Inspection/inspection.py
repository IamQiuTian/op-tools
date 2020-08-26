#!/usr/bin/env python
# coding:utf8

import ConfigParser
import paramiko
import re
import threading
import time
import zipfile
import shutil
import os

#用来处理ssh连接
class Inspection(threading.Thread):
    #用于获取一个IP列表和备份应用列表
    def __init__(self):
        threading.Thread.__init__(self)
        cp = ConfigParser.SafeConfigParser()
        cp.read('conf.d/ip.cnf') 
        self.ip_list = cp.sections()
    	self.backup_file = ["nginx", "oracle", "mysql", "tomcat"]
    
    #用于处理ssh连接
    def ssh_connection(self, host, port, user, pwd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username=user, password=pwd)
        return ssh 

    #用于命令执行
    def SSH_Command_execution(self, conn, cmd):
        stdin,stdout,stderr = conn.exec_command(cmd)
        return stdout.read()

    #用于日志文件传输
    def Log_file_transfer(self, ip, port, username, password, spath, dpath):
        ssh = paramiko.Transport((ip, int(port)))
	ssh.connect(username=username, password=password)
	sftp = paramiko.SFTPClient.from_transport(ssh)
	sftp.get(spath,dpath)
        ssh.close()        
        
    
    #用于读取配置文件的用户名和密码
    def Conf(self, ip):
        cp = ConfigParser.SafeConfigParser()
        cp.read('ip.conf')
        port = cp.get(ip,"port")
        user = cp.get(ip,"user")
        passwd = cp.get(ip,"password")
        return ip, port, user, passwd
    
    #用于巡检功能整合
    def scaffold(self, ip,  cmd):
        ip, port, user, passwd = self.Conf(ip)
        conn = self.ssh_connection(ip, int(port), user, passwd)
        res = self.SSH_Command_execution(conn, cmd)
	conn.close()
        return res

    #用于日志功能整合
    def Log_shipping(self, ip, spath, dpath):
	ip, port, user, passwd = self.Conf(ip)
	self.Log_file_transfer(ip, port, user, passwd, spath, dpath)

#各种巡检项
class Main_body(Inspection):
    def __init__(self):
        Inspection.__init__(self)
   
    def Log_Check(self, ip):
	now_time  = time.strftime('%Y%m%d')
        self.scaffold(ip, "/usr/bin/python /root/log.py")
	self.Log_shipping(ip, "/root/error_log/"+now_time+".zip", "/root/error_log/"+ip+".zip")
	z = zipfile.ZipFile("/root/error_log/"+ip+".zip", 'r')
	f = z.namelist()
	for name in f: 
            f_handle=open("/root/error_log/"+name,"wb") 
       	    f_handle.write(z.read(name))       
            f_handle.close() 
	z.close()
	shutil.move("/root/error_log/root/error_log/"+now_time+".log", "/root/error_log/"+ip+".log")
	os.remove("/root/error_log/"+ip+".zip")
	return "/root/error_log/"+ip+".log"

    def Cpu_Check(self, ip):
        _cmd = self.scaffold(ip, "top -b -n 1")
        used = re.search('(\d\.\d)(\s|\%)',_cmd).group(1)
        return used

    def Memory_Check(self, ip):
        _cmd = self.scaffold(ip, "free -m")
        if re.search('(\.[a-z]+)(6|7)',self.scaffold(ip, "uname -a")).group(2) == "6":
            used = re.search('(buffers/cache:\s+)([0-9]+)',_cmd).group(2)
            total = re.search('(Mem:\s+)([0-9]+)',_cmd).group(2)
            count = float(used) / float( total) * 100
            return count
        elif re.search('(\.[a-z]+)(6|7)',self.scaffold(ip, "uname -a")).group(2) == "7":
            used = re.search('(Mem:)\s+(\d+)\s+(\d+)',_cmd).group(3)
            total = re.search('(Mem:)\s+(\d+)\s+(\d+)',_cmd).group(2)
            count = float(used) / float(total) * 100
            return count

    def Disk_Check(self, ip):
        _cmd = self.scaffold(ip, "df -h")
        gen_used = re.search('(\d+\%) (\/)',_cmd).group(1)
        return gen_used
        
    def Backup_Check(self, ip):
        cp = ConfigParser.SafeConfigParser()
        cp.read('ip.conf')
	time_nowadays = time.strftime('%Y%m%d')
	for path in self.backup_file:
	    try:
		if cp.get(ip, path):
		    tmp_1 = cp.get(ip, path)
		    file_path = tmp_1.format(time = time_nowadays)
		    _cmd = self.scaffold(ip, "[ -e %s ] && echo $?" %file_path)

		    if _cmd:
	                return True, path
		    else:
		        return False, path
		else:
                    pass
            except Exception as e:
		#print e
	        continue

    #数据库检查
    def Oracle_Check(self, ip): 
        pass
        
    #用于主体运行
    def run(self):
        for ip in self.ip_list:
            print ">>>"+ip
            print "+  cpu使用率为" + self.Cpu_Check(ip) + "%"
            print "+  内存使用率为%.1f" %self.Memory_Check(ip) + "%"
            print "+  磁盘使用率为" + self.Disk_Check(ip)

	    try :
	        status,path = self.Backup_Check(ip)
	    	if status:
		    print "+  今天的%s备份文件存在" %path
	        else:
		    print "+  今天的%s备份文件不存在" %path
	    except Exception as e:
		    pass
	    print  "+  错误日志存放在 %s" %self.Log_Check(ip)
	    print
	print "当前时间是 %s" %(time.strftime('%Y-%m-%d %H:%m:%S'))


if __name__ == "__main__":
    s = Main_body()
    s.start()
    for t in threading.enumerate():  
        if t is threading.currentThread():
            continue
        t.join() 
