"""
测试封装selenium的类和基于进程id重用selenium的类
"""
from contrib import selenium
def t_base_selenium():
    selenium.BaseSelenium()


def t_base_reuseselenium():
    selenium.ReuseChrome()