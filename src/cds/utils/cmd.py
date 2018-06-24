#!/usr/bin/env python
"""
script used to migrate volume from cds1 to cds2
"""
import logging
import os
import subprocess
import ConfigParser
import time
import json


class Command(object):
    """
    class for migration data from cds1 to cds2
    """

    def __init__(self, cds_tool, cds_master, cds_token, logger=None):
        self._cds_tool = cds_tool
        self._cds_master = cds_master
        self._cds_token = cds_token
        # default timeout time for command in second
        if logger:
            self._logger = logger
        else:
            self._logger = logging
        self._logger.info('cds_tool path: %s' % self._cds_tool)
        self._logger.info('cds_master: %s', self._cds_master)

    def check_cds_success(self, out):
        """
        check the cds output and guarantee it succeed.
        :param out:
        :return:
        """
        return out.get('status').get('errcode') == 0

    def cds_cmd(self, cmd):
        """
        run cds command
        :param cmd:
        :return:
        """
        run_cmd = self._cds_tool + ' --print_cinder_msg=true --master=' + self._cds_master + \
                  ' --token=' + self._cds_token + ' --op=' + cmd
        self._logger.info('[[[cds_tool]]]running: ' + run_cmd)
        print(run_cmd)
        p = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            print(out)
            self._logger.info('[[[cds_tool]]] out:\n' + out)
        if err:
            print(err)
            self._logger.info('[[[cds_tool]]] err:\n' + err)
        parts = out.split('[CINDER_TEXT]')
        json_msg = parts[1]
        return json.loads(json_msg)

    def cds_cmd_and_check(self, cmd):
        """
        run cds command and check if it succeed.
        :param cmd:
        :return:
        """
        out = self.cds_cmd(cmd)
        return self.check_cds_success(out)

    def _get_job_percentage(self, out, detail=False):
        if detail:
            return out.get('info').get('percent')
        else:
            return out.get('percent')

    def wait_job(self, job_uuid, timeout=0):
        """
        wait cds job to finish
        :param job_uuid:
        :param timeout:
        :return:
        """
        start = int(time.time())
        cmd = 'get_job_status --job_uuid=%s --detail' % job_uuid
        while True:
            out = self.cds_cmd(cmd)
            ret = self.check_cds_success(out)
            if not ret:
                return False
            percent = self._get_job_percentage(out)
            if percent is None:
                self._logger.info('no percentage')
                return False
            self._logger.info('job: %s is done: %d' % (job_uuid, percent))
            if percent >= 100:
                return True
            time.sleep(1)
            time_used_s = int(time.time()) - start
            self._logger.error('time_used_s %d, timeout %d' % (time_used_s, timeout))
            if time_used_s > timeout > 0:
                self._logger.error('job %s timeout time used %d second' % (job_uuid, time_used_s))
                return False

    def _get_value(self, line):
        parts = line.split(':')
        return parts[-1].strip()

    def _get_addr(self, line):
        parts = line.split(':')
        return ':'.join(parts[-2:]).strip()

    def _parse_volumes(self, list_volume_out):
        volumes = dict()
        lines = list_volume_out.split('\n')
        volume = dict()
        for line in lines:
            if 'volume_uuid' in line:
                volume = dict()
                volume['uuid'] = self._get_value(line)
                volumes[volume['uuid']] = volume
            elif 'bootable' in line:
                volume['bootable'] = self._get_value(line)
            elif 'node' in line:
                volume['attached_client'] = self._get_addr(line)
        return volumes

    def get_all_volumes(self):
        """
        get all the volumes in the cluster
        :return:
        """
        cmd = 'list_volume'
        out, err = self.cds_cmd(cmd)
        ret = self.check_cds_success(out)
        if not ret:
            return False
        return self._parse_volumes(out)


def read_config(conf_file=None):
    """
     read configuration from file
    :param conf_file:
    :return:
    """
    if not conf_file:
        conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cds.conf')
    if not os.path.exists(conf_file):
        logging.error('configuration file does not exist')
        return None
    conf = ConfigParser.ConfigParser()
    conf.read(conf_file)
    return conf

