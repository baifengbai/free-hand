from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from utils.common import Contraler_Time

class Douyin_SpecialMethod:
    @staticmethod
    def check_publishtime_istoday(s: str):
        """
        根据抖音视频页面的发布时间表示情况写的方法 判断是否为当天
        :param s 类似 2021-12-07 的字符串
        :output Boolean
        """
        pubTime = "".join(s.split("-"))
        if (pubTime != Contraler_Time.getCurDate("%Y%m%d")):
            # 判断不是当天的视频则跳过
            return False
        else:
            return True

    @staticmethod
    def check_timelength_between(s, min=1, max=6):
        """
        判断视频长度是否符合条件
        :param s 视频长度字符串 如 06:30
        :param min 最小几分钟
        :param max 最大几分钟
        根据抖音视频页面的发布时间表示情况写的方法 判断视频长度是否符合要求： >=1min, <=6min
        """
        if (s.split(":")[0].startswith('0')):
            if (s.split(":")[0].replace('0', '') != ''):
                minute = s.split(":")[0].lstrip('0')
            else:
                minute = '0'
            if (int(minute) >= min and int(minute) <= max):
                # 符合条件
                return True
            else:
                return False
        else:
            return False

    # 处理滑块验证的方法：1 直接关闭 2 滑动验证
    def handleSlideCheck(self, cracker, *browser_lis:list):
        '''
        :params cracker 破解对象
        :params browser_lis 浏览器对象列表
        '''
        sleep(5)
        for browser in browser_lis:
            try:
                self.EffectiveCookies0 = cracker.handle_SlideCheck(browser)
            except Exception as e:
                pass
            sleep(1)

    # 滑块验证 XX 滑块验证有点问题， 手动验证吧，自动化滑块验证还做不了
    # 遇到的问题，滑块验证采用拼图的形式，需要先检验待拼的位置坐标才行
    #   抖音的验证流程， 服务器发送一个cookie s_v_web_id:Value 到客户端，客户端进行滑块验证，验证成功的话发送一个成功的请求到服务器端，服务器端对 对应s_v_web_id  做一些调整（赋予权限），客户端就能正常浏览了
    #   s_v_web_id在一次会话结束时候失效
    def checkSlide(self, browser, x):
        sleep(2)
        # 实例化鼠标操作
        action = ActionChains(browser)
        # 按住滑块
        action.click_and_hold(browser.find_element_by_xpath("//*[@class='captcha_verify_img_slide react-draggable sc-VigVT ggNWOG']")).perform()
        for i in range(x):
            action.move_by_offset(1, 0)
        sleep(2)
        # 释放滑块
        action.release().perform()
        pass

    def check_conditions_video(self, pubTime, timelength, title):
        if(self.check_publishtime_istoday(pubTime)):
            if(title.replace(' ','')!=''):
                # 是当天发布
                if(len(timelength.split(":"))>2):
                    print('视频时长太长')
                    return False
                else:
                    return True
            else:
                # 去标签后的标题为空
                print('去标签后的标题为空')
                return False
        else:
            print('非当天发布')
            return False


