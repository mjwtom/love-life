#!/usr/bin/env python
import subprocess
import json
import time

time_gap_s = 480 # 8min


def cds_tool_cmd(cmd):
    run_cmd = './bin/cds_tool --print_cinder_msg --op=' + cmd
    p = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print(err)
    parts = out.split('[CINDER_TEXT]')
    json_msg = parts[1]
    return json.loads(json_msg)


def is_root_volume(volume_uuid):
    cmd = 'stat_volume --volume_uuid=' + volume_uuid
    volume_stat = cds_tool_cmd(cmd)
    if not volume_stat.get('status') or \
            volume_stat.get('status').get('errcode') != 0:
        # print('stat volume error %s' % volume_uuid)
        return False
    # print(volume_stat)
    if volume_stat.get('volume_info').get('bootable'):
        return True
    else:
        return False


def get_root_rollback_jobs(jobs):
    root_volume_jobs = []
    for job in jobs:
        if not job.get('volume_uuid'): # delete snapshot?
            # print('job %s has no volume_uuid, type %d' % (job.get('job_uuid'),
                  # job.get('job_type')))
            continue
        if is_root_volume(job.get('volume_uuid')):
            root_volume_jobs.append(job)
    return root_volume_jobs


def get_timeout_root_rollback():
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
            create_timestamp = job_info.get('create_timestamp')
        )
        jobs.append(job)
    jobs = get_root_rollback_jobs(jobs)
    now = time.time()
    for job in jobs:
        time_passed = int(now) - int(job.get('create_timestamp'))
        if job.get('job_type') != 5:
            continue
        if job.get('job_state') != 3:
            continue
        if time_passed > time_gap_s:
            warning_info = 'root_volume %s rebuild fail, job: %s, time_s: %d' \
                           % (job.get('volume_uuid'), job.get('job_uuid'), time_passed)
            print(warning_info)


if __name__ == '__main__':
    get_timeout_root_rollback()
