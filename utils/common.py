"""
    一些常用的方法
"""
import time
from urllib import parse
import re
import os, shutil, hashlib, base64
import cv2
import numpy as np


# 时间处理类
class Controler_Time:
    """
        时间（时间戳、日期、年月日等）处理相关的基类和方法
    """
    @staticmethod
    def getMilliSecond():
        '''
        返回毫秒级时间戳
        '''
        return int(round(time.time() * 1000))

    # 获取当前日期
    @staticmethod
    def getCurDate(formatStr:str):
        '''
        获取当前日期
        :param formatStr: 指定格式 如 "%Y%m%d"
        :return:
        '''
        return time.strftime(formatStr, time.localtime())

    # 返回指定日期时间戳 时间格式 '%Y%m%d %H:%M:%S' 20210924 00：00：00 该方法用于哔哩哔哩时间的判断
    @staticmethod
    def getSecondByDate(date):
        b = time.strptime(date, '%Y%m%d %H:%M:%S')
        return time.mktime(b)





# 加密类
class Encode:
    """
        加密相关的基类和方法
    """
    # 统一输出类型为str
    def bytes2str(self, b):
        return str(b, encoding='utf-8')

    def str2bytes(self, s):
        return bytes(s, encoding='utf-8')

    def encodeByMd5(self, s):
        return hashlib.md5(s.encode(encoding='utf-8')).hexdigest()

    # base64输出的为bytes类型 要转化为字符串
    def encodeByBase64(self, s):
        res = base64.encodebytes(s).strip()
        # 转换为字符串
        res = self.bytes2str(res)
        return res

    def encodeBySHA1(self, s):
        if(not isinstance(s, bytes)):
            text = bytes(s, 'utf-8')
        sha = hashlib.sha1(text)
        encrypts = sha.hexdigest()
        return encrypts

    def encode0(self,s):
        return self.encodeByBase64(self.str2bytes(self.encodeByMd5(s)))

    @staticmethod
    def str2urlcode(s):
        '''
        将字符串转换为浏览器url编码格式
        '''
        return parse.quote(s)

    @staticmethod
    def urlcode2str(urlcode):
        '''
        将url编码转换为字符串格式
        '''
        return parse.unquote(urlcode)


# 字符处理相关的基类和方法
class IsCheck_uchar:
    '''
        底层设计 —— 字符判断 输出均为布尔值
    '''
    @staticmethod
    def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if(u'\u4e00' <= uchar <=u'\u9fa5'):
            return True
        else:
            return False

    @staticmethod
    def is_number(uchar):
        """判断一个unicode是否是数字"""
        if(u'\u0030' <= uchar <= u'\u0039'):
            return True
        else:
            return False

    @staticmethod
    def is_alphabet(uchar):
        """判断一个unicode是否是英文字母"""
        if(u'\u0041' <= uchar <= u'\u005a' or u'\u0061' <= uchar <= u'\u007a'):
            return True
        else:
            return False

    @staticmethod
    def is_other(uchar):
        """判断是否非汉字、非数字、非英文字符"""
        if(not (IsCheck_uchar.is_chinese(uchar) or IsCheck_uchar.is_number(uchar) or IsCheck_uchar.is_alphabet(uchar))):
            return True
        else:
            return False

    @staticmethod
    def all_isNumber(s):
        """验证字符串是否全部为数字"""
        p = re.compile('^[0-9]*$')
        result = p.match(s)
        if (result):
            # 说明全部位数字，返回1
            return True
        else:
            return False


# 目录处理类
class Controler_Dir:
    """
        文件及目录处理相关的基类和方法
    """
    # 获取当前根目录路径
    @staticmethod
    def getCurOriPath():
        return os.path.abspath(os.path.dirname(__file__))

    # 判断目录是否存在，不存在则创建
    @staticmethod
    def checkACreateDir(dirPath):
        exist = os.path.exists(dirPath)
        if (not exist):
            os.makedirs(dirPath)
        else:
            pass
        pass

    # 清空指定目录下所有文件
    @staticmethod
    def clearDirFiles(dirPath):
        lis = os.listdir(dirPath)
        for i in lis:
            os.remove(dirPath + i)

    @staticmethod
    def copyFile(src, dst):
        '''
            复制文件
        '''
        shutil.copyfile(src, dst)

    @staticmethod
    def renameFile(imgSrc, imgDst):
        """图片重命名"""
        os.rename(imgSrc, imgDst)





'''
    针对图片的基础操作
'''
class Controler_Img:
    @staticmethod
    def get_imgHeight(img_path):
        """获取图片的高度"""
        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
        h = img.shape[0]
        return h

    @staticmethod
    def cutting_single_img(img_path, cutBottomHeight):
        """裁切单张图片 并且覆盖原图片"""
        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
        if (img is not None):
            h = img.shape[0]
            w = img.shape[1]
            cutHeight = h - cutBottomHeight
            cutWidth = w
            print('img_shape: ', img.shape, 'cutWidth:cutHeight ', cutWidth, ":", cutHeight)
            cropped = img[0:cutHeight, 0:cutWidth]  # 裁剪坐标为[y0:y1, x0:x1]
            try:
                # cv2.imwrite(imgSrc, cropped) #这种方式保存命名中文会乱码
                cv2.imencode('.jpg', cropped)[1].tofile(img_path)
            except:
                print("图片裁切失败： ", img_path)

    @staticmethod
    def cutting_imgs_dir(dirpath, cutBottomHeight=55):
        '''
            以指定裁切高度裁切指定目录下的所有图片
        :param dirpath 待处理的目录  路径结尾需要\\结尾
        :cutBottomHeight 指定裁切高度
        '''
        imgName_list = os.listdir(dirpath)
        for imgName in imgName_list:
            imgpath = dirpath + imgName
            Controler_Img.cutting_single_img(img_path=imgpath, cutBottomHeight=cutBottomHeight)

    @staticmethod
    def change_imgMD5(imgSrc):
        """修改单张图片的md5"""
        with open(imgSrc, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        file = open(imgSrc, 'rb').read()
        with open(imgSrc, 'wb') as new_file:
            new_file.write(file + bytes('\0', encoding='utf-8'))  # here we are adding a null to change the file content
            newMD5 = hashlib.md5(open(imgSrc, 'rb').read()).hexdigest()
        print("修改MD5的文件：", imgSrc,"\n旧MD5: ", md5, " \t 新MD5： ",newMD5)

    @classmethod
    def change_imgMD5_dir(cls, dirPath):
        """批量修改目录下图片的MD5"""
        imgNameList = os.listdir(dirPath)
        for imgName in imgNameList:
            imgSrc = dirPath + '\\' + imgName
            cls.changeMD5(imgSrc)





"""
    通用的一些处理
"""


# 字符串正则处理类
class Handler_String_ByRe:
    def extract_StrByRe(self, string, patternStr=r'[[](.*?)[]]'):
        '''
        正则匹配字符串获取指定内容(匹配[]包括这的内容)
        :param string: 待匹配的字符串
        :param patternStr: 正则表达式模式
        :return: 列表
        '''
        pattern = re.compile(patternStr, re.S)  # 最小匹配
        return re.findall(pattern, string)



class Handle_PackageInfo:
    '''
        处理报文信息 如 cookie和headers字符串和对象的转换
    '''
    def translate_Cookies_Row2Obj(self, cookiesRow):
        cookieList = cookiesRow.split(";")
        self.cookies = {}
        for cookieItem in cookieList:
            i = cookieItem.strip().split("=")
            k = i[0]
            v = i[1]
            self.cookies[k] = v
        return self.cookies

    def translate_Headers_Row2Obj(self, headersRow):
        headerList = headersRow.split('\n')
        self.headers = {}
        for headerItem in headerList:
            i = headerItem.strip().split(":")
            if (i != ['']):
                k = i[0]
                v = i[1]
                self.headers[k] = v
        return self.headers


