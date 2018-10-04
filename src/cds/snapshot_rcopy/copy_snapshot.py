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


def copy_object(host, dst_bucket, src_bucket, backup_bucket, ak, sk, object_name, retry_num):
    credentials = BceCredentials(ak, sk)
    bos_conf = BceClientConfiguration(credentials=credentials, endpoint=host)
    bos_client = BosClient(bos_conf)

    retry = 0
    excpt = Exception
    while retry < retry_num:
        retry += 1
        try:
            bos_client.copy_object(src_bucket, object_name, dst_bucket, object_name)
        except Exception:
            try:
                bos_client.copy_object(backup_bucket, object_name, dst_bucket, object_name)
            except Exception as e:
                excpt = e
                continue
            return
        return
    print(excpt)
    print('except: %s' % object_name)
    raise excpt


def get_object_data(host, dst_bucket, ak, sk, object_name, retry_num):
    credentials = BceCredentials(ak, sk)
    bos_conf = BceClientConfiguration(credentials=credentials, endpoint=host)
    bos_client = BosClient(bos_conf)

    retry = 0
    excpt = Exception
    while retry < retry_num:
        retry += 1
        try:
            data = bos_client.get_object_as_string(dst_bucket, object_name)
        except Exception as e:
            excpt = e
            continue
        return data
    print(excpt)
    print('except: %s' % object_name)
    raise excpt


def process_extent(host, dst_bucket, src_bucket, backup_bucket, ak, sk, extent_name, retry_num):
    copy_object(host, dst_bucket, src_bucket, backup_bucket, ak, sk, extent_name, retry_num)
    data = get_object_data(host, dst_bucket, ak, sk, extent_name, retry_num)
    extent_header = ExtentPbHeader()
    extent_header.ParseFromString(data)
    for slice in extent_header.slice_pb:
        slice_name = str(slice.slice_object_name)
        copy_object(host, dst_bucket, src_bucket, backup_bucket, ak, sk, slice_name, retry_num)


def process_copy(host, dst_bucket, src_bucket, backup_bucket, ak, sk,
                 snapshot, retry_num=10, batch_size=100):
    print('start')
    cds_snapshot_id = 'cds_snapshot_' + snapshot
    print(cds_snapshot_id)
    copy_object(host, dst_bucket, src_bucket, backup_bucket, ak, sk, cds_snapshot_id, retry_num)
    data = get_object_data(host, dst_bucket, ak, sk, cds_snapshot_id, retry_num)
    snapshot_top = SnapshotPbHeader()
    snapshot_top.ParseFromString(data)
    extent_names = []
    for extent in snapshot_top.extent_pb:
        extent_name = str(extent.extent_object_name)
        extent_names.append(extent_name)
    index = 0
    while index < len(extent_names):
        threads = []
        for _ in range(batch_size):
            extent_name = extent_names[index]
            info = '%s, index: %d\n' %(extent_name, index)
            print(info)
            args = (host, dst_bucket, src_bucket, backup_bucket, ak, sk, extent_name, retry_num)
            t = threading.Thread(target=process_extent, args=args)
            t.start()
            threads.append(t)
            index += 1
            if index >= len(extent_names):
                break
        for t in threads:
            t.join()
    print('finished')


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
    backup_bucket = conf.get('GLOBAL', 'backup_bucket')
    ak = conf.get('GLOBAL', 'bos_ak')
    sk = conf.get('GLOBAL', 'bos_sk')
    snapshot = conf.get('GLOBAL', 'snapshot')
    batch_size = conf.get('GLOBAL', 'batch_size')
    process_copy(host, dst_bucket, src_bucket, backup_bucket, ak, sk, snapshot, 10, int(batch_size))


if __name__ =='__main__':
    copy_snapshot()
