from db_util import MysqlClient


conf = dict(
    host = '115.28.239.239',
    user = 'trhz',
    password = 'zhimakaimen',
    port = 3306,
    database = 'trhz',
    charset = 'utf8'
)


def showTables():
    client = MysqlClient(conf)
    r = client.select('show tables')
    print(r)


def createData():
    pass


if __name__ == '__main__':
    createData()
    showTables()
