'''
    针对basement的测试
'''
from basement__ import ContralerDatabase, Timer
import os



class Test_ContralerDatabase:
    def __init__(self, databaseName, user, passwd):
        self.contraler_db = ContralerDatabase.Contraler_Database(databaseName, user, passwd)

    def test_openDB(self):
        return self.contraler_db.openDB()

    def test_getAllDataFromDB(self, sql):
        return self.contraler_db.getAllDataFromDB(sql)

    def test_getOneDataFromDB(self, sql):
        return self.contraler_db.getOneDataFromDB(sql)

    def test_insertData2DB(self, sql):
        return self.contraler_db.insertData2DB(sql)

    def test_closeDb(self):
        return self.contraler_db.closeDb()

    def run(self):
        '''
            开始测试
        '''
        print("开始")
        print('1.1 ', self.test_openDB())
        sql_0 = 'select * from tb_comment_gelonghui_content'
        print('1.2 执行sql语句：', sql_0, '\n', self.test_getAllDataFromDB(sql=sql_0))
        sql_1 = 'select * from tb_comment_gelonghui_content where `id`=1'
        print('1.3 执行sql语句：', sql_1, '\n', self.test_getOneDataFromDB(sql=sql_1))
        sql_2 = "INSERT INTO `commentdatabase`.`tb_comment_gelonghui_content` (`comment`, `publishTime`) VALUES ('2', '2');"
        print('1.4 执行sql语句：', sql_2, '\n', self.test_insertData2DB(sql=sql_2))
        print('1.5', self.test_closeDb())
        print("结束")

class Test_Timer_Base_Timer_0:
    def __init__(self):
        self.timerConfig = {
            "beginTime" : '09:06:00', # 注意表示 一位数字的要0开头
            "endTime" : '23:00:00',
            "taskExcuteDelta" : 3600,  # 任务间隔1h
            "timeExcuteDelta" : 86400,   # 定时器间隔 每个一天运行一次
        }
        self.base_timer_0 = Timer.Base_Timer_0(timerConfig=self.timerConfig)

    def test_timerTaskRun(self):
        self.base_timer_0.timerTaskRun()

class Test_TaskTimer_Spider:
    timerConfig = {
        "beginTime": '08:30:00',  # 注意表示 一位数字的要0开头
        "endTime": '23:00:00',
        "taskExcuteDelta": 3600,  # 任务间隔1h
        "timeExcuteDelta": 43200,  # 定时器间隔 每个一天运行一次
        "tasktype": 'selenium',
        "origin": 'kuaishou'
    }
    tasktimer_spider = Timer.TaskTimer_Spider(timerConfig=timerConfig)

    def test_timerTaskRun(self):
        self.tasktimer_spider.timerTaskRun()


class Test_TaskTimer_Spider2:
    timerConfig = {
        "beginTime": '08:30:00',  # 注意表示 一位数字的要0开头
        "endTime": '23:00:00',
        "taskExcuteDelta": 3600,  # 任务间隔1h
        "timeExcuteDelta": 43200,  # 定时器间隔 每个一天运行一次
        "tasktype": 'scrapy'
    }
    articles_configs = {
        'gelonghui': {
            "spiderPath": "C:\\Users\\Administrator\\Desktop\\Projects\\Crawl_Dealwith_Post_Auto\\commentGelonghui_Crawl_Dealwith_Post_Auto\\commentGelonghui_Crawl_Dealwith_Post_Auto",
            "spiderName": "gelonghuiSpider",
            "command": "Scrapy crawl gelonghuiSpider"
        },
        'guba': {
            "spiderPath": "C:\\Users\\Administrator\\Desktop\\Projects\\Crawl_Dealwith_Post_Auto\\commentGuba_Crawl_Dealwith_Post_Auto\\commentGuba_Crawl_Dealwith_Post_Auto",
            "spiderName": "gubaSpider",
            "command": "Scrapy crawl gubaSpider"
        },
        'stockstar': {
            "spiderPath": "C:\\Users\\Administrator\\Desktop\\Projects\\Crawl_Dealwith_Post_Auto\\commentStockstar\\commentStockstar",
            "spiderName": "gubaSpider",
            "command": "Scrapy crawl stockstarSpider"
        },
        'xueqiu': {
            "spiderPath": "C:\\Users\\Administrator\\Desktop\\Projects\\Crawl_Dealwith_Post_Auto\\commentXueqiu_Crawl_Dealwith_Post_Auto\\commentXueqiu_Crawl_Dealwith_Post_Auto",
            "spiderName": "xueqiuSpider",
            "command": "Scrapy crawl xueqiuSpider"
        }
    }
    tasktimer_spider = Timer.TaskTimer_Spider_2(timerConfig=timerConfig, env_configs_dict=articles_configs)

    def test_timerTaskRun(self):
        self.tasktimer_spider.timerTaskRun()

class Test_TaskTimer_AutoDealwithPost:
    # 获取当前目录所在绝对路径
    proj_absPath = os.path.abspath(os.path.dirname(__file__))
    oriDomain = 'huxiu'
    timerConfig = {
        "beginTime": '08:32:00',  # 注意表示 一位数字的要0开头
        "endTime": '23:00:00',
        "taskExcuteDelta": 3600,  # 任务间隔1h
        "timeExcuteDelta": 43200,  # 定时器间隔 每个一天运行一次
        "whichKind": 'articleComment',
        'keywordList' : ['个股', '股市', 'A股', '港股', '新股', '炒股', '散户', '短线', '操盘', '波段', '股票'],
        'databaseUser' : 'root',
        'databasePasswd' : 'root',
        "databaseName": 'commentdatabase',  # 对应的数据库名
        "tableName": ['tb_comment_taoguba1_content'],  # 待处理的表名——存放图片url信息的表
        "tableName2Clear": ['tb_comment_taoguba1_content'],
        "sql": 'SELECT id, comment FROM `commentdatabase`.`tb_comment_taoguba1_content`;'
    }
    tasktimer_autodealwithpost = Timer.TaskTimer_AutoDealwithPost(timerConfig=timerConfig)

    def test_timerTaskRun(self):
        self.tasktimer_autodealwithpost.timerTaskRun()



if(__name__=='__main__'):
    print("---------------测试basement__的功能-------------")
    # print("1 ContralerDatabase")
    # test_cdb = Test_ContralerDatabase('commentdatabase', 'root', 'root')
    # test_cdb.run()
    # print("2 Timer_Base_Timer_0")
    # test_tbt = Test_Timer_Base_Timer_0()
    # test_tbt.test_timerTaskRun()
    # print("3 TaskTimer_Spider")
    # test_tbs = Test_TaskTimer_Spider()
    # test_tbs.test_timerTaskRun()
    # print("4 TaskTimer_AutoDealwithPost")
    # test_adp = Test_TaskTimer_AutoDealwithPost()
    # test_adp.test_timerTaskRun()
    print("3 TaskTimer_Spider_2")
    test_tbs = Test_TaskTimer_Spider2()
    test_tbs.test_timerTaskRun()

