"""
"""

__all__ = [
    'get_encript_key'
]
import hashlib
from conf import setting

# 默认验证签名
def get_encript_key(user, pwd, curDate):
    return hashlib.md5(('datapool' + user + pwd + curDate).encode('utf-8')).hexdigest()
