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


def process_extent(host, dst_bucket, src_bucket, ak, sk, extent_name):
    print(dst_bucket)
    print(src_bucket)
    credentials = BceCredentials(ak, sk)
    bos_conf = BceClientConfiguration(credentials=credentials, endpoint=host)
    bos_client = BosClient(bos_conf)

    try:
        bos_client.copy_object(src_bucket, extent_name, dst_bucket, extent_name)
    except:
        print('except')
    data = bos_client.get_object_as_string(dst_bucket, extent_name)
    extent_header = ExtentPbHeader()
    extent_header.ParseFromString(data)
    for slice in extent_header.slice_pb:
        slice_name = str(slice.slice_object_name)
        print(slice_name)
        try:
            bos_client.copy_object(src_bucket, slice_name, dst_bucket, slice_name)
        except:
            print('except')


def process_copy(host, dst_bucket, src_bucket, ak, sk, snapshot):
    print(dst_bucket)
    print(src_bucket)
    credentials = BceCredentials(ak, sk)
    bos_conf = BceClientConfiguration(credentials=credentials, endpoint=host)
    bos_client = BosClient(bos_conf)

    cds_snapshot_id = 'cds_snapshot_' + snapshot
    print(cds_snapshot_id)
    try:
        bos_client.copy_object(src_bucket, cds_snapshot_id, dst_bucket, cds_snapshot_id)
    except:
        print('except')
    data = bos_client.get_object_as_string(dst_bucket, cds_snapshot_id)
    snapshot_top = SnapshotPbHeader()
    snapshot_top.ParseFromString(data)
    threads = []
    for extent in snapshot_top.extent_pb:
        extent_name = str(extent.extent_object_name)
        print(extent_name)
        args = (host, dst_bucket, src_bucket, ak, sk, extent_name)
        t = threading.Thread(target=process_extent, args=args)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print('success')


def read_config(conf_file=None):
    """
     read configuration from file
    :param conf_file:
    :return:
    """
    if not conf_file:
        conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'copy.conf')
    if not os.path.exists(conf_file):
        return -1
    conf = ConfigParser.ConfigParser()
    conf.read(conf_file)
    return conf


def copy_snapshot():
    conf = read_config()
    host = conf.get('GLOBAL', 'bos_host')
    dst_bucket = conf.get('GLOBAL', 'dst_bucket')
    src_bucket = conf.get('GLOBAL', 'src_bucket')
    ak = conf.get('GLOBAL', 'bos_ak')
    sk = conf.get('GLOBAL', 'bos_sk')
    snapshot = conf.get('GLOBAL', 'snapshot')
    process_copy(host, dst_bucket, src_bucket, ak, sk, snapshot)


if __name__ =='__main__':
    copy_snapshot()
