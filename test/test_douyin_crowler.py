from taskslib.task_selenium_auto import Sele_Spider_Runner
from core.timer.base import TaskTimer_Spider
import os

if(__name__ == '__main__'):
    # 获取当前目录所在绝对路径
    proj_absPath = os.path.abspath(os.path.dirname(__file__))
    oriDomain = 'douyin'
    setting4Spider_douyin = {
        "beginTime" : '08:00:00', # 注意表示 一位数字的要0开头
        "endTime" : '17:50:00',
        "taskExcuteDelta" : 3600,  # 任务间隔1h
        "timeExcuteDelta" : 43200,   # 定时器间隔 每个一天运行一次
        "whichKind": 'video',
        "crawlMethod": 'Selenium',
        "tasktype": 'selenium',
        "proj_absPath": proj_absPath,  # 当前环境路径
        "origin": oriDomain,  # 对应域名
        "crawlUrl_list" : [
            "https://www.douyin.com/search/%E8%82%A1?publish_time=1&sort_type=2&source=normal_search&type=video",
            "https://www.douyin.com/search/%E8%82%A1%E7%A5%A8?publish_time=1&sort_type=2&source=normal_search&type=video",
            "https://www.douyin.com/search/%E6%B6%A8%E8%B7%8C?publish_time=1&sort_type=2&source=normal_search&type=video",
            "https://www.douyin.com/search/%E5%A4%A7%E7%9B%98?publish_time=1&sort_type=2&source=normal_search&type=video",
            "https://www.douyin.com/search/B%E8%82%A1?publish_time=1&sort_type=2&source=normal_search&type=video",
            "https://www.douyin.com/search/%E7%9F%AD%E7%BA%BF?publish_time=1&sort_type=2&source=normal_search&type=video",
            "https://www.douyin.com/search/%E6%8C%87%E6%95%B0?publish_time=1&sort_type=2&source=normal_search&type=video"
        ],
        'databaseName': 'videodatabase',
        'tableName2Clear' : 'tb_douyin_videoinfo'
    }
    douyin_timer = TaskTimer_Spider(
        timerConfig=setting4Spider_douyin
    )
    douyin_timer.timerTaskRun()
    # Sele_Spider_Runner.run_douyin(proj_absPath, crawlUrl_list=setting4Spider_douyin['crawlUrl_list'], oriDomain='douyin')

