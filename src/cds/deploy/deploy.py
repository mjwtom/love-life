#!/usr/bin/env python

import ConfigParser


def read_conf():
    conf = ConfigParser.ConfigParser()
    conf.read('cds.conf')
    return conf


def deploy_bin(conf):
    user = conf.get('global', 'user')
    root_dir = conf.get('global', 'root_dir')
    bin_dir = conf.get('global', 'bin_dir')
    conf_dir = conf.get('global', 'conf_dir')
    nodes_line = conf.get('global', 'nodes')
    nodes = nodes_line.strip().split(',')
    for node in nodes:
        info = '====== copying files to node %s ======' % node
        print(info)
        cmd = 'ssh %s@%s "cd %s && mkdir -p master/bin && mkdir -p master/conf"' % (user, node, root_dir)
        print(cmd)
        cmd = 'ssh %s@%s "cd %s && mkdir -p blockserver/bin && mkdir -p blockserver/conf"' % (user, node, root_dir)
        print(cmd)
        cmd = 'ssh %s@%s "cd %s && mkdir -p heavyworker/bin && mkdir -p heavyworker/conf"' % (user, node, root_dir)
        print(cmd)
        cmd = 'scp %s/master %s@%s %s/master/bin' % (bin_dir, user, node, root_dir)
        print(cmd)
        cmd = 'scp %s/blockserver %s@%s %s/blockserver/bin' % (bin_dir, user, node, root_dir)
        print(cmd)
        cmd = 'scp %s/heavyworker %s@%s %s/heavyworker/bin' % (bin_dir, user, node, root_dir)
        print(cmd)
        cmd = 'scp %s/master.conf %s@%s %s/master/conf' % (conf_dir, user, node, root_dir)
        print(cmd)
        cmd = 'scp %s/blockserver.conf %s@%s %s/blockserver/conf' % (conf_dir, user, node, root_dir)
        print(cmd)
        cmd = 'scp %s/heavyworker.conf %s@%s %s/heavyworker/conf' % (conf_dir, user, node, root_dir)
        print(cmd)
        print('\n')


def generate_cmds():
    conf = read_conf()


if __name__ == '__main__':
    generate_cmds()