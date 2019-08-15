import httplib
from keystone import KeyStone
import ConfigParser
import json
import urllib


class Cinder(object):
    def __init__(self, conf_path='openstack.conf'):
        conf = ConfigParser.ConfigParser()
        conf.read(conf_path)
        endpoint = conf.get('OpenStack', 'endpoint')
        username = conf.get('OpenStack', 'username')
        password = conf.get('OpenStack', 'password')
        tenant_name = conf.get('OpenStack', 'tenant_name')
        self._snapshot_uri = '/snapshots/detail'
        self._keystone = KeyStone(endpoint, username, password, tenant_name)

    def _get_cinder_url(self, resp):
        catalogs = resp.get('token').get('catalog')
        for cata in catalogs:
            if 'volumev2' != cata.get('type'):
                continue
            endpoints = cata.get('endpoints')
            for endpint in endpoints:
                if 'public' != endpint.get('interface'):
                    continue
                return endpint.get('url')

    def _get_cinder_inf(self):
        headers, keystone_resp = self._keystone.get_auth()
        cinder_url = self._get_cinder_url(keystone_resp)
        substr = cinder_url[len('http://'):]
        pos = substr.find('/')
        self._cinder_endpoint = substr[:pos]
        self._cinder_url  = cinder_url
        self._token = headers.get('x-subject-token')

    def list_snapshot(self, status=None):
        self._get_cinder_inf()
        headers = dict()
        headers['Content-type'] = 'application/json'
        headers['x-auth-token'] = self._token
        h = httplib.HTTPConnection(self._cinder_endpoint)
        offset = 0
        limit = 100
        all_snapshots = []
        while True:
            params = urllib.urlencode({'offset': str(offset), 'limit': str(limit)})
            url = self._cinder_url + self._snapshot_uri + '?' + params
            print(url)
            h.request('GET', url=url,
                      headers=headers)
            resp = h.getresponse()
            data = resp.read()
            snapshots = json.loads(data).get('snapshots')
            print(snapshots)
            all_snapshots.extend(snapshots)
            offset += len(snapshots)
            if len(snapshots) < limit:
                break
        return all_snapshots


def test():
    cinder_client = Cinder()
    snaps = cinder_client.list_snapshot()
    print(len(snaps))


if __name__ == '__main__':
    test()