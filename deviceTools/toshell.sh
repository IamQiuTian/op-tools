#!/bin/bash

function update_update()
{
    cat /home/install/deviceTools/conf.d/device.list.setup |grep -v "#"|while read line
    do
	    adb connect $line
	    usleep 1000
	    adb -s $line:5555 root
	    usleep 1000
	    adb connect $line
	    usleep 1000
	    adb -s $line:5555 remount
	    usleep 500
	    adb -s $line:5555 push /home/update/librockchip_update_jni.so /system/app/RKUpdateService/lib/arm/
	    adb -s $line:5555 push /home/update/RKUpdateService.apk /system/app/RKUpdateService/
	    adb disconnect $line
    done
}

function start_update_service()
{
   cat /home/install/deviceTools/conf.d/device.list.setup |grep -v "#"|while read line
   do
	    adb connect $line
	    usleep 1000
	    adb -s $line:5555 shell su -c  pm enable android.rockchip.update.service
	    sleep 10
	    timeout 2 adb -s $line:5555 shell reboot
	    adb disconnect $line
   done
}

function update_unzip()
{
	cat /home/install/deviceTools/conf.d/device.list.setup |grep -v "#"|while read line
	do
        adb connect $line
        usleep 1000
        adb -s $line:5555 root
	usleep 1000
        adb connect $line
        usleep 1000
        adb -s $line:5555 push /home/update/unzip /data/unzip
        adb -s $line:5555 shell  /home/update/chmod 777 /data/unzip
        adb -s $line:5555 shell su -c /data/unzip
        adb disconnect $line
	done
}

input=$1
case $input in
        update_update)
        update_update;;
        start_update_service)
        start_update_service;; 
        update_unzip)
        update_unzip;;
esac
