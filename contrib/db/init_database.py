"""初始化默认的数据库 本模块只在创建项目的时候调用一次 用于初始化默认的数据库"""
from db.backends.mysql.init_default_db import Init_DB

if __name__ == '__main__':
    Init_DB().run_default()
