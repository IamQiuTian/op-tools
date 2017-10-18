#/usr/bin/env python
#coding:utf8

import commands

import time
import re
import os
import sys
import zipfile

class Inspection(object):
    def __init__(self):
        self.mail_log = "/var/log/maillog"
        self.messages_log = "/var/log/messages"
        self.secure_log = "/var/log/secure"
	    self.now_time = str(time.strftime('%Y%m%d'))
    
    def Log_Check(self):
	    self._path = "/root/error_log/" + self.now_time + ".log"
	    f = open(self._path,"w")
        with open(self.mail_log,'r') as mail:
            for l in mail:
                if "warning" in l or "error" in l:
			f.write("mail --> ")
			f.write(l)

        with open(self.messages_log,'r') as messages:
            for l in messages:
                if "warning" in l or "error" in l or "ERROR" in l or "Failed" in l:
			f.write("messages --> ")
                        f.write(l)

        with open(self.secure_log,'r') as secure:
            for l in secure:
                if "Failed" in l or "error" in l:
			f.write("secure --> ")
                        f.write(l)
	    f.close()

    def Compression(self):
        self.Log_Check()
	    z = zipfile.ZipFile("/root/error_log/"+self.now_time+'.zip', 'w') 
	    z.write(self._path)
	    z.close()
	
	
if __name__ == "__main__":
    t = Inspection()
    t.Compression()
