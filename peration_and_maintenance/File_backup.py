#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import time
import os
import tarfile
import hashlib
import pickle
 
def check_md5(fname): #MD5加密文件
    m = hashlib.md5() #创建对象
    with open(fname) as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data) #MD5加密数据
    return m.hexdigest() #返回数据加密后的MD5值
 
def full_backup(): #完全备份函数
    base_dir,back_dir = os.path.split(src_dir.rstrip('/')) #将/home/demo以/号拆分为'/home', 'demo'
    back_name = '%s_full_%s.tar.gz' %(back_dir,time.strftime('%Y%m%d')) #设置备份文件的名称
    full_path = os.path.join(dst_dir,back_name) #拼接备份文件存放目标路径
 
    tar = tarfile.open(full_path,'w') #创建tar.gz文件
    tar.add(back_dir) #将demo目录放入压缩包内
    tar.close
 
    for path,dirs,files in os.walk(src_dir): #遍历源备份文件目录
        md5dict = {}
        for each_file in files:
            full_name = os.path.join(path,each_file) #拼接备份文件的绝对路径
            md5dict[full_name] = check_md5(full_name) #以字典方式存储备份文件的MD5值
    
    with open(md5file,'w') as fobj:
        pickle.dump(md5dict,fobj)
 
def incr_backup(): #增量备份
    new_md5 = {}
    with open(md5file) as fobj:
        old_md5 = pickle.load(fobj)
 
    base_dir,back_dir = os.path.split(src_dir.rstrip('/'))
    back_name = '%s_full_%s.tar.gz' %(back_dir,time.strftime('%Y%m%d'))
    full_path = os.path.join(dst_dir,back_name)
 
    for path,dirs,files in os.walk(src_dir):
        for each_file in files:
            full_name = os.path.join(path,each_file)
            new_md5[full_name] = check_md5(full_name)   
 
    with open(md5file,'w') as fobj:
        pickle.dump(new_md5,fobj)
    
    tar = tarfile.open(full_path)
    for key in new_md5:
        if old_md5.get(key) != new_md5[key]:
            tar.add(key.split(base_dir)[1].lstrip('/'))
    tar.close()
    
if __name__ == '__main__':
    src_dir = '/home/demo' #源备份文件目录
    dst_dir = '/home/backup' #备份后文件的目录
    md5file = '/home/backup/md5.data' #MD5校验文件
 
    if time.strftime('%a') == 'Mon': #如果当前时间为周一
        full_backup() #就执行完全备份
    else:
        incr_backup() #否则就执行增量备份