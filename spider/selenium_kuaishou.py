import json

from selenium import webdriver
from time import sleep
import pymysql, time, requests
from contrib.poster.poster_video import Poster_Video as VideoPoster
from middleware.filter.video_mid import KuaishouFilter
from db.backends.mysql.operations import OperatorMysql
from fake_useragent import UserAgent
from utils.common import Encode
from middleware.cleaner import title_mid



# 已有链接下载的方法
def downVideo(urlpath, name, dstDirPath):
    # 获取当前日期
    r = requests.get(urlpath, verify=False)
    video = r.content       #响应的二进制文件
    print(name)
    with open(dstDirPath + str(name) + '.mp4','wb') as f:     #二进制写入
        f.write(video)
    r.close()   # 关闭很重要，确保不要过多的连接


class Crawler_Kuaishou_Base:
    def __init__(self, url="https://www.kuaishou.com/search/video?searchKey=%E8%82%A1"):
        self.filter = KuaishouFilter(dirOriPath="E:\Projects\\4spideWeb\\tutorial\\videoDownload\\")
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(executable_path="E:\Projects\webDriver\\chrome\\chromedriver.exe",options=option)
        self.browser.get(url)
        self.url = url
        param = {
            'USER': 'root',
            'DBNAME': 'videodatabase',
            'PASSWORD': 'root',
            'HOST': '',
            'PORT': '',
        }
        self.contraler_db = OperatorMysql(param)
        # 登陆验证的
        self.browser.add_cookie({
            "domain": ".kuaishou.com",
            "name": "userId",
            "value": "2560728971",
            "path": '/',
            "expires": None
        })
        # 滑块验证的
        self.browser.add_cookie({
            "domain": ".kuaishou.com",
            "name": "did",
            "value": "web_dd4765fe13d667c461fd6269a10ae0df",
            "path": '/',
            "expires": None
        })
        self.browser.add_cookie({
            "domain": ".www.kuaishou.com",
            "name": "kpf",
            "value": "PC_WEB",
            "path": '/',
            "expires": None
        })
        self.browser.add_cookie({
            "domain": ".www.kuaishou.com",
            "name": "kpn",
            "value": "KUAISHOU_VISION",
            "path": '/',
            "expires": None
        })
        self.browser.add_cookie({
            "domain": ".kuaishou.com",
            "name": "clientid",
            "value": "3",
            "path": '/',
            "expires": None
        })
        self.browser.add_cookie({
            "domain": ".kuaishou.com",
            "name": "client_key",
            "value": "65890b29",
            "path": '/',
            "expires": None
        })
        self.browser.add_cookie({
            "domain": ".kuaishou.com",
            "name": "kuaishou.server.web_ph",
            "value": "f026d92ae2b0265bf86ec666fa786f635d5b",
            "path": '/',
            "expires": None
        })
        self.browser.add_cookie({
            "domain": ".kuaishou.com",
            "name": "kuaishou.server.web_st",
            "value": "ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABWHDql4qaYN0DtvJlDUI2vX9v2hDjf2eJUChEjJHM9YZiNRQRhDkcURY8NFHcPTyo3KaaN9tV-q9kFdDhaa6sLjoDSmhK5UjN2byF-eFVit8lfNtBhKzJ-dtvFTmsotI8eHddsdCisokwNMCBCXzdiwA7fmnM7SKqP3qEsXkJsOZJlJ1-CAUQSCJwVaVaU3SvYCeGb3Vi9BVfw0RtpgCzexoS8JByODRPv5hk-B95zTquvFHcIiCS6UA7jHPQUTMshtZGa63oO8ZPkqrI5c9ylvllsQswiCgFMAE",
            "path": '/',
            "expires": None
        })
        self.poster = VideoPoster(videoDirPath='E:\\test\\', coverSavedPath='E:\\test_kuaishou.png')
        print("请先登陆")

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

    def pull_down(self):
        """下拉到底"""
        # 下拉到底
        # js = "var q=document.documentElement.scrollTop=20000"
        self.browser.execute_script("""
                        (function () {
                        var y = 0;
                        var step = 100;
                        window.scroll(0, 0);
                        function f() {
                        if (y < document.body.scrollHeight) {
                        y += step;
                        window.scroll(0, y);
                        setTimeout(f, 100);
                        } else {
                        window.scroll(0, 0);
                            document.title += "scroll-done";
                        }
                        }
                        setTimeout(f, 1000);
                        })();
                        """)
        print("下拉中...")
        time.sleep(2)
        # while (True):
        #     if ("scroll-done" in self.browser.title):
        #         break
        #     else:
        #         print("还没有拉到最底端...")
        #         sleep(3)
        n = 0
        while (n <= 10):
            if ("scroll-done" in self.browser.title):
                break
            else:
                print("还没有拉到最底端...")
                sleep(3)
            n = n + 1

    # 提取视频名字的方法
    def videoNameExtract(self, videoSrc):
        return str(videoSrc).split("?")[0].split("/")[-1].replace('.mp4', '')


class Crawler_Kuaishou_newest(Crawler_Kuaishou_Base):
    def update_db(self, lis, searchword):
        for item in lis:
            authorid = item['author']['id']
            author_index = 'https://www.kuaishou.com/profile/' + authorid
            authorname = item['author']['name']
            sql = 'INSERT INTO `videodatabase`.`tb_kuaishou_author` (`name`, `index_url`, `seardword`) VALUES (\'{}\', \'{}\', \'{}\');'.format(
                authorname, author_index, searchword
            )
            if(self.contraler_db.getOneDataFromDB('SELECT * FROM `videodatabase`.`tb_kuaishou_author` WHERE `index_url`=\'{}\''.format(author_index))):
                continue
            self.contraler_db.insertData2DB(sql)


    def get_author_from_api(self, searchword, pcursor, url_api):
        searchword_urlcode = Encode.str2urlcode(searchword)
        cookies = self.getCookies(self.browser)
        headers = headers = {
            'Host': 'www.kuaishou.com',
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'accept': '*/*',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'content-type': 'application/json',
            'Origin': 'https://www.kuaishou.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        headers['Referer'] = 'https://www.kuaishou.com/search/video?searchKey={}'.format(searchword_urlcode)
        headers['User-Agent'] = UserAgent().random
        data = {
            "operationName": "visionSearchPhoto",
            "variables": {
                "keyword": "股",
                "pcursor": "",
                "page": "search"
            },
            "query": """query visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {
        					visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {
        						result
        						llsid
        						webPageArea
        						feeds {
        							type
        							author {
        								id
        								name
        								following
        								headerUrl
        								headerUrls {
        									cdn
        									url
        									__typename
        								}
        								__typename
        							}
        							tags {
        								type
        								name
        								__typename
        							}
        							photo {
        								id
        								duration
        								caption
        								likeCount
        								realLikeCount
        								coverUrl
        								photoUrl
        								liked
        								timestamp
        								expTag
        								coverUrls {
        									cdn
        									url
        									__typename
        								}
        								photoUrls {
        									cdn
        									url
        									__typename
        								}
        								animatedCoverUrl
        								stereoType
        								videoRatio
        								__typename
        							}
        							canAddComment
        							currentPcursor
        							llsid
        							status
        							__typename
        						}
        						searchSessionId
        						pcursor
        						aladdinBanner {
        							imgUrl
        							link
        							__typename
        						}
        						__typename
        					}
        				}"""
        }
        # 两次请求页面
        # 关键参数的配置
        data['variables']['keyword'] = searchword
        data['variables']['pcursor'] = str(pcursor)
        data_json = json.dumps(data)
        res = requests.post(url=url_api, headers=headers, cookies=cookies, data=data_json)
        return res


    def get_all_authorId(self, searchword, url_api):
        res0 = self.get_author_from_api(searchword=searchword, pcursor='',url_api=url_api)
        authors0 = res0.json()['data']['visionSearchPhoto']['feeds']
        # 关键参数的配置
        res1 = self.get_author_from_api(searchword=searchword, pcursor='1',url_api=url_api)
        authors1 = res1.json()['data']['visionSearchPhoto']['feeds']
        self.update_db(authors0, searchword=searchword)
        self.update_db(authors1, searchword=searchword)

        authorId_list = []
        for item in authors0:
            if(item not in authorId_list):
                authorId_list.append(item['author']['id'])

        for item in authors1:
            if (item not in authorId_list):
                authorId_list.append(item['author']['id'])
        return authorId_list

    # 获取clientCacheKey
    def get_videoPageUrlList(self, srcList):
        clientCacheKeyList = []
        videoPageUrlList = []
        for src in srcList:
            if ('clientCacheKey' in src):
                clientCacheKey = str(src).split("//")[1].split("clientCacheKey=")[1].split(".")[0]
                if (clientCacheKey not in clientCacheKeyList):
                    # 插入数据库操作
                    sql = "INSERT INTO `videodatabase`.`tb_kuaishou_resource` (`clientCacheKey`) VALUES (\'{}\');".format(clientCacheKey)
                    self.contraler_db.insertData2DB(sql=sql)
                    clientCacheKeyList.append(clientCacheKey)
            else:
                continue
        for item in clientCacheKeyList:
            videoPageUrl = 'https://www.kuaishou.com/short-video/' + item
            videoPageUrlList.append(videoPageUrl)
        return videoPageUrlList

    # 已经获取了clientCacheKey，下面这个方法已经不用了
    def crawlImgSrc(self, url):
        self.browser.get(url)
        sleep(3)
        # self.pull_down()    # 下拉
        videoImgList = self.browser.find_elements_by_xpath("//div[@class='video-card-main']//div[@class='card-link']/div[@class='poster']/img[@class='poster-img']")
        # 只看前10个视频
        videoImgList = videoImgList[:6]
        clientCacheListOrigin = []
        for item in videoImgList:
            clientCacheListOrigin.append(item.get_attribute('src'))
        return clientCacheListOrigin


    def getVideoListInfoByList(self,lis):
        videosInfoList = []
        for src in lis:
            videoInfo = self.getSingleVideoInfo(src)
            if(videoInfo):
                # 进入这里说明是视频是当天发布的，可以下载
                sql = "INSERT INTO `videodatabase`.`tb_kuaishou_videoinfo` (`title`, `author`, `time`, `videoSrc`, `videoName`) VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');".format(
                    videoInfo["videoTitle"],
                    videoInfo["author"],
                    videoInfo["publishTime"],
                    videoInfo["videoSrc"],
                    videoInfo["videoName"]
                )
                self.contraler_db.insertData2DB(sql)
                videosInfoList.append(videoInfo)
        return videosInfoList

    # 获取视频
    def getSingleVideoInfo(self, src):
        self.browser.get(src)
        sleep(4)
        # 获取视频信息
        try:
            # publishTime = self.browser.find_element_by_xpath("//div[@class='short-video-info']//div[@class='title-warp']//span[@class='photo-time']").text
            publishTime = self.browser.find_element_by_xpath("//span[@class='photo-time']").text
        except Exception as e:
            # publishTime = '小时'
            print(src, '有问题')

        videoInfo = {}
        if (self.filter.checkIfCurDatePub_kuaishou(publishTime)):
            time.sleep(2)
            # 进入这里说明是当天发布的
            author = self.browser.find_element_by_xpath(
                "//div[@class='short-video-info']//div[@class='title-warp']//span[@class='profile-user-name-title']").text
            videoTitle = self.browser.find_element_by_xpath("//div[@class='short-video-info-container-detail']/p").text
            videoSrc = self.browser.find_element_by_xpath("//video").get_attribute("src")
            videoName = self.videoNameExtract(videoSrc)
            videoInfo = {
                "author": author,
                "publishTime": publishTime,
                "videoTitle": videoTitle,
                "videoSrc": videoSrc,
                "videoName": videoName
            }
        return videoInfo

    def run(self, searchword='股票'):
        # 1 爬取搜索关键词视频下所有作者的id
        authorId_list = self.get_all_authorId(searchword=searchword, url_api='https://www.kuaishou.com/graphql')
        print("总共有作者数： ", len(authorId_list))
        self.authorId_list = authorId_list
        # 2 for循环 进入每个作者的首页，获取当天视频
        for authorId in authorId_list:
            author_index = 'https://www.kuaishou.com/profile/' + authorId
            clientCacheListOrigin = self.crawlImgSrc(author_index)
            # 处理爬取到的Src
            videoPageUrlList = self.get_videoPageUrlList(clientCacheListOrigin)
            videosInfoList = self.getVideoListInfoByList(videoPageUrlList)
            for videoInfo in videosInfoList:
                # 下载视频并上传
                downVideo(urlpath=videoInfo['videoSrc'], name=videoInfo['videoName'], dstDirPath='E:\\test\\')
                if(self.filter.filter_keyword_title(videoInfo['videoTitle'])):
                    # 说明含有相关过滤词，跳过
                    print("标题含过滤词，过滤： ", videoInfo)
                    continue
                # 清洗标题
                videoInfo["videoTitle"] = title_mid.TitleMiddleware.clean_douyin_method2(videoInfo["videoTitle"])
                if(videoInfo["videoTitle"].replace(' ','')==''):
                    continue
                res = self.poster.post_videoSingle(videoInfo['videoName'] + '.mp4', title0=videoInfo["videoTitle"])
        self.browser.close()
        return authorId_list
