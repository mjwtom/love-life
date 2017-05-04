#!/usr/bin/env python

'''
caution: need root to run this script
'''

import os
import subprocess
import shutil


work_dir = os.getcwd()
code_dir = os.path.join(work_dir, 'baidu', 'bce', 'cds-agent')
agent_dir = os.path.join('/home', 'bcc', 'cds-agent')

cds_agent_git_url = 'git clone ssh://majingwei@icode.baidu.com:8235/baidu/bce/cds-agent baidu/bce/cds-agent &&' \
                    ' scp -p -P 8235 majingwei@icode.baidu.com:hooks/commit-msg baidu/bce/cds-agent/.git/hooks/'

cds_master = 'newcds-test.qa.baidu.com:8050'
agent_port = 1025


def code_compile():
    subprocess.call(cds_agent_git_url, shell=True)
    os.chdir(code_dir)
    subprocess.call('bcloud build', shell=True)
    os.chdir(work_dir)


def generate_config(conf, port, master):
    with open(conf, 'w') as conf_file:
        line = '--ip_and_port=0.0.0.0:%d\n' % port
        conf_file.write(line)
        line = '--master=%s\n' % master
        conf_file.write(line)
        content = \
'''
--bthread_concurrency=16
--defer_close_second=120
--socket_max_unwritten_bytes=12582912

--casio_port=4401

#VLOG level <= verbose will print
--verbose=0
#LOG level >= min_log_level will print. (0=INFO 1=NOTICE 2=WARNING 3=ERROR 4=FATAL)
--min_log_level=0
#LOG(FATAL) and CHECK will cause crash
--crash_on_fatal_log=true

--comlog_path=log
--comlog_process=executor
#split_type: 0(TRUNCT), 1(SIZECUT in mb, default 2048m split once), 2(DATECUT in min, default 60min split once)
--comlog_split_type=1
--comlog_quota_size=2048000
--comlog_quota_day=15
--comlog_enable_wf=true
--comlog_enable_async=false
'''
        conf_file.write(content)


def start_agent():
    os.chdir(agent_dir)
    # make sure the controller and agent can run
    cmd = 'chmod +x ./bin/*'
    subprocess.call(cmd, shell=True)
    cmd = './bin/control start'
    subprocess.call(cmd, shell=True)


def deploy():
    print('copy output...')
    src = os.path.join(code_dir, 'output')
    print(src)
    print(agent_dir)
    shutil.copytree(src, agent_dir)
    super_dir = os.path.join(agent_dir, 'supervise')
    os.mkdir(super_dir)
    super_src_file = os.path.join(code_dir, 'output', 'supervise.cds-agent')
    super_dst_file = os.path.join(super_dir, 'supervise.cds-agent')
    shutil.copy(super_src_file, super_dst_file)
    lock_dir = os.path.join('/home', 'bcc', 'locks')
    if not os.path.exists(lock_dir):
        os.makedirs(lock_dir)


def construct():
    print('compile...')
    #code_compile()
    print('deploy...')
    deploy()
    print('generate configuration...')
    conf = os.path.join(agent_dir, 'conf', 'executor_newcds.conf')
    generate_config(conf, agent_port, cds_master)
    print('start agent')
    start_agent()


def clean():
    print('kill super...')
    subprocess.call('pkill supervise.cds-agent', shell=True)
    print('kill agent...')
    subprocess.call('pkill cds-agent', shell=True)
    if os.path.exists(code_dir):
        print('remove agent code directory...')
        #shutil.rmtree(code_dir)
    if os.path.exists(agent_dir):
        print('remove agent deploy directory...')
        shutil.rmtree(agent_dir)


if __name__ == '__main__':
    clean()
    construct()