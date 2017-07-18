#!/usr/bin/env python

import os
import logging
import ConfigParser
import json
from datetime import datetime


class Parser(object):
    def __init__(self, files, output):
        self._files = files
        self._init_log()
        self._jobs = dict()
        self._output = output
        self._logger.info('parsing the following files:')
        self._current_job = None

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

    def _dump(self):
        with open(self._output, 'w') as f:
            json.dump(self._jobs, f)

    def _get_time(self, line):
        parts = line.split()
        time = ' '.join(parts[:2])
        return time

    def _get_arg(self, line, arg):
        pos = line.find(arg)
        if pos == -1:
            return None
        parts = line[pos:].split()
        parts = parts[0].split('=')
        parts = parts[-1].split('\'')
        arg = parts[0]
        return arg

    def _get_volume_uuid(self, line):
        return self._get_arg(line, '--volume_uuid')

    def _get_job_uuid(self, line):
        return self._get_arg(line, '--job_uuid')

    def _get_snapshot_uuid(self, line):
        return self._get_arg(line, '--snapshot_uuid')

    def _create_root(self, line):
        root_volume = dict()
        root_volume['start_time'] = self._get_time(line)
        root_volume['snapshot_uuid'] = self._get_snapshot_uuid(line)
        root_volume['volume_uuid'] = self._get_volume_uuid(line)
        job_uuid = self._get_job_uuid(line)
        root_volume['job_uuid'] = job_uuid
        self._jobs[job_uuid] = root_volume

    def _check_status(self, line):
        self._current_job = self._get_job_uuid(line)

    def _timedelta_total_seconds(self, timedelta):
        return (timedelta.microseconds + 0.0 +
        (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

    def _get_percentage(self, line):
        pos = line.find('percent')
        sub_string = line[pos:]
        parts = sub_string.split()
        parts = parts[0].split(':')
        parts = parts[-1].split('}')
        percent = int(parts[0])
        return percent

    def _percentage(self, line):
        percent = self._get_percentage(line)
        if percent == 100:
            volume = self._jobs.get(self._current_job)
            if volume is None:
                return
            finish_time = self._get_time(line)
            volume['finish_time'] = finish_time
            start_time = volume.get('start_time')
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
            finish_time = datetime.strptime(finish_time, "%Y-%m-%d %H:%M:%S.%f")
            td = finish_time - start_time
            volume['time_used_s'] = self._timedelta_total_seconds(td)

    def _parse_line(self, line):
        if '--op=clone_volume' in line and '--bootable=true' in line:
            self._logger.info('find create root volume')
            self._logger.info(line)
            self._create_root(line)
        elif '--op=get_job_status' in line:
            self._logger.info('get job status')
            self._logger.info(line)
            self._check_status(line)
        elif 'errcode' in line \
                and 'percent' in line\
                and 'CINDER_TEXT' not in line \
                and 'clone volume' not in line:
            self._logger.info('get percent')
            self._logger.info(line)
            self._percentage(line)

    def parse(self):
        for file in self._files:
            self._logger.info('parsing file %s' % file)
            with open(file, 'r') as f:
                for line in f:
                    self._parse_line(line)
            self._dump()


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


def get_log_files(log_dir, log_bak_dir, prefix):
    back_files = []
    files = list(os.listdir(log_bak_dir))
    for file in files:
        if file.startswith(prefix):
            path = os.path.join(log_bak_dir, file)
            back_files.append(path)
    back_files = sorted(back_files)
    current_files = []
    files = list(os.listdir(log_dir))
    for file in files:
        if file.startswith(prefix):
            path = os.path.join(log_dir, file)
            current_files.append(path)
    current_files = sorted(current_files)
    if len(current_files) > 0 and current_files[0].endswith('.log'):
        file = current_files.pop(0)
        current_files.append(file)
    back_files.extend(current_files)
    return back_files


def parse_log():
    conf = read_config()
    log_dir = conf.get('cinder', 'log_dir', '/home/bcc/logs')
    log_bak_dir = conf.get('cinder', 'log_bak_dir', '/home/bcc/logs/log_bak')
    volume_log_prefix = conf.get('cinder', 'volume_log_prefix', 'cinder-volume.log')
    output = conf.get('profile', 'output', 'jobs.json')
    files = get_log_files(log_dir, log_bak_dir, volume_log_prefix)
    parser = Parser(files, output)
    parser.parse()


if __name__ == '__main__':
    parse_log()
