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
						
				else: #否则就是没有匹配到，不进行任何操作
					pass
			for k,v in self.ip_count.iteritems():
				print (k,'ssh login frequency is',v)
				
				
if __name__ == '__main__':
	log = ssh_log_statistics()
	log.logfile_read()
