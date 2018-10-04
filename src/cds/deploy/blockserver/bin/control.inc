#!/bin/bash

#file:includes.sh
#This script includes the basic OP-AOS interface definition and some common functions.
#By zhangleiop@baidu.com liujie@baidu.com

VERSION="1.0.3.0"

#AOS_OK = 0,				//操作成功
#AOS_ERR_FAILED_OPERATION = 1,		//操作失败
#AOS_ERR_STARTED = 2,			//程序已启动
#AOS_ERR_NOT_STARTED = 3,		//程序没有启动
#AOS_ERR_TIMEOUT = 4,			//操作超时
#AOS_ERR_FILE_NOTFOUND = 5,		//文件未找到
#AOS_ERR_ACCESS = 6			//权限问题导致无法访问
#AOS_ERR_PARAMATER = 7                  //参数错误
#AOS_ERR_NOT_WORKING = 8		//模块正常，但日志不滚动

AOS_OK=0
AOS_ERR_FAILED_OPERATION=1
AOS_ERR_STARTED=2
AOS_ERR_NOT_STARTED=3
AOS_ERR_TIMEOUT=4
AOS_ERR_FILE_NOTFOUND=5
AOS_ERR_ACCESS=6
AOS_ERR_PARAMATER=7
AOS_ERR_NOT_WORKING=8

function file_exist
{
	local file_name
	if [ $# -ne 1 ];then
		return 1
	fi
	file_name=$1
	if [ -e $file_name -a ! -d $file_name ];then
		return 0
	else
		return 1
	fi
}
function file_executable
{
	local file_name
	if [ $# -ne 1 ];then
		return 1
	fi
	file_name=$1
	if [ -x $file_name -a ! -d $file_name ];then
		return 0
	else
		return 1
	fi
}

function check_proc_exist
{
	local proc_name proc_port port_name
	if [ $# -eq 2 -a $2 -gt 0 2>/dev/null ];then
		proc_name=$1
		proc_port=$2
		port_name=`/usr/sbin/lsof -P -i :$proc_port |grep "*:$proc_port\>"|awk '{print $1}'|uniq`
		if [ "$proc_name" = "$port_name" ];then
			return 0
		else
			return 1
		fi
        elif [ $# -eq 1 ];then
		proc_name=$1

        all_id=`ps -eo ppid,pid,comm|grep " $proc_name\>"|awk '{printf $1"\n"$2"\n"}'|sort -n|uniq|grep -v "\<1\>"` 
        if [ -z "$all_id" ];then
            return 1
        fi

        pwd=`pwd | sed 's/\/bin$//'`
    
        for proc_id in $all_id 
        do
            real_cmd=`ls -l /proc/$proc_id/exe | awk '{ print $NF; }'`
            if [ -z "$real_cmd" ]; then 
                continue    
            fi
        
            if [[ $real_cmd == $pwd* ]]; then
                return 0
            fi
        done
        return 1
    else    
        return 1
    fi
}

function check_proc_num
{
	local proc_num proc_name real_num
	local default_num=3	
	if [ $# -eq 2 -a $2 -gt 0 2>/dev/null ];then
		proc_name=$1
		proc_num=$2
	elif [ $# -eq 1 ];then
		proc_name=$1
		proc_num=$default_num
	else
		return 1
	fi
	real_num=`pstree -pl|grep "\-[{]\{0,1\}${proc_name}[}]\{0,1\}([0-9].*)"|wc -l |awk '{print$1}'`
	#real_num=` -pl|grep "\-$proc_name([0-9].*)"|wc -l|awk '{print $1}'`
	if [ $real_num -ge $proc_num ];then
		return 0
	else
		return 1
	fi
}

function check_log_roll
{
	local time_limit log_name i this_time last_time
	if [ $# -ne 2 ];then
		return 1
	fi
	if [ ! -r $1 ];then
		return 1
	fi
	if [ $2 -gt 0 2>/dev/null ];then
		time_limit=$2
	else
		return 1
	fi
	log_name=$1
	for((i=0,this_time=`date +%s -r $log_name`,last_time=this_time;i<=time_limit;i++))
	do
		if [ $this_time -gt $last_time ];then
			return 0
		fi
		sleep 1
		last_time=$this_time
		this_time=`date +%s -r $log_name`
	done
	return 1
}


#liujie@baidu.com
#example: kill_proc "as_r"
#         will kill supervise & as_r
#propose: kill process of "as_r" and all parents of its
#
function kill_proc
{
    local proc_name all_id proc_id
    if [ $# -ne 1 ];then
        return 1
    fi
    proc_name=$1

    all_id=`ps -eo ppid,pid,comm|grep " $proc_name\>"|awk '{printf $1"\n"$2"\n"}'|sort -n|uniq|grep -v "\<1\>"` 
    if [ -z "$all_id" ];then
        return 1
    fi

	pwd=`pwd | sed 's/\/bin$//'`
    
    for proc_id in $all_id 
    do
        real_cmd=`ls -l /proc/$proc_id/exe | awk '{ print $NF; }'`
        if [ -z "$real_cmd" ]; then 
            return 1
        fi      

        if [[ $real_cmd == $pwd* ]]; then
            kill $proc_id 2>/dev/null
        fi      
    done    
    return 0
}


