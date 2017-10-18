#!/usr/bin/env python
# coding:utf8

import os
import json

def get_apk_filepath(packagename):
    with open("conf.d/package_hash.json", 'r') as f:
        infodict = json.load(f)
        return(infodict[packagename][2])

def get_apk_filename(packagename):
    with open("conf.d/package_hash.json", 'r') as f:
        infodict = json.load(f)
        return(infodict[packagename][1])


def get_apk_filenhash(packagename):
    with open("conf.d/package_hash.json", 'r') as f:
        infodict = json.load(f)
        return(infodict[packagename][0])


def get_all_apk():
    apk_list = []
    with open("conf.d/package_hash.json", 'r') as f:
        infodict = json.load(f)
        for k, v in infodict.items():
            apk_list.append(k) 
    return(apk_list)    


def get_apk_version(packagename):
    apk_list = []
    with open("conf.d/package_hash.json", 'r') as f:
        infodict = json.load(f)
    return(infodict[packagename][3])
