from db_util import MysqlClient, OracleClient
from statements import conf


# oracle connection information 'username/password@adress:port:databasename
oracle_conn_info = 'trhz/zhimakaimen@115.28.239.239:1521/trhzuuid'


def copy_table(table_name):
    mysql_client = MysqlClient(conf)
    oracle_client = OracleClient(oracle_conn_info)
    sql = 'SELECT * FROM %s' % table_name
    data = mysql_client.select(sql)
    for item in data:
        print('inserting', item)
        sql = 'INSERT INTO %s VALUES' % table_name
        oracle_client.insert(sql, item)
    data = oracle_client.select(sql)
    print(data)
    mysql_client.close()
    oracle_client.close()

if __name__ == "__main__":
    copy_table('docinstance')