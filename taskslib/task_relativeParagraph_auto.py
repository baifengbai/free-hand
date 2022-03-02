'''
    自动化引擎
        从相关段落数据库中获取数据 进行 清洗 筛选 并上传 （已完成）
'''
from globalTools import globalTools
from basement__ import ContralerDatabase as dbOp
from customFunction__.Filter import filter_posted, filter_relativeparagraph
from customFunction__.Poster import poster_paragraph as Poster

def run(setting):
    # setting = {
    #     'databaseName' : 'nanfangcaifudatabase',
    #     'databaseUser' : 'root',
    #     'databasePasswd' : 'root',
    #     'keywordList' : ['个股', '股市', 'A股', '港股', '新股', '美股', '创业板', '证券股', '股票', '炒股', '散户', '短线', '操盘', '波段']
    # }
    # setting['sql'] = "select id,paragraph from `nanfangcaifudatabase`.`tb_articlecontent`;"

    # 1 获取对应数据
    dbOperator = dbOp.Contraler_Database(databaseName=setting['databaseName'], user=setting['databaseUser'], passwd=setting['databasePasswd'])
    dataList = dbOperator.getAllDataFromDB(setting['sql'])

    # 2 对所有段落内容判断，若上传过则删除对应上传过的段落
    filter4postedcheck = filter_posted.Filter_Posted()
    dataList = filter4postedcheck.run(dataOriList=dataList)

    # 3 过滤操作 输入的列表为从数据库中获取的列表（过滤操作包含清洗操作，不用单独进行清洗）
    filterInstance = filter_relativeparagraph.Filter_Relativeparagraph()
    postableList = filterInstance.integratedOp(paragraphList=dataList, keywordList=setting['keywordList'])

    # 4 上传列表
    posterInstance = Poster.Poster_Paragraph(interface='http://121.40.187.51:8088/api/relation_paragraph_api')
    posterInstance.post_auto(postableList, task_type='relativeParagraph')

    # 5 将上传过的数据放到postedurldatabase中
    postedDBOP = dbOp.Contraler_Database(databaseName='postedurldatabase', user='root', passwd='root')
    for paragraph in postableList:
        sql = "INSERT INTO `postedurldatabase`.`tb_paragraph_posted` (`paragraph`) VALUES (\'{}\');".format(paragraph[0])
        postedDBOP.insertData2DB(sql)
    globalTools.finishTask()