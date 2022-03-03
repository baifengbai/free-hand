"""
    待继承的一些主干基类
        中间件基类
        selenium启动基类
        定时器基类
"""
'''
    底层功能设计
'''
__all__ = [

]
# - 定时任务器Timer
'''
    - 爬虫定时器参数配置
        setting4Spider_bilibili = {
            "spiderPath": "E:\\Projects\\Crawl_Dealwith_Post_Auto\\video_bilibili_Crawl_Dealwith_Post_Auto\\video_bilibili_Crawl_Dealwith_Post_Auto",
            "spiderName": "bilibiliSpider",
            "command": "Scrapy crawl bilibiliSpider",
            "beginTime" : '08:00:00', # 注意表示 一位数字的要0开头
            "endTime" : '17:50:00',
            "taskExcuteDelta" : 3600,  # 任务间隔1h
            "timeExcuteDelta" : 43200,   # 定时器间隔 每个一天运行一次
        }

    - 数据处理及上传定时器参数配置
        setting4AutoDP_bilibili = {
            "beginTime" : '08:00:00', # 注意表示 一位数字的要0开头
            "endTime" : '17:50:00',
            "taskExcuteDelta" : 3600,  # 任务间隔1h
            "timeExcuteDelta" : 43200,   # 定时器间隔 每个一周运行一次

            "whichKind": 'video',
            'crawlMethod': 'Scrapy',
            'databaseName': 'videodatabase',
            'databaseUser': 'root',
            'databasePasswd': 'root',
            'tableName': 'tb_bilibili_videoinfo',
            'tableName2Clear': 'tb_bilibili_videoinfo',
            'videoDirPath': 'E:\\test\\',
            'coverSavedPath': 'E:\\test\\cur_Cover.jpg'
        }

    - 数据库对应上传过的数据清除的类(没用上)
        setting = {
            "beginTime": '08:00:00',  # 注意表示 一位数字的要0开头
            "endTime": '09:00:00',
            "excuteDelta": 3600,  # 间隔1h 也就是说一天执行一次
            "whichKind": 'keyParagraph',
            "databaseName" : ['stocksnamecode'],   # 对应的数据库名列表
            "tableName" : ['tb_namecode']    # 待清空的表名
        }

'''