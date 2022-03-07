from taskslib import task_comment_auto, task_contentImgs_auto, task_thumbnailImgs_auto,task_keyParagraph_auto, task_relativeParagraph_auto, task_article_auto
from core.timer.base import Base_Timer_0
from timer_handle_database import TimedTask4AutoClearDB
from db.backends.mysql.operations import OperatorMysql
"""处理数据相关的定时器"""
class TaskTimer_AutoDealwithPost(Base_Timer_0):
    """定时任务 ———— 处理数据及上传 段落数据 到接口的类（完成）"""
    def task(self):
        if(self.timerConfig["task_type"] == 'keyParagraph'):
            task_keyParagraph_auto.run(setting=self.timerConfig)
        elif(self.timerConfig["task_type"] == 'relativeParagraph'):
            task_relativeParagraph_auto.run(setting=self.timerConfig)
        elif(self.timerConfig["task_type"] == 'contentImgs'):
            task_contentImgs_auto.run(proj_absPath=self.timerConfig["proj_absPath"], origin=self.timerConfig["origin"], database=self.timerConfig['databaseName'], tableNameList=self.timerConfig['tableName'], maskFilt=self.timerConfig['maskFilt'])
        elif(self.timerConfig["task_type"] == 'thumbnailImgs'):
            task_thumbnailImgs_auto.run(proj_absPath=self.timerConfig["proj_absPath"], origin=self.timerConfig["origin"], database=self.timerConfig['databaseName'], tableNameList=self.timerConfig['tableName'])
        elif(self.timerConfig["task_type"]=='articleComment'):
            task_comment_auto.run(setting=self.timerConfig)
        elif(self.timerConfig['task_type']=='articles'):
            task_article_auto.run(setting=self.timerConfig)
        else:
            print('参数 task_type 出错')
        print("上传数据完成，接下来清空数据库")
        # 上传完直接清空数据库，不用再用定时器
        db_clearer = OperatorMysql()
        if(self.timerConfig['databaseName'] != db_clearer.cur_conn_params['database']):
            dic = db_clearer.cur_conn_params
            dic['database'] = self.timerConfig['databaseName']
            db_clearer.cur_conn_params = dic
        db_clearer.truncate_table(self.timerConfig['tableName'])
        db_clearer.closeDb()
        # clearDB = TimedTask4AutoClearDB(timerConfig=self.timerConfig)
        # clearDB.task()