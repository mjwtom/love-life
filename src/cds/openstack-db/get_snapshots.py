#!/usr/bin/env python

import MySQLdb
import ConfigParser
import json


def get_cinder_snapshot_via_db(mysql_conf):
    """
    get the cinder uuid of the evm
    :param mysql_conf:
    :param volumes:
    :return:
    """
    print('db configuration')
    print(mysql_conf)
    snapshots = dict()
    conn = MySQLdb.connect(**mysql_conf)
    cursor = conn.cursor()
    cmd = 'SELECT id, volume_size, created_at, updated_at, deleted_at, status FROM snapshots'
    cursor.execute(cmd)
    results = cursor.fetchall()
    cursor.close()
    for result in results:
        id = result[0]
        volume_size = result[1]
        created_at = result[2]
        updated_at = result[3]
        deleted_at = result[4]
        status = result[5]
        updated_str = None
        if updated_at:
            updated_str = updated_at.strftime("%Y%m%d %H:%M:%S.%f")
        deleted_str = None
        if deleted_at:
            deleted_str = deleted_at.strftime("%Y%m%d %H:%M:%S.%f")
        info = dict(
            id=id,
            volume_size = volume_size,
            created_at=created_at.strftime("%Y%m%d %H:%M:%S.%f"),
            updated_at=updated_str,
            deleted_at_at= deleted_str,
            status=status
        )
        snapshots[id] = info
    conn.close()
    return snapshots


def get_all_snapshot():
    conf = ConfigParser.ConfigParser()
    conf.read('cinder-mysql.conf')
    mysql_conf = dict(
        host=conf.get('CINDER_MYSQL', 'host'),
        port=int(conf.get('CINDER_MYSQL', 'port')),
        user=conf.get('CINDER_MYSQL', 'user'),
        passwd=conf.get('CINDER_MYSQL', 'passwd'),
        db=conf.get('CINDER_MYSQL', 'db')
    )
    snapshots = get_cinder_snapshot_via_db(mysql_conf)
    with open('snapshots.json', 'w') as f:
        json.dump(snapshots, f)


if __name__ == '__main__':
    get_all_snapshot()