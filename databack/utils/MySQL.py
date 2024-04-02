import pymysql
from dbutils.pooled_db import PooledDB
from dbutils.persistent_db import PersistentDB
from pymysql.constants import CLIENT


class MysqlHelper(object):
    conn = None

    def __init__(self, host, username, password, db=None, charset='utf8', port=3306):
        self.__pool = PooledDB(creator=pymysql,
                               mincached=10,
                               maxcached=0,
                               maxshared=20,
                               maxconnections=200,
                               maxusage=20,
                               blocking=True,
                               user=username,
                               passwd=password,
                               db=db,
                               host=host,
                               port=port,
                               client_flag=CLIENT.MULTI_STATEMENTS
                               )

    def connect(self):
        conn = self.__pool.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # print("连接成功")
        return conn, cursor

    def close(self):
        conn, cursor = self.connect()
        cursor.close()
        conn.close()

    def get_one(self, sql, params=()):
        result = None
        title = []
        try:
            conn, cursor = self.connect()
            cursor.execute(sql, params)
            result = cursor.fetchone()
            des = cursor.description
            # title = [item[0] for item in des]
            self.close()
        except Exception as e:
            print(e)
        return result

    def get_all(self, sql, params=()):
        list_data = ()
        title = []
        try:
            conn, cursor = self.connect()
            cursor.execute(sql, params)
            list_data = cursor.fetchall()
            des = cursor.description
            # title = [item[0] for item in des]
            self.close()
        except Exception as e:
            print(e)
        return list_data

    def insert(self, sql, params=()):
        return self.__edit(sql, params)

    def inrow(self, sql, params=()):
        count = 0
        try:
            conn, cursor = self.connect()
            count = cursor.execute(sql, params)
            conn.commit()
            self.close()
            return count
        except Exception as e:
            print(e)
            return False

    def update(self, sql, params=()):
        return self.__edit(sql, params)

    def delete(self, sql, params=()):
        return self.__edit(sql, params)

    def __edit(self, sql, params):
        count = 0
        try:
            conn, cursor = self.connect()
            count = cursor.execute(sql, params)
            conn.commit()
            self.close()
            return True
        except Exception as e:
            print(e)
            return False


from config import host, username, password, port, db
mydb = MysqlHelper(host=host, db=db, username=username, password=password, port=port)
# from sqlalchemy import create_engine
#
# conn = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(username, password, host, port, db))
