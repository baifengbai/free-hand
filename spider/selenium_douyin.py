import random
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from contrib.poster.poster_video import Poster_Video as VideoPoster
from middleware.filter.video_mid import DouyinFilter
from utils import tools
from db.backends.mysql.operations import OperatorMysql
from core.base.cracker import cracker_douyin
from core.base.download.base import BaseDownloader
from core.base.selenium.base import BaseSelenium
from .universal.special_methods_douyin import Douyin_SpecialMethod
from middleware.cleaner.title_mid import TitleMiddleware


# --------------------------- 爬取抖音视频的类 ----------------------------------
"""
    获得视频列表
    过滤视频列表
        筛选条件：
        1 判断视频时长 1~6min
        2 判断发布时间为当天
        3 标题筛选 筛掉包含过滤词的视频
        上传视频
"""
class Crawler_Douyin(
    BaseSelenium,
    Douyin_SpecialMethod
):
    def __init__(self, captchaPath, videoDirPath, chromeDriverPath=r'E:\Projects\webDriver\\chrome\\chromedriver.exe'):
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

        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证
        # 滑块验证参数
        self.captchaPath = captchaPath
        # self.roll_tobottom_method1(browser=self.videolis_browser, times=350)

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
            ul = self.videolis_browser.find_element_by_xpath("//ul[@class='fbe2b2b02040793723b452dc2de2b770-scss _924e252b5702097b657541b9e3b21448-scss']")
            liList = ul.find_elements_by_xpath("./li")
            for li in liList:
                try:
                    a = li.find_element_by_xpath(".//a[@class='caa4fd3df2607e91340989a2e41628d8-scss a074d7a61356015feb31633ad4c45f49-scss _9c976841beef15a22bcd1540d1e84c02-scss']")
                except Exception as e:
                    continue
                timeLength = li.find_element_by_xpath(".//span[@class='d170ababc38fdbf760ca677dbaa9206a-scss']").text
                publishTime = li.find_element_by_xpath(".//span[@class='b32855717201aaabd3d83c162315ff0a-scss _5b7c9df52185835724fdb7f876969abd-scss']").text
                title = TitleMiddleware.clean_douyin_method2(a.text)  # 标题过滤标签
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
        try:
            pubTime = self.video_browser.find_element_by_xpath("//span[@class='_87bab22a14dd86d6a0038ee4b3fdaea4-scss']").text.split("：")[1].split(' ')[0]
        except Exception as e:
            try:
                pubTime = self.video_browser.find_element_by_xpath("//span[@class='h7qyKhTd']").text.split("：")[1].split(' ')[0]
            except Exception as e:
                print('获取不到视频页发布日期')

        timelength = self.video_browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/xg-controls/xg-inner-controls/xg-left-grid/xg-icon[2]/span[3]').text
        if(not self.check_conditions_video(pubTime, timelength, video[0])):
            return None
        # 视频有效，获取准确的可下载的视频链接
        try:
            videoUrl = self.video_browser.find_elements_by_xpath("//video//source")
            try:
                if (len(videoUrl) > 1):
                    videoUrl = videoUrl[0].get_attribute("src")
            except Exception as e:
                videoUrl = videoUrl.get_attribute("src")
        except Exception as e:
            print('无法获取到视频源链接(用于下载)： ', video[0], ' ', video[1])
            return None
        return (video[0], video[1], video[2], videoUrl)

    def handle_videolis(self, video_lis, videoDirPath, coverSavedPath):
        poster = VideoPoster(videoDirPath=videoDirPath, coverSavedPath=coverSavedPath)
        filter_video = DouyinFilter(dirOriPath=videoDirPath)
        # 1. 过滤掉上传过的视频 去重
        if (video_lis):
            video_lis = self.filter.filter_posted(video_lis) # 过滤掉上传过的视频
            video_lis = tools.cleanRepeated(video_lis)  # 去重
        else:
            print('经过去重操作，待处理视频列表为空')
            return None
        # 2. 视频标题过滤 条件： 过滤词 时间信息
        if (video_lis):
            # 过滤标题操作
            video_lis = filter_video.filter_keywordFromTitle(video_lis)
        else:
            print('经过视频标题过滤操作，待处理视频列表为空')
            return None
        # 3. 处理单个视频 - 下载和上传
        effective_lis = []
        for video in video_lis:
            res = self.handle_single_video(video)
            if(res):
                # 视频有效 可下载上传
                i = random.randint(1,100)
                print('下载视频: ', res[0], ' ', res[3])
                BaseDownloader.downVideo(urlpath=res[3], name=str(i), dstDirPath=videoDirPath)
                print('上传视频: ', res[0], ' ', str(i) + '.mp4')
                post_res = poster.post_videoSingle(str(i) + '.mp4', title=res[0])
                print('上传结果：', post_res.text if(post_res) else post_res)
                print()
                effective_lis.append(res)
            # 更新上传过的数据库 postedurldatabase
            sql = "INSERT INTO `postedurldatabase`.`tb_video_posted` (`title`) VALUES ('{}');".format(
                video[0]
            )
            self.dboperator.insertData2DB(sql=sql)
        return effective_lis
