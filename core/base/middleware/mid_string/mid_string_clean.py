"""针对字符串的处理 字符串清洗"""
from ..mixin import MiddlewareMixin
from static.universal_word_dict import UNIVERSAL_CLEANWORD_DICT
import re

class StringMiddleware(MiddlewareMixin):
    _clean = ''
    @classmethod
    def clean_startwith_char(cls, s:str, key:str='startwith'):
        for x in UNIVERSAL_CLEANWORD_DICT[key]:
            if(s.startswith(x)):
                s = s[1:]
        return s

    @classmethod
    def __clean_by_key(cls, s:str, key:str):
        """
        清除指定字符
        :param s
        :param key UNIVERSAL_CLEANWORD_DICT 中对应的键名
        """
        for o in UNIVERSAL_CLEANWORD_DICT[key]:
            s = s.replace(o, '')
        return s

    @classmethod
    def clean_space(cls, s:str, key:str='space'):
        """
        清除所有空格
        :param s
        :param key UNIVERSAL_CLEANWORD_DICT 中对应的键名
        """
        return cls.__clean_by_key(s, key)

    @classmethod
    def clean_headnum(cls, s, key='xuhao1'):
        return cls.__clean_by_key(s, key)

    @classmethod
    def clean_between(cls, s, s_left, s_right):
        """
        去除字符串中指定左右间的内容
            如： s = '财讯网（记者 XXX）AAAAA'     #去除（记者 XXX）
                s = del_content_between(s, s_left='（记者', s_right='）')
        """
        try:
            r_rule = u"\\" + s_left + u".*?" + s_right
            res = re.sub(r_rule, "", s)
        except Exception as e:
            r_rule = u"\\" + s_left + u".*?" + "\\" + s_right
            res = re.sub(r_rule, "", s)
        return res

    @classmethod
    def clean_content_brackets(cls, s, size='', o='', delAll=False):
        """
        去除字符串中的括号间的内容
            如： [sth] saji 【盎司附近两千】qjioq
        :param s 待处理的字符串
        :param size 尺寸
            小括号 small
            中括号 middle
            大括号 large
        :param o 全角或半角
            半角 half
            全角 full
        :param dellAll 是否删除所有括号里的内容
        """
        if(delAll==True):
            return re.sub(u"\\(.*?\\)|\\[.*?]|\\{.*?}|\\（.*?\\）|\\【.*?】|\\【.*?】", "", s)

        if(o=='half'):
            if (size == 'small'):
                return re.sub(u"\\(.*?\\)", "", s)
            elif (size == 'middle'):
                temp = re.sub(u"\\［.*?］", "", s)
                return re.sub(u"\\[.*?]", "", temp)
            elif (size == 'large'):
                return re.sub(u"\\{.*?}", "", s)
            else:
                raise AttributeError("请确认括号尺寸size 小括号small 中括号middle 大括号large")
        elif(o=='full'):
            if (size == 'small'):
                return re.sub(u"\\（.*?\\）", "", s)
            elif (size == 'middle'):
                return re.sub(u"\\【.*?】", "", s)
            elif (size == 'large'):
                return re.sub(u"\\{.*?}", "", s)
            else:
                raise AttributeError("请确认括号尺寸size 小括号small 中括号middle 大括号large")
        else:
            raise AttributeError('请输入全角 full 或是 半角 half 属性')

    @classmethod
    def clean_before_symple(cls, s, symple, del_direction):
        """
        删除指定符号之前的内容或者之后的内容
        :param s 待处理的字符串
        :param symple 指定符号 如： '|'
        :param del_direction 指定删除的方向
            left 删除指定符号左边的内容， 输出符号右边的内容
            right 删除指定符号右边的内容， 输出符号左边的内容
        """
        if(del_direction == 'left'):
            return s.split(symple)[-1]
        elif(del_direction=='right'):
            return s.split(symple)[0]
        else:
            raise AttributeError("请指定正确的方向 left right")

    @classmethod
    def clean_webTag(cls, s):
        '''
        (针对爬取的评论内容设计的方法) 清除评论内容中有标签内容的
        :param comment:
        :return:
        '''
        res = ''
        for m in s.split('>'):
            res = res + m.split('<')[0]
        return res

    @classmethod
    def clean_stocks(cls, s, stocksNameCodeList):
        '''
        （用于段落字符串清洗）清除字符串中的股票名/股票代码
        :param s:
        :param stocksNameCodeList:股票列表
        :return:
        '''
        for item in stocksNameCodeList:
            li = []
            li.append(item[0] + "（{}）".format(item[1]))
            li.append("（{}）".format(item[0]))
            li.append("（{}）".format(item[1]))
            li.append(item[0])
            li.append(item[1])
            for stock in li:
                paragraph = paragraph.replace(stock, "")  # 删除股票关键字（包括中文及代买关键字）
        return paragraph

    def process_default(self, s:str):
        """针对字符串通用清洗操作 统一前奏操作"""
        # 1 清空白
        s = self.clean_space(s)
        # 2 清括号内容
        s = self.clean_content_brackets(s, delAll=True)
        # 3 清序号
        for k in ['xuhao1', 'xuhao2', 'xuhao3']:
            s = self.clean_headnum(s, k)
        return s