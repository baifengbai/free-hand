import time
from ..base import Base_Task
import subprocess

class Task_Scrapy(Base_Task):
    """
        基于scrapy的 scrapy项目 爬取任务 对于无许特殊处理的scrapy爬虫直接用该方法即可
        使用方法：将run方法压入队列即可
    """
    def run(self):
        """
        :param env_config 环境配置
            格式：
                {
                    "spiderPath": "C:\\Users\\Administrator\\Desktop\\Projects\\Crawl_Dealwith_Post_Auto\\articlesAigupiao\\articlesAigupiao",
                    "spiderName": "aigupiaoSpider",
                    "command": "Scrapy crawl aigupiaoSpider"
                }
        注意： self.env_config 这个变量不能公用，因此只能通过创建多个对象来保存这个值了
        """
        self.change_env_4scrapy(self.env_config['spiderPath'])
        p = subprocess.Popen(self.env_config['command'])
        while(1):
            # 等待命令执行完毕
            if(subprocess.Popen.poll(p)==None):
                time.sleep(2)
                print('shell执行尚未完成')
            elif(subprocess.Popen.poll(p)==0):
                return True
