#!/usr/bin/env python
from db_util import MysqlClient
from statements import conf
import json


def de_duplication_metadata():
    client = MysqlClient(conf)
    sql = 'SELECT id, url FROM docmetadata'
    r = client.select(sql)
    dup = []
    collect = set()
    for id, url in r:
        if not url:
            dup.append(id)
            continue
        url = set(json.loads(url))
        if url not in collect:
            collect.add(id)
        else:
            dup.append(id)
    for id in dup:
        info = 'deleting %s from trhz.docmetadata' % (id)
        print(info)
        sql = 'DELETE FROM docmetadata WHERE id=\'%s\'' % (id)
        client.execute(sql)
    client.close()


def clean_metadata():
    client = MysqlClient(conf)
    sql = 'SELECT DISTINCT metadataId FROM docinstancestru'
    result = client.select(sql)
    instance_structure = [d[0] for d in result]
    sql = 'SELECT DISTINCT metadataId FROM doctemplatestru'
    result = client.select(sql)
    template_structure = [d[0] for d in result]
    referenced_metadata_ids = set(template_structure).union(set(instance_structure))
    sql = 'SELECT id FROM docmetadata'
    result = client.select(sql)
    metadata_ids = [d[0] for d in result]
    for metadata_id in metadata_ids:
        if metadata_id not in referenced_metadata_ids:
            print('clean metadata %s' % metadata_id)
            sql = 'DELETE FROM  docmetadata WHERE id=\'%s\'' % metadata_id
            client.execute(sql)
    client.close()


def clean_doc_instance_structure():
    client = MysqlClient(conf)
    sql = 'SELECT DISTINCT id FROM docinstance'
    result = client.select(sql)
    instance_ids = [d[0] for d in result]
    sql = 'SELECT id, insId FROM docinstancestru'
    result = client.select(sql)
    for structure_id, ins_id in result:
        if ins_id not in instance_ids:
            print('clean document instance structure %s' % structure_id)
            sql = 'DELETE FROM docinstancestru WHERE id=\'%s\'' % structure_id
            client.execute(sql)
    client.close()


def clean_doc_template_structure():
    client = MysqlClient(conf)
    sql = 'SELECT DISTINCT id FROM doctemplate'
    result = client.select(sql)
    template_ids = [d[0] for d in result]
    sql = 'SELECT id, tplId FROM doctemplatestru'
    result = client.select(sql)
    for structure_id, tpl_id in result:
        if tpl_id not in template_ids:
            print('clean document template tructure %s' % structure_id)
            sql = 'DELETE FROM doctemplatestru WHERE id=\'%s\'' % structure_id
            client.execute(sql)
    client.close()


def clean_all():
    de_duplication_metadata()
    clean_doc_instance_structure()
    clean_doc_template_structure()
    clean_metadata()


if __name__ == '__main__':
    clean_all()
