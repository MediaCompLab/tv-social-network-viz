import sqlite3


class SQLiteHelper(object):
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name,check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create(self, query, params=()):
        """执行创建语句（如INSERT）"""
        self.cursor.execute(query, params)
        self.connection.commit()

    def update(self, query, params=()):
        """执行更新语句（如UPDATE）"""
        self.cursor.execute(query, params)
        self.connection.commit()

    def get_all(self, query, params=()):
        """执行查询语句（如SELECT）并返回结果"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_one(self, query, params=()):
        """执行查询语句（如SELECT）并返回结果"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        """关闭数据库连接"""
        self.connection.close()