#!/bin/python
def get_ip_list():
    with open('/home/install/deviceTools/conf.d/device.list.setup','r') as f:
        L=f.readlines()
    ip_list=[]
    for ip in L:
        if "#" in ip:continue
        ip_list.append(ip.strip())
    return(ip_list)
