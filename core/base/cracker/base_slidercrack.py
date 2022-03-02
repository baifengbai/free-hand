import cv2
import numpy as np
from .base import BaseCracker
from selenium.webdriver.common.action_chains import ActionChains
import time

"""
    滑块验证 基类
    集成各种通用验证方法：
        滑块验证等
    注意 使用cv2 路径不能有中文名
"""
class Base_Slidercrack(BaseCracker):
    def __init__(self, driverPath):
        BaseCracker.__init__(self, driverPath)

    # 滑块验证 输出水平移动的距离 计算坐标的偏移量
    # templatePath 滑块 , targetPath 背景模板
    @staticmethod
    def getMovement_sliderCheck_method1(templatePath, targetPath, elWidth):
        '''
            滑块验证 输出水平移动的距离 计算坐标的偏移量
            注意：这一个算法没问题，只是可能需要试几次才有一次正确的
        :param elWidth: 背景图在网页上显示的宽度，用于比例计算实际滑动距离
        :param templatePath: 滑块图片路径
        :param targetPath: 背景图片路径
        :return: 偏移量
        '''
        target_rgb = cv2.imdecode(np.fromfile(targetPath, dtype=np.uint8), -1)
        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
        template_rgb = cv2.imread(templatePath, 0)
        ori_width = target_rgb.shape[1]
        ori_height = target_rgb.shape[0]
        res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
        value = cv2.minMaxLoc(res)
        # (因为下载的图片跟网页上的图片是有缩放的)所以要根据比例计算网页端需要移动的偏移量
        effectiveVal = value[2][0] * elWidth / ori_width
        print('effectiveVal:', effectiveVal)
        print('value2:', value[2][0])
        print('value3:', value[3][0])
        print('res:', res.shape)
        return effectiveVal

    @classmethod
    def handle_SlideCheck(cls, *browser):
        '''处理滑块验证 根据不同站点的滑块验证进行重写'''
        pass

    @classmethod
    def download_slideImgs(cls, *browser, dstDirPath='E:\Projects\packageDIY\\videoRef\\assets\\'):
        '''
            下载滑块以及滑块背景用于识别位置 根据不同站点的滑块验证进行重写
        :return: targetWidth 背景图在网页中的宽度 用于步长计算
        '''
        pass

    # 模拟人操作
    def get_tracks(self, distance, rate=0.6, t=0.2, v=0):
        """
        将distance分割成小段的距离
        :param distance: 总距离
        :param rate: 加速减速的临界比例
        :param a1: 加速度
        :param a2: 减速度
        :param t: 单位时间
        :param t: 初始速度
        :return: 小段的距离集合
        """
        tracks = []
        # 加速减速的临界值
        mid = rate * distance
        # 当前位移
        s = 0
        # 循环
        while s < distance:
            # 初始速度
            v0 = v
            if s < mid:
                a = 20
            else:
                a = -3
            # 计算当前t时间段走的距离
            s0 = v0 * t + 0.5 * a * t * t
            # 计算当前速度
            v = v0 + a * t
            # 四舍五入距离，因为像素没有小数
            tracks.append(round(s0))
            # 计算当前距离
            s += s0
        return tracks


    def move_sliderTemplate(self, movement, *browser, templateSelector):
        '''
            移动滑块，根据不同站点进行重写
        :param movement:
        :return:
        '''
        if(browser==()):
            # 无指定浏览器
            # 实例化鼠标操作
            action = ActionChains(self.browser)
            # 按住滑块
            action.click_and_hold(templateSelector).perform()

            for i in range(movement):
                action.move_by_offset(1, 0)
            # 释放滑块
            action.release().perform()
        else:
            # 实例化鼠标操作
            action = ActionChains(browser[0])
            # 按住滑块
            action.click_and_hold(templateSelector).perform()

            print("验证中...")
            for i in range(movement):
                action.move_by_offset(1, 0)
            # 释放滑块
            action.release().perform()

    def move_sliderTemplate_likeHuman(self, movement, *browser, templateSelector):
        '''
            移动滑块 根据不同站点进行重写
        :param movement: 移动的距离
        :param templateSelector: 滑块selector
        :return:
        '''
        if (browser == ()):
            # 无指定浏览器
            # 实例化鼠标操作
            action = ActionChains(self.browser)
            # 按住滑块
            action.click_and_hold(templateSelector).perform()

            print("验证中...")
            _tracks = self.get_tracks(movement)
            new_1 = _tracks[-1] - (sum(_tracks) - movement)
            _tracks.pop()
            _tracks.append(new_1)
            print(_tracks)
            for mouse_x in _tracks:
                action.move_by_offset(mouse_x, 0)
            # 释放滑块
            action.release().perform()
            time.sleep(2)

        else:
            # 实例化鼠标操作
            action = ActionChains(browser[0])
            # 按住滑块
            action.click_and_hold(templateSelector).perform()

            print("验证中...")
            _tracks = self.get_tracks(movement)
            new_1 = _tracks[-1] - (sum(_tracks) - movement)
            _tracks.pop()
            _tracks.append(new_1)
            print(_tracks)
            for mouse_x in _tracks:
                action.move_by_offset(mouse_x, 0)
            # 释放滑块
            action.release().perform()
            time.sleep(2)

    def get_selector(self):
        '''获取对应selector 根据不同站点进行重写'''
        pass

    @classmethod
    def slidecrack_run(cls):
        '''运行滑块破解功能 根据不同站点进行重写'''
        pass