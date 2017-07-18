#!/usr/bin/env python

import os
import subprocess
import logging
import ConfigParser
import time

def read_config(conf_file=None):
    """
     read configuration from file
    :param conf_file:
    :return:
    """
    if not conf_file:
        conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'profile.conf')
    if not os.path.exists(conf_file):
        logging.error('configuration file does not exist')
        return -1
    conf = ConfigParser.ConfigParser()
    conf.read(conf_file)
    return conf


class Collector(object):
    def __init__(self, servers, work_dir, output):
        self._servers = servers
        self._work_dir = work_dir
        self._output = output
        self._init_log()

    def _remote_run(self, server, cmd):
        cmd = 'ssh rd@%s "%s"' % (server, cmd)
        subprocess.call(cmd, shell=True)

    def _copy_file(self, server):
        cmd = 'scp profile_cinder_log.py rd@%s:%s' \
              % (server, self._work_dir)
        subprocess.call(cmd, shell=True)
        cmd = 'scp profile.conf rd@%s:%s' \
              % (server, self._work_dir)
        subprocess.call(cmd, shell=True)

    def _deploy(self):
        for server in self._servers:
            cmd = 'mkdir %s' % self._work_dir
            self._remote_run(server, cmd)
            self._copy_file(server)

    def _run_client(self):
        for server in self._servers:
            cmd = 'cd %s && nohup python profile_cinder_log.py > run.txt 2>&1 &' \
                  % self._work_dir
            self._remote_run(server, cmd)

    def _clean(self):
        for server in self._servers:
            cmd = 'rm -rf %s' % self._work_dir
            self._remote_run(server, cmd)

    def _check_exist(self, server, process):
        cmd = 'ssh rd@%s "ps -aux | grep %s | grep -v color | grep -v grep"' % (server, process)
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate()
        if len(out) == 0:
            return False
        else:
            self._logger.info(server)
            self._logger.info(out)
            return True

    def _wait_parsers(self):
        while True:
            all_done = True
            for server in self._servers:
                ret = self._check_exist(server, 'profile_cinder_log.py')
                if ret:
                    all_done = False
            if all_done:
                break
            else:
                time.sleep(1)

    def _init_log(self):
        # create logger with 'spam_application'
        logger = logging.getLogger('roc parser')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('roc_parser.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        self._logger = logger

    def _collect_node_data(self, server):
        file = os.path.join(self._work_dir, self._output)
        cmd = 'scp rd@%s:%s ./%s.output.json' \
              % (server, file, server)
        subprocess.call(cmd, shell=True)

    def _collect_data(self):
        for server in self._servers:
            self._collect_node_data(server)

    def run(self):
        self._deploy()
        self._run_client()
        self._wait_parsers()
        self._collect_data()


def get_servers(host_path):
    cmd = 'get_hosts_by_path %s' % host_path
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()
    servers = []
    parts = out.split('\n')
    for part in parts:
        servers.append(part.strip())
    return servers


def collect():
    conf = read_config()
    host_path = conf.get('profile', 'host_path')
    servers = get_servers(host_path)
    word_dir = conf.get('profile', 'work_dir')
    output = conf.get('profile', 'output')
    collector = Collector(servers, word_dir, output)
    collector.run()


if __name__ == '__main__':
    collect()
