#!/usr/bin/env python
# coding:utf8

import subprocess
import time

def shell(cmdline,wait=0):
    # Execute the shell
    a = subprocess.Popen(cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # Wait for 120 seconds after the command is executed
    if wait == 0:
        status=a.wait(timeout=60*20)
    else:
        time.sleep(wait)
        status=a.kill()
        return
    # Output the command execution result
    stdout=a.stdout.readlines()
    # Write errors and write errors after command execution fails
    if status !=0:
        raise Exception(cmdline)
    return(status,stdout)
