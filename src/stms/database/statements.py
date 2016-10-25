import json
from db_util import MysqlClient

conf = dict(
    host='115.28.239.239',
    user='trhz',
    password='zhimakaimen',
    port=3306,
    database='trhz',
    charset='utf8'
)


def get_property_id(client, table_name):
    ids = []
    sql = 'select id from %s' % table_name
    result = client.select(sql)
    for id, in result:
        ids.append(id)
    ids.sort()
    if len(ids) == 0:
        return 0
    cur = 0
    pre = cur
    while ids:
        cur = ids.pop(0)
        if cur-pre > 1:
            return pre+1
        pre = cur
    return cur+1


#code '1'章节 '2'正文
def structure_insert(instanceId, pid, order_num, code, level,
                     name, digest, metadataId=None, id=None):
    client = MysqlClient(conf)
    if not id:
        id = get_property_id(client, 'trhz.docinstancestru')
    data = (id,
            pid,
            instanceId,
            order_num,
            code,
            level,
            metadataId,
            name,
            digest,
            1013,
            '0')
    sql = 'INSERT INTO trhz.docinstancestru ' \
          '(id, pId, insId, orderNum, struSign, struLevel, metadataId, struName, struDigest, addedBy, deleted) ' \
          'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    client.insert(sql, data)
    sql = 'select id from trhz.docinstancestru ' \
          'where insId = %d and orderNum = %d and addedBy = 1013' \
          % (instanceId, order_num)
    r = client.select(sql)
    client.close()
    ids = [id for id, in r]
    if id not in ids:
        print('wrong id')
    return id


def instance_insert(param_map, projectId, name='test',
                    digest='test', init_map=None, id=None):
    params = json.dumps(param_map)
    if init_map:
        init = json.dumps(init_map)
    else:
        init = None
    client = MysqlClient(conf)
    if not id:
        id = get_property_id(client, 'trhz.docinstance')
    data = (id,
            1,
            name,
            digest,
            'test',
            'test',
            params,
            projectId,
            1013,
            1013,
            '0',
            init,
            'test.docx',
            '2016-09-22 17:37:04',
            '2016-09-22 17:37:04'
            )
    sql = 'INSERT INTO trhz.docinstance' \
          '(id, tplId, insName, insDigest, identifier, version, params, projectId,' \
          'addedBy, editedBy, deleted, metadata, physicalFileName, addedTime, editedTime) ' \
          'VALUES ' \
          '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    client.insert(sql, data)
    sql = 'select id from trhz.docinstance where params = \'%s\' and addedBy = 1013' \
          ' and projectId = %d' \
          % (params, projectId)
    r = client.select(sql)
    client.close()
    ids = [id for id, in r]
    if id not in ids:
        print('wrong id')
    return id


def clean_instance():
    sql = 'delete from trhz.docinstance where addedBy = 1013'
    return sql


def clean_structure():
    sql = 'delete from trhz.docinstancestru where addedBy = 1013'
    return sql


def clean_metadata():
    sql = 'delete from trhz.docmetadata where addedBy = 1013'
    return sql
