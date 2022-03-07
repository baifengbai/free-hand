from db.backends.mysql.operations import OperatorMysql
from core.timer.base import Base_Timer_0

"""数据库处理相关的定时器"""

# 3. 定时任务 ———— 数据库对应上传过的数据清除的类
class TimedTask4AutoClearDB(Base_Timer_0):
    """本类状态： 无使用 无维护"""
    def task(self):
        '''setting = {
             "beginTime": '08:00:00',  # 注意表示 一位数字的要0开头
            "endTime": '09:00:00',
            "excuteDelta": 3600,  # 间隔1h 也就是说一天执行一次
            "task_type": 'keyParagraph',
            "databaseName" : ['stocksnamecode'],   # 对应的数据库名列表
            "tableName" : ['tb_namecode']    # 待清空的表名
            }
        '''
        self.setting = self.timerConfig
        if(self.setting['task_type'] == 'keyParagraph' or self.setting['task_type'] == 'relativeParagraph' or self.setting['task_type'] == 'articleComment'):
            # 处理的是段落相关的表
            if(type(self.setting['table_wait2bclean'])==str):
                # 传入的等待清空的是表名字符串
                # 2 清空数据库表的sql
                sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                    self.setting["databaseName"],
                    self.setting['table_wait2bclean']
                )
                param = {
                    'USER': 'root',
                    'DBNAME': self.setting["databaseName"],
                    'PASSWORD': 'root',
                    'HOST': '',
                    'PORT': '',
                }
                dbOperator = OperatorMysql(param)
                # 清空表之前先复制的操作已经放在了上传数据完成的后面
                # dbOperator.cursor.execute(sql4copy2tb_posted)
                dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()
            else:
                # 传入的等待清空的是表名列表
                for table in self.setting['table_wait2bclean']:
                    # 2 清空数据库表的sql
                    sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                        self.setting["databaseName"],
                        table
                    )
                    param = {
                        'USER': 'root',
                        'DBNAME': self.setting["databaseName"],
                        'PASSWORD': 'root',
                        'HOST': '',
                        'PORT': '',
                    }
                    dbOperator = OperatorMysql(param)
                    # 清空表之前先复制的操作已经放在了上传数据完成的后面
                    # dbOperator.cursor.execute(sql4copy2tb_posted)
                    dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()

        elif(self.setting['task_type'] == 'thumbnailImgs'):
            if (type(self.setting['table_wait2bclean']) == str):
                # 传入的等待清空的是表名字符串
                # 1 清空数据库表的sql
                sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                    self.setting["databaseName"],
                    self.setting['table_wait2bclean']
                )
                param = {
                    'USER': 'root',
                    'DBNAME': self.setting["databaseName"],
                    'PASSWORD': 'root',
                    'HOST': '',
                    'PORT': '',
                }
                dbOperator = OperatorMysql(param)
                dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()
            else:
                # 传入的等待清空的是表名列表
                # 处理的是缩略图相关的表
                for table in self.setting['table_wait2bclean']:
                    # 2 清空数据库表的sql
                    sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                        self.setting["databaseName"],
                        table
                    )
                    # 清空表之前先复制
                    param = {
                        'USER': 'root',
                        'DBNAME': self.setting["databaseName"],
                        'PASSWORD': 'root',
                        'HOST': '',
                        'PORT': '',
                    }
                    dbOperator = OperatorMysql(param)
                    dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()

        elif (self.setting['task_type'] == 'contentImgs'):

            if (type(self.setting['table_wait2bclean']) == str):
                # 传入的等待清空的是表名字符串
                # 2 清空数据库表的sql
                sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                    self.setting["databaseName"],
                    self.setting['table_wait2bclean']
                )
                # 清空表之前先复制
                param = {
                    'USER': 'root',
                    'DBNAME': self.setting["databaseName"],
                    'PASSWORD': 'root',
                    'HOST': '',
                    'PORT': '',
                }
                dbOperator = OperatorMysql(param)
                dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()
            else:
                # 传入的等待清空的是表名列表
                # 处理的是缩略图相关的表
                for table in self.setting['table_wait2bclean']:
                    # 2 清空数据库表的sql
                    sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                        self.setting["databaseName"],
                        table
                    )
                    # 清空表之前先复制
                    param = {
                        'USER': 'root',
                        'DBNAME': self.setting["databaseName"],
                        'PASSWORD': 'root',
                        'HOST': '',
                        'PORT': '',
                    }
                    dbOperator = OperatorMysql(param)
                    dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()

        elif(self.setting['task_type'] == 'video'):
            if (type(self.setting['table_wait2bclean']) == str):
                # 传入的等待清空的是表名字符串
                # 2 清空数据库表的sql
                sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                    self.setting["databaseName"],
                    self.setting['table_wait2bclean']
                )
                # 清空表之前先复制
                param = {
                    'USER': 'root',
                    'DBNAME': self.setting["databaseName"],
                    'PASSWORD': 'root',
                    'HOST': '',
                    'PORT': '',
                }
                dbOperator = OperatorMysql(param)
                dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()
            else:
                # 传入的等待清空的是表名列表
                # 处理视频相关的表
                for table in self.setting['table_wait2bclean']:
                    # 2 清空数据库表的sql
                    sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                        self.setting["databaseName"],
                        table
                    )
                    # 清空表之前先复制
                    param = {
                        'USER': 'root',
                        'DBNAME': self.setting["databaseName"],
                        'PASSWORD': 'root',
                        'HOST': '',
                        'PORT': '',
                    }
                    dbOperator = OperatorMysql(param)
                    dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()