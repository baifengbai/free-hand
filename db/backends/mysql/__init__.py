"""
说明： 连接数据库和执行操作只需要调用如下
    from db.backends.mysql.operations import OperatorMysql
    db_instance = OperatorMysql(settings_dict)
    其中 settings_dict 是配置文件中的 DATABASES
"""