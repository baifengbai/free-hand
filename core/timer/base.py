"""
    定时器相关的基类和方法
"""
import datetime, os, time
import subprocess, threading
import ctypes, inspect
from db.backends.mysql.operations import OperatorMysql as dbOp
from contrib.manager.article_manager import Article_Manager
from taskslib.tasks_scrapy.task_articles import Task_Article_Scrapy
from taskslib import sk_comment_auto, task_video_auto, task_selenium_auto, task_contentImgs_auto, task_thumbnailImgs_auto,task_keyParagraph_auto, task_relativeParagraph_auto, s
from core.base.utils.u_process import Process_Handler

# 定时任务器基类(设计多个基类)
class Base_Timer_0:
    """每隔指定间隔时间，在指定时间段内，指定时间间隔执行一次任务"""
    def __init__(self, timerConfig):
        self.timerConfig = timerConfig
        self.beginTime = self.timerConfig['beginTime']  # 定时任务每天的启动时间 例子早上8点 08:00:00
        self.endTime = self.timerConfig['endTime']  # 定时任务执行在几点之前 例子早上9点 09:00:00
        self.taskExcuteDelta = self.timerConfig['taskExcuteDelta']  # 定时任务间隔几秒执行一次
        self.timeExcuteDelta = self.timerConfig['timeExcuteDelta']

    def timer_entrance(self):
        '''
        定时器入口，设置每隔指定时间间隔，执行一次定时器
        :param
        :return
        '''
        self.timer_interval() # 入口执行一次函数，从此刻开始计时
        t = threading.Timer(self.timeExcuteDelta, self.timer_entrance)
        t.start()


    def timer_interval(self):
        '''
        定时器间隔函数 8点-9点，隔3600秒执行一次任务task
        :return:
        '''
        self.task()
        now_time = datetime.datetime.now()
        today_9 = datetime.datetime.strptime(
            str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month) + '-' + str(
                datetime.datetime.now().day) + ' ' + str(self.endTime), '%Y-%m-%d %H:%M:%S')
        # 因为定时任务会延后10秒钟执行，所以设置终止条件时，需要提前10秒钟
        if (now_time <= today_9 - datetime.timedelta(seconds=10)):
            print("当前时间 " + str(now_time) + " ,该时间在任务执行时段内，继续间隔 " + str(self.taskExcuteDelta) + " 执行任务")
            t = threading.Timer(self.taskExcuteDelta, self.timer_interval)
            t.start()
        else:
            print("当前时间 " + str(now_time) + " ,该时间不在任务执行时段内，等待 " + str(self.timeExcuteDelta) + " 后再重新开启执行任务定时器")

    def task(self):
        '''
        定时任务内容，通过继承重写
        :return:
        '''
        print(' ---------- task任务开始执行 ---------- ')
        print("本定时器未设置定时任务内容")
        time.sleep(1)
        print(' ---------- task任务执行完毕 ---------- ')

    def timerTaskRun(self):
        # 获取当前时间
        now_time = datetime.datetime.now()
        # 获取当前年月日
        now_year = now_time.year
        now_month = now_time.month
        now_day = now_time.day

        # 今天早上8点时间表示
        # today_8 = datetime.datetime.strptime(str(now_year)+'-'+str(now_month)+'-'+str(now_day)+' '+'08:00:00','%Y-%m-%d %H:%M:%S')
        today_8 = datetime.datetime.strptime(str(now_year) + '-' + str(now_month) + '-' + str(now_day) + ' ' + str(self.beginTime), '%Y-%m-%d %H:%M:%S')
        # 明天早上8点时间表示
        tomorrow_8 = datetime.datetime.strptime(str(now_year) + '-' + str(now_month) + '-' + str(now_day) + ' ' + str(self.beginTime), '%Y-%m-%d %H:%M:%S')

        # 判断当前时间是否过了今天凌晨8点,如果没过，则今天早上8点开始执行，过了则从明天早上8点开始执行，计算程序等待执行的时间
        if (now_time <= today_8):
            wait_time = (today_8 - now_time).total_seconds()
        else:
            wait_time = (tomorrow_8 - now_time).total_seconds()

        # 等待wait_time秒后（今天早上8点或明天早上8点），开启线程去执行func函数
        self.thread = threading.Timer(wait_time, self.timer_entrance)  # 当前线程
        self.thread.start()

    @classmethod
    def permanent_runner(cls, process_recordintb_id, origin, whatkind):
        """
        让定时器永久运行
        注意：要使用此方法需要让对应执行的爬虫项目文件在启动后 在对应数据表里对应记录更新pid值
        :param process_recordintb_id 数据库表里面对应的id编号，以获取对应的pid
        :param origin 站点名
        :param whatkind 爬虫还是上传器
        """
        while(True):
            cdb = Contraler_Database('resourcedatabase')
            command = cdb.getOneDataFromDB('SELECT `execute_command` FROM `tb_process_info` WHERE `id` = {};'.format(str(process_recordintb_id)))
            pid = cdb.getOneDataFromDB('SELECT `pid` FROM `tb_process_info` WHERE `id` = 2;')
            if (not Process_Handler.check_if_alive(pid=pid[0])):
                print('{}{}停止了，重启{}{}'.format(origin, whatkind,origin, whatkind))
                Process_Handler.start_process(command[0])
            else:
                print('{}运行良好'.format(origin, whatkind))
            time.sleep(5)


# 结束线程的类没有用到
class StopThread():
    '''结束线程的类'''
    def _async_raise(self,tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if(not inspect.isclass(exctype)):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if(res == 0):
            raise ValueError("invalid thread id")
        elif(res != 1):
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    # 任务自动执行结束 结束本线程实例，在调用本方法之前得先调用 timedTaskRun()
    def stopCurThread(self, thread):
        self._async_raise(thread.ident, SystemExit)


'''
    下面是定时器特定任务定制，继承自基类的定时器
'''
class TaskTimer_Spider(Base_Timer_0):
    """定时任务 ———— 爬取数据的的类"""
    def task(self):
        """方案1 单任务执行 每个新任务都创建新线程"""
        self.setting = self.timerConfig
        if(self.setting['crawler_method']=='scrapy'):
            # 通过os改变工作路径,注意路径是绝对路径，而且还要是\\  只要环境是同一个 这样可以执行对应的爬虫项目
            os.chdir(self.setting['spiderPath'])
            subprocess.Popen(self.setting['command'])
        elif(self.setting['crawler_method']=='selenium'):
            if(self.setting['origin'] == 'douyin'):
                task_selenium_auto.Sele_Spider_Runner.run_douyin(proj_absPath=self.setting['proj_absPath'], crawlUrl_list=self.setting['crawlUrl_list'], origin='douyin')
            elif(self.setting['origin'] == 'kuaishou'):
                task_selenium_auto.Sele_Spider_Runner.run_kuaishou()
            elif(self.setting['origin'] == 'sougou'):
                task_selenium_auto.Sele_Spider_Runner.run_sougou()
            elif(self.setting['origin'] == 'douyin_guxiaocha'):
                task_selenium_auto.Sele_Spider_Runner.run_douyin_guxiaocah(proj_absPath=self.setting['proj_absPath'], crawlUrl_list=self.setting['crawlUrl_list'], origin='douyin')
        else:
            print('crawler_method参数出错')

class TaskTimer_Spider_2(Base_Timer_0):
    def __init__(self, timerConfig, env_configs_dict):
        self.timerConfig = timerConfig
        self.env_configs_dict = env_configs_dict
        self.beginTime = self.timerConfig['beginTime']  # 定时任务每天的启动时间 例子早上8点 08:00:00
        self.endTime = self.timerConfig['endTime']  # 定时任务执行在几点之前 例子早上9点 09:00:00
        self.taskExcuteDelta = self.timerConfig['taskExcuteDelta']  # 定时任务间隔几秒执行一次
        self.timeExcuteDelta = self.timerConfig['timeExcuteDelta']

    def task(self):
        """方案2 队列任务执行"""
        self.setting = self.timerConfig
        if(self.setting['crawler_method']=='scrapy'):
            manager_articles = Article_Manager()
            task_queue = manager_articles.init_queue('articles')
            for item in self.env_configs_dict.values():
                article_task = Task_Article_Scrapy()
                article_task.env_config = item
                manager_articles.push_task(task_queue, article_task.run)
            # 文章对象需要创建多个 不同站点 不同对象
            while (task_queue.qsize() != 0):
                """间隔60s执行任务"""
                res = task_queue.get()()
                # time.sleep(60) # 由于每个任务完成的时间不一样，因此等待1min是有必要的, 现在不用这种方法等待shell命令完成了
            print('任务执行完毕')
        else:
            print('crawler_method参数出错')

class TaskTimer_AutoDealwithPost(Base_Timer_0):
    """定时任务 ———— 处理数据及上传 段落数据 到接口的类（完成）"""
    def task(self):
        self.setting = self.timerConfig
        if(self.setting["task_type"] == 'keyParagraph'):
            task_keyParagraph_auto.run(setting=self.setting)
        elif(self.setting["task_type"] == 'relativeParagraph'):
            task_relativeParagraph_auto.run(setting=self.setting)
        elif(self.setting["task_type"] == 'contentImgs'):
            task_contentImgs_auto.run(proj_absPath=self.setting["proj_absPath"], origin=self.setting["origin"], database=self.setting['databaseName'], tableNameList=self.setting['tableName'], maskFilt=self.setting['maskFilt'])
        elif(self.setting["task_type"] == 'thumbnailImgs'):
            task_thumbnailImgs_auto.run(proj_absPath=self.setting["proj_absPath"], origin=self.setting["origin"], database=self.setting['databaseName'], tableNameList=self.setting['tableName'])
        elif(self.setting["task_type"]=='articleComment'):
            task_comment_auto.run(setting=self.setting)
        elif(self.setting['task_type']=='articles'):
            s.run(setting=self.setting)
        else:
            print('参数 task_type 出错')
        print("上传数据完成，接下来清空数据库")
        # 上传完直接清空数据库，不用再用定时器
        clearDB = TimedTask4AutoClearDB(timerConfig=self.setting)
        clearDB.task()


# 3. 定时任务 ———— 数据库对应上传过的数据清除的类
class TimedTask4AutoClearDB(Base_Timer_0):
    """本类状态： 无使用 无维护"""
    def task(self):
        '''
            setting = {
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
                dbOperator = dbOp.Contraler_Database(self.setting["databaseName"])
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

                    dbOperator = dbOp.Contraler_Database(self.setting["databaseName"])
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
                dbOperator = dbOp.Contraler_Database(self.setting["databaseName"])
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
                    dbOperator = dbOp.Contraler_Database(self.setting["databaseName"])
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
                dbOperator = dbOp.Contraler_Database(self.setting["databaseName"])
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
                    dbOperator = dbOp.Contraler_Database(self.setting["databaseName"])
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
                dbOperator = dbOp.Contraler_Database(self.setting["databaseName"])
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
                    dbOperator = dbOp.Contraler_Database(self.setting["databaseName"])
                    dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()