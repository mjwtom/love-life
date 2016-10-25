import json
from db_util import MysqlClient
from statements import conf
from statements import get_property_id


def metadata_insert(map, name='test', digest='test', id=None):
    url = json.dumps(map)

    client = MysqlClient(conf)
    if not id:
        id = get_property_id(client, 'trhz.docmetadata')
    data = (id,
            name,  # metadata的名称
            digest,  # 摘要
            '2',  # 签名，暂时应该没有用处
            url,  # 指定url，说明用哪个类的哪个函数来处理
            1013,
            '0')
    sql = 'INSERT INTO trhz.docmetadata (id, metadata, digest, sign, url, addedBy, deleted) ' \
          'VALUES (%s, %s, %s, %s, %s, %s, %s)'
    client.insert(sql, data)
    sql = 'select id from trhz.docmetadata where metadata = \'%s\' and digest=\'%s\' and addedBy = 1013 and url = \'%s\'' \
          % (name, digest, url)
    r = client.select(sql)
    client.close()
    ids = [id for id, in r]
    if id not in ids:
        print('wrong id')
    return id


#code '1'章节 '2'正文
def template_structure_insert(tpl_id, pid, order_num, code, level,
                     name, digest, metadataId=None, id=None):
    client = MysqlClient(conf)
    if not id:
        id = get_property_id(client, 'trhz.doctemplatestru')
    data = (id,
            pid,
            tpl_id,
            order_num,
            code,
            level,
            metadataId,
            name,
            digest,
            1013,
            '0')
    sql = 'INSERT INTO trhz.doctemplatestru ' \
          '(id, pId, tplId, orderNum, struSign, struLevel, metadataId, struName, struDigest, addedBy, deleted) ' \
          'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    client.insert(sql, data)
    sql = 'select id from trhz.doctemplatestru ' \
          'where tplId = %d and orderNum = %d and addedBy = 1013 and pid=%d' \
          % (tpl_id, order_num, pid)
    r = client.select(sql)
    client.close()
    ids = [id for id, in r]
    if id not in ids:
        print("wrong id")
    return id


def template_insert(name, digest, id=None):
    client = MysqlClient(conf)
    if not id:
        id = get_property_id(client, 'trhz.doctemplate')
    data = (id,
            '1',
            name,
            digest,
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
    client.insert(sql, data)
    sql = 'select id from trhz.doctemplate where addedBy = 1013'
    r = client.select(sql)
    client.close()
    ids = [id for id, in r]
    if id not in ids:
        print('wrong id')
    return id


def get_break_page_metada_id():
    client = MysqlClient(conf)
    sql = 'SELECT id FROM trhz.docmetadata where metadata=\'%s\' ' \
          'and digest=\'%s\'' % ('【全局】分页', '分页')
    r = client.select(sql)
    client.close()
    if r:
        return r[0][0]
    map=dict(
            className='com.stms.tps.doc.Common',
            methodName='breakPage',
            params=None
        )
    id = metadata_insert(map, '【全局】分页', '分页')
    return id


def get_table_of_content_metada_id():
    client = MysqlClient(conf)
    sql = 'SELECT id FROM trhz.docmetadata where metadata=\'%s\' ' \
          'and digest=\'%s\'' % ('【全局】生成目录', '目录生成')
    r = client.select(sql)
    client.close()
    if r:
        return r[0][0]
    map=dict(
            className='com.stms.tps.doc.Common',
            methodName='tableOfContents',
            params=None
        )
    id = metadata_insert(map, '【全局】生成目录', '目录生成')
    return id


def clean_template():
    sql = 'delete from trhz.doctemplate where addedBy = 1013'
    return sql


def clean_template_structure():
    sql = 'delete from trhz.doctemplatestru where addedBy = 1013'
    return sql


def clean_metadata():
    sql = 'delete from trhz.docmetadata where addedBy = 1013'
    return sql
