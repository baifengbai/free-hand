from utils import globalTools
from spider.selenium_douyin import Crawler_Douyin

def run(setting):
    """
    视频内容爬取需求：

    """
    # setting = {
    #     'databaseName' : 'articledatabase',
    #     'databaseUser' : 'root',
    #     'databasePasswd' : 'root',
    #     "tableName": ['tb_article_toutiao_content'],
    #     'whichKind': 'articles',
    #     'website': 'douyin'
    # }
    # setting['sql'] = "select id,comment from ``.``;"
    if(setting['tasktype']=='selenium'):
        if(setting['website']=='douyin'):
            pass
    elif(setting['tasktype']=='scrapy'):
        # # 1 获取对应数据
        # dbOperator = dbOp.Contraler_Database(databaseName=setting['databaseName'], user=setting['databaseUser'],passwd=setting['databasePasswd'])
        # dataList = dbOperator.getAllDataFromDB(setting['sql'])
        # # 2 上传列表
        # posterInstance = poster_article.Poster_Article(interface='http://121.40.187.51:8088/api/article_get')
        # posterInstance.post_auto(dataList, whichKind='article')
        print('tasktype设置出错，暂时无scrapy的视频爬取任务')
    globalTools.finishTask()


