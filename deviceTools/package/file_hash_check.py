#!/usr/bin/env python
# coding:utf8

import json
import hashlib

# Check apk hash
def hash_check(package):
    with open("conf.d/package_hash.json", "r") as f1:
        hashdict = json.load(f1)
    filepath = hashdict[package][2]    

    with open(filepath, "rb") as f2:
        md5_obj = hashlib.md5()
        md5_obj.update(f2.read())
        hash_code = md5_obj.hexdigest()
        filehash = str(hash_code).lower()

    if hashdict[package][0] != filehash:
        return 1
    else:
        return 0
