import json
from db_util import MysqlClient

conf = dict(
    host = '115.28.239.239',
    user = 'trhz',
    password = 'zhimakaimen',
    port = 3306,
    database = 'trhz',
    charset = 'utf8'
)


def metadata_insert(map):
    url = json.dumps(map)
    data = ('test', #metadata的名称
            'test', #摘要
            'majingwei', #签名，暂时应该没有用处
            url, #指定url，说明用哪个类的哪个函数来处理
            'majingwei',
            '0')
    sql = 'INSERT INTO trhz.docmetadata (metadata, digest, sign, url, addedBy, deleted) ' \
          'VALUES (%s, %s, %s, %s, %s, %s)'
    client = MysqlClient(conf)
    client.insert(sql, data)
    sql = 'select id from trhz.docmetadata where metadata = "test" and addedBy = "majingwei" and url = \'%s\'' % url
    r = client.select(sql)
    if r:
        return r[0][0]
    else:
        return None


def structure_insert(instanceId, order_num, metadataId=None):
    data =('-1',
           instanceId,
           order_num,
           '2',
           '3',
           metadataId,
           'test',
           'test',
           'majingwei',
           '0')
    sql = 'INSERT INTO trhz.docinstancestru ' \
          '(pId, insId, orderNum, struSign, struLevel, metadataId, struName, struDigest, addedBy, deleted) ' \
          'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    client = MysqlClient(conf)
    client.insert(sql, data)
    sql = 'select id from trhz.docinstancestru ' \
          'where insId = %d and orderNum = %d and addedBy = "majingwei" and metadataId = "%s"' \
          % (instanceId, order_num, metadataId)
    r = client.select(sql)
    if r:
        return r[0][0]
    else:
        return None


def instance_insert(param_map, projectId, init_map=None):
    params = json.dumps(param_map)
    init = json.dumps(init_map)
    data = ('1',
            '2',
            'test',
            'test',
            'test',
            'test',
            params,
            projectId,
            'majingwei',
            '2016-08-28 18:22:55',
            'majingwei',
            '2016-08-28 21:12:01',
            '0',
            init,
            'test.docx'
    )
    sql = 'INSERT INTO trhz.docinstance' \
          '(libId, tplId, insName, insDigest, identifier, version, params, projectId,' \
          'addedBy, addedTime, editedBy, editedTime, deleted, metadata, physicalFileName) ' \
          'VALUES ' \
          '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    client = MysqlClient(conf)
    client.insert(sql, data)
    sql = 'select id from trhz.docinstance where params = \'%s\' and addedBy = "majingwei"' \
          ' and projectId = "%s" and metadata = \'%s\'' \
          % (params, projectId, init)
    r = client.select(sql)
    if r:
        return r[0][0]
    else:
        return None


def clean_instance():
    sql = 'delete from trhz.docinstance where addedBy = "majingwei"'
    return sql


def clean_structure():
    sql = 'delete from trhz.docinstancestru where addedBy = "majingwei"'
    return sql


def clean_metadata():
    sql = 'delete from trhz.docmetadata where addedBy = "majingwei"'
    return sql
