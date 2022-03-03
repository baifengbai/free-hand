from utils import globalTools
from utils.common import Contraler_Time, Contraler_Dir
from spider import selenium_douyin,selenium_sougou_weixin, selenium_kuaishou, selenium_douyin_stockA


class Sele_Spider_Runner:
    @classmethod
    def run_douyin(cls,proj_absPath, crawlUrl_list, origin):
        updateTime = Contraler_Time.getCurDate("%Y%m%d")
        videoDirPath = proj_absPath + '\\assets\\videos\\' + updateTime + '\\' + origin + '\\'
        coverSavedPath = proj_absPath + '\\assets\\videos\\' + updateTime + '\\cover_douyin.jpg'
        captchaPath = proj_absPath + '\\assets\\captcha\\' + updateTime + '\\' + origin + '\\'
        # 判断配置里的目录是否存在，不存在则创建对应目录
        Contraler_Dir.checkACreateDir(videoDirPath)
        Contraler_Dir.checkACreateDir(captchaPath)

        # 抖音视频的爬取及上传
        spider_douyin = selenium_douyin.Crawler_Douyin(captchaPath=captchaPath, videoDirPath=videoDirPath)
        for url in crawlUrl_list:
            video_lis = spider_douyin.get_videolis(sliderTimes=1, url_index=url)
            effective_lis = spider_douyin.handle_videolis(video_lis, videoDirPath, coverSavedPath)
        spider_douyin.videolis_browser.close()
        spider_douyin.video_browser.close()
        globalTools.finishTask()

    @classmethod
    def run_douyin_guxiaocah(cls, proj_absPath, crawlUrl_list, origin):
        updateTime = Contraler_Time.getCurDate("%Y%m%d")
        videoDirPath = proj_absPath + '\\assets\\videos\\' + updateTime + '\\' + origin + '\\'
        coverSavedPath = proj_absPath + '\\assets\\videos\\' + updateTime + '\\cover_douyin.jpg'
        captchaPath = proj_absPath + '\\assets\\captcha\\' + updateTime + '\\' + origin + '\\'
        # 判断配置里的目录是否存在，不存在则创建对应目录
        Contraler_Dir.checkACreateDir(videoDirPath)
        Contraler_Dir.checkACreateDir(captchaPath)

        # 抖音视频的爬取及上传
        spider_douyin = selenium_douyin_stockA.Crawler_Douyin(captchaPath=captchaPath, videoDirPath=videoDirPath)
        for url in crawlUrl_list:
            video_lis = spider_douyin.get_videolis(sliderTimes=1, url_index=url)
            if(video_lis):
                effective_lis = spider_douyin.handle_videolis(video_lis, videoDirPath, coverSavedPath)
            else:
                print('当前链接无符合条件的视频：', url)
        spider_douyin.videolis_browser.close()
        spider_douyin.video_browser.close()
        globalTools.finishTask()

    @classmethod
    def run_kuaishou(cls):
        # 视频的爬取上传
        kuaishou = selenium_kuaishou.Crawler_Kuaishou()
        kuaishou.run()
        globalTools.finishTask()
        del kuaishou

    @classmethod
    def run_sougou(cls):
        sougou = selenium_sougou_weixin.Crawler_Sougou()
        sougou.run()
        globalTools.finishTask()
        del sougou




