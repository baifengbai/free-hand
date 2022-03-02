from queue import Queue
"""
    任务调度管理器 基类
        队列调度任务执行

"""

class Manager:
    """
        任务管理器
        主要功能有 压入任务 执行任务 弹出任务
    """
    @classmethod
    def init_queue(cls, task_type:str):
        """
        :param task_type 任务类型
            'article_crawl' 文章爬取
            'paramgraph_crawl' 段落爬取
            'imgs_crawl' 图片爬取
        """
        print('初始化 {} 队列任务管理器'.format(task_type))
        task_queue = Queue()
        return task_queue

    @classmethod
    def push_task(cls, task_queue:Queue, *tasks: tuple):
        '''
        将任务压入队列
        :param task 任务元组 逐个压入队列
        '''
        for task in tasks:
            task_queue.put(task)
        return '任务进入队列完成'



    def run_manager(self, task_queue:Queue, *tasks):
        """
            执行指定任务管理器里的任务
        """
        # task_queue.push_task(task_queue, tasks)
        pass