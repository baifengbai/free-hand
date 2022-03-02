import time
from selenium.webdriver.common.keys import Keys


"""用于selenium的通用类"""
class Roll_To_Bottom:
    """滚动到底部的类"""
    @classmethod
    # 下滑到最底部
    def roll_tobottom_method1(cls, browser, times=350):
        '''
        向下滑动滚动条指定次数
        :param browser 指定浏览器引擎
        :param times 滑动次数
        '''
        for i in range(0, times):
            browser.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN)  # 在这里使用模拟的下方向键
            time.sleep(0.1)
        return None

    @classmethod
    def roll_tobottom_method2(cls, browser, distance):
        '''
        向下滑动滚动条指定px距离
        :param browser 指定浏览器引擎
        :param distance 指定像素距离
        '''
        # 以当前位置为参照向下滚动
        browser.execute_script('window.scrollBy(0 ,{})'.format(distance)) # 从当前位置向下滚动1000px
        return None

class Click_Element:
    def click_element(self, ele):
        ele.click()

class Close_Browser:
    """关闭浏览器对象的类"""
    @classmethod
    def close_browser(cls, browser):
        """关闭浏览器"""
        browser.close()




