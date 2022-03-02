import math
import time
import execjs


class Executor_Javascript:
    """执行javascript代码/文件 输出结果"""
    @classmethod
    def execute_jsfile(cls, filepath):
        """
        输出js执行环境
        :param filepath js文件路径
        :output
        """
        js = ''
        with open(filepath, 'r', encoding="utf-8") as f:
            jsLis = f.readlines()
            for li in jsLis:
                js = js + li
        js_executor = execjs.compile(js)
        return js_executor

    @classmethod
    def execute_jsfunc(cls, js_executor, funcName, *funcArgs):
        """
        用execjs.compile().call(函数名, 函数参数)方法在js执行函数里执行指定函数
        """
        return js_executor.call(funcName, funcArgs)