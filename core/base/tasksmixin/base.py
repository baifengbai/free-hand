import os

class Base_Task:
    def __init__(self):
        self.__env_config = {}

    @classmethod
    def change_env_4scrapy(cls, spiderPath):
        """
        :param spiderPath 环境配置 "C:\\Users\\Administrator\\Desktop\\Projects\\Crawl_Dealwith_Post_Auto\\articlesAigupiao\\articlesAigupiao"
        """
        # 通过os改变工作路径,注意路径是绝对路径，而且还要是\\  只要环境是同一个 这样可以执行对应的爬虫项目
        os.chdir(spiderPath)
        return '改变环境路径 {}'.format(spiderPath)

    @property
    def env_config(self):
        return self.__env_config

    @env_config.setter
    def env_config(self, env_config):
        self.__env_config = env_config
        print('修改 env_config 为 ：', env_config)
        return '修改 env_config 为 ：', env_config

