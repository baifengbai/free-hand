from core.manager.base import Manager
import time

"""文章任务管理器"""

class Article_Manager(Manager):
    def __init__(self):
        pass

    def run_manager(self, *tasks):
        self.article_crawler_queue = self.init_queue(task_type='article')
        # 入队
        self.push_task(self.article_crawler_queue, tasks)
        # 执行
        while (self.article_crawler_queue.qsize() != 0):
            """间隔60s执行任务"""
            self.article_crawler_queue.get()()
            time.sleep(10)
            print()
        print('文章爬取任务执行完毕')