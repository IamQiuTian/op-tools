#!/bin/sh
SERVICE=$1
if [ ! -n "$SERVICE" ];then
     exit 3 
fi

function serviceC() {
    ReservedNum=10
    FileNum=$(ls -d  /data/service/releases/${SERVICE}/${SERVICE}-* |wc -l)    
    while(( FileNum > ReservedNum))
    do
        OldFile=$(ls -rtd  /data/service/releases/${SERVICE}/${SERVICE}-* | head -1)
        if [ ! -n "$OldFile" ];then
            exit 3
        fi 
        rm -rf $OldFile
        let "FileNum--"
   done
}

function ErrorC() {
    eReservedNum=50
    eFileNum=$(ls /data/service/releases/${SERVICE}/logs/*ERROR-*log.gz |wc -l)
    while(( eFileNum > eReservedNum))
    do
        eOldFile=$(ls -rt /data/service/releases/${SERVICE}/logs/*ERROR-*log.gz | head -1)
        if [ ! -n "$eOldFile" ];then
            exit 3
        fi
        rm -f $eOldFile
        let "eFileNum--"
    done
}

function InfoC() {
    iReservedNum=50
    iFileNum=$(ls /data/service/releases/${SERVICE}/logs/*INFO-*log.gz |wc -l)
    while(( iFileNum > iReservedNum))
    do
        iOldFile=$(ls -rt /data/service/releases/${SERVICE}/logs/*INFO-*log.gz | head -1)
        if [ ! -n "$iOldFile" ];then
            exit 3
        fi
        rm -f $iOldFile
        let "iFileNum--"
    done
}

function main() {
    serviceC
    ErrorC
    InfoC
}

main
