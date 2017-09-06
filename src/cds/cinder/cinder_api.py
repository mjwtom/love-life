#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @author : Kong Shuaikang <kongshuaikang@baidu.com>
    @brief : basic class of all test cases
"""
import os
import time
import keystone_api
import sys
import json
import threading
import uuid

_NOW_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
_CONF_DIR = _NOW_PATH + '../../conf/vpc/'
_CONF_FILE = _CONF_DIR + 'config.ini'

sys.path.append(_NOW_PATH + '../../../')

from cases.lib import http
from cup.util.conf import Configure2Dict
from cup import log as logging

_conf_dict = Configure2Dict(_CONF_FILE).get_dict()
_test_type = _conf_dict["test_type"]
_test_region = _conf_dict["test_region"]
if _test_type == 'offline':
    _zone = _conf_dict[_test_type][_test_region]["az_zone"]
_logical_timeout = int(_conf_dict['logical_timeout'])


class CinderApi(object):
    """cinder api"""

    def __init__(self, user_name=None, password=None, tenant=None,
                 domain_name="Default", domain_id='default', keystone=None):
        """init"""
        super(CinderApi, self).__init__()
        self.expire = 0
        self.token = None
        if keystone:
            self.keystone = keystone
        else:
            self.keystone = keystone_api.Keystone(user_name, password,
                                                  tenant, domain_name, domain_id)
        self.cinder_url = self.keystone.getEndpoint('volumev2')
        if self.cinder_url == None:
            logging.warn("cinder URL is None in Iam, can't continue test")
            sys.exit(1)
        self.http_conn = http.Http(self.cinder_url)
        self.timeout = _logical_timeout

    def _getToken(self):
        """get token"""
        now = time.time()
        if now >= self.expire:
            self.token, self.expire = self.keystone.getToken()

        return self.token

    def _getHeaders(self):
        """get headers """
        headers = {
            "Content-type": "application/json",
            "X-Auth-Token": self._getToken()
        }
        return headers

    def createVol(self, **kwargs):
        """create volume """
        headers = self._getHeaders()
        volume = {}
        volume['size'] = kwargs.get('SIZE')
        volume['display_name'] = kwargs.get('DISPLAY_NAME', None)
        volume['snapshot_id'] = kwargs.get('SNAPSHOT_ID', None)
        volume['volume_type'] = kwargs.get('VOLUME_TYPE', 'ssd')
        volume['availability_zone'] = kwargs.get('AZ', _zone)
        body = {}
        body['volume'] = volume
        status, resp, _ = self.http_conn.access('POST', "/volumes", body=body, headers=headers)

        if status == 202:
            vol_info = json.loads(resp)['volume']
        else:
            return {}

        if self._waitVolOk(vol_info, self.timeout):
            return vol_info

        return {}

    def _waitVolOk(self, vol_info, timeout):
        """
        @param:in/out(dict)    vol_info, vol infomation
        @param:in(int > 0)     timeout, timeout for wait
        @return:out(bule)      return True if wait OK,else return False
        """
        t = 0
        while t < timeout:
            vol_status = self.getVolInfo(vol_info['id'])
            if not vol_status:
                return False

            if vol_status['status'] == 'available':
                return True

            time.sleep(5)
            t += 5

        return False

    def getVolInfo(self, vol_id):
        """get vol info"""
        headers = self._getHeaders()

        status, resp, _ = self.http_conn.access('GET', "/volumes/%s" % vol_id,
                                                headers=headers)
        if status != 200:
            return {}

        return json.loads(resp)['volume']

    def deleteVol(self, vol_id):
        """delete volume """
        headers = self._getHeaders()

        status, resp, _ = self.http_conn.access("DELETE", "/volumes/%s" % vol_id,
                                                headers=headers)

        if status != 202:
            return False

        return True

    def createSnap(self, vol_id, **kwargs):
        """create snapshot """
        headers = self._getHeaders()

        name = kwargs.get('name', '')
        type = kwargs.get('type', 'manual')

        snapshot = {}
        snapshot['name'] = name
        snapshot['volume_id'] = vol_id
        metadata = {}
        metadata['create_method'] = type
        snapshot['metadata'] = metadata
        snapshot['force'] = True
        body = {}
        body['snapshot'] = snapshot

        status, resp, _ = self.http_conn.access('POST', "/snapshots", body=body, headers=headers)

        if status == 202:
            snap_info = json.loads(resp)['snapshot']
        else:
            return {}

        if self._waitSnapOk(snap_info, self.timeout):
            return snap_info

        return {}

    def deleteSnap(self, snap_id):
        """delete snapshot """
        headers = self._getHeaders()

        status, resp, _ = self.http_conn.access("DELETE", "/snapshots/%s" % snap_id,
                                                headers=headers)

        if status != 202:
            return False

        return True

    def _waitSnapOk(self, snap_info, timeout):
        """
        @param:in/out(dict)    snap_info, snap infomation
        @param:in(int > 0)     timeout, timeout for wait
        @return:out(bule)      return True if wait OK,else return False
        """
        t = 0
        while t < timeout:
            snap_status = self.getSnapInfo(snap_info['id'])
            if not snap_status:
                return False

            if snap_status['status'] == 'available':
                return True

            time.sleep(5)
            t += 5

        return False

    def getSnapInfo(self, snap_id):
        """get snap info"""
        headers = self._getHeaders()

        status, resp, _ = self.http_conn.access('GET', "/snapshots/%s" % snap_id,
                                                headers=headers)
        if status != 200:
            return {}

        return json.loads(resp)['snapshot']

    def listSnap(self):
        """list snap """
        headers = self._getHeaders()

        status, resp, _ = self.http_conn.access('GET', "/snapshots/detail",
                                                headers=headers)
        if status != 200:
            return {}

        return json.loads(resp)['snapshots']

    def listVolSnap(self, vol_id):
        """list snap by volume """
        headers = self._getHeaders()

        status, resp, _ = self.http_conn.access('GET', "/snapshots/" + vol_id + "/os-snapshots",
                                                headers=headers)
        if status != 200:
            return {}

        return json.loads(resp)['snapshots']

    def listSnapcnt(self):
        """list snapcnt """
        headers = self._getHeaders()

        status, resp, _ = self.http_conn.access('GET', "/snapshots/list_project_snapshots_cnt",
                                                headers=headers)
        if status != 200:
            return {}

        return json.loads(resp)['snapshots']

    def resizeVol(self, vol_id, new_vol_size):
        """resize vol """
        headers = self._getHeaders()

        body = {
            "os-extend": {
                "new_size": new_vol_size
            }
        }

        status, resp, _ = self.http_conn.access('POST', "/volumes/%s/action" % vol_id,
                                                body=body, headers=headers)

        if status != 202:
            return False

        vol_info = {'id': vol_id}

        if self._waitVolOk(vol_info, self.timeout):
            return True

        return True

    def rollbackSnap(self, vol_id, snap_id):
        """rollback """
        headers = self._getHeaders()

        body = {}
        rollback = {}
        rollback['snapshot_id'] = snap_id
        body['os-rollback'] = rollback

        status, resp, _ = self.http_conn.access('POST', "/volumes/" + vol_id + "/action",
                                                body=body, headers=headers)
        if status != 202:
            return False

        vol_info = {'id': vol_id}

        if self._waitVolOk(vol_info, self.timeout):
            return True

        return False

