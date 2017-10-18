import os
import re
import hashlib


class HashedDirectoryDoesNotExist(Exception):
    def __init__(self, directory_name):
        self.directory_name = directory_name

    def __str__(self):
        return '{} does not exist'.format(self.directory_name)


def md5(directory_name, filters=None):
    return get_hash(directory_name, hashlib.md5, filters)


def sha1(directory_name, filters=None):
    return get_hash(directory_name, hashlib.sha1, filters)


def get_hash(directory_name, hash_func, filters):
    if not os.path.isdir(directory_name):
        raise HashedDirectoryDoesNotExist(directory_name)
    filters = tuple(filters) if filters else ('', )
    hash_values = []
    for root, dirs, files in os.walk(directory_name, topdown=True):
        if not re.search(r'/\.', root):
            hash_values.extend([file_hash(os.path.join(root, f), hash_func) for f in files
                                if not f.startswith('.') and not re.search(r'/\.', f) and
                                f.endswith(filters)])
    return reduce_hash(hash_values, hash_func)


def file_hash(filepath, hashfunc):
    hasher = hashfunc()
    blocksize = 64 * 1024
    with open(filepath, 'rb') as fp:
        while True:
            data = fp.read(blocksize)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def reduce_hash(hashlist, hashfunc):
    hasher = hashfunc()
    for hashvalue in sorted(hashlist):
        hasher.update(hashvalue.encode('utf-8'))
    return hasher.hexdigest()
