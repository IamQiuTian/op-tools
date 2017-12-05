#!/usr/bin/env python
# coding:utf8

import hashlib
from package import get_apk_info

# Check apk hash
def hash_check(package):
    filepath = get_apk_info.get_apk_filepath(package)
    apkhash = get_apk_info.get_apk_filenhash(package)

    with open(filepath, "rb") as f:
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        filehash = str(hash_code).lower()

    if filehash != apkhash:
        return 1
    else:
        return 0
