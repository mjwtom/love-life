import json
from db_util import MysqlClient
from statements import conf
from statements import get_property_id

global all_metadata
all_metadata = None

def empty_template(template_id):
    client = MysqlClient(conf)
    sql = 'SELECT id FROM doctemplate WHERE id=\'%s\'' % template_id
    r = client.select(sql)
    ids = [id for id, in r]
    if template_id not in ids:
        client.close()
        return None
    sql = 'SELECT id FROM doctemplatestru WHERE tplId=\'%s\'' % template_id
    r = client.select(sql)
    ids = [id for id, in r]
    for structure_id in ids:
        text = 'deleting %s from doctemplatestru' % structure_id
        print(text)
        sql = 'DELETE FROM doctemplatestru WHERE id=\'%s\'' % structure_id
        client.execute(sql)
    client.close()
    return template_id


def find_metadata(map):
    global all_metadata
    if not all_metadata:
        client = MysqlClient(conf)
        sql = 'SELECT id, url FROM docmetadata'
        all_metadata = client.select(sql)
        client.close()
    for id, url in all_metadata:
        url_dict = json.loads(url)
        same = True
        for key, value in map.items():
            if value != url_dict.get(key):
                same = False
                break
        if same:
            return id
    return None


def insert_to_all_metadata(id ,map):
    global all_metadata
    all_metadata.append((id, map))


def metadata_insert(map, name='test', digest='test', id=None):
    # try to find it in the docmetadata table
    id = find_metadata(map)
    if id:
        return id
    url = json.dumps(map)
    client = MysqlClient(conf)
    if not id:
        id = get_property_id(client, 'docmetadata')
    data = (id,
            name,  # metadata的名称
            digest,  # 摘要
            '2',  # 签名，暂时应该没有用处
            url,  # 指定url，说明用哪个类的哪个函数来处理
            1013,
            '0')
    sql = 'INSERT INTO docmetadata (id, metadata, digest, sign, url, addedBy, deleted) ' \
          'VALUES (%s, %s, %s, %s, %s, %s, %s)'
    client.insert(sql, data)
    sql = 'SELECT id FROM docmetadata WHERE metadata = \'%s\' AND digest=\'%s\' AND addedBy = 1013 AND url = \'%s\'' \
          % (name, digest, url)
    r = client.select(sql)
    client.close()
    ids = [id for id, in r]
    if id not in ids:
        print('wrong id')
    insert_to_all_metadata(id, map)
    return id


#code '1'章节 '2'正文
def template_structure_insert(tpl_id, pid, order_num, code, level,
                     name, digest, metadataId=None, id=None):
    client = MysqlClient(conf)
    if not id:
        id = get_property_id(client, 'doctemplatestru')
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
    sql = 'INSERT INTO doctemplatestru ' \
          '(id, pId, tplId, orderNum, struSign, struLevel, metadataId, struName, struDigest, addedBy, deleted) ' \
          'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    client.insert(sql, data)
    sql = 'select id from doctemplatestru ' \
          'where tplId = \'%s\' and orderNum = %d and addedBy = 1013 and pid=\'%s\'' \
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
        id = get_property_id(client, 'doctemplate')
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
    sql = 'INSERT INTO doctemplate' \
          '(id, libId, tplName, tplDigest,' \
          'addedBy, editedBy, deleted, addedTime, editedTime) ' \
          'VALUES ' \
          '(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    client.insert(sql, data)
    sql = 'select id from doctemplate where addedBy = 1013'
    r = client.select(sql)
    client.close()
    ids = [id for id, in r]
    if id not in ids:
        print('wrong id')
    return id


def get_break_page_metada_id():
    client = MysqlClient(conf)
    sql = 'SELECT id FROM docmetadata where metadata=\'%s\' ' \
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
    sql = 'SELECT id FROM docmetadata where metadata=\'%s\' ' \
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
    sql = 'delete from doctemplate where addedBy = 1013'
    return sql


def clean_template_structure():
    sql = 'delete from doctemplatestru where addedBy = 1013'
    return sql


def clean_metadata():
    sql = 'delete from docmetadata where addedBy = 1013'
    return sql
