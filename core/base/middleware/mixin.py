from utils.common import IsCheck_uchar

"""基类"""
class MiddlewareMixin:
    """
    中间件元基类内部基本方法， 定义了中间件需要重写的方法
    """
    def process_default(self, obj):
        """
        定义统一需要执行的操作
        若无统一操作则直接pass
        子类必须重写
        """
        return obj

    def process_operation(self, obj):
        """集成操作，子类需要重写该方法"""
        obj = self.process_default(obj)
        return obj

    def _str_check(self, s, is_which='url'):
        """相似度判断字符串是否是链接，字母占比超过80%判定为链接
        :param s 待判定的字符串 【注意】 该字符串需要经过清洗之后再传进来
        :param is_which 是否为某某 如 url
        :output bool值
        """
        if(is_which=='url'):
            alpha_num = 0
            for c in s:
                if(IsCheck_uchar.is_alphabet(c)):
                    alpha_num = alpha_num + 1
            ratio = alpha_num/len(s)
            if(ratio>0.75):
                return True
            else:
                return False
