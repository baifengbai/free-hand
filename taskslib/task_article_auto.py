from utils import globalTools
from db.backends.mysql.operations import OperatorMysql
from spider__ import selenium_toutiao
from customFunction__.Poster import poster_article

def run(setting):
    """
    文章内容爬取需求：
        1 源： 今日头条财经频道 UC浏览器财经频道
        2 清洗： 去除 除p标签和img标签之外的其它标签 去除所有样式属性 img标签保留src属性
        3 字数： 大于500（若是文章内容为图片的话就不要了）
    """
    # setting = {
    #     'databaseName' : 'articledatabase',
    #     'databaseUser' : 'root',
    #     'databasePasswd' : 'root',
    #     "tableName": ['tb_article_toutiao_content'],
    #     'task_type': 'articles',
    #     'website': 'toutiao'
    # }
    # setting['sql'] = "select id,comment from ``.``;"
    if(setting['crawler_method']=='selenium'):
        if(setting['website']=='toutiao'):
            selenium_toutiao.run()
    elif(setting['crawler_method']=='scrapy'):
        # 1 获取对应数据
        dbOperator = dbOp.Contraler_Database(databaseName=setting['databaseName'], user=setting['databaseUser'],passwd=setting['databasePasswd'])
        dataList = dbOperator.getAllDataFromDB(setting['sql'])
        # 2 上传列表
        posterInstance = poster_article.Poster_Article(interface='http://121.40.187.51:8088/api/article_get')
        posterInstance.post_auto(dataList, task_type='article')
    globalTools.finishTask()


