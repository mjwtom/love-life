#!/usr/bin/env python
import subprocess
import json
import time


def cds_tool_cmd(cmd):
    run_cmd = './bin/cds_tool --print_cinder_msg --op=' + cmd
    p = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print(err)
    parts = out.split('[CINDER_TEXT]')
    json_msg = parts[1]
    return json.loads(json_msg)


def get_volume_size(volume_uuid):
    cmd = 'stat_volume --volume_uuid=' + volume_uuid
    volume_stat = cds_tool_cmd(cmd)
    if not volume_stat.get('status') or \
            volume_stat.get('status').get('errcode') != 0:
        # print('stat volume error %s' % volume_uuid)
        return 0
    # print(volume_stat)
    size = volume_stat.get('volume_info').get('volume_size')
    return size


def get_pre_delete_volume_size(jobs):
    sum_size = 0
    for job in jobs:
        volume_uuid = job.get('volume_uuid')
        if not volume_uuid: # delete snapshot?
            # print('job %s has no volume_uuid, type %d' % (job.get('job_uuid'),
                  # job.get('job_type')))
            continue
        snapshot_uuid = job.get('snapshot_uuid')
        if not snapshot_uuid:
            continue
        if not snapshot_uuid.startswith('pre_del'):
            continue
        print('get size of %s' % volume_uuid)
        sum_size += get_volume_size(volume_uuid)
    return sum_size


def get_pre_delete_sum_size():
    list_job_result = cds_tool_cmd('list_job')
    if not list_job_result:
        print('list_job error')
        return
    if not list_job_result.get('status') or \
            list_job_result.get('status').get('errcode') != 0:
        print('list_job error')
        return
    jobs = []
    for job_info in list_job_result.get('job_info'):
        job = dict(
            job_uuid = job_info.get('job_uuid'),
            job_type = job_info.get('job_type'),
            job_state = job_info.get('job_state'),
            volume_uuid = job_info.get('volume_uuid'),
            snapshot_uuid = job_info.get('snapshot_uuid'),
            create_timestamp = job_info.get('create_timestamp')
        )
        jobs.append(job)
    size = get_pre_delete_volume_size(jobs)
    print('totally %d GB' % (size /1024/1024/1024))


if __name__ == '__main__':
    get_pre_delete_sum_size()
