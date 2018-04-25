#!/usr/bin/env python

import json
import os
import ConfigParser
from baidubce.services import bos
from baidubce.services.bos.bos_client import BosClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials


class MyBosClient(object):
    def __init__(self, ak, sk, host):
        credentials = BceCredentials(ak, sk)
        bos_conf = BceClientConfiguration(credentials=credentials, endpoint=host)
        self.bos_client = BosClient(bos_conf)

    def list_objects(self, bucket, file_path):
        objects = []
        response = self.bos_client.list_all_objects(bucket)
        for object in response:
            objects.append(object.key)
        with open(file_path, 'w') as f:
            json.dump(objects, f)


def read_config(conf_file=None):
    """
     read configuration from file
    :param conf_file:
    :return:
    """
    if not conf_file:
        conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hkg.conf')
    if not os.path.exists(conf_file):
        return -1
    conf = ConfigParser.ConfigParser()
    conf.read(conf_file)
    return conf


def test():
    conf = read_config()
    ak = conf.get('ONLINE_HKG', 'ak')
    sk = conf.get('ONLINE_HKG', 'sk')
    host = conf.get('ONLINE_HKG', 'host')
    bucket = conf.get('ONLINE_HKG', 'bucket')
    client_a = MyBosClient(ak, sk, host)
    client_a.list_objects(bucket, 'test.json')

    with open('test.json', 'r') as f:
        obj = json.load(f)
    print('object in bucket:')
    print(len(obj))


if __name__ == '__main__':
    test()
