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


def metadata_insert(map):
    url = json.dumps(map)
    data = ('test',  # metadata的名称
            'test',  # 摘要
            '4',  # 签名，暂时应该没有用处
            url,  # 指定url，说明用哪个类的哪个函数来处理
            1013,
            '0')
    sql = 'INSERT INTO trhz.docmetadata (metadata, digest, sign, url, addedBy, deleted) ' \
          'VALUES (%s, %s, %s, %s, %s, %s)'
    client = MysqlClient(conf)
    client.insert(sql, data)
    sql = 'select id from trhz.docmetadata where metadata = "test" and addedBy = 1013 and url = \'%s\'' % url
    r = client.select(sql)
    client.close()
    if r:
        return r[0][0]
    else:
        return None


#code '1'章节 '2'正文
def structure_insert(instanceId, pid, order_num, code, level,
                     name, digest, metadataId=None):
    data = (pid,
            instanceId,
            order_num,
            code,
            level,
            metadataId,
            name,
            digest,
            1013,
            '0')
    sql = 'INSERT INTO trhz.doctemplatestru ' \
          '(pId, tplId, orderNum, struSign, struLevel, metadataId, struName, struDigest, addedBy, deleted) ' \
          'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    client = MysqlClient(conf)
    client.insert(sql, data)
    sql = 'select id from trhz.doctemplatestru ' \
          'where tplId = %d and orderNum = %d and addedBy = 1013' \
          % (instanceId, order_num)
    r = client.select(sql)
    client.close()
    if r:
        return r[0][0]
    else:
        return None


def instance_insert(param_map, projectId, id=None, init_map=None):
    params = json.dumps(param_map)
    if init_map:
        init = json.dumps(init_map)
    else:
        init = None
    data = (id,
            '1',
            'test',
            'test',
            1013,
            1013,
            '0',
            '2016-09-22 17:37:04',
            '2016-09-22 17:37:04'
            )
    sql = 'INSERT INTO trhz.doctemplate' \
          '(id, libId, tplName, tplDigest,' \
          'addedBy, editedBy, deleted, addedTime, editedTime) ' \
          'VALUES ' \
          '(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    client = MysqlClient(conf)
    client.insert(sql, data)
    sql = 'select id from trhz.doctemplate where addedBy = 1013'
    r = client.select(sql)
    client.close()
    if r:
        return r[0][0]
    else:
        return None


def clean_instance():
    sql = 'delete from trhz.doctemplate where addedBy = 1013'
    return sql


def clean_structure():
    sql = 'delete from trhz.doctemplatestru where addedBy = 1013'
    return sql


def clean_metadata():
    sql = 'delete from trhz.docmetadata where addedBy = 1013'
    return sql
