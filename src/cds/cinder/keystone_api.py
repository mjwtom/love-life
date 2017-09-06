"""Created on Oct 28, 2014
@author: yangbinglin
"""
import datetime
import hashlib
import hmac
import json
import time
import urlparse
import urllib
import os
import sys

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
    _keystone_endpoint = _conf_dict[_test_type][_test_region]['OS_AUTH_URL']
    _admin_user = _conf_dict[_test_type][_test_region]['OS_USERNAME']
    _admin_pass = _conf_dict[_test_type][_test_region]['OS_PASSWORD']
    _admin_tenant = _conf_dict[_test_type][_test_region]['OS_TENANT_NAME']
else:
    _keystone_endpoint = None
    _admin_user = None
    _admin_pass = None
    _admin_tenant = None

class Keystone(object):
    """keystone api"""
    def __init__(self, username=_admin_user, password=_admin_pass, tenantname=_admin_tenant,
                 domain_name="PASSPORT:2256818296", 
                 domain_id='f1cd05328cad4155b5839393f2c24ce8', is_console_user=False):
        """init"""
        super(Keystone, self).__init__()
        global _keystone_endpoint
        if username is None:
            self.username = _admin_user
        if password is None:
            self.password = _admin_pass
        if tenantname is None:
            self.tenantname = _admin_tenant
        self.domain_name = domain_name
        self.domain_id = domain_id
        if 'v2.0' in _keystone_endpoint:
            self.version = 2
        elif 'v3' in _keystone_endpoint:
            self.version = 3
        if is_console_user:
            _keystone_endpoint = _keystone_endpoint.replace('v2.0', 'v3')
            self.version = 3

        self.http_conn = http.Http(_keystone_endpoint)
        
        if self.version == 2:
            self.response_cache = self._getResponse()
            self.tenant_id = self.response_cache['access']['token']\
                                                ['tenant']['id']
            self.user_id = self.response_cache['access']['user']\
                                                ['id']
        else:
            self.response_cache = self._get_v3_response(is_console_user)
            self.tenant_id = self.response_cache['token']['project']['id']
            self.user_id = self.response_cache['token']['user']['id']

    def _get_v3_response(self, is_console_user=False):
        """v3 api"""
        if is_console_user:
            data = {
                "auth": {
                    "identity": {
                        "methods":["password"],
                        "password": {
                            "user": {
                                "domain": {
                                    "id":"%s" % self.domain_id
                                },
                                "id": "%s" % self.domain_id,
                                "password": "%s" % self.password
                            }
                        }
                    },
                    "scope": {
                        "project": {
                            "domain": {
                                "id": "%s" % self.domain_id
                            },
                            "id": "%s" % self.tenantname
                        }
                    }
                }
            }
        else:
            data = {
                "auth": {
                    "identity": {
                        "methods":["password"],
                        "password": {
                            "user": {
                                "domain": {
                                    "name":"%s" % self.domain_name
                                },
                                "name": "%s" % self.username,
                                "password": "%s" % self.password
                            }
                        }
                    },
                    "scope": {
                        "project": {
                            "domain": {
                                "id": "%s" % self.domain_id
                            },
                            "name": "%s" % self.tenantname
                        }
                    }
                }
            }

        header = {"Content-type": "application/json"}
        params = json.dumps(data)
        status, resp, headers = self.http_conn.access('POST', url='/auth/tokens',
                                    body=params, headers=header)

        if status != 201:
            logging.warn("Get token Fail")
            return None

        resp = json.loads(resp, strict=False)
        resp['token']['id'] = headers.get('x-subject-token')
        return resp

    def _getResponse(self):
        """get iam response"""
        passwordCredentials = {}
        auth = {}
        data = {}
        passwordCredentials['username'] = self.username
        passwordCredentials['password'] = self.password
        auth['passwordCredentials'] = passwordCredentials
        auth['tenantName'] = self.tenantname
        data['auth'] = auth
        params = json.dumps(data)
        header = {"Content-type": "application/json"}
        status, resp, _ = self.http_conn.access('POST', url='/tokens',
                            body=params, headers=header)

        if status != 200:
            logging.warn("Get token Fail")
            return None

        return json.loads(resp, strict=False)

    def _get_v3_token(self):
        """get v3 api token"""
        token = None
        if not self.response_cache or not self.response_cache.get('token', None)\
            or not self.response_cache['token'].get('expires_at', None)\
            or time.time() - 60 > time.mktime(time.strptime(
                                                  self.response_cache['token']['expires_at'],
                                                  "%Y-%m-%dT%H:%M:%S.%fZ"))\
                                  - time.timezone:
            self.response_cache = self._get_v3_response()

        if not self.response_cache or not self.response_cache.get('token', None) \
            or not self.response_cache['token'].get('expires_at', None):
            return (None, None)

        token = self.response_cache['token']['id']
        expire = time.strptime(self.response_cache['token']['expires_at'],
                    "%Y-%m-%dT%H:%M:%S.%fZ")
        expire = time.mktime(expire) - time.timezone
        return (token, expire)

    def _get_v2_token(self):
        """get v2 token"""
        token = None
        if not self.response_cache or not self.response_cache.get("access", None)\
                or not self.response_cache['access'].get('token', None)\
                or time.time() - 60 > time.mktime(time.strptime(
                                           self.response_cache['access']['token'].get(
                                               'expires', "1970-01-01T00:00:00Z"),
                                               "%Y-%m-%dT%H:%M:%SZ"))\
                                      - time.timezone:
            self.response_cache = self._getResponse()

        if not self.response_cache or not self.response_cache.get('access', None)\
                or not self.response_cache['access'].get('token', None):

            return (None, None)

        token = self.response_cache['access']['token']['id']
        expire = time.strptime(self.response_cache['access']['token']['expires'],
                     "%Y-%m-%dT%H:%M:%SZ")
        expire = time.mktime(expire) - time.timezone
        return (token, expire)

    def getToken(self):
        """get token"""
        if self.version == 2:
            return self._get_v2_token()
        else:
            return self._get_v3_token()

    def getTenantId(self):
        """get tenant_id"""
        return self.tenant_id

    def getUserId(self):
        """get user id"""
        return self.user_id

    def _get_v3_endpoint(self, service_type):
        """get v3 endpoint info"""
        if self.response_cache and self.response_cache.get('token', None)\
            and self.response_cache['token'].get('catalog', None):
            for value in self.response_cache['token']['catalog']:
                if value and value.get('type', None) == service_type:
                    for endpoint in value.get('endpoints', []):
                        if endpoint.get('interface', None) == 'public':
                            return endpoint.get('url', None)

        return None

    def _get_v2_endpoint(self, service_type):
        """get v2 endpoint info"""
        if self.response_cache and self.response_cache.get('access', None)\
                and self.response_cache['access'].get('serviceCatalog', None):
            for value in self.response_cache['access']['serviceCatalog']:
                if value and value.get('type') == service_type:
                    return value.get('endpoints')[0].get('publicURL')
                else:
                    continue

        return None

    def getEndpoint(self, service_type):
        """get endpoint info"""
        if self.version == 2:
            return self._get_v2_endpoint(service_type)
        else:
            return self._get_v3_endpoint(service_type)

    def _createTenant(self, tenant_name, admin_token):
        """create tenant"""
        if self.version == 2:
            resource = "tenant"
        else:
            resource = "project"
        body = {}
        body[resource] = {}
        body[resource]["name"] = tenant_name
        body[resource]["description"] = "%s tenant" % tenant_name

        headers = {}
        headers["Content-type"] = "application/json"
        headers["X-Auth-Token"] = admin_token

        status, resp, _ = self.http_conn.access('POST', '/%ss' % resource, body, headers)

        if status != 200 and status != 409 and status != 201:
            logging.warn("Create Tenant  Fail")
            return None

        return json.loads(resp, strict=False)[resource]['id']

    def _getUser(self, user_name, admin_token):
        """get user"""
        headers = {}
        headers["Content-type"] = "application/json"
        headers["X-Auth-Token"] = admin_token

        status, resp, _ = self.http_conn.access('GET', '/users?name=%s' % user_name,
                           headers=headers)
        if status != 200:
            logging.warn("Get All User info Fail")
            return None

        users = json.loads(resp)
        if self.version == 2:
            users = users.get('user', {})
        else:
            users = users.get('users', [])
            if not users:
                return None
            users = users[0]
        if users.get('name', None) == user_name:
            return users.get('id', None)

        return None

    def _getTenant(self, tenant_name, admin_token):
        """get tenant"""
        if self.version == 2:
            resource = "tenant"
        else:
            resource = "project"

        headers = {}
        headers["Content-type"] = "application/json"
        headers["X-Auth-Token"] = admin_token

        status, resp, _ = self.http_conn.access('GET', '/%ss?name=%s' % (resource, tenant_name),
                           headers=headers)
        if status != 200:
            logging.warn("Get All User info Fail")
            return None

        tenants = json.loads(resp)
        if self.version == 2:
            tenants = tenants.get(resource, {})
        else:
            tenants = tenants.get("%ss"%resource, [])
            if not tenants:
                return None
            tenants = tenants[0]

        if tenants.get('name', None) == tenant_name:
            return tenants.get('id', None)

        return None

    def _createUser(self, user_name, admin_token):
        """create user"""
        body = {}
        body["user"] = {}
        body["user"]["name"] = user_name
        body["user"]["email"] = "%s@baidu.com" % user_name
        body["user"]["password"] = user_name

        headers = {}
        headers["Content-type"] = "application/json"
        headers["X-Auth-Token"] = admin_token

        status, resp, _ = self.http_conn.access('POST', '/users', body, headers)

        if status != 200 and status != 201 and status != 409:
            logging.warn("Create User Fail")
            return None

        return json.loads(resp, strict=False)['user']['id']

    def _addUserRole(self, user_id, tenant_id, admin_token):
        """add user role"""
        headers = {}
        headers["Content-type"] = "application/json"
        headers["X-Auth-Token"] = admin_token
        if self.version == 2:

            status, resp, _ = self.http_conn.access('GET', '/OS-KSADM/roles',
                                headers=headers)
        else:
            status, resp, _ = self.http_conn.access('GET', '/roles?name=_member_',
                                headers=headers)
            resource = 'project'

        if status != 200:
            logging.warn("Get Roles info Fail")

        roles = json.loads(resp)
        if not roles.get('roles', None):
            return False

        role_id = None
        for role in roles['roles']:
            if role['name'] == '_member_':
                role_id = role['id']
                break

        if not role_id:
            return False

        if self.version == 2:
            status, resp, _ = self.http_conn.access('PUT',
                                '/tenants/%s/users/%s/roles/OS-KSADM/%s'
                                % (tenant_id, user_id, role_id), headers=headers)
        else:
            status, resp, _ = self.http_conn.access('PUT',
                                '/projects/%s/users/%s/roles/%s'
                                % (tenant_id, user_id, role_id), headers=headers)

        if status != 200 and status != 409 and status != 204:
            return False

        return True

    def _deleteUser(self, user_id, admin_token):
        """delete user"""
        headers = {}
        headers["Content-type"] = "application/json"
        headers["X-Auth-Token"] = admin_token

        status, resp, _ = self.http_conn.access('DELETE', '/users/%s' % user_id, headers=headers)

        if status != 204:
            return False

        return True

    def _deleteTenant(self, tenant_id, admin_token):
        """delete tenant"""
        headers = {}
        headers["Content-type"] = "application/json"
        headers["X-Auth-Token"] = admin_token

        if self.version == 2:
            resource = 'tenant'
        else:
            resource = 'project'

        status, resp, _ = self.http_conn.access('DELETE',
                            '/%ss/%s' % (resource, tenant_id),
                            headers=headers)

        if status != 204:
            return False

        return True

    def createUser(self, user_name, admin_token):
        """create user"""
        user_id = self._getUser(user_name, admin_token)
        tenant_id = self._getTenant('%s_project' % user_name, admin_token)

        if user_id and tenant_id:
            return True

        if not user_id:
            user_id = self._createUser(user_name, admin_token)

        if not user_id:
            return False

        if not tenant_id:
            tenant_id = self._createTenant("%s_project" % user_name, admin_token)

        if not tenant_id:
            return False

        if not self._addUserRole(user_id, tenant_id, admin_token):
            return False

        return True

    def deleteUser(self, user_name, admin_token):
        """delete user"""
        user_id = self._getUser(user_name, admin_token)
        tenant_id = self._getTenant('%s_project' % user_name, admin_token)
        if user_id:
            self._deleteUser(user_id, admin_token)

        if tenant_id:
            self._deleteTenant(tenant_id, admin_token)

    def _createAksk(self, user_id, admin_token):
        """internal create ak sk"""
        headers = {}
        headers["Content-type"] = "application/json"
        headers["X-Auth-Token"] = admin_token

        status, resp, _ = self.http_conn.access('POST',
                            '/users/%s/accesskeys' % user_id,
                            headers=headers)

        if status != 201:
            return None, None

        resp = json.loads(resp)
        ak = resp.get('accesskey', {}).get('access', None)
        sk = resp.get('accesskey', {}).get('secret', None)
        return ak, sk

    def _getAksk(self, user_id, admin_token):
        """get ak sk"""
        headers = {}
        headers["Content-type"] = "application/json"
        headers["X-Auth-Token"] = admin_token

        status, resp, _ = self.http_conn.access('GET',
                            '/users/%s/accesskeys' % user_id,
                            headers=headers)

        if status != 200:
            return None, None

        resp = json.loads(resp)
        aksks = resp.get('accesskeys', [])
        if not aksks:
            return None, None

        aksk = aksks[0]
        ak = aksk.get('access', None)
        sk = aksk.get('secret', None)

        return ak, sk

    def createAksk(self, user_name, admin_token):
        if self.version == 2:
            logging.warn("AK/SK need v3 keystone url")
            return None, None
        user_id = self._getUser(user_name, admin_token)

        ak, sk = self._getAksk(user_id, admin_token)
        if not ak and not sk:
            ak, sk = self._createAksk(user_id, admin_token)

        return ak, sk

    @staticmethod
    def gen_signature(ak, sk, url, method, headers, version=1):
        """genarate signature"""
        if not headers.get('Host', None):
            logging.warn("signature need host info")
            return None
        if not headers.get('x-bce-date', None):
            logging.warn("signature need x-bce-date info")
            return None

        url_list = urlparse.urlparse(url)
        query_param = url_list.query.split('&')
        query_param.sort()
        query_param = '&'.join(query_param)
        str_req = '\n'.join([method, url_list.path, query_param,
            "host:%s" % (urllib.quote(headers.get('Host'))),
            "x-bce-date:%s" % (urllib.quote(headers.get('x-bce-date')))])
        timestamp = headers.get('x-bce-date')
        str_sign = '/'.join(['bce-auth-v%s' % str(version), ak, timestamp, '1800'])
        str_key = hmac.new(str(sk), str_sign, digestmod=hashlib.sha256).hexdigest()
        signature = hmac.new(str_key, str_req, digestmod=hashlib.sha256).hexdigest()

        signature = '/'.join([str_sign, 'host;x-bce-date', signature])
        return signature

