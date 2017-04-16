import pymysql
from builtins import int

class SqlManager(object):
    conn = None
    cur = None
    flag = True

    # 连接数据库
    @staticmethod
    def connDB(user, passwd, database):
        try:
            SqlManager.conn = pymysql.connect(host = 'localhost', port = 3306, user = user, password = passwd, db = database,
                                              charset = 'utf8')
            SqlManager.cur = SqlManager.conn.cursor()
        except:
            SqlManager.flag = False
            print('数据库连接错误!')
        return

    # 执行sql语句
    @staticmethod
    def exeSql(sql):
        if SqlManager.flag:
            sta = SqlManager.cur.execute(sql)
            SqlManager.conn.commit()
        else:
            sta = None
        return (sta)

    # 更新语句，可执行Update，Insert语句
    @staticmethod
    def exeUpdate(sql):
        if SqlManager.flag:
            sta = SqlManager.cur.execute(sql)
            SqlManager.conn.commit()
        else:
            sta = None
        return (sta)

    # 删除语句，可批量删除
    @staticmethod
    def exeDelete(IDs):
        if SqlManager.flag:
            for eachID in IDs.split(' '):
                sta = SqlManager.cur.execute('delete from students where Id=%d' % int(eachID))
            SqlManager.conn.commit()
        else:
            sta = None
        return (sta)

    # 查询语句
    @staticmethod
    def exeQuery(sql):
        if SqlManager.flag:
            SqlManager.cur.execute(sql)
            return SqlManager.cur
        else:
            return None

    # 关闭所有连接
    @staticmethod
    def connClose():
        if SqlManager.flag:
            SqlManager.cur.close()
            SqlManager.conn.close()