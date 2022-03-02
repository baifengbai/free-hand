from utils import globalTools
from db.backends.mysql.operations import OperatorMysql
from middleware.filter.comment_mid import Filter_Comment
from middleware.filter.posted_mid import Filter_Posted_Comment
from contrib.poster import poster_comment as Poster
from core.base.tasksmixin.tasks_postdata.base import Base_Task_Post
from middleware.cleaner.comment_mid import CommentMiddleware

class Task_Post_Comment(Base_Task_Post):
    def run(self, db_user, db_pwd, database_name, table_name, keywordList):
        # setting = {
        #     'databaseName' : 'commentdatabase',
        #     'databaseUser' : 'root',
        #     'databasePasswd' : 'root',
        #     'keywordList' : ['个股', '股市', 'A股', '港股', '新股', '美股', '创业板', '证券股', '股票', '炒股', '散户', '短线', '操盘', '波段']
        # }
        # setting['sql'] = "select id,comment from ``.``;"

        # 1 获取 对应数据
        sql = 'select `id`,`comment` from {};'.format(table_name)
        params = {
            'USER': db_user,
            'DBNAME': database_name,
            'PASSWORD': db_pwd,
            'HOST': '',
            'PORT': '',
        }
        dbOperator = OperatorMysql(params)
        dataList = dbOperator.getAllDataFromDB(sql)
        # 2 对所有段落内容判断，若上传过则删除对应上传过的段落
        filter4postedcheck = Filter_Posted_Comment()
        dataList = filter4postedcheck.run(dataOriList=dataList)
        # 3 去重
        dataList = self.del_repeatdata(task_type='articleComment', lis=dataList)
        # 4 过滤操作 输入的列表为从数据库中获取的列表（过滤操作包含清洗操作，不用单独进行清洗）
        filterInstance = Filter_Comment()
        postableList = filterInstance.integratedOp(commentList=dataList, keywordList=keywordList)

        # 5 上传列表
        if (postableList):
            posterInstance = Poster.Poster_Comment(interface='http://121.40.187.51:8088/api/articlecomment_api')
            posterInstance.post_auto(postableList, task_type='articleComment')

        # 6 将上传过的数据放到postedurldatabase中
        params = {
            'USER': db_user,
            'DBNAME': 'postedurldatabase',
            'PASSWORD': db_pwd,
            'HOST': '',
            'PORT': '',
        }
        postedDBOP = OperatorMysql(params)
        for comment in postableList:
            sql = "INSERT INTO `postedurldatabase`.`tb_comment_posted` (`comment`) VALUES (\'{}\');".format(comment[0])
            postedDBOP.insertData2DB(sql)
        globalTools.finishTask()