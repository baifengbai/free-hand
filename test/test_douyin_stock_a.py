from spider__ import selenium_douyin_stockA
from basement__.ContralerTime import Contraler_Time
from basement__.ContralerDir import Contraler_Dir
from basement__ import ContralerDatabase as dbOp
from basement__.Encode import Encode
from globalTools import globalTools
import os
from basement__.Encode import Encode


def get_url():
    sql_get = 'SELECT `name`, `code` FROM `tb_namecode`;'
    contraler_db = dbOp.Contraler_Database(databaseName='stocksnamecode')
    stocks_lis = contraler_db.getAllDataFromDB(sql_get)
    stocks_lis = stocks_lis[200:]
    url_lis = []
    for item in stocks_lis:
        name = Encode.str2urlcode(item[0])
        code = item[1]
        url = 'https://www.douyin.com/search/' + code + name + '?publish_time=7&sort_type=1&source=tab_search&type=video'
        url_lis.append(url)
    contraler_db.cursor.close()
    contraler_db.conn.close()
    del contraler_db
    return url_lis

# Selenium 爬取 爬取视频源 抖音
def run_douyin_guxiaocha(proj_absPath, crawlUrl_list, origin):
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
        stock_code = url.split('search/')[-1].split('?')[0][0:6]
        stock_name = Encode.urlcode2str(url.split('search/')[-1].split('?')[0][6:])
        video_lis = spider_douyin.get_videolis(sliderTimes=1, url_index=url)
        if (video_lis):
            effective_lis = spider_douyin.handle_videolis(video_lis, videoDirPath, coverSavedPath, stock_code, stock_name)
        else:
            print('当前链接无符合条件的视频：', url)
    # spider_douyin.videolis_browser.close()
    # spider_douyin.video_browser.close()
    # globalTools.finishTask()


if __name__=='__main__':
    origin = 'douyin_guxiaocha'
    proj_absPath = os.path.abspath(os.path.dirname(__file__))
    config = {
        "beginTime": '00:01:59',  # 注意表示 一位数字的要0开头
        "endTime": '23:51:01',
        "taskExcuteDelta": 3600,  # 任务间隔1h
        "timeExcuteDelta": 43200 * 100,  # 定时器间隔 每个一天运行一次
        "whichKind": 'video',
        "tasktype": 'selenium',
        'origin': 'douyin_guxiaocha',
        "crawlMethod": 'Selenium',
        "proj_absPath": proj_absPath,  # 当前环境路径
        "crawlUrl_list": [
            "https://www.douyin.com/search/%E8%82%A1?publish_time=1&sort_type=2&source=normal_search&type=video",
            "https://www.douyin.com/search/%E8%82%A1%E7%A5%A8?publish_time=1&sort_type=2&source=normal_search&type=video",
            "https://www.douyin.com/search/%E6%B6%A8%E8%B7%8C?publish_time=1&sort_type=2&source=normal_search&type=video",
            "https://www.douyin.com/search/%E5%A4%A7%E7%9B%98?publish_time=1&sort_type=2&source=normal_search&type=video",
            "https://www.douyin.com/search/B%E8%82%A1?publish_time=1&sort_type=2&source=normal_search&type=video",
            "https://www.douyin.com/search/%E7%9F%AD%E7%BA%BF?publish_time=1&sort_type=2&source=normal_search&type=video",
            "https://www.douyin.com/search/%E6%8C%87%E6%95%B0?publish_time=1&sort_type=2&source=normal_search&type=video"
        ],
        'databaseName': 'videodatabase',
        'tableName2Clear': 'tb_douyin_videoinfo'
    }
    run_douyin_guxiaocha(proj_absPath=proj_absPath,crawlUrl_list=get_url(), origin=origin)
