from core.base.cracker.base_slidercrack import Base_Slidercrack
import time

class Slidercheck_Toutiao(Base_Slidercrack):
    def __init__(self, captchaDstDirPath, driverPath='E:\Projects\webDriver\chrome\\chromedriver.exe'):
        Base_Slidercrack.__init__(self, driverPath=driverPath)
        self.captchaDstDirPath = captchaDstDirPath  # 滑块验证图片保存的路径

    def get_selector(self, *browser):
        if (browser == ()):
                # 无指定浏览器
                self.sliderTargetSelector = self.browser.find_element_by_xpath("//div[@class='captcha_verify_container style__CaptchaWrapper-sc-1gpeoge-0 zGYIR']//img[@id='captcha-verify-image']")  # 背景
                self.sliderTemplateSelector = self.browser.find_element_by_xpath(
                    "//img[@class='captcha_verify_img_slide react-draggable sc-VigVT ggNWOG']"
                )  # 滑块
        else:
                self.sliderTargetSelector = browser[0].find_element_by_xpath("//div[@class='captcha_verify_container style__CaptchaWrapper-sc-1gpeoge-0 zGYIR']//img[@id='captcha-verify-image']")  # 背景
                self.sliderTemplateSelector = browser[0].find_element_by_xpath(
                    "//img[@class='captcha_verify_img_slide react-draggable sc-VigVT ggNWOG']"
                )  # 滑块

    def handle_SlideCheck(self, *browser):
        '''
            处理指定browser的头条滑块验证
        :param browser: 指定的browser
        :return:
        '''
        while(1):
            if (browser == ()):
                self.get_selector()
                # 无指定浏览器
                targetWidth = self.download_slideImgs(self.browser)  # 滑块图片下载器 返回目标网页显示的宽
                movement = self.getMovement_sliderCheck_method1(
                    self.captchaDstDirPath + 'template.png',
                    self.captchaDstDirPath + 'target.png',
                    targetWidth
                )  # 验证码处理器
                print("滑动的实际距离：", movement)
                # 滑动滑块
                # self.move_sliderTemplate(int(movement), self.sliderTemplateSelector)
                self.move_sliderTemplate_likeHuman(int(movement), templateSelector=self.sliderTemplateSelector)
            else:
                self.get_selector(browser[0])
                targetWidth = self.download_slideImgs(browser)  # 滑块图片下载器 返回目标网页显示的宽
                movement = self.getMovement_sliderCheck_method1(
                    self.captchaDstDirPath + 'template.png',
                    self.captchaDstDirPath + 'target.png',
                    targetWidth
                )
                print("滑动的实际距离：", movement)
                # 滑动滑块
                # self.move_sliderTemplate(int(movement))
                self.move_sliderTemplate_likeHuman(int(movement), browser[0], templateSelector=self.sliderTemplateSelector)

            # 滑完一会查看是否需要验证，不需要则滑块验证通过，否则重新执行该方法
            time.sleep(2)
            try:
                if (browser == ()):
                    # 无指定浏览器
                    sliderTargetSelector = self.browser.find_element_by_xpath("//div[@class='captcha_verify_container style__CaptchaWrapper-sc-1gpeoge-0 zGYIR']//img[@id='captcha-verify-image']']")  # 背景
                else:
                    sliderTargetSelector = browser.find_element_by_xpath("//div[@class='captcha_verify_container style__CaptchaWrapper-sc-1gpeoge-0 zGYIR']//img[@id='captcha-verify-image']")  # 背景

            except Exception as e:
                print("验证通过")
                break
            # 验证通过后输出cookie
        return self.get_Obj_allCookies()

    def download_slideImgs(self, *browser):
        '''
        下载滑块以及滑块背景用于识别位置
        :return: targetWidth 背景图在网页中的宽度 用于步长计算
        '''

            # 背景 target
            # 滑块 template
        try:
            targetImgUrl = self.sliderTargetSelector.get_attribute('src')  # 背景图url
            templateImgUrl = self.sliderTemplateSelector.get_attribute('src')  # 滑块url
            targetWidth = self.sliderTargetSelector.size['width']  # 背景图片宽
            templateWidth = self.sliderTemplateSelector.size['width']  # 滑块宽
            # 下载模板图片——滑块
            dstDirPath = self.captchaDstDirPath
            self.downloader.download_img(templateImgUrl, 'template', dstDirPath)
            # 下载背景图片
            self.downloader.download_img(targetImgUrl, 'target', dstDirPath)
            return targetWidth

        except Exception as e:
            print("无滑块出现，下载失败请刷新浏览器重新操作")
            return ''


    '''头条的滑块验证功能'''
    def slidecrack_run(self):
        '''
        :param browser 待操作的浏览器
        :param saved_path 图片保存的路径
        '''
        time.sleep(3)
        # 获取滑块
        self.get_selector()
        # 移动滑块
        self.handle_SlideCheck()

