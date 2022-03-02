from core.manager.base import Manager
import time

"""评论任务管理器"""

class Comment_Manager(Manager):
    def __init__(self):
        self.comment_crawler_queue = self.init_queue(task_type='comment')

    def run_manager(self, *tasks):
        # 入队
        self.push_task(self.comment_crawler_queue, tasks)
        # 执行
        while (self.comment_crawler_queue.qsize() != 0):
            """间隔60s执行任务"""
            self.comment_crawler_queue.get()()
            time.sleep(60)
        print('评论爬取任务执行完毕')