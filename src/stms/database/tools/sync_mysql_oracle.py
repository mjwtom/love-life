from db_util import MysqlClient, OracleClient
from statements import conf


# oracle connection information 'username/password@adress:port:databasename
oracle_conn_info = 'trhz/zhimakaimen@115.28.239.239:1521/trhz'


def copy_table(table_name):
    mysql_client = MysqlClient(conf)
    oracle_client = OracleClient(oracle_conn_info)
    sql = 'SELECT * FROM %s' % table_name
    data = mysql_client.select(sql)
    for item in data:
        print('inserting', item)
        width = len(item)
        value_string = []
        for i in range(width):
            value_string.append(':'+str(i+1))
        value_string = ','.join(value_string)
        sql = 'INSERT INTO %s VALUES (%s)' % (table_name, value_string)
        try:
            oracle_client.insert(sql, item)
        except Exception as e:
            print(e)
    sql = 'SELECT * FROM %s' % table_name
    data = oracle_client.select(sql)
    for item in data:
        print(item)
    mysql_client.close()
    oracle_client.close()

if __name__ == "__main__":
    copy_table('docinstance')