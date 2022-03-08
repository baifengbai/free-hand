"""连接默认数据库 创建单例连接 调用的基类"""
from db.backends.mysql.operations import OperatorMysql
import threading

class DB_Singleton_DEFAULT(OperatorMysql):
    _instance_lock = threading.Lock()
    def __new__(cls, *args, **kwargs):
        if(not hasattr(DB_Singleton_DEFAULT, '_instance')):
            with DB_Singleton_DEFAULT._instance_lock:
                if (not hasattr(DB_Singleton_DEFAULT, '_instance')):
                    DB_Singleton_DEFAULT._instance = object.__new__(cls)
        return DB_Singleton_DEFAULT._instance

