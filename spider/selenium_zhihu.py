import json
from selenium import webdriver
from time import sleep
import pymysql, time, requests
from db.backends.mysql.operations import OperatorMysql
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from utils.common import Encode

class Crawler_Zhihu_Base:
    def __init__(self, url="https://www.zhihu.com/search?q=%E9%85%8D%E8%B5%84&type=content"):
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(executable_path="E:\Projects\webDriver\\chrome\\chromedriver.exe",options=option)
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
            "source":"""
                Object.defineProperty(navigator, 'webdriver), {
                    get: (): => undefined
                }
            """
        })
        self.browser.get(url)
        self.url = url
        param = {
            'USER': 'root',
            'DBNAME': 'postedurldatabase',
            'PASSWORD': 'root',
            'HOST': '',
            'PORT': '',
        }
        self.contraler_db = OperatorMysql(param)

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
        while (n <= 30):
            if ("scroll-done" in self.browser.title):
                break
            else:
                print("还没有拉到最底端...")
                sleep(3)
            n = n + 1

    # 提取视频名字的方法
    def videoNameExtract(self, videoSrc):
        return str(videoSrc).split("?")[0].split("/")[-1].replace('.mp4', '')


class Crawler_Zhihu_newest(Crawler_Zhihu_Base):
    def insert_db(self, lis, searchword):
        tag = searchword
        sql = 'INSERT INTO `data_usable_database`.`tb_zhihu_search_articleinfo` (`tag`, `article_url`, `title`, `describe`) VALUES (\'{}\',\'{}\',\'{}\',\'{}\');'
        for item in lis:
            self.contraler_db.insertData2DB(sql.format(
                tag,
                item['article_url'],
                item['title'],
                item['describe']
            ))

    def insert_db_content(self, lis, article_id):
        sql = 'INSERT INTO `data_usable_database`.`tb_zhihu_search_content` (`question_id`, `answer`, `totle_answer`) VALUES (\'{}\',\'{}\',\'{}\');'
        for item in lis:
            self.contraler_db.insertData2DB(sql.format(
                item['article_id'],
                item['content'],
                item['totle_answer']
            ))

    def filter_articleinfo_peizitaolun(self, s):
        filterword = ['配资', '股票', '炒股']
        check = False
        for word in filterword:
            if(word in s):
                check = True
                return check
        return check

    def get_search_articleinfo_result(self, searchword, lis_xpath, item_a_xpath):
        '''
            搜索关键词，获取所有搜索结果
        :param searchword 搜索关键词
        :output lis 文章信息列表
        '''
        lis = []
        time.sleep(3)
        self.pull_down()

        articles_lis = self.browser.find_elements_by_xpath(lis_xpath)
        for article in articles_lis:
            a = article.find_elements_by_xpath(item_a_xpath)
            if(len(a)==1):
                if(self.filter_articleinfo_peizitaolun(a[0].text)):
                    template = {
                        'article_url': '',
                        'title': '',
                        'describe': ''
                    }
                    template['article_url'] = a[0].get_attribute('href')
                    template['title'] = a[0].text
                    template['describe'] = ''
                    lis.append(template)
            elif(len(a)>1):
                for i in a:
                    t = i.text
                    if(t=='' or '更多' in t or '查看全部' in t or '个回答' in t or t=='场外配资' or t=='配资公司' or t=='什么是配资' or t=='配资是什么' or t=='什么是配资怎么配' or t=='配仓'):
                        continue
                    elif(self.filter_articleinfo_peizitaolun(a[0].text)):
                        template = {
                            'article_url': '',
                            'title': '',
                            'describe': ''
                        }
                        template['article_url'] = i.get_attribute('href')
                        template['title'] = i.text
                        template['describe'] = ''
                        lis.append(template)
        return lis

    def click_viewall(self):
        """查看是否有查看所有内容的按钮"""
        try:
            view_all_button = self.browser.find_element_by_xpath("//div[@class='Card ViewAll']//a")
            # 点击
            """
                注意selenium的a标签的点击方法不能直接用click() 要用send_keys方法
            """
            view_all_button.send_keys(Keys.ENTER)
        except Exception as e:
            pass

    def close_loginform(self):
        """关闭登录表单"""
        try:
            login_form = self.browser.find_element_by_xpath("//button[@class='Button Modal-closeButton Button--plain']")
            login_form.send_keys(Keys.ENTER)
        except Exception as e:
            pass


    def get_search_content_result(self, url):
        """
        获取指定知乎链接下所有回答的内容
        :output lis 回答内容的字典列表，包括url
        """
        lis = []
        if('question' in url):
            article_id = self.contraler_db.getOneDataFromDB("SELECT `id` FROM `tb_zhihu_search_articleinfo` WHERE `article_url`=\'{}\'".format(url))[0]
            self.browser.get(url)
            self.close_loginform()
            self.pull_down()
            self.click_viewall() # 点击查看更多
            self.close_loginform()
            self.pull_down()
            totle_answer = self.browser.find_element_by_xpath("//div[@class='List-header']//h4//span").text.replace(' 个回答','')
            contentslist = self.browser.find_elements_by_xpath("//div[@role='list']//div[@class='List-item']//div[@class='ContentItem AnswerItem']")
            for item in contentslist:
                template = {
                    'article_id': int(article_id),
                    'content': '',
                    'totle_answer': totle_answer
                }
                s = ''
                pList = item.find_elements_by_xpath(".//div[@class='RichContent RichContent--unescapable']//span[@class='RichText ztext CopyrightRichText-richText css-hnrfcf']//p")
                for p in pList:
                    s = s + '\n' + p.text
                template['content'] = s
                lis.append(template)
        return lis

    def run_articleInfo(self, searchword='配资'):
        # 抓取文章信息数据
        lis = self.get_search_articleinfo_result(
            searchword=searchword,
            lis_xpath="//div[@role='list']//div[@role='listitem']",
            item_a_xpath=".//a"
        )
        # 将文章数据上传到数据库
        self.insert_db(lis, searchword=searchword)
    def run_articleContent_special_qsid(self, questionId, pulldowntimes):
        url_item = self.contraler_db.getOneDataFromDB('SELECT `id`,`article_url` FROM `tb_zhihu_search_articleinfo` WHERE `id`=\'{}\';'.format(questionId))
        content_lis = self.get_search_content_result(url_item[1])
        self.insert_db_content(lis=content_lis, article_id=url_item[0])

    def run_articleContent(self, tag):
        url_lis = self.contraler_db.getAllDataFromDB('SELECT `id`,`article_url` FROM `tb_zhihu_search_articleinfo` WHERE `tag`=\'{}\';'.format(tag))
        for item in url_lis:
            content_lis = self.get_search_content_result(item[1])
            self.insert_db_content(lis=content_lis, article_id=item[0])
            time.sleep(3)

    def run_articleInfo_gupiaopeizi(self, searchword='股票配资', url='https://www.zhihu.com/topic/19958084/hot'):
        """注意： 数据库里若是知乎内容部分question_id为198之后的数据中若是有question_id<198，说明对应链接与前面重复了"""
        lis = self.get_search_articleinfo_result(
            searchword,
            lis_xpath="//div[@role='list']//div[@class='List-item TopicFeedItem']",
            item_a_xpath=".//h2//a"
        )
        self.insert_db(lis=lis,searchword=searchword)

