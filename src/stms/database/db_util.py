import mysql.connector


class MysqlClient(object):
    def __init__(self, conf):
        self.conn = mysql.connector.connect(**conf)

    def select(self, cmd):
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        result = [r for r in cursor]
        cursor.close()
        return result

    def insert(self, cmd):
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        cursor.close()

    def close(self):
        self.conn.close()