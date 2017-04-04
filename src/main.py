from src.tools.sql_manager import SqlManager
from src.login import Login

class ZhihuHelper(object):
    def __init__(self):
        #   初始化数据库链接
        SqlManager.connDB('root', 'hanchao', 'python_zhihu_db')
        return

    def start(self):
        login = Login()
        login.start()
