from core.base.selenium.base import BaseSelenium
from core.base.download.base import BaseDownloader



class BaseCracker(BaseSelenium):
    '''（基于selenium）破解器基类 集成一些通用常用功能'''
    def __init__(self, *driverPath):
        if(driverPath!=()):
            # 显示继承父类
            BaseSelenium.__init__(self, driverPath[0])
            self.downloader = BaseDownloader()  # 资源下载器
        else:
            self.downloader = BaseDownloader()  # 资源下载器

    def enter_url(self, url):
        '''
        进入指定链接
        :param url: 注意需要加上协议 如：https://
        :return:
        '''
        self.browser.get(url)
        pass

    def del_All_cookies(self):
        '''
        删除本地保存的所有cookie，以便网站弹出验证框
        :return: none
        '''
        self.browser.delete_all_cookies()
        pass

    def get_Ori_allCookies(self):
        return self.browser.get_cookies()

    def get_Obj_allCookies(self):
        # 获取cookie
        dictCookies = self.browser.get_cookies()
        cookies = {}
        for item in dictCookies:
            key = item['name']
            cookies[str(key)] = str(item['value'])
        return cookies

    def get_URL(self, *browser):
        if(browser==()):
            curUrl = self.browser.current_url()
        else:
            curUrl = browser.browser.current_url()
        return curUrl

