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

    def insert(self, sql, data):
        cursor = self.conn.cursor()
        cursor.execute(sql, data)
        cursor.close()
        self.conn.commit()

    def execute(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()

    def execute_data(self, sql, data):
        cursor = self.conn.cursor()
        cursor.execute(sql, data)
        cursor.close()
        self.conn.commit()

    def close(self):
        self.conn.close()