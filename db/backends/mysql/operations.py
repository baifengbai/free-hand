from .base import BaseDatabase
from static.default_variable_map import TRUNCATE_TB_SQL

class OperatorMysql(BaseDatabase):
    """
    数据库操作
    """
    def getAllDataFromDB(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print('getAllDataFromDB(sql)方法 出错： ', sql)
            return -1
        data = self.cursor.fetchall()
        # 将数据转换成列表
        result = []
        for item in data:
            result.append(
                [
                    item[i] for i in range(len(item))
                ]
            )
        return result


    def getOneDataFromDB(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            # 查找不到的话返回None
            return data
        except Exception as e:
            # 报错才返回-1
            print(e, 'sql: ', sql)
            return -1

    def insertData2DB(self, sql):
        try:
            self.cursor.execute(sql)
            return '数据插入成功'
        except Exception as e:
            print(e, 'sql: ', sql)
            return -1

    def truncate_table(self, table_name):
        if (type(table_name) == str):
            # 传入的等待清空的是表名字符串
            self.cursor.execute(TRUNCATE_TB_SQL.format(table_name))
        else:
            # 传入的等待清空的是表名列表
            for table in table_name:
                self.cursor.execute(TRUNCATE_TB_SQL.format(table))

