#!/usr/bin/env python
#-*- coding=utf-8 -*-

import requests
import json
import time

class Json_code(object):
    def __init__(self,url,headers):
        self.url = url
        self.headers = headers
        self.old_json = {}
        self.new_json = {}
        

    def Retrieve_data(self):
        _res = requests.get(self.url, headers=self.headers)
        _data = json.loads(_res.text)
        return _data

    def Dictionary_intersection(self):
        dict3 = {}
        self.old_json = t.Retrieve_data()["data"]["list"]
        time.sleep(300)
        self.new_json = t.Retrieve_data()["data"]["list"]
        self.new_json["192.168.1.1"] = ["10","11"]
        self.new_json["192.168.2.1"] = ["13","15"]
        self.new_json["117.149.134.139"] = ["8","9"]
        #self.old_json = {"127.0.0.1":["1","2","3"],"192.168.1.1":["2","3","4"]}
        #self.new_json ={"127.0.0.1":["1","2","3"],"192.168.1.1":["2","3","4"],"168.54.24.1":["8"]}

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
                
        return dict3

    def main(self):
        while True:
            try:
                _res = t.Dictionary_intersection()
                _tmp = []
                if _res:
                    for k,v in _res.items():
                        _tmp.append(k)
                        with open("tmp.log","a") as f:
                            for i in _tmp:
                                f.write("{time} {ip} 的端口发生改变,现值是{new_code},原值是{old_code}\n\n".format(time=time.strftime("%Y-%m-%d %A %X %Z",time.localtime()),ip=i,new_code=self.new_json[i],old_code=self.old_json[i]))
									
            except KeyError:
                if _res:
                    for k,v in _res.items():
                        if k not in self.old_json:
                            with open("tmp.log","a") as f:
                                f.write("{time} 新添加IP {ip}\n\n".format(time=time.strftime("%Y-%m-%d %A %X %Z",time.localtime()),ip=k)) 

                        
if __name__ == "__main__":
    url = "https://x.x.x.x"
    headers = { 'API-KEY':'xxxx',
                'API-SECRET':'yyyy',
                'API-ID':'dddd'}
					   
    t = Json_code(url,headers)
    t.main()
