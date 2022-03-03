from selenium import webdriver
import time
from ..utils import u_selenium
from selenium.webdriver import Remote
from selenium.webdriver.chrome import options
from selenium.common.exceptions import InvalidArgumentException
from conf import setting

# Selenium driver多进程调用的类
class ReuseChrome(Remote):
    def __init__(self, command_executor, session_id):
        self.r_session_id = session_id
        Remote.__init__(self, command_executor=command_executor, desired_capabilities={})

    def start_session(self, capabilities, browser_profile=None):
        """重写该方法"""
        if(not isinstance(capabilities, dict)):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if(browser_profile):
            if("moz:firefoxOptions" in capabilities):
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({"firefox_profile": browser_profile.encoded})
        self.capabilities = options.Options().to_capabilities()
        self.session_id = self.r_session_id
        self.w3c = False

# 通过selenium获取指定信息的类
class BaseSelenium(
    u_selenium.Roll_To_Bottom,
    u_selenium.Click_Element
):
    DRIVER_PATH = setting.DRIVER_SELENIUM_PATH
    def __init__(self, *driverPath):
        if(driverPath!=()):
            self.browser = self.init_webdriver(chromeDriverPath=driverPath)

    @classmethod
    def init_webdriver(cls, chromeDriverPath=DRIVER_PATH, *toggle_device):
        """
        创建输出webdriver对象 下面的option避免了被检测到是模拟浏览器
        :chromeDriverPath 引擎的路径
        :option
        """
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument('--disable-blink-features=AutomationControlled')
        if(toggle_device!=()):
            option = cls.toggle_device(option)
        browser = webdriver.Chrome(executable_path=chromeDriverPath, options=option)
        return browser

    def add_agent(self, proxyHost="u7125.5.tp.16yun.cn", proxyPort= "6445", proxyUser="16OINIUS", proxyPass= "971935", browser_driver_path="E:\Projects\webDriver\\chrome\\chromedriver.exe"):
        """创建添加爬虫代理的browser 根据不同代理源再customFunction__.Contraler_selenium.contraler_selenium 中重写"""
        pass

    def getCookies(self, browser, *url):
        '''
        类方法，以对象形式输出指定链接返回的cookies
        :param url: 待打开的链接
        :param browser: 浏览器引擎
        :return: cookies对象
        '''
        # 获取cookie
        dictCookies = browser.get_cookies()
        cookies = {}
        for item in dictCookies:
            key = item['name']
            cookies[str(key)] = str(item['value'])
        return cookies

    def del_all_cookies(self):
        self.browser.delete_all_cookies()

    def get_params(self, url, *browser):
        if(browser==()):
            self.browser.get(url)
            time.sleep(1)
            cookies = self.getCookies(url, self.browser)
            headers = {}
            return {
                'cookies': cookies,
                'headers': headers
            }
        else:
            browser.get(url)
            time.sleep(1)
            cookies = self.getCookies(url, browser)
            headers = {}
            return {
                'cookies': cookies,
                'headers': headers
            }

    def toggle_device(self, options):
        """
        切换设备模式，如切换成iphone6
        :param option webdriver.ChromeOptions()对象 通过添加相关参数的方式调整
        """
        # 手机模式
        mobile_emulation = {"deviceName": "iPhone 6"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        # 开发者模式
        # options.add_experimental_option("--auto-open-devtools-for-tabs")
        return options

    def close_browser(self, *browser):
        '''
        关闭指定浏览器，若浏览器为None则关闭对象浏览器
        :param browser:
        :return: None
        '''
        if(browser==()):
            self.browser.close()
        else:
            browser[0].close()



