from globalTools import globalTools
from basement__ import ContralerDatabase as dbOp
from customFunction__.Poster import poster_question

def run():
    dbOperator = dbOp.Contraler_Database(databaseName='data_usable_database')
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

