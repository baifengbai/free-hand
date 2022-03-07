import json
from conf import setting
import requests
import hashlib
from core.utils import encription
from utils.common import Controler_Time
from db.backends.mysql.operations import OperatorMysql
from requests_toolbelt import MultipartEncoder
from middleware.cleaner.article_mid import ArticleMiddleware
from ..logger.base import logger_comment
from utils import globalTools


class KeyGenerator:
    """生成上传数据需要的key值"""
    def __init__(self):
        self._key = None
        pass
    @property
    def key(self):
        self._key = self._update_key()
        # print('key值已更新 ', Controler_Time.getCurDate('%Y-%m-%d %H:%M:%S'))
        return self._key

    def _update_key(self):
        return encription.get_encript_key()

class BasePoster(KeyGenerator):
    """默认通用"""
    userName = setting.AUTHENTICATION['userName']
    password = setting.AUTHENTICATION['password']
    curDate = str(Controler_Time.getCurDate(formatStr="%Y%m%d"))
    dbOperator = OperatorMysql(settings_dict=setting.DATABASES)
    def __init__(self, uri):
        KeyGenerator.__init__(self)
        self._interface = uri

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, val):
        self._interface = val
        print('配置接口完成 %s %s'%(val, Controler_Time.getCurDate('%Y-%m-%d %H:%M:%S')))


    # 规范化待上传的列表
    def _regulate_postablelis(self, task_type, lis):
        """
        根据配置文件定义的 API_Params 位置关系，将传入的列表中每个元组的数据映射成 API_Params 位置关系的格式
        [title, content/comment, keyword, rekeyword, question, answer]
        """
        output_lis = []
        for i in lis:
            if(task_type=='keyParagraph'):
                output_lis.append(
                    ('', i[0], i[1], '配资', '', '')
                )
            elif (task_type == 'relativeParagraph'):
                output_lis.append(
                    ('', i[0], i[1], '', '', '')
                )
            elif(task_type=='articleComment'):
                output_lis.append(
                    ('', i[0], i[1], '', '', '')
                )
            elif(task_type=='article'):
                output_lis.append(
                    (i[1], i[2], '', '', '', '')
                )
            elif (task_type == 'question'):
                output_lis.append(
                    ('', '', '', '', i[0], i[1])
                )
        return output_lis

    # 请求体内容映射
    def _package_body_map(self, task_type, item):
        """
        根据item内容拼接报文body，然后将值为空的键名删除（也可不删，应该影响不大）
        注意 item里的内容应该为可以直接上传已经处理好了的
        :param task_type 任务类型
        :param item 数据对象
        """
        body = setting.API_PARAMS_DICT[task_type]
        body['userName'] = self.userName
        body['password'] = self.password
        body['key'] = self.key
        body['title'] = item[0]
        body['content'] = item[1]
        body['keyword'] = item[2]
        body['rekeyword'] = item[3]
        body['question'] = item[4]
        body['answer'] = json.dumps(item[5]) if item[5] else ''
        key_lis = ['title','content','keyword','rekeyword','question','answer']
        # 将空值的键值删除
        for key in key_lis:
            if(not body[key]):
                body.pop(key)
        return body

    # 上传单个数据列表的方法
    @staticmethod
    def poster(postableData, interface):
        '''
        接收表单参数，构建请求post请求
        formData = ({"key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'file': (imgName, f, "image/jpeg"),
                    'title': imgName.split('.')[0]
                    })
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

    # 优化后的上传方法 20220304
    def post_auto_2(self, effectiveDataList, task_type):
        posted_success_lis = []
        posted_failed_lis = []
        data_lis = self._regulate_postablelis(task_type, effectiveDataList)
        for item in data_lis:
            item = list(item)
            if(
                task_type == 'keyParagraph' or
                task_type == 'relativeParagraph'
            ):
                body = self._package_body_map(task_type, item)
                res = self.poster(postableData=body, interface=self.interface)
            elif(task_type == 'articleComment'):
                item[0] = item[0].replace(item[1], '股票').replace('&nbsp;', ' ')
                body = self._package_body_map(task_type, item)
                res = self.poster(postableData=body, interface=self.interface)
            elif(task_type == 'article'):
                cleaner_Article = ArticleMiddleware()
                item[1] = cleaner_Article.clean_title(item[1])
                item[2] = cleaner_Article.clean_content(item[2])
                if (len(item[2]) > 500 and len(item[1]) > 10 and '；' not in item[1]):
                    body = self._package_body_map(task_type, item)
                    res = self.poster(postableData=body, interface=self.interface)
            if (res and res.json()['code'] == 1):
                # 上传成功的
                posted_success_lis.append(item)
            else:
                posted_failed_lis.append(item)
        self.log_post_res(effectiveDataList, lis_success=posted_success_lis, lis_failed=posted_failed_lis)  # 日志记录

    # 原上传方法
    def post_auto(self, effectiveDataList, task_type):
        curDate = Controler_Time.getCurDate(formatStr="%Y%m%d")
        self.key = encription.get_encript_key(self.userName, self.password, curDate)
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

class BasePoster_Img(BasePoster):
    """上传图片专用类"""
    def __init__(self, uri, imgs_dir_path):
        KeyGenerator.__init__(self)
        BasePoster.__init__(self, uri=uri)
        self.imgDirPath = imgs_dir_path
        self.imgNameList = None  # 待上传的图片名列表

    # 修改单张图片的md5
    def changeMD5(self, img_path):
        with open(img_path, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        file = open(img_path, 'rb').read()
        with open(img_path, 'wb') as new_file:
            new_file.write(file + bytes('\0', encoding='utf-8'))  # here we are adding a null to change the file content
            newMD5 = hashlib.md5(open(img_path, 'rb').read()).hexdigest()
        # print("修改MD5的文件：", imgSrc, "\n旧MD5: ", md5, " \t 新MD5： ", newMD5)

    def poster(self, postableData, interface):
        m = MultipartEncoder(postableData)
        headers2 = {
            "Content-Type": m.content_type
        }
        postResult = requests.post(url=self.interface, data=m, headers=headers2)
        return postResult

    def post_auto(self, task_type):
        if(self.imgNameList):
            for imgName in self.imgNameList:
                img_path = self.imgDirPath + "\\" + imgName
                print("任务类型： %s, 处理图片： %s" % (task_type, img_path))
                # 改md5
                self.changeMD5(img_path)
                # 打开图片
                # f = open('E:\Projects\imgReconization\imgsDontHasWaterMask\\2+商品-家居家装-吸顶灯 + 非自然图像-图像素材-图像素材.jpg', 'rb')
                f = open(img_path, 'rb')
                # fileByte = base64.b64encode(f.read())  # 不要用这个，不然图片显示不了
                # 这里传文件的时候用绝对路径传，不然传了之后显示不了
                body = ({
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'file': (imgName, f, "image/jpeg"),
                    'title': imgName.split('.')[0]
                })
                res = self.poster(postableData=body, interface=self.interface)
                f.close()
                try:
                    # 上传完删除对应单张图片
                    globalTools.delVideoSingle(img_path)
                except Exception as e:
                    print("删除图片出错： ", img_path)
        else:
            print('当前目录下无图片 %s'%self.imgDirPath)