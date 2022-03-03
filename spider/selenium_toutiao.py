from spider.selenium_jinritoutiao import Crawler_toutiao
from core.base.selenium.base import ReuseChrome
from db.backends.mysql.operations import OperatorMysql
import time
from contrib.poster import poster_article
from contrib.identifier.base import Base_Identifier

def run():
    param = {
        'USER': 'root',
        'DBNAME': 'data_usable_database',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    }
    dbOperator = OperatorMysql(param)
    sql_get = 'SELECT * FROM `tb_selenium_info` WHERE `id`=\'1\';'
    driver_info = dbOperator.getOneDataFromDB(sql_get)
    browser_toutiao = ReuseChrome(command_executor=driver_info[1], session_id=driver_info[2])
    browser_toutiao.refresh()
    browser_toutiao.get("https://toutiao.com")
    c = Crawler_toutiao()
    time.sleep(5)
    c.click_chaijing(browser_toutiao)
    time.sleep(3)
    c.click_chaijing(browser_toutiao)
    time.sleep(2)
    c.roll_tobottom_method1(browser_toutiao, 1000)
    # 1 上传列表
    articleList = c.get_articleContent(browser_toutiao) # 文章元组对象
    # 2 清洗数据并过滤掉不符合条件的数据
    postableList = []
    for article in articleList:
        # 文章字数过滤
        if(len(article[2])>500 and Base_Identifier.is_intterrogative(article[1])):
            postableList.append((article[0], article[1], article[2]))
    browser_toutiao.get('https://www.baidu.com')
    # 3 数据插入数据库
    # dbOperator = dbOp.Contraler_Database(databaseName=setting['databaseName'], user=setting['databaseUser'],passwd=setting['databasePasswd'])
    # for article in postableList:
    #     sql = "INSERT INTO `articledatabase`.`tb_article_toutiao_content` (`url`, `title`, `content`) VALUES ('{}', '{}', '{}');".format(
    #         article[0],
    #         article[1],
    #         article[2]
    #     )
    #     dbOperator.insertData2DB(sql=sql)

    # 3 上传数据
    print('可上传文章的数量：', len(postableList))
    poster = poster_article.Poster_Article('http://121.40.187.51:8088/api/article_get')
    poster.post_auto(postableList, 'article')

    # 4 将上传过的数据放到postedurldatabase中
    # postedDBOP = dbOp.Contraler_Database(databaseName='postedurldatabase', user='root', passwd='root')
    # for article in postableList:
    #     sql = "INSERT INTO `postedurldatabase`.`tb_article_posted` (`url`, `title`, `content`) VALUES (\'{}\', \'{}\');".format(
    #         article[0],
    #         article[1],
    #         article[2]
    #     )
    #     postedDBOP.insertData2DB(sql)