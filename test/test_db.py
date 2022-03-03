from db.backends.mysql.operations import OperatorMysql
from conf import setting

"""
    数据库操作测试成功
"""
if __name__ == '__main__':
    print(setting.DATABASES)
    db_instance = OperatorMysql(setting.DATABASES)
    lis = db_instance.getAllDataFromDB('select * from `data_usable_database`.`filter_video_keyword`;')
    print(lis)