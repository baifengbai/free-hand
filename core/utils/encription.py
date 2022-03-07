"""加密相关的功能函数、类"""
import hashlib
from utils.common import Controler_Time
from conf import setting


# 默认验证签名
def get_encript_key():
    curDate = Controler_Time.getCurDate('%Y%m%d')
    return hashlib.md5(('datapool' + setting.AUTHENTICATION['userName'] + setting.AUTHENTICATION['password'] + curDate).encode('utf-8')).hexdigest()
