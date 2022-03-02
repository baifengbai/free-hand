'''
    自动化引擎
        从相关段落数据库中获取数据 进行 清洗 筛选 并上传 （已完成）
'''
from utils import globalTools
from db.backends.mysql.operations import OperatorMysql
from middleware.filter.posted_mid import Filter_Posted
from middleware.filter.relativeparagraph_mid import Filter_Relativeparagraph
from contrib.poster.poster_paragraph import Poster_Paragraph as Poster
from core.base.tasksmixin.tasks_postdata.base import Base_Task_Post


class Task_Post_Relativeparagraph(Base_Task_Post):
    def run(self, db_user, db_pwd, database_name, table_name, keywordList):
        # setting = {
        #     'databaseName' : 'nanfangcaifudatabase',
        #     'databaseUser' : 'root',
        #     'databasePasswd' : 'root',
        #     'keywordList' : ['个股', '股市', 'A股', '港股', '新股', '美股', '创业板', '证券股', '股票', '炒股', '散户', '短线', '操盘', '波段']
        # }

        # 1 获取对应数据
        sql = 'SELECT `id`, `paragraph` FROM {};'.format(table_name),
        params = {
            'USER': db_user,
            'DBNAME': database_name,
            'PASSWORD': db_pwd,
            'HOST': '',
            'PORT': '',
        }
        dbOperator = OperatorMysql(params)
        dataList = dbOperator.getAllDataFromDB(sql)

        # 2 过滤操作 输入的列表为从数据库中获取的列表（过滤操作包含清洗操作，不用单独进行清洗）
        filterInstance = Filter_Relativeparagraph()
        postableList = filterInstance.integratedOp(paragraphList=dataList, keywordList=keywordList)

        # 3 上传列表
        posterInstance = Poster.Poster_Paragraph(interface='http://121.40.187.51:8088/api/relation_paragraph_api')
        posterInstance.post_auto(postableList, task_type='relativeParagraph')

        # 5 将上传过的数据放到postedurldatabase中
        params = {
            'USER': db_user,
            'DBNAME': 'postedurldatabase',
            'PASSWORD': db_pwd,
            'HOST': '',
            'PORT': '',
        }
        postedDBOP = OperatorMysql(params)
        for paragraph in postableList:
            sql = "INSERT INTO `postedurldatabase`.`tb_paragraph_posted` (`paragraph`) VALUES (\'{}\');".format(paragraph[0])
            postedDBOP.insertData2DB(sql)
        globalTools.finishTask()