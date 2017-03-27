#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import re #导入正则匹配模块
 
def count_patt(fname,patt):
    patt_dict = {} #设置统计字典，{IP：次数}
    cpatt = re.compile(patt) #获取正则对象
    with open(fname) as fobj: #遍历日志文件
        for line in fobj:
            m = cpatt.search(line) #按行匹配正则
            if m: #如果返回值不为None值得话
                key = m.group() #将匹配到的值设为KEY
                patt_dict[key] = patt_dict.get(key,0) + 1 #如果KEY不在字典中就设值为1，否则就加1
    return patt_dict #返回字典
 
 
if __name__ == '__main__':
    log_file = '/var/log/httpd/access_log' #日志文件路径
    ip_patt = '^(\d+\.){3}\d+' #匹配IP ，x.x.x.x
    br_patt = 'Mozilla|Chrome' #匹配游览器类型

    print(count_patt(log_file,ip_patt)) #打印字典
    print(count_patt(log_file,br_patt))
