#!/usr/bin/env python
#-*- coding=utf-8 -*-

#import requests
import urllib2
import json
import time
import smtplib
from email.mime.text import MIMEText


class Json_code(object):
    def __init__(self,url,headers):
        self.url = url
        self.headers = headers
        self.old_json = {}
        self.new_json = {}

        self.mailto_list=["xxx@163.com","yyy@163.com"]
        self.mail_host="smtp.163.com" 
        self.mail_user="user"
        self.mail_pass="pass"
        self.mail_postfix="163.com"
        
    def Retrieve_data(self):
        #_res = requests.get(self.url, headers=self.headers)
        _reques = urllib2.Request(url=self.url,headers=self.headers)
        _response = urllib2.urlopen(_reques)
        _result = _response.read()
        
        _data = json.loads(_result)
        if _data:
            return _data
        else:
            t.Send_mail(self.mailto_list,"接口异常","接口获取数据为空!")
            

    def Dictionary_intersection(self):
        dict3 = {}
        self.old_json = t.Retrieve_data()["data"]["list"]
        time.sleep(1800)
        self.new_json = t.Retrieve_data()["data"]["list"]
        #测试IP不一致情况
        #self.new_json["192.168.1.1"] = ["10","11"]
        #self.old_json["192.168.2.1"] = ["13","15"]
        #测试数据不一致情况
        #self.new_json["117.149.134.139"] = ["8","9"]

        l3 = []
        for key,value in  self.new_json.items():
            if key in self.old_json:
                l1 = self.new_json[key]
                l2 = self.old_json[key]
                for i in l1:
                    if i in l2:
                        pass
                    else:
                        l3.append(i)
                if len(l3) == 0:
                    pass
                else:
                    dict3[key] = l3
                    l1 = []
                    l2 = []
                    l3 = []
            else:
                dict3[key] = value
    
        for key,value in self.old_json.items():
            if key not in self.new_json:
                dict3[key] = value
            else:
                pass
        return dict3


    def Send_mail(self,to_list,sub,content):
        me="Qiudays"+"<"+self.mail_user+"@"+self.mail_postfix+">"  
        msg = MIMEText(content,_subtype='plain',_charset='utf-8') 
        msg["Accept-Language"]="zh-CN"
        msg["Accept-Charset"]="ISO-8859-1,utf-8" 
        msg['Subject'] = sub  
        msg['From'] = me  
        msg['To'] = ";".join(to_list)  
        try:  
            server = smtplib.SMTP_SSL()  
            server.connect(self.mail_host, port=465)  
            server.login(self.mail_user, self.mail_pass)  
            server.sendmail(me, to_list, msg.as_string())  
            server.close()  
            return True  
        except Exception as e:  
            print(str(e)) 
            return False 

    def Main(self):
        while True:
            try:
                _res = t.Dictionary_intersection()
                _tmp = []
                if _res:
                    for k,v in _res.items():
                        _tmp.append(k)
                        with open("tmp.log","a") as f:
                            for i in _tmp:
                                self.text = "{time} {ip} 的端口发生改变,现值是{new_code},原值是{old_code}\n\n".format(time=time.strftime("%Y-%m-%d %A %X %Z",time.localtime()),ip=i,new_code=self.new_json[i],old_code=self.old_json[i])
                                f.write(self.text)
                        t.Send_mail(self.mailto_list,"端口发生变化",self.text)

            except KeyError:
                if _res:
                    for k,v in _res.items():
                        if k not in self.old_json:
                            self.text2 = "{time} 新添加IP {ip}\n\n".format(time=time.strftime("%Y-%m-%d %A %X %Z",time.localtime()),ip=k)
                            with open("tmp.log","a") as f:
                                f.write(self.text2)
                            t.Send_mail(self.mailto_list,"IP发生变化",self.text2)

                        if k in self.old_json and not self.new_json:
                            self.text3 = "{time} 减少一个IP {ip}\n\n".format(time=time.strftime("%Y-%m-%d %A %X %Z",time.localtime()),ip=k) 
                            with open("tmp.log","a") as f:
                                f.write(self.text3)
                            t.Send_mail(self.mailto_list,"IP发生变化",self.text3)
                            
            
if __name__ == "__main__":
    url = "https://x.x.x.x"
    headers = { 'API-KEY':'xxxx',
                'API-SECRET':'xxxxx',
                'API-ID':'xxxx'}
    t = Json_code(url,headers)
    t.Main()
