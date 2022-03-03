from basement__ import Timer

class Test_TaskTimer_AutoDealwithPost:
    timerConfig = {
        "beginTime": '00:01:00',  # 注意表示 一位数字的要0开头
        "endTime": '23:59:00',
        "taskExcuteDelta": 600,  # 任务间隔
        "timeExcuteDelta": 43200,  # 定时器间隔 每个一天运行一次
        "whichKind": 'articles',
        'databaseUser' : 'root',
        'databasePasswd' : 'root',
        "databaseName": 'articledatabase',  # 对应的数据库名
        "tableName": ['tb_article_toutiao_content'],  # 待处理的表名——存放图片url信息的表
    }
    tasktimer_autodealwithpost = Timer.TaskTimer_AutoDealwithPost(timerConfig=timerConfig)

    def test_timerTaskRun(self):
        self.tasktimer_autodealwithpost.timerTaskRun()


if(__name__=='__main__'):
    print("---------------测试头条文章自动化爬取的功能-------------")
    print("4 TaskTimer_AutoDealwithPost")
    test_adp = Test_TaskTimer_AutoDealwithPost()
    test_adp.test_timerTaskRun()


