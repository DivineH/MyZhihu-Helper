import pymysql
from builtins import int

class SqlManager(object):
    conn = None
    cur = None

    # 连接数据库
    @staticmethod
    def connDB(user, passwd, database):
        SqlManager.conn = pymysql.connect(host = 'localhost', port = 3306, user = user, password = passwd, db = database,
                               charset = 'utf8')
        SqlManager.cur = SqlManager.conn.cursor()
        return

    # 执行sql语句
    @staticmethod
    def exeSql(sql):
        print(sql)
        sta = SqlManager.cur.execute(sql)
        SqlManager.conn.commit()
        return (sta)

    # 更新语句，可执行Update，Insert语句
    @staticmethod
    def exeUpdate(sql):
        sta = SqlManager.cur.execute(sql)
        SqlManager.conn.commit()
        return (sta)

    # 删除语句，可批量删除
    @staticmethod
    def exeDelete(IDs):
        for eachID in IDs.split(' '):
            sta = SqlManager.cur.execute('delete from students where Id=%d' % int(eachID))
        SqlManager.conn.commit()
        return (sta)

    # 查询语句
    @staticmethod
    def exeQuery(sql):
        SqlManager.cur.execute(sql)
        return SqlManager.cur

    # 关闭所有连接
    @staticmethod
    def connClose():
        SqlManager.cur.close()
        SqlManager.conn.close()
