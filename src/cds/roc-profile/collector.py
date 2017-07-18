#!/usr/bin/env python

import os
import subprocess
import logging
import ConfigParser
import time
import json
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DAILY, DateFormatter, rrulewrapper, RRuleLocator, drange


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

    def _get_dst_name(self, server):
        return '%s.output.json' % server

    def _collect_node_data(self, server):
        file = os.path.join(self._work_dir, self._output)
        dst_name = self._get_dst_name(server)
        cmd = 'scp rd@%s:%s ./%s' \
              % (server, file, dst_name)
        subprocess.call(cmd, shell=True)

    def _collect_data(self):
        for server in self._servers:
            self._collect_node_data(server)
        self._jobs = dict()
        for server in self._servers:
            dst_name = self._get_dst_name(server)
            with open(dst_name) as f:
                data = json.load(f)
                self._jobs.update(data)
        with open(self._output, 'w') as f:
            json.dump(self._jobs, f)

    def run(self):
        self._deploy()
        self._run_client()
        self._wait_parsers()
        self._collect_data()
        self._clean()


def get_servers(host_path):
    cmd = 'get_hosts_by_path %s' % host_path
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()
    servers = []
    parts = out.split('\n')
    for part in parts:
        if len(part.strip()) == 0:
            continue
        servers.append(part.strip())
    for server in servers:
        print('server: %s' % server)
    return servers


def draw2(output):
    with open(output, 'r') as f:
        data = json.load(f)
    start_time_list = []
    time_used_list = []
    for volume in data.values():
        start_time = volume.get('start_time')
        time = volume.get('time_used_s')
        if not time:
            continue
        time_used_list.append(time)
        start_time_list.append(start_time)
    figure = plt.figure()
    val = 0.  # this is the value where you want the data to appear on the y-axis.
    plt.plot(time_used_list, np.zeros_like(time_used_list) + val, '+')
    plt.legend('clone time for roc v2')
    plt.xlabel('clone time (seconds)')

    with PdfPages(output+'.pdf') as pdf:
        pdf.savefig(figure)


def draw(output):
    with open(output, 'r') as f:
        data = json.load(f)
    start_time_list = []
    time_used_list = []
    dates = []
    for volume in data.values():
        start_time = volume.get('start_time')
        time = volume.get('time_used_s')
        if not time:
            continue
        time_used_list.append(time)
        start_time_list.append(start_time)
        date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
        dates.append(date)

    # tick every 5th easter
    rule = rrulewrapper(DAILY, interval=1)
    loc = RRuleLocator(rule)
    formatter = DateFormatter('%m/%d/%y')

    fig, ax = plt.subplots()
    plt.plot_date(dates, time_used_list, 'x')
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(formatter)
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=30, fontsize=10)
    #plt.legend('clone time for roc v2')
    #plt.xlabel('date')
    plt.ylabel('roc v2 clone time (seconds)')

    with PdfPages(output+'.pdf') as pdf:
        pdf.savefig(fig)


def collect():
    conf = read_config()
    host_path = conf.get('profile', 'host_path')
    servers = get_servers(host_path)
    word_dir = conf.get('profile', 'work_dir')
    output = conf.get('profile', 'output')
    collector = Collector(servers, word_dir, output)
    collector.run()
    draw(output)


if __name__ == '__main__':
    collect()
