from utils import globalTools
from db.backends.mysql.operations import OperatorMysql
from contrib.poster import poster_question

def run():
    param = {
        'USER': 'root',
        'DBNAME': 'data_usable_database',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    }
    dbOperator = OperatorMysql(param)
    questionList = dbOperator.getAllDataFromDB(sql='SELECT * FROM data_usable_database.tb_zhihu_search_question;')
    QAList = []
    for question in questionList:
        answerList = []
        data = dbOperator.getAllDataFromDB(sql='SELECT `answer` FROM data_usable_database.tb_zhihu_search_content WHERE `question_id`={};'.format(question[0]))
        if(not data):
            continue
        for ans in data:
            answerList.append(ans[0])
        QAList.append((question[2], answerList))
    # 上传数据
    poster = poster_question.Poster_Question('http://121.40.187.51:8088/api/question_get')
    poster.post_auto(QAList, 'question')
    globalTools.finishTask()

