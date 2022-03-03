import random
import time
from time import sleep
from contrib.poster.poster_video import Poster_Video as VideoPoster
from middleware.filter.video_mid import DouyinFilter
from utils import tools
from db.backends.mysql.operations import OperatorMysql
from core.base.selenium.base import BaseSelenium
from core.base.cracker import cracker_douyin
from core.base.download.base import BaseDownloader
from .universal.special_methods_douyin import Douyin_SpecialMethod

# --------------------------- 爬取抖音视频的类 ----------------------------------
"""
    要求： 爬取抖音上所有a股股票得视频。按照最多点赞，一周内得爬取。
        a股股票定时更新数据库。
        然后按照 股票代码和股票名字 合起来 搜索  :  688019安集科技
    过滤视频列表
        筛选条件：
            判断视频时长 1~6min
            必须包含 #财经 这个标签 没有得 都过滤
    上传视频
"""
class Crawler_Douyin(
    BaseSelenium,
    Douyin_SpecialMethod
):
    def __init__(self, captchaPath, videoDirPath, chromeDriverPath=r'E:\Projects\webDriver\\chrome\\chromedriver.exe'):
        self.chromeDriverPath = chromeDriverPath
        param = {
            'USER': 'root',
            'DBNAME': 'postedurldatabase',
            'PASSWORD': 'root',
            'HOST': '',
            'PORT': '',
        }
        self.dboperator = OperatorMysql(param)
        self.filter = DouyinFilter(dirOriPath=videoDirPath)
        self.videolis_browser = self.init_webdriver(chromeDriverPath)
        self.video_browser = self.init_webdriver(chromeDriverPath)
        self.videolis_browser.get('https://www.douyin.com')
        self.video_browser.get('https://www.douyin.com')
        sleep(2)
        self.cracker = cracker_douyin.DouyinCrack(captchaDstDirPath=captchaPath)
        sleep(2)

        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser)  # 滑块验证
        # 滑块验证参数
        self.captchaPath = captchaPath
        # self.roll_tobottom_method1(browser=self.videolis_browser, times=350)

    def filter_regulation(self, title):
        if('#财经' not in title or '股票' not in title):
            return False
        else:
            return True

    # 首次进入 move2BottomTimes 为向下滑动的次数 默认350
    def get_videolis(self, sliderTimes, url_index):
        """
        获取符合条件 时间长度在 1-6min 之间的视频信息（title,url, publishtime）
        :param sliderTimes 向下滑动的距离
        :parma url_index 待爬取链接
        """
        self.videolis_browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defneProperty(navigator, "webdriver", {get: () => undefined})'
        })
        self.videolis_browser.get(url_index)
        # 滑块验证
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证

        # 2.通过浏览器向服务器发送URL请求
        self.videolis_browser.get(url_index)
        # 滑块验证
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证

        # 等待某个元素是否出现
        # WebDriverWait(self.videolis_browser, 10).until(
        #     # EC.text_to_be_present_in_element((By.XPATH, ''))
        #     EC.presence_of_element_located((By.XPATH, "//ul[@class='_3636d166d0756b63d5645bcd4b9bcac4-scss']"))
        # )
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证
        liEffectiveList = []  # 可上传的视频信息列表
        # 滑块验证
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证
        # 向下滚动
        self.roll_tobottom_method1(browser=self.videolis_browser, times=sliderTimes)
        try:
            # 1. 获取视频信息列表
            ul = self.videolis_browser.find_element_by_xpath("//ul[@class='qrvPn3bC H2eeMN3S']")
            liList = ul.find_elements_by_xpath("./li")
            for li in liList:
                try:
                    a = li.find_element_by_xpath(".//a[@class='B3AsdZT9 yf0WMGW6 OuiStkZo']")
                except Exception as e:
                    continue
                timeLength = li.find_element_by_xpath(".//span[@class='uK7yEPTZ']").text
                publishTime = li.find_element_by_xpath(".//span[@class='uPLxyScW yJE4WUkV']").text
                title = a.text
                """针对guxiaocha平台新增的筛选条件"""
                if(not self.filter_regulation(title)):
                    continue
                videoPageUrl = a.get_attribute("href")
                if (self.check_timelength_between(timeLength)):
                    liEffectiveList.append((title, videoPageUrl, publishTime))
                else:
                    continue
        except Exception as e:
            print('获取不到视频信息列表')
        return liEffectiveList

    def handle_single_video(self, video):
        # 2.通过浏览器向服务器发送URL请求
        self.video_browser.get(video[1])
        # 滑块验证
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证
        self.video_browser.get(video[1])
        sleep(5)
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证

        # 获取发布时间，判断发布时间是否是当天，是的话才进行下一步操作，不是的话跳出循环进入下一个循环
        # try:
        #     pubTime = self.video_browser.find_element_by_xpath("//span[@class='_87bab22a14dd86d6a0038ee4b3fdaea4-scss']").text.split("：")[1].split(' ')[0]
        # except Exception as e:
        #     try:
        #         pubTime = self.video_browser.find_element_by_xpath("//span[@class='h7qyKhTd']").text.split("：")[1].split(' ')[0]
        #     except Exception as e:
        #         print('获取不到视频页发布日期')

        # timelength = self.video_browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/xg-controls/xg-inner-controls/xg-left-grid/xg-icon[2]/span[3]').text
        # if(not self.check_conditions_video(pubTime, timelength, video[0])):
        #     return None
        # 视频有效，获取准确的可下载的视频链接
        time.sleep(2)
        videoUrl = self.video_browser.find_elements_by_xpath("//video//source")
        if (videoUrl):
            videoUrl = videoUrl[0].get_attribute("src")
        else:
            # 针对douyin 通过blob方式传输视频的处理
            print('当前链接的视频通过blob传输')
            self.temp_driver = self.init_webdriver(self.chromeDriverPath, True)
            self.temp_driver.get(video[1])
            time.sleep(2)
            try:
                videoUrl = self.temp_driver.find_elements_by_xpath("//video")[0].get_attribute("src")
                self.temp_driver.close()
            except Exception as e:
                print('无法获取到视频源链接(用于下载)： ', video[0], ' ', video[1])
                return None
        return (video[0], video[1], video[2], videoUrl)

    def handle_videolis(self, video_lis, videoDirPath, coverSavedPath, stock_code, stock_name):
        poster = VideoPoster(videoDirPath=videoDirPath, coverSavedPath=coverSavedPath, interface='https://www.guxiaocha.com/api/video_upload')
        filter_video = DouyinFilter(dirOriPath=videoDirPath)
        # 1. 过滤掉上传过的视频 去重
        if (video_lis):
            video_lis = self.filter.filter_posted(video_lis)  # 过滤掉上传过的视频
            video_lis = tools.cleanRepeated(video_lis)  # 去重
        else:
            print('经过去重操作，待处理视频列表为空')
            return None
        # 2. 视频标题过滤 条件： 过滤词 时间信息
        # if (video_lis):
        #     # 过滤标题操作
        #     video_lis = filter_video.filter_keywordFromTitle(video_lis)
        # else:
        #     print('经过视频标题过滤操作，待处理视频列表为空')
        #     return None
        # 3. 处理单个视频 - 下载和上传
        effective_lis = []
        for video in video_lis:
            res = self.handle_single_video(video)
            if (res):
                # 视频有效 可下载上传
                i = random.randint(1, 100)
                if(res[3] == []):
                    print("res[3] == []: ", res)
                print('下载视频: ', res[0], ' ', res[3])
                BaseDownloader.downVideo(urlpath=res[3], name=str(i), dstDirPath=videoDirPath)
                print('上传视频: ', res[0], ' ', str(i) + '.mp4')
                if(res[0].split('#')[0]!=''):
                    title = res[0].split('#')[0] + " #财经"
                else:
                    title = res[0].split('#')[1] + " #财经"
                post_res = poster.post_videoSingle(str(i) + '.mp4', title=title, stock_code=stock_code, stock_name=stock_name)
                print('上传结果：', post_res.text if (post_res) else post_res)
                print()
                effective_lis.append(res)
            # 更新上传过的数据库 postedurldatabase
            sql = "INSERT INTO `postedurldatabase`.`tb_video_posted` (`title`) VALUES ('{}');".format(
                video[0]
            )
            self.dboperator.insertData2DB(sql=sql)
        return effective_lis


