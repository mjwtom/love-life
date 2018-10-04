import sys
import os
import json
import subprocess
import time
import MySQLdb
import ConfigParser
from baidubce.services.bos.bos_client import BosClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce import exception


def get_snapshots_via_db(mysql_conf):
    """
    get the cinder uuid of the evm
    :param mysql_conf:
    :param volumes:
    :return:
    """
    snapshots = []
    print('db configuration')
    print(mysql_conf)
    conn = MySQLdb.connect(**mysql_conf)
    cursor = conn.cursor()
    cmd = 'SELECT id, volume_id, snapshot_id FROM snapshots WHERE status="available"'
    cursor.execute(cmd)
    snapshots_from_db = cursor.fetchall()
    cursor.close()
    conn.close()
    for parts in snapshots_from_db:
        snapshot = dict(
            id=parts[0],
            volume_id=parts[1],
            snapshot_id=parts[2]
        )
        snapshots.append(snapshot)

    return snapshots


def read_config(conf_file=None):
    """
     read configuration from file
    :param conf_file:
    :return:
    """
    if not conf_file:
        conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snapshot1to2.conf')
    if not os.path.exists(conf_file):
        return -1
    conf = ConfigParser.ConfigParser()
    conf.read(conf_file)
    return conf


def do_copy_snapshot(host, bucket, ak, sk, snapshots, retry_num=10):
    credentials = BceCredentials(ak, sk)
    bos_conf = BceClientConfiguration(credentials=credentials, endpoint=host)
    bos_client = BosClient(bos_conf)

    for snapshot in snapshots:
        src_obj = 'cds_snapshot_' + str(snapshot['snapshot_id'])
        dst_obj = 'cds_snapshot_' + str(snapshot['id'])
        info = 'check %s -----> %s' % (src_obj, dst_obj)
        print(info)

        if int(snapshot['snapshot_id']) == 0:
            print('cds2 snapshot')
            continue

        found = False
        retry = 0
        while retry < retry_num:
            retry += 1
            try:
                response = bos_client.get_object_meta_data(bucket, dst_obj)
                print('Get meta:')
                print(response.metadata)
                found = True
                break
            except exception.BceError as e:
                print(e)
        if found:
            continue

        info = 'do %s -----> %s' % (src_obj, dst_obj)
        print(info)

        retry = 0
        while retry < retry_num:
            retry += 1
            try:
                bos_client.copy_object(bucket, src_obj, bucket, dst_obj)
            except exception.BceError as e:
                print(e)
                continue
            break


def copy_snapshot():
    conf = read_config()
    mysql_conf = dict(
        host=conf.get('CINDER_MYSQL', 'host'),
        port=int(conf.get('CINDER_MYSQL', 'port')),
        user=conf.get('CINDER_MYSQL', 'user'),
        passwd=conf.get('CINDER_MYSQL', 'passwd'),
        db=conf.get('CINDER_MYSQL', 'db'),
    )

    snapshots = get_snapshots_via_db(mysql_conf)

    host = conf.get('BOS', 'bos_host')
    bucket = conf.get('BOS', 'bucket')
    ak = conf.get('BOS', 'bos_ak')
    sk = conf.get('BOS', 'bos_sk')

    do_copy_snapshot(host, bucket, ak, sk, snapshots)


if __name__ == '__main__':
    copy_snapshot()