#!/bin/bash
filepath="/root/Sever/Sever.py"
start(){
    nohup python3 $filepath>/dev/null 2>&1 &
    echo 'kecheng service OK'
}
stop(){
    serverpid=`ps -aux|grep "$filepath"|grep -v grep|awk '{print $2}'`
    kill -9 $serverpid
    echo 'kecheng stop OK'
}
restart(){
    stop
    echo 'kecheng stop OK'
    start
    echo 'kecheng service OK'
}
case $1 in
    start)
    start
    ;;
    stop)
    stop
    ;;
    restart)
    restart
    ;;
    *)
    start
esac