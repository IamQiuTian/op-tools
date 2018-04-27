#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys,os
import urllib, urllib2
import base64
import hmac
from hashlib import sha1
import time
import uuid
import json
import gzip
import shutil
import requests
import threading


# 设置秘钥
access_key_id = 'xxxxxxxxxxxx'
access_key_secret = 'xxxxxxxxxxxx'
cdn_server_address = 'https://cdn.aliyuncs.com'
CONFIGSECTION = 'Credentials'

# 定义编码utf8
def percent_encode(str):
    res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res

# 计算签名
def compute_signature(parameters, access_key_secret):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])

    canonicalizedQueryString = ''
    for (k,v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)

    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])

    h = hmac.new(access_key_secret + "&", stringToSign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature

# 拼接URL
def compose_url(user_params):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    parameters = { \
            'Format'        : 'JSON', \
            'Version'       : '2014-11-11', \
            'AccessKeyId'   : access_key_id, \
            'SignatureVersion'  : '1.0', \
            'SignatureMethod'   : 'HMAC-SHA1', \
            'SignatureNonce'    : str(uuid.uuid1()), \
            'TimeStamp'         : timestamp, \
    }

    for key in user_params.keys():
        parameters[key] = user_params[key]

    signature = compute_signature(parameters, access_key_secret)
    parameters['Signature'] = signature
    url = cdn_server_address + "/?" + urllib.urlencode(parameters)
    return url

# 解析api返回的json， 返回日志下载列表
def resolve_Json(jsonData):
    down_log_list = []
    logDist = {}
    url_Dict = jsonData["DomainLogModel"]["DomainLogDetails"]["DomainLogDetail"]
    for dis in url_Dict:
        logDist[dis['LogName']] = dis['LogPath']
    down_log_list.append(logDist)
    return down_log_list

# 解析页面
def open_URL(url):
    r = requests.get(url)
    jsonData = json.dumps(r.json())
    down_log_list = resolve_Json(json.loads(jsonData))
    return down_log_list


# 下载日志文件
def down_LogFile(down_log_list):
    down_file_path = './logdown/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
             'Connection':'keep-alive',}
    if os.path.exists(down_file_path):
        shutil.rmtree(down_file_path)
        os.mkdir(down_file_path)
    for line in  down_log_list:
        for filename, filepath in line.items():
            r = requests.get("http://" + filepath, headers=headers)
            with open(down_file_path + filename, "wb") as f:
                f.write(r.content)
            print filename

# 合并日志文件
def merge_File_Search(url):
    os.chdir('./logdown/')
    fileList = os.listdir('./')
    logfile = open("logfile.log", "w+")

    for filename in fileList:
        con = read_gz_file(filename)
        if getattr(con, '__iter__', None):
            for line in con:
                logfile.write(line)
    logfile.close()

    urlCount = 0
    ipList = []
    with open("logfile.log", "r") as f:
        for line in f.readlines():
            if url in line:
                urlCount += 1
                ip = line.split(' ')[2]
                ipList.append(ip)

    print "PV: {}   IP: {}".format(urlCount, len(list(set(ipList))) + 1)

# 从gz压缩包中直接读取数据
def read_gz_file(path):
    with gzip.open(path, 'r') as pf:
        for line in pf:
            yield line

if __name__ == '__main__':
    user_params = {"Action": "DescribeCdnDomainLogs", "DomainName":  "xxx.xxxx.com", "StartTime": "2018-4-4T00:00:00Z", "EndTime": "2018-4-27T00:00:00Z", "PageSize": "1000",}
    uRL = compose_url(user_params)
    down_log_list = open_URL(uRL)
    down_LogFile(down_log_list)
    merge_File_Search("http://xxx.xxxx.xxxx.html")
