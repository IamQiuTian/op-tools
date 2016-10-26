#!/usr/bin/env python
#-*- coding:utf8 -*-

import re

class ssh_log_statistics:
	def __init__(self):
		self.logfile_path = "/var/log/secure" #secure文件路径
		self.ip_count = {} #ip计数
	
	def logfile_read(self):
		with open(self.logfile_path,'r') as my_log: #读取日志文件
			for line in my_log: 
				new_line = line.strip() #取出行，不要空白
				if re.search("Failed password",new_line): #如果成功匹配到就....
					every_segment = new_line.split() #以空白分割为列表
					ip = every_segment[-4] #取出列表中IP的部分
					if self.ip_count.has_key(ip): #如果计数字典中已经存在了此IP
						self.ip_count[ip] += 1 #就在此基础上给IP对应的数值加一，表示又出现了一次
					else:
						self.ip_count[ip]= 1 #否则就表示此IP是第一次出现
						
				else: #否则就是没有匹配到，就不进行任何操作
					pass
			#sort_li = reversed((sorted(zip(self.ip_count.itervalues(),self.ip_count.iterkeys())))) #从大到小排序
			#for l in sort_li: 
			#	#print (i)
			#    if l[0] > 30: #如果有IP的登录失败次数超过30次
			#	print (l) #就打印出来
			w = max(map(len,self.ip_count.keys()))
            		for k in self.ip_count:
			    if self.ip_count[k] >= 30:
		                print k.ljust(w),':',self.ip_count[k]	
				
				
if __name__ == '__main__':
	log = ssh_log_statistics()
	log.logfile_read()
