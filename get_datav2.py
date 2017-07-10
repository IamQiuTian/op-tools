#!/usr/bin/python
#-*- coding=utf-8 -*-

import urllib2
import json
import time
import threading
import os
import sys
import csv
import ConfigParser


class Json_code(threading.Thread):
    #初始化了一些需要的变量,预期端口和用户名密码之类的
    def __init__(self,argv,dirpath):
        threading.Thread.__init__(self)
        self._argv = argv
        self.dirpath = dirpath
        #黑名单
        self.blacklist = ["61.167.56.41"]
        cp = ConfigParser.SafeConfigParser()
        cp.read('cdn_port.conf')
        self.port_list = [int(x) for x in cp.get(argv, "port").split(",")]
        try:
            #白名单
            self.ip_list = cp.get(argv, "ip").split(",")
        except Exception as e:
            self.ip_list = []
            pass
        self._time = time.strftime('%Y-%m-%d %H:%m')
        self.date = time.strftime('%Y%m%d')
        self.coeunt = 0
    
    #从接口获取数据,并进行json处理
    def Retrieve_data(self):
        _url = "https://kenan.3spear.com/outerapi/ports?tags=%s" %self._argv
        _headers = { 'API-KEY':'o7Y3qYaN','API-SECRET':'RhmuTCZQMuz1D00y','API-ID':'isurecloud'}
        _reques = urllib2.Request(url=_url,headers=_headers)
        _response = urllib2.urlopen(_reques)
        _result = _response.read()
        _data = json.loads(_result)
        #判断接口获取值为空就报警及退出
        if _data["data"]["list"]:
            return _data
        else:
            print "1"
            sys.exit(3)

    #判断端口和预期值的差
    def Port_alignment(self):
        #最终结果字典
        dict_port = {}
        #调用Retrieve_data函数获取ip及对应端口列表
        self.new_json = self.Retrieve_data()["data"]["list"]
        for key,value in  self.new_json.items():
            if key in self.blacklist:
                continue
            if self.ip_list:
                if key in self.ip_list:
                    continue
            else:
                pass
            _tmp = []
            for p in value:
                #如果端口在预计的列表里的话就pass
                if int(p) in self.port_list:
                    pass
                else:
                    #否则就扔到一个临时的列表里
                    _tmp.append(p)
            #然后IP和对应端口进行组装
            if _tmp:dict_port[key] = _tmp
        return dict_port

  
    def Csv(self, file_path, mode, ip, port, status ):
        write_file = open(file_path+".csv",mode)
        write_csv = csv.writer(write_file)
        write_csv.writerow([ip, port, status])
        write_file.flush()
         
   
#继承Json_code父类
class Utils(Json_code):
    def __init__(self,argv):
        Json_code.__init__(self,argv,dirpath)

    #将端口相关写入日志
    def Port_count(self):
        port_data = Json_code.Port_alignment(self)
        if len(port_data.values()) > 0:
            pass
        else:
           sys.exit(4)

        self.Csv(self.dirpath+"/"+self.date+"_tag", "a",self._argv,"","")
        status = 0
        for k,v in port_data.items():
            v = [l.encode('utf-8') for l in v ]
            self.coeunt += 1

            self.Csv(self.dirpath+"/"+self.date+"_tag", "a",  k, v, "incompatible")
        self.Csv(self.dirpath+"/"+self.date+"_tag", "a",  "", "", "")
	
    def Write_File(self):
        ip_count = self._argv+' : '+str(self.coeunt)
        if self.coeunt > 0:
            print ip_count
        else:
            sys.exit(3)

  
    #执行总体代码
    def run(self):
        self.Port_count()
        self.Write_File()
         
if __name__ == "__main__":
    argv = sys.argv[1]
    dirpath = sys.argv[2]
    t = Utils(argv)
    t.start()
    for t in threading.enumerate(): 
        if t is threading.currentThread(): 
            continue
        t.join() 
