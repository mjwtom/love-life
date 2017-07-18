#!/usr/bin/env python
import os
import sys
import subprocess
import uuid
import threading
import logging
import time


class Test(object):
    def __init__(self, cds_tool_dir,
                 volume_size,
                 volume_num,
                 cds_token='default_token'):
        self._cds_tool_dir = cds_tool_dir
        self._cds_token = cds_token
        self._volume_size = volume_size
        self._volume_num = volume_num
        self._image_volume = None
        self._snapshot_uuid = None
        self._origin_volume = None
        self._snapshot_uuid = None
        self._volumes = []
        self._volume_conf = dict()
        # default timeout time for command in second
        self._timeout = 60
        logging.info('cds_tool path: %s' % self._cds_tool_dir)
        logging.info('cds token: %s' % self._cds_token)

    def _cds_cmd(self, cmd):
        run_cmd = './bin/cds_tool --token=' + self._cds_token + ' --op=' + cmd
        logging.info('[[[cds_tool]]]running: ' + run_cmd)
        p = subprocess.Popen(run_cmd, shell=True,
            cwd=self._cds_tool_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            logging.info('[[[cds_tool]]] out: %s\n' % out)
        if err:
            logging.info('[[[cds_tool]]] err: %s\n' % err)
        return out, err

    def _check_cds_success(self, out):
        lines = out.split('\n')
        success = False
        for line in lines:
            if 'errcode' in line:
                parts = line.split(':')
                if int(parts[-1]) == 0:
                    success = True
                    break
        return success

    def _cds_cmd_and_check(self, cmd):
        out, err = self._cds_cmd(cmd)
        return self._check_cds_success(out)

    def _get_uuid(self):
        return 'majingwei-test-%s' % uuid.uuid4()

    def _wait_job(self, job_uuid):
        cmd = 'get_job_status --job_uuid=%s' % job_uuid
        while True:
            out, err = self._cds_cmd(cmd)
            ret = self._check_cds_success(out)
            if not ret:
                return False
            percent = self._get_job_percentage(out)
            if percent is None:
                logging.info('no percentage')
                return False
            logging.info('job: %s is done: %d' % (job_uuid, percent))
            if percent >= 100:
                return True
            time.sleep(1)

    def _get_job_percentage(self, info):
        lines = info.split('\n')
        for line in lines:
            if 'percent' in line:
                parts = line.split()
                percent = int(parts[-1])
                return percent
        return None

    def _generate_local_file(self, path, size):
        with open(path, 'wb') as fout:
            fout.write(os.urandom(size))

    def _generate_volume_data(self, path, offset, length):
            cmd = './bin/cds_check_tool --monitor_interval_s=1 --f=%s --io_op=write --io_offset=%d --io_size=%d --l=%d --volume_uuid=%s' \
            % (path, offset, length, length, self._origin_volume)
            subprocess.call(cmd, cwd=self._cds_tool_dir, shell=True)

    def _batch_generate_volume_data(self, size):
        length = 1024*1024
        threads = []
        num = size // length
        for i in range(num):
            offset = i*length
            path = self._origin_volume + '_' + str(offset) + '_' + str(length)
            t = threading.Thread(target=self._generate_volume_data, args=(path, offset, length))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def _serial_generate_volume_data(self, size):
        length = 1024*1024
        cycle = size // length
        for i in range(cycle):
            offset = i*length
            path = self._origin_volume + '_' + str(offset) + '_' + str(length)
            self._generate_volume_data(path, offset, length)

    def _origin_create_volume(self):
        self._origin_volume = self._get_uuid() + '-origin'
        cmd = 'create_volume --volume_uuid=%s --volume_size=50 --disk_type=ssd' \
            % self._origin_volume
        self._cds_cmd_and_check(cmd)

    def _generate_snapshot(self):
        self._snapshot_uuid = self._get_uuid()
        job_uuid = self._get_uuid()
        cmd = 'create_snapshot --volume_uuid=%s --snapshot_uuid=%s --job_uuid=%s' \
            % (self._origin_volume, self._snapshot_uuid, job_uuid)
        self._cds_cmd_and_check(cmd)
        self._wait_job(job_uuid)

    def _clone_volume(self):
        volume = self._get_uuid()
        self._volumes.append(volume)
        job_uuid = self._get_uuid()
        cmd = 'clone_volume --volume_uuid=%s --snapshot_uuid=%s --job_uuid=%s --disk_type=ssd --bootable=true' \
              % (volume, self._snapshot_uuid, job_uuid)
        self._cds_cmd_and_check(cmd)
        self._wait_job(job_uuid)

    def _batch_clone(self, volume_num):
        threads = []
        for _ in range(volume_num):
            t = threading.Thread(target=self._clone_volume)
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def _delete_volume(self, volume_uuid):
        job_uuid = self._get_uuid()
        cmd = 'delete_volume --volume_uuid=%s --job_uuid=%s' \
            % (volume_uuid, job_uuid)
        self._cds_cmd_and_check(cmd)
        self._wait_job(job_uuid)

    def _clean(self):
        threads = []
        for volume in self._volumes:
            t = threading.Thread(target=self._delete_volume, args=(volume,))
            threads.append(t)
        t = threading.Thread(target=self._delete_volume, args=(self._origin_volume,))
        threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def run(self):
        self._origin_create_volume()
        # self._batch_generate_volume_data(self._volume_size)
        self._serial_generate_volume_data(self._volume_size)
        self._generate_snapshot()
        self._batch_clone(self._volume_num)
        self._clean()

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    test = Test('/home/cds/tools',1024*1024*1024, 10)
    test.run()
