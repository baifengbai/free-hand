"""初始化默认的数据库"""
from contrib.db.db_connect import DB_Singleton

if __name__ == '__main__':
    db = DB_Singleton()
