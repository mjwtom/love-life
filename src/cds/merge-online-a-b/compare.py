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
        conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'compare.conf')
    if not os.path.exists(conf_file):
        return -1
    conf = ConfigParser.ConfigParser()
    conf.read(conf_file)
    return conf


def compare():
    online_a_file = 'online_a_obj.json'
    online_b_file = 'online_b_obj.json'
    conf = read_config()
    ak = conf.get('ONLINE-A', 'ak')
    sk = conf.get('ONLINE-A', 'sk')
    host = conf.get('ONLINE-A', 'host')
    bucket = conf.get('ONLINE-A', 'bucket')
    client_a = MyBosClient(ak, sk, host)
    client_a.list_objects(bucket, online_a_file)

    ak = conf.get('ONLINE-B', 'ak')
    sk = conf.get('ONLINE-B', 'sk')
    host = conf.get('ONLINE-B', 'host')
    bucket = conf.get('ONLINE-B', 'bucket')
    client_a = MyBosClient(ak, sk, host)
    client_a.list_objects(bucket, online_b_file)

    with open(online_a_file, 'r') as f:
        onlinea_obj = set(json.load(f))

    with open(online_b_file, 'r') as f:
        onlineb_obj = set(json.load(f))

    conflict = set()
    for a in onlinea_obj:
        if a in onlineb_obj:
            conflict.add(a)

    uniquea = set()
    for a in onlinea_obj:
        if a not in conflict:
            uniquea.add(a)

    uniqueb = set()
    for b in onlineb_obj:
        if b not in conflict:
            uniqueb.add(b)

    with open('conflict.json', 'w') as f:
        json.dump(list(conflict), f)

    with open('uniquea.json', 'w') as f:
        json.dump(list(uniquea), f)

    with open('uniqueb.json', 'w') as f:
        json.dump(list(uniqueb), f)

    print('object in a:')
    print(len(onlinea_obj))

    print('object in b:')
    print(len(onlineb_obj))

    print('conflict:')
    print(len(conflict))

    print('uniquea:')
    print(len(uniquea))

    print('uniqueb:')
    print(len(uniqueb))


if __name__ == '__main__':
    compare()
