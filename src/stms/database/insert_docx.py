from db_util import MysqlClient
from statements import instance_insert, metadata_insert, structure_insert, \
clean_instance, clean_structure, clean_metadata, instance_insert


conf = dict(
    host = '115.28.239.239',
    user = 'trhz',
    password = 'zhimakaimen',
    port = 3306,
    database = 'trhz',
    charset = 'utf8'
)


def clean():
    client = MysqlClient(conf)
    sql = clean_instance()
    client.execute(sql)
    sql = clean_structure()
    client.execute(sql)
    sql = clean_metadata()
    client.execute(sql)
    client.close()


def insert_test_report():
    init_map = dict(
        className = 'com.stms.tps.doc.TestOutlineImpl',
        methodName = 'initMetadata',
        params =  ["projectId"]
    )
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    order_num = 0
    #instance_id = instance_insert(param_map, '13', init_map)
    instance_id = instance_insert(param_map, '13')
    metadata_params = ['projectId']
    metadata_map = dict(
        className = 'com.stms.tps.doc.TestReportImpl',
        methodName = 'getTpsProductSpec',
        params = metadata_params
    )
    metadata_id = metadata_insert(metadata_map)
    structure_insert(instance_id, order_num, metadata_id)
    order_num += 1
    structure_insert(instance_id, order_num)
    order_num += 1
    print("doc instance id %s" % instance_id)


if __name__ == '__main__':
    clean()
    insert_test_report()
