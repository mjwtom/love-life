import httplib
import json
import ConfigParser


class KeyStone(object):
    def __init__(self, endpoint, username, password,
                 tenant_name='service',
                 user_domain_name='default',
                 project_domain_name='default'):
        self._endpoint = endpoint
        self._username = username
        self._password = password
        self._tenant_name = tenant_name
        self._user_domain_name = user_domain_name
        self._project_domain_name = project_domain_name
        self._key_stone_uri = '/v3/auth/tokens'
        self._cache_path = '.cache'

    def _get_headers(self):
        headers = dict()
        headers['Content-type'] = 'application/json'
        return headers

    def _resp_headers_to_dict(self, hearders_list):
        header_dict = dict()
        for key, value in hearders_list:
            header_dict[key] = value
        return header_dict

    def get_auth(self):
        body_data = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "domain": {
                                "id": "%s" % self._user_domain_name
                            },
                            "name": "%s" % self._username,
                            "password": "%s" % self._password
                        }
                    }
                },
                "scope": {
                    "project": {
                        "domain": {
                            "id": "%s" % self._project_domain_name
                        },
                        "name": "%s" % self._tenant_name
                    }
                }
            }
        }
        body = json.dumps(body_data)
        h = httplib.HTTPConnection(self._endpoint)
        h.request('POST', url=self._key_stone_uri, body=body,
                                  headers=self._get_headers())
        resp = h.getresponse()
        data = resp.read()
        headers = resp.getheaders()
        print(headers)
        print(data)
        return self._resp_headers_to_dict(headers), json.loads(data)


def test_keystone():
    conf = ConfigParser.ConfigParser()
    conf.read('openstack.conf')
    endpoint = conf.get('OpenStack', 'endpoint')
    username = conf.get('OpenStack', 'username')
    password = conf.get('OpenStack', 'password')
    tenant_name = conf.get('OpenStack', 'tenant_name')
    keystone = KeyStone(endpoint, username, password, tenant_name)
    headers, body = keystone.get_auth()
    print(headers)
    print(body)


if __name__ == '__main__':
    test_keystone()