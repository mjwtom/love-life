#!/usr/bin/env python
'''

before use this script, please change the cds_git_url to yours

'''


import subprocess
import os
import shutil
import socket
import time

# number of nodes
node_num = 4

cds_git_url = 'git clone ssh://majingwei@icode.baidu.com:8235/baidu/bce/cds baidu/bce/cds &&' \
              ' scp -p -P 8235 majingwei@icode.baidu.com:hooks/commit-msg baidu/bce/cds/.git/hooks/'
work_dir = os.getcwd()
cds_dir = os.path.join(work_dir, 'baidu', 'bce', 'cds')

master_start_port = 8710
blockserver_start_port = 8720
heavyworker_start_port = 8730
tool_start_port = 8750


def get_ip():
    ip = socket.gethostbyname(socket.gethostname())
    return ip


def code_and_compile():
    os.chdir(work_dir)
    print('current work directory')
    print(work_dir)
    if os.path.exists(cds_dir):
        shutil.rmtree(cds_dir)
    subprocess.call(cds_git_url, shell=True)
    os.chdir(cds_dir)
    print('change to directory')
    print(cds_dir)
    subprocess.call('bcloud build', shell=True)
    os.chdir(work_dir)


def change_port(conf, port):
    bak_file = conf+'.bak'
    if os.path.exists(bak_file):
        os.remove(bak_file)
    os.rename(conf, bak_file)
    with open(bak_file, 'r') as template, open(conf, 'w') as conf_file:
        for line in template:
            if line.startswith('--ip_and_port='):
                line = '--ip_and_port=0.0.0.0:%d\n' % port
            conf_file.write(line)


def change_master(conf, master):
    bak_file = conf+'.bak'
    if os.path.exists(bak_file):
        os.remove(bak_file)
    os.rename(conf, bak_file)
    with open(bak_file, 'r') as template, open(conf, 'w') as conf_file:
        for line in template:
            if line.startswith('--master='):
                line = '--master=%s' % master
            conf_file.write(line)


def copy_dir(src, dst):
    shutil.copytree(src, dst)


def node_dir(i):
    directory = os.path.join(work_dir, 'node%d' % i)
    return directory


def bootstrap_master(conf):
    bak_file = conf + '.bak'
    if os.path.exists(bak_file):
        os.remove(bak_file)
    os.rename(conf, bak_file)
    with open(bak_file, 'r') as template, open(conf, 'w') as conf_file:
        for line in template:
            if line.startswith('--ip_and_port=0.0.0.0'):
                conf_file.write(line)
                line = '--bootstrap=true\n'
            conf_file.write(line)


def add_masters():
    directory = os.path.join(node_dir(0), 'output')
    os.chdir(directory)
    ip = get_ip()
    cur_nodes = ip + ':' + str(master_start_port)
    for i in range(1, node_num):
        node = ip +':' + str(master_start_port+i)
        cmd = './bin/cds_tool --op=add_master_node --node=%s --cur_nodes=%s' % (node, cur_nodes)
        subprocess.call(cmd, shell=True)
        cur_nodes = cur_nodes +','+node
        time.sleep(3)
    cmd = './bin/cds_tool --op=list_master_node'
    subprocess.call(cmd, shell=True)


def add_blockservers():
    directory = os.path.join(node_dir(0), 'output')
    os.chdir(directory)
    ip = get_ip()
    for i in range(node_num):
        node = ip +':' + str(blockserver_start_port+i)
        cmd = './bin/cds_tool --op=add_node --node=%s --region=toy_region --zone=toy_zone --force=true' % node
        subprocess.call(cmd, shell=True)
        time.sleep(3)
    cmd = './bin/cds_tool --op=stat_cluster'
    subprocess.call(cmd, shell=True)


def deploy():
    cds_output_dir = os.path.join(cds_dir, 'output')
    for i in range(node_num):
        print('configure node%d' % i)
        directory = node_dir(i)
        os.mkdir(directory)
        output_dir = os.path.join(directory, 'output')
        print('copy output...')
        copy_dir(cds_output_dir, output_dir)
        # change master port
        print('change master port...')
        master_conf = os.path.join(output_dir, 'conf', 'master.conf')
        port = master_start_port + i
        change_port(master_conf, port)
        # change blockserver port
        print('change blockserver port...')
        blockserver_conf = os.path.join(output_dir, 'conf', 'blockserver.conf')
        port = blockserver_start_port + i
        change_port(blockserver_conf, port)
        # change tool port
        print('change tool port...')
        tool_conf = os.path.join(output_dir, 'conf', 'tool.conf')
        port = tool_start_port + i
        change_port(tool_conf, port)
    print('configure bootstrap master...')
    master_conf = os.path.join(node_dir(0), 'output', 'conf', 'master.conf')
    bootstrap_master(master_conf)
    ip = get_ip()
    port = master_start_port
    master = ip+':'+str(port)
    print('master is...')
    print(master)
    for i in range(node_num):
        print('configure the master of blockserver on node%d'%i)
        blockserver_conf = os.path.join(node_dir(i), 'output', 'conf', 'blockserver.conf')
        change_master(blockserver_conf, master)
        print('configure the master of tool on node%d' % i)
        tool_conf = os.path.join(node_dir(i), 'output', 'conf', 'tool.conf')
        change_master(tool_conf, master)


def start_all():
    for i in range(node_num):
        print('node%d'%i)
        directory = os.path.join(node_dir(i), 'output')
        os.chdir(directory)
        print('start master....')
        cmd = 'nohup ./bin/master > master.run 2>&1 &'
        subprocess.call(cmd, shell=True)
        print('start blockserver....')
        cmd = 'nohup ./bin/blockserver > blockserver.run 2>&1 &'
        subprocess.call(cmd, shell=True)


def construct():
    print('get code and compile...')
    code_and_compile()
    print('deploy...')
    deploy()
    print('start the servers')
    start_all()
    print('sleep for a while to wait startup...')
    time.sleep(3)
    print('add nodes...')
    add_masters()
    print('add blockservers...')
    add_blockservers()


def check():
    # because of the port
    assert(node_num < 10)


def clean():
    print('kill master...')
    subprocess.call('pkill master', shell=True)
    print('kill blockservers...')
    subprocess.call('pkill blockserver', shell=True)
    if os.path.exists(cds_dir):
        print('remove cds directory...')
        shutil.rmtree(cds_dir)
    for i in range(node_num):
        directory = node_dir(i)
        if os.path.exists(directory):
            print('remove node%d' %i)
            shutil.rmtree(directory)


if __name__ == '__main__':
    check()
    clean()
    construct()
