#!/usr/bin/env python

'''
created by Jingwei Ma (majingwei@baidu.com)
This is the tool to
'''

import sys
import uuid
from mysql import connector
import subprocess


if True:
    mysql_host = 'localhost'
    database = 'cinder'
    mysql_passwd = None
else:
    mysql_host = '10.58.144.11'
    mysql_passwd = 'bcetest'
    database = 'cinder'


def get_snapshots(volume):
    conf = dict(
        host=mysql_host,
        user='root',
        password=mysql_passwd,
        database=database,
        charset='utf8'
    )
    sql = 'SELECT id FROM snapshots WHERE volume_id="%s"' % volume
    conn = connector.connect(**conf)
    cur = conn.cursor()
    cur.execute(sql)
    snapshots = [s[0] for s in cur]
    cur.close()
    conn.close()
    return snapshots


def slice2block(slice_key):
    pieces = slice_key.split('_')
    # slice_key is defined as 'block_id_versio_index', there are '_'s in block_id
    block_id = '_'.join(pieces[:-2])
    return block_id


def get_volume_and_index(block_id):
    pieces = block_id.split('_')
    volume_uuid = '_'.join(pieces[:-1])
    index = pieces[-1]
    return volume_uuid, index

def generate_block_id(volume_uuid, index):



def send_mark_request(block_id):
    cmd = 'emv_tool --option = mark_block_slice_as_unuploaded --block_id=%s' % block_id
    subprocess.call(cmd, shell=True)


def send_create_snapshot_request(volume_uuid):

    cmd = 'emv_tool --mark_block_slice_as_unuploaded --block_id=%s' % block_id


def get_impacted_volumes(volumes):
    for volumes, blocks


def repair_slices(*slice_keys): # we like to deal with slices in batch
    # find affected blocks
    block_ids = set()
    for slice_key in slice_keys:
        block_ids.add(slice2block(slice_key))
    # find affected volumes. 1. get the directly affected volumes
    volumes = dict()
    for block_id in block_ids:
        volume_uuid, index = block2volume(block_id)
        if volume_uuid in volumes:
            volumes.get(volume_uuid).append[index]
        else:
            volumes[volume_uuid] = [index]
    # walk the reference tree and find all the affected volumes
    get_impacted_volumes(volumes)


def repair(slice_key):
    pass


if __name__ == '__main__':
    for slice_key in sys.argv[1:]:
        repair(slice_key)