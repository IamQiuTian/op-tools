#!/usr/bin/env python
#-*- coding:utf8 -*-

import re
import requests
#import commands
import smtplib
from email.mime.text import MIMEText

class err_send_mail(object):
	def __init__(self):
	#配置邮件设置，以163邮箱为例
		self.mailto_list=["收件邮箱"] 
		self.mail_host="smtp.163.com" 
		self.mail_user="用户名"
		self.mail_pass="密码"
		self.mail_postfix="163.com"
	#发送邮件
	def send_mail(self,to_list,sub,content):  
		me="发件人名"+"<"+self.mail_user+"@"+self.mail_postfix+">"  
		msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
		msg['Subject'] = sub  
		msg['From'] = me  
		msg['To'] = ";".join(to_list)  
		try:  
			server = smtplib.SMTP()  
			server.connect(self.mail_host)  
			server.login(self.mail_user,self.mail_pass)  
			server.sendmail(me, to_list, msg.as_string())  
			server.close()  
			return True  
		except Exception, e:  
			print str(e)  
			return False
	
	#配置邮件发送条件
	def	web_status_code(self):
		#code = commands.getoutput("curl -I www.unbook.cn")
		#status_code = re.search('HTTP/1.1\s([0-9]+)\s(\w+)',code).group(1)
		info_status = requests.get('http://www.unbook.cn/status_code.html').status_code #获取网页返回码，200为可以正常访问
		try:
			if info_status == 200:
				status = u"网站正常"
				content = u'网站返回状态码为 {code}'.format(code=info_status)
				#self.send_mail(self.mailto_list,status,content)
				print ("网站可以访问")
			else:
				status = u"网站故障" 
				content = u'网站返回状态码为 {code}'.format(code=info_status)
				self.send_mail(self.mailto_list,status,content)
				print ("网站故障")
		except Exception,e:
			print (e)
			return False
  
if __name__ == '__main__':
	err =  err_send_mail()
	err.web_status_code()  
