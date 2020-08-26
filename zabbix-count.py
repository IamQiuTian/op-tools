#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import urllib2
from urllib2 import URLError
import os.path
import sys
import time
import datetime
import requests
import csv
import smtplib
import unicodecsv as ucsv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# zabbix服务端地址
zabbix_addresses=['http://ops-monitor.xxoo.com,  username, password']
# 企业微信webhook
webhookUrl='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxoo'
# 邮件相关参数
sendUsr =  "***@163.com"    
recUsr = "***@163.com"
smtpServer = "smtp.163.com"
maiPass = "*****"


class ZabbixTools:
    def __init__(self,address,username,password):

        self.address = address
        self.username = username
        self.password = password

        self.url = '%s/api_jsonrpc.php' % self.address
        self.header = {"Content-Type":"application/json"}


    # zabbix用户登录，获取auth
    def user_login(self):
        data = json.dumps({
                           "jsonrpc": "2.0",
                           "method": "user.login",
                           "params": {
                                      "user": self.username,
                                      "password": self.password
                                      },
                           "id": 0
                           })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print("Auth Failed, please Check your name and password:", e.code)
        else:
            response = json.loads(result.read())
            result.close()
            #print response['result']
            self.authID = response['result']
            return self.authID

    # 获取报警事件
    def event_get(self,time_from,time_till):
        data = json.dumps({
                           "jsonrpc": "2.0",
                           "method": "alert.get",
                           "params":{
                               # https://www.zabbix.com/documentation/3.4/zh/manual/api/reference/alert/object    
                               "output":["eventid","subject","hosts"],
                               "selectHosts": "hosts",
                               "time_from":self.timecovert(time_from),
                               "time_till":self.timecovert(time_till)
                           },
                           "auth": self.user_login(),
                           "id":1              
        })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print("Error as ", e)
        else:
            response = json.loads(result.read())
            result.close()
            issues = response['result']
            return issues
    
    # 通过server ID 获取主机名
    def get_hosts(self):
        data = json.dumps({
                           "jsonrpc": "2.0",
                           "method": "host.get",
                           "params":{
                               "output":["name"], 
                               #"hostids": "%s" % (hostid), 
                           },
                           "auth": self.user_login(),
                           "id":1              
        })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print("Error as ", e)
        else:
            response = json.loads(result.read())
            result.close()
            issues = response['result']
            return issues
    
    # 转换时间戳
    def timecovert(self,stringtime):
        timeArray = time.strptime(stringtime, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp 
    
        

# 用于离线搜索主机名
def hostSearch(allHost,hostid):
    for i in allHost:
        if hostid == i['hostid']:
            return i['name']
# 通过企业微信的webhook 向群组发送消息
def sendWeixin(url,s):
   headers = {"Content-Type": "text/plain"}
   data = {
      "msgtype": "text",
      "text": {
         "content": s,
      }
   }
   r = requests.post(
      url,headers=headers, json=data)
   return r.text

# 发送邮件
def sendMail(sendUsr, recUsr, smtpServer, mail_pass, subject, csvPath):
    message = MIMEMultipart()
    message['From'] = Header(sendUsr, 'utf-8')
    message['To'] =  Header(recUsr, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    
    message.attach(MIMEText(subject,'plain','utf-8'))
    basename = os.path.basename(csvPath)

    att = MIMEText(open(csvPath, 'rb').read(), 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="%s"'% basename.encode('gb2312')
    message.attach(att)
    
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(smtpServer, 25)
        smtpObj.login(sendUsr,mail_pass)  
        smtpObj.sendmail(sendUsr, recUsr, message.as_string())
        print "send mail ok"
    except Exception as e:
        print e

    

if __name__ == "__main__":
    argList = sys.argv
    if len(argList) != 3:
        time_from = (datetime.datetime.now()  + datetime.timedelta(hours = -12)).strftime("%Y-%m-%d %H:%m:%S")
        time_till = datetime.datetime.now().strftime("%Y-%m-%d %H:%m:%S")
    else:
        try:
           time_from =  argList[1]
           time_till =  argList[2]
        except Exception as e:
            print(e)
            sys.exit(2)
           


    for zabbix_addres in zabbix_addresses:
        address,username,password = zabbix_addres.split(',')
        z = ZabbixTools(address=address, username=username, password=password)
        #time_from = "2020-08-18 13:50:00"
        #time_till = "2020-08-18 14:10:32"
        content = z.event_get(time_from, time_till)
        allHost = z.get_hosts()
        
        eventCount = {}
        s_tmp = {}
        tmp = []
        jnum = 0 
        # 报警类型关键字
        statusList = [u'磁盘',u'内存',u'IO负载','Redis',
                      'disk','mongo',u'监控丢失',u'系统负载',
                      u'运行状态进程',u'出口流量',u'入口流量',
                      u'重启',u'系统用户信息被更改',u'服务状态异常',
                      u'云主机steal time',]
       
        for dic in content:
            # 这个判断用于报警事件去重        
            if  u"故障" in dic["subject"] and dic["subject"] not in tmp:
                #print(dic["subject"])
                jnum += 1
                hostname = hostSearch(allHost,dic['hosts'][0]['hostid'])
                for s in statusList:
                    if s in dic["subject"]:
                        # 以下语句均用于字典嵌套
                        if hostname not in eventCount.keys():
                            s_tmp[s] = 1
                            eventCount[hostname] = dict(s_tmp)
                        elif  hostname in eventCount.keys():
                            if s in eventCount[hostname].keys():
                                eventCount[hostname][s] += 1
                            else:
                                s_tmp[s] = 1
                                eventCount[hostname] =  dict(s_tmp)
                                
                s_tmp = {}
                
                tmp.append(dic["subject"])           
        
        
        resList = []
                
        for k,v in eventCount.items():
            aertmes = json.dumps(v).decode("unicode-escape").strip('{}').split(',')
            if len(aertmes) == 1:
                TMPr = json.dumps(aertmes[0].replace('"',"")).decode("unicode-escape")
                tmpList = [k,TMPr]
                resList.append(tmpList)   
            else:
                for l in aertmes:
                    tmpList = [k,l]
                    resList.append(tmpList)
                    
                    
        # 降序排列            
        def new_func(c):return int(c[1].split(":")[1].replace('"',"").strip())

        resList.sort(key=new_func,reverse=True)
        s =  u"* 从%s 到 %s 的报警事件共 %s件" %(time_from,time_till,jnum) 
        print("\n")
        s =  s+"\n"+u"主机              报警类型   数量"
        
        # 写入表格附件和发送消息内容
        todayTime = datetime.datetime.now().strftime("%Y-%m-%d")
        filePath = './zabbixCount_%s.csv'%todayTime 
        with open(filePath, 'wb') as f:
            wcsv = ucsv.writer(f, encoding = 'gbk')
            wcsv.writerow([u"* 从%s 到 %s 的报警事件共 %s件"%(time_from,time_till,jnum)])
            wcsv.writerow([u"主机",u"报警类型",u"数量"])
            for r in resList:
               s = s+"\n"+r[0]+"   "+r[1]
               rltmp = r[1].replace('"','').split(':')
               wcsv.writerow([r[0],rltmp[0],rltmp[1].replace(" ","")])  
        
        # 发送邮件
        subject = u"zabbix报警统计—%s"%todayTime
        sendMail(sendUsr,recUsr,smtpServer,maiPass,subject,filePath)
        # 发送企业微信消息
        resCode = sendWeixin(webhookUrl,s)
        print resCode
