#!/bin/bash

# 日志所在文件夹
LOGS_PATH=/data/service_logs/nginx/
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

function mvLog()
{
    cd $LOGS_PATH
    for LOGS_NAME in ./*.log
    do
        mv ${LOGS_NAME} history/${LOGS_NAME}-${YESTERDAY}
    done
    kill -USR1 `ps axu | grep "nginx: master process" | grep -v grep | awk '{print $2}'`
}

function tarLog()
{
    cd $LOGS_PATH
    for LOGS_NAME in ./*.log
    do
        cd $LOGS_PATH/history
        tar -zcf ${LOGS_NAME}-${YESTERDAY}.tar.gz ${LOGS_NAME}-${YESTERDAY} --remove-files
    done
}

function main()
{
    # 删除7天前的日志
    cd $LOGS_PATH/history
    find . -mtime +7 -type f -name "*.tar.gz" -exec rm -f {} \;
    # 切割日志，nginx重载日志
    mvLog
    wait
    sleep 10
    # 压缩日志
    tarLog
}
main
