from utils import globalTools
from db.backends.mysql.operations import OperatorMysql
from middleware.filter.keyparagraph_mid import Filter_Keyparagraph
from contrib.poster.poster_paragraph import Poster_Paragraph as Poster
from core.base.tasksmixin.tasks_postdata.base import Base_Task_Post


class Task_Post_Keyparagraph(Base_Task_Post):
    def run(self, db_user, db_pwd, database_name, table_name, tableName4Tag):
        # setting = {
        #     'databaseName': 'magicsunshadingdatabase',
        #     'databaseUser': 'root',
        #     'databasePasswd': 'root',
        #     'tableName': 'tb_articlecontent',
        #     'tableName4Tag': 'tb_articleinfo',
        #     'tagRefSqlKind': 'url',
        # }

        # 1 获取 对应数据
        sql = 'SELECT * FROM {};'.format(table_name),
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
        filterInstance = Filter_Keyparagraph()
        postableList = filterInstance.integratedOp(
            paragraphList=dataList,
            databaseName=database_name,
            tableName=table_name,
            tableName4Tag=tableName4Tag,
            tagRefSqlKind='url'
        )
        print("过滤操作完成， 接下来完成上传操作")
        # 4 上传列表
        posterInstance = Poster.Poster_Paragraph(interface='http://121.40.187.51:8088/api/key_paragraph_api')
        posterInstance.post_auto(postableList, task_type='keyParagraph')

        print("上传操作完成， 接下来完成 postedurldatabase 数据库的更新操作")
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
