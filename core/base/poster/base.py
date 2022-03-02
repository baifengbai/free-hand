import json
from conf import setting
import requests, hashlib
from core.utils import encription
from utils.common import Contraler_Time
from db.backends.mysql.operations import OperatorMysql
from requests_toolbelt import MultipartEncoder
from middleware.cleaner.article_mid import ArticleMiddleware
from ..logger.base import logger_comment


class BasePoster:
    interface = ''
    userName = setting['AUTHENTICATION']['userName']
    password = setting['AUTHENTICATION']['password']
    curDate = str(Contraler_Time.getCurDate(formatStr="%Y%m%d"))
    key = encription.get_encript_key(userName, password, curDate)
    dbOperator = OperatorMysql(settings_dict=setting['DATABASES'])

    # 上传单个数据列表的方法
    @staticmethod
    def poster(postableData, interface):
        '''
        上传单条数据的方法
        :param postableData:
        :param interface: 接口
        :return:
        '''
        # 这里传文件的时候用绝对路径传，不然传了之后显示不了
        formData = (postableData)
        m = MultipartEncoder(formData)
        headers2 = {
            "Content-Type": m.content_type
        }
        postResult = requests.post(url=interface, data=m, headers=headers2)
        # 判断是否上传成功 失败则打印
        # if(postResult and postResult.text[0]!='1'):
        #     # Base_Poster.log_poster_res(postableData)
        #     print('上传失败：',postResult )
        return postResult

    @staticmethod
    @logger_comment
    def log_post_res(lis_totle, lis_success, lis_failed):
        """打印上传日志"""
        pass

    def post_auto(self, effectiveDataList, task_type):
        self.curDate = str(self.contralTime.getCurDate(formatStr="%Y%m%d"))
        self.key = hashlib.md5(('datapool' + self.userName + self.password + self.curDate).encode('utf-8')).hexdigest()
        posted_success_lis = []
        posted_failed_lis = []
        for item in effectiveDataList:
            if (task_type == 'keyParagraph'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'content': item[0],
                    'keyword': item[1],
                    'rekeyword': '配资'
                }
                res = self.poster(postableData=postableData, interface=self.interface)
            elif (task_type == 'relativeParagraph'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'content': item[0],
                    'keyword': item[1]
                }
                res = self.poster(postableData=postableData, interface=self.interface)
            elif (task_type == 'articleComment'):
                comment = item[0].strip()
                sql = "SELECT * FROM `postedurldatabase`.`tb_comment_posted` where `comment` = \'{}\';".format(comment)
                if (self.dbOperator.getOneDataFromDB(sql)):
                    # 数据库中存在对应评论
                    continue
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'comment': item[0].replace(item[1], '股票').replace('&nbsp;', ' ')
                }
                res = self.poster(postableData=postableData, interface=self.interface)
                # 更新数据库
                self.update_postedurldb(item)
            elif(task_type == 'article'):
                cleaner_Article = ArticleMiddleware()
                title = cleaner_Article.clean_title(item[1])
                content = cleaner_Article.clean_content(item[2])
                # content = cleaner_Article.integratedOp(item[2])
                if (len(item[2]) > 500 and len(title) > 10 and '；' not in title):
                    postableData = {
                        "key": self.key,
                        "account": self.userName,
                        "password": self.password,
                        'title': title,
                        'content': content
                    }
                    res = self.poster(postableData=postableData, interface=self.interface)

            elif (task_type == 'question'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'question': str(item[0]),
                    'answer': json.dumps(item[1])
                }
                res = self.poster(postableData=postableData, interface=self.interface)
            if (res and res.json()['code'] == 1):
                # 上传成功的
                posted_success_lis.append(item)
            else:
                posted_failed_lis.append(item)
        self.log_post_res(effectiveDataList, lis_success=posted_success_lis, lis_failed=posted_failed_lis)  # 日志记录
