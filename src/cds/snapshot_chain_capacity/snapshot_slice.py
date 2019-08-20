#!/usr/bin/env python

import os
import threading
import ConfigParser
from snapshot_pb2 import SnapshotPbHeader
from snapshot_pb2 import ExtentPb
from snapshot_pb2 import ExtentPbHeader
from snapshot_pb2 import SlicePb
from baidubce.services import bos
from baidubce.services.bos.bos_client import BosClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
import json
import sys


def get_object_data(host, bucket, ak, sk, object_name, retry_num):
    credentials = BceCredentials(ak, sk)
    bos_conf = BceClientConfiguration(credentials=credentials, endpoint=host)
    bos_client = BosClient(bos_conf)

    retry = 0
    excpt = Exception
    while retry < retry_num:
        retry += 1
        try:
            data = bos_client.get_object_as_string(bucket, object_name)
        except Exception as e:
            excpt = e
            continue
        return data
    print('except: %s' % object_name)
    raise excpt


def process_extent(host, bucket, ak, sk, extent_name, retry_num):
    slices = set()
    data = get_object_data(host, bucket, ak, sk, extent_name, retry_num)
    extent_header = ExtentPbHeader()
    extent_header.ParseFromString(data)
    for slice in extent_header.slice_pb:
        slice_name = str(slice.slice_object_name)
        print('slice: %s' % slice_name)
        slices.add(slice_name)
    return slices


def process_capacity(host, bucket, ak, sk,
                 snapshot, retry_num=10):
    slices = set()
    print('start')
    cds_snapshot_id = 'cds_snapshot_' + snapshot
    print(cds_snapshot_id)
    data = get_object_data(host, bucket, ak, sk, cds_snapshot_id, retry_num)
    snapshot_top = SnapshotPbHeader()
    snapshot_top.ParseFromString(data)
    for extent in snapshot_top.extent_pb:
        extent_name = str(extent.extent_object_name)
        exent_slices = process_extent(host, bucket, ak, sk, extent_name, retry_num)
        slices.update(exent_slices)
    print('finished')
    return slices


def read_config():
    conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'capacity.conf')
    conf = ConfigParser.ConfigParser()
    conf.read(conf_file)
    return conf


def get_snapshot_slice(snapshot_uuid):
    conf = read_config()
    host = conf.get('GLOBAL', 'bos_host')
    bucket = conf.get('GLOBAL', 'bucket')
    ak = conf.get('GLOBAL', 'bos_ak')
    sk = conf.get('GLOBAL', 'bos_sk')
    slices = process_capacity(host, bucket, ak, sk, snapshot_uuid)
    # with open('snapshot_' + snapshot_uuid + '_slices.json', 'w') as f:
        # json.dump(slices, f)
    return slices


def snapshot_list_capacity(list_file):
    slices = set()
    with open(list_file, 'r') as f:
        for line in f.readlines():
            snapshot_slices = get_snapshot_slice(line.strip())
            slices.update(snapshot_slices)
    info = ('file %s size %d MB' % (list_file, len(slices)))
    print(info)
    with open(list_file + '_slice_num.txt', 'w') as f:
        f.write(info)


if __name__ =='__main__':
    if len(sys.argv) <= 1:
        print('give snapshot list')
    snapshot_list_capacity(sys.argv[1])
