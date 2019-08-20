#!/usr/bin/env python

import json

with open('jobs.json', 'r') as f:
    jobs = json.load(f)

snapshotmap = dict()
for job in jobs:
    if int(job.get('bootable')) == 1:
        print('bootable')
        continue
    snapshot_uuid = job.get('snapshot_uuid')
    job_list = snapshotmap.get(snapshot_uuid)
    if job_list:
        job_list.append(job)
    else:
        job_list = [job]
        snapshotmap[snapshot_uuid] = job_list

for snapshot_uuid, job_list in snapshotmap.items():
    print('%s len: %d' % (snapshot_uuid, len(job_list)))
