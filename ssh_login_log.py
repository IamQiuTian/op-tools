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
				#if re.search("Accepted password",new_line): #匹配登录成功的的
				if re.search("Failed password",new_line): #匹配登录失败的
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
	
	
'''
110.19.222.168  : 3
110.19.222.242  : 2
123.119.130.73  : 1
1.30.133.230    : 1
123.119.138.59  : 1
221.218.24.41   : 11
1.31.59.7       : 2
1.30.134.69     : 1
123.119.140.238 : 5
111.202.109.162 : 16
125.33.175.93   : 5
1.31.59.167     : 1
1.30.161.101    : 4
106.121.12.167  : 4
1.30.161.252    : 7
1.31.57.200     : 2
1.31.57.201     : 2
123.119.142.180 : 2
1.31.57.163     : 3
'''
