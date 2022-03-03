'''
    自动化引擎
        从评论数据库中获取数据 进行 清洗 筛选 并上传 （已完成）
'''
from utils import globalTools
from db.backends.mysql.operations import OperatorMysql
from middleware.filter import comment_mid, posted_mid
from contrib.poster import poster_comment as Poster

def run(setting):
    # setting = {
    #     'databaseName' : 'commentdatabase',
    #     'databaseUser' : 'root',
    #     'databasePasswd' : 'root',
    #     'keywordList' : ['个股', '股市', 'A股', '港股', '新股', '美股', '创业板', '证券股', '股票', '炒股', '散户', '短线', '操盘', '波段']
    # }
    # setting['sql'] = "select id,comment from ``.``;"

    # 1 获取对应数据
    param = {
        'USER': 'root',
        'DBNAME': setting['databaseName'],
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    }
    dbOperator = OperatorMysql(param)
    dataList = dbOperator.getAllDataFromDB(setting['sql'])

    # 2 对所有段落内容判断，若上传过则删除对应上传过的段落
    filter4postedcheck = posted_mid.Filter_Posted_Comment()
    dataList = filter4postedcheck.run(dataOriList=dataList)

    # 3 过滤操作 输入的列表为从数据库中获取的列表（过滤操作包含清洗操作，不用单独进行清洗）
    filterInstance = comment_mid.Filter_Comment()
    postableList = filterInstance.integratedOp(commentList=dataList, keywordList=setting['keywordList'])


    # 4 上传列表
    posterInstance = Poster.Poster_Comment(interface='http://121.40.187.51:8088/api/articlecomment_api')
    posterInstance.post_auto(postableList, task_type='articleComment')

    # 5 将上传过的数据放到postedurldatabase中
    param = {
        'USER': 'root',
        'DBNAME': 'postedurldatabase',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    }
    postedDBOP = OperatorMysql(param)
    for comment in postableList:
        sql = "INSERT INTO `postedurldatabase`.`tb_comment_posted` (`comment`) VALUES (\'{}\');".format(comment[0])
        postedDBOP.insertData2DB(sql)
    globalTools.finishTask()