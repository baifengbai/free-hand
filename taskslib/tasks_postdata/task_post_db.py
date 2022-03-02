from core.base.tasksmixin.tasks_postdata.base import Base_Task_Post
from db.backends.mysql.operations import OperatorMysql
from core.base.poster.base import BasePoster


"""上传指定数据库 指定表里的数据到指定接口"""
class Task_Post_DB(Base_Task_Post):
    def run(self, task_type, db_user, db_pwd, database_name, table_name):
        """
            主要针对 段落、文章、评论 且保存在数据路里的这类数据（字符串类型）的处理和上传， 图片、视频等类型数据不适合本类方法
            注意：
                本类方法不做任何过滤操作和其它数据清洗操作，特殊操作根据不同task_type选择不同task 如 task_post_articles.py
        """
        # 1 获取 对应task_type所需参数
        special_config = self.get_by_tasktype_config(task_type=task_type, table_name=table_name)
        # 2 获取 从数据库获取数据列表
        params = {
            'USER': db_user,
            'DBNAME': database_name,
            'PASSWORD': db_pwd,
            'HOST': '',
            'PORT': '',
        }
        dbOperator = OperatorMysql(params)
        del dbOperator
        dataList = dbOperator.getAllDataFromDB(special_config['sql_getdata'])
        # 3 去重
        dataList = self.del_repeatdata(task_type=task_type, lis=dataList)
        # 4 上传 处理后的列表
        posterInstance = BasePoster()
        posterInstance.interface = special_config['interface']
        posterInstance.post_auto(dataList, task_type=task_type)
        # 5 更新 将上传过的数据放到postedurldatabase中

