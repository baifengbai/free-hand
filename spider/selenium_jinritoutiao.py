from core.base.selenium.base import BaseSelenium
from contrib.poster import poster_article
import time
from middleware.cleaner.paragraph_mid import ParagraphMiddleware

class Crawler_toutiao(BaseSelenium):
    def click_chaijing(self, browser):
        caijing = browser.find_elements_by_xpath('//ul[@class="feed-default-nav"]//li[@aria-label="财经频道"]//div[@class="show-monitor"]')[1]
        self.click_element(caijing)

    def get_articleUrllist(self, browser):
        liList = browser.find_elements_by_xpath("//h2")
        urlList = []
        for li in liList:
            url = li.find_element_by_xpath(".//..").get_attribute('href') # 父节点
            try:
                publishTime = li.find_element_by_xpath(".//..//..").find_element_by_xpath(".//div[@class='feed-card-footer-time-cmp']").text
            except Exception as e:
                continue
            if(not self.check_if_todaypub(publishTime)):
                continue
            if(url not in urlList):
                urlList.append(url)
        return urlList

    def check_if_todaypub(self, s:str):
        """验证是否当天"""
        if('小时' in s):
            return True
        else:
            return False

    def filter_paragraph(self, s):
        word_lis = [
            '新闻记者 ', '责任编辑：', '图片编辑：', '校对：', '内容仅供参考', '编辑 ', '校对 ', '财经记者 ', '请私信', '编辑/', '作者：', '本文源自', '来源：',
            '版权声明', '原创', '记者：', '记者 ', '值班主任：', '值班总监：', '内容审核：', '想了解更多', '声明', '转载请注明', '编辑：', '联系我们', '欢迎关注', '版权所有',
            '来源于', '联系删除', '转载', '资料参考', '摄像：', '侵删', '仅分享', '免责声明', '文|', '编辑|', '资料：', '在评论区留言', '来源/', '微信号：'
        ]
        check = False
        for word in word_lis:
            if(word in s):
                check = True
                return check
        return check

    def get_Content(self, browser, url):
        """
            获取文章内容 包括里面的标签 之后传送前再根据需求清洗 清洗的步骤放在了这里
            文章内容里最后一张图片若出现再末尾 统一删掉
        """
        content = ''
        browser.get(url)
        title = browser.find_element_by_xpath('//h1').text
        # content = browser.find_element_by_xpath('//article').get_property("innerHTML")
        content_item_lis = browser.find_elements_by_xpath('//article/*')
        if(browser.find_elements_by_xpath("//article//table")!=[]):
            # 有表格的不要
            return (url, title, '')

        # 判断最后一个元素是否为图片，为图片则删除最后一个元素
        if(content_item_lis[-1].tag_name == 'img'):
            content_item_lis.pop(-1)
        else:
            if ('<img' in content_item_lis[-1].get_property("innerHTML")):
                content_item_lis.pop(-1)
        cleaner_Paragraph = ParagraphMiddleware()
        for item in content_item_lis:
            if(item.tag_name == 'p'):
                if(item.text!=''):
                    if(self.filter_paragraph(item.text)):
                        continue
                    content  = content + '<p>' + cleaner_Paragraph.process_operation(item.text) + '</p>'
            elif(item.tag_name == 'img'):
                content = content + '<img src=\'' + item.get_attribute('src') + '\'></img>'
            else:
                if('<p' in item.get_property("innerHTML") and '<img' in item.get_property("innerHTML")):
                    plis = item.find_elements_by_xpath(".//p")
                    s = ''
                    for pli in plis:
                        s = s + pli.text
                    content = content + '<img src=\'' + item.find_element_by_xpath(".//img").get_attribute('src') + '\'></img>'
                    if(s!=''):
                        content = content + '<p>' + cleaner_Paragraph.process_operation(s) + '</p>'
                elif('<img' in item.get_property("innerHTML")):
                    content  = content  + '<img src=\'' + item.find_element_by_xpath(".//img").get_attribute('src') + '\'></img>'
                elif('<p' in item.get_property("innerHTML")):
                    p_lis = item.find_elements_by_xpath(".//p")
                    for p_i in p_lis:
                        if(p_i.text!=''):
                            content  = content  + '<p>' + cleaner_Paragraph.process_operation(p_i.text) + '</p>'
        return (url, title, content)

    def get_articleContent(self, browser):
        urlList = self.get_articleUrllist(browser)
        articleList = []
        print('爬取今日头条文章， 符合发布时间条件的文章数量：', len(urlList))
        for url in urlList:
            time.sleep(2)
            try:
                article = self.get_Content(browser, url)
                articleList.append(article)
            except Exception as e:
                print("该链接获取文章内容失败", url)
        return articleList






