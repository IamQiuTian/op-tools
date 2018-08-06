#!/usr/bin/env python
# coding:utf8


import sys
import urllib
import urllib2
import json
import datetime
import MySQLdb as mysql
from dingtalkchatbot.chatbot import DingtalkChatbot


reload(sys) 
sys.setdefaultencoding("utf-8" )

timeT = datetime.datetime.now()  + datetime.timedelta()
dingdingUrl = "https://oapi.dingtalk.com/robot/send?access_token=xxoo"

def userList(cur):
    userlist = {}
    cur.execute("select * from zt_user where dept != 1 and deleted = 1")
    for u in cur.fetchall():
        userlist[u[2]] = u[5]
    userlist.pop('xx')
    userlist.pop('oo')
    userlist.pop('xx')
    userlist.pop('oo')
    return userlist

def allbugCount(cur, userlist):
    all_bug_count = {}
    for u in userlist:
        sql = "select count(*) from zt_history where field = 'assignedTo'  AND new = '{}'".format(u,u)
        cur.execute(sql)
        res = cur.fetchall()[0][0]
        if res != 0:
            all_bug_count[u] = res
    return all_bug_count
    
def unsolvedbugCount(cur, userlist):
    unsolved_bug_count = {}
    for u in userlist:
        sql = "select count(*) from zt_bug where assignedTo = '{}' and status != 'resolved'".format(u)
        cur.execute(sql)
        res = cur.fetchall()[0][0]
        if res != 0:
            unsolved_bug_count[u] = res
    return unsolved_bug_count
        

def timeoutbugCount(cur, userlist):
    timeout_bug_count = {}
    for u in userlist:
        sql = "select openedDate from zt_bug WHERE assignedTo = '{}' and status != 'resolved'".format(u)
        cur.execute(sql)
        for res in cur.fetchall():
            timeout = (timeT - res[0]).days
            if timeout != 0 and timeout >= 7:
                if timeout_bug_count.has_key(u) == False:
                    timeout_bug_count[u] = 1
                else:
                    timeout_bug_count[u] = timeout_bug_count[u] + 1
    return timeout_bug_count


if __name__ == '__main__':
    db = mysql.connect(user='root',passwd='xxoo',host='localhost',db='zentao',charset='utf8', unix_socket='/usr/local/mysql/mysql.sock')

    userlist = userList(db.cursor())
    all_bug_count = allbugCount(db.cursor(), userlist)
    unsolved_bug_count = unsolvedbugCount(db.cursor(), userlist)
    timeout_bug_count = timeoutbugCount(db.cursor(), userlist)
    db.close()

    message = "用户  总数 未解决的数  久未解的数\n"
    res = {}
    unsolved_bug = ""
    timeout_bug = ""
        
    for u,_ in userlist.items():
        if all_bug_count.has_key(u):
            all_bug = all_bug_count[u]
        else:
           all_bug = 0
        if unsolved_bug_count.has_key(u):
            unsolved_bug = unsolved_bug_count[u]
        else:
           unsolved_bug = 0
        if timeout_bug_count.has_key(u):
            timeout_bug = timeout_bug_count[u] 
        else:
           timeout_bug = 0
        if all_bug != 0 or unsolved_bug != 0 or timeout_bug != 0:
            res[u] = [all_bug, unsolved_bug, timeout_bug]
    
    for r in sorted(res.iteritems(), key=lambda res : res[1][1], reverse=True):
        message = message + userlist[r[0]] + "       "  + str(r[1][0]) + "          " + str(r[1][1]) + "            " + str(r[1][2]) + "\n"
    
    DingtalkChatbot(dingdingUrl).send_text(msg=message, is_at_all=True)

