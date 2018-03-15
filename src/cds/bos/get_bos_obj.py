#!/usr/bin/env python
import os
import sys
import ConfigParser
from baidubce.services import bos
from baidubce.services.bos.bos_client import BosClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials


class MyBosClient(object):
    def __init__(self, ak, sk, host, bucket=None):
        credentials = BceCredentials(ak, sk)
        bos_conf = BceClientConfiguration(credentials=credentials, endpoint=host)
        self.bos_client = BosClient(bos_conf)

    def exist(self, bucket, object):
        print(bucket)
        print(object)
        response = self.bos_client.get_object_meta_data(bucket, object)
        print(response)
        #print(self.bos_client.get_object_as_string(bucket, object))


def read_config(conf_file=None):
    """
     read configuration from file
    :param conf_file:
    :return:
    """
    if not conf_file:
        conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bos.conf')
    if not os.path.exists(conf_file):
        return -1
    conf = ConfigParser.ConfigParser()
    conf.read(conf_file)
    return conf


def exist(object):
    conf = read_config()
    ak = conf.get('BOS', 'ak')
    sk = conf.get('BOS', 'sk')
    host = conf.get('BOS', 'host')
    bucket = conf.get('BOS', 'bucket')
    client = MyBosClient(ak, sk, host)
    return client.exist(bucket, object)


if __name__ == '__main__':
    exist('vol3e1b69a3-9e5e-441f-a28b-94fab143fd65_0_0_0')
    #print(exist(sys.argv[1]))