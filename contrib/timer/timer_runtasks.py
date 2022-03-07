import os
import subprocess
from contrib.manager.article_manager import Article_Manager
from taskslib.tasks_scrapy.task_articles import Task_Article_Scrapy
from taskslib import task_selenium_auto
from core.timer.base import Base_Timer_0

class TaskTimer_Spider(Base_Timer_0):
    """定时任务 ———— 爬取数据的的类
    特殊配置
    crawler_method 基于哪种框架的爬取 有 scrapy selenium
        - crawler_method为 scrapy：
        · spiderPath 爬虫项目的路径
        · command 采用scrapy爬取的执行命令 如 Scrapy crawl XXXSpider
        - crawler_method为 selenium：
    """
    def task(self):
        """方案1 单任务执行 每个新任务都创建新线程"""
        if(self.timerConfig['crawler_method']=='scrapy'):
            # 通过os改变工作路径,注意路径是绝对路径，而且还要是\\  只要环境是同一个 这样可以执行对应的爬虫项目
            os.chdir(self.timerConfig['spiderPath'])
            subprocess.Popen(self.timerConfig['command'])
        elif(self.timerConfig['crawler_method']=='selenium'):
            if(self.timerConfig['origin'] == 'douyin'):
                task_selenium_auto.Sele_Spider_Runner.run_douyin(proj_absPath=self.timerConfig['proj_absPath'],
                                                                 crawlUrl_list=self.timerConfig['crawlUrl_list'],
                                                                 origin='douyin')
            elif(self.timerConfig['origin'] == 'kuaishou'):
                task_selenium_auto.Sele_Spider_Runner.run_kuaishou()
            elif(self.timerConfig['origin'] == 'sougou'):
                task_selenium_auto.Sele_Spider_Runner.run_sougou()
            elif(self.timerConfig['origin'] == 'douyin_guxiaocha'):
                task_selenium_auto.Sele_Spider_Runner.run_douyin_guxiaocah(proj_absPath=self.timerConfig['proj_absPath'], crawlUrl_list=self.timerConfig['crawlUrl_list'], origin='douyin')
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
        self.timerConfig = self.timerConfig
        if(self.timerConfig['crawler_method']=='scrapy'):
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



