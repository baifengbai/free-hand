import base64, requests
import time
from selenium.webdriver import ActionChains

from utils.base_baidu_api import Baidu_Api

class Captcha_Word_Reco(Baidu_Api):
    """
        点击验证码破解
        1. 下载图片
        2. 调用百度通用文字识别出文字的位置
        3. 点击对应位置
    """
    def __init__(self):
        self.request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
        Baidu_Api.set_APPID(22980199)
        Baidu_Api.set_API_KEY('uSfmmTPA7biAOVpTZ67ijYeM')
        Baidu_Api.set_SECRET_KEY('NbE48Agx6PUjxeb7Ul0bEppIOtVxN4pw')

    @classmethod
    def reco_by_baiduapi(cls, img_path, request_url="https://aip.baidubce.com/rest/2.0/ocr/v1/accurate"):
        # 二进制方式打开图片文件
        f = open(img_path, 'rb')
        img_target = base64.b64encode(f.read())
        params = {"image": img_target}
        access_token = cls.getAccessToken(cls.get_API_KEY(), cls.get_SECRET_KEY())
        request_url = request_url + "?access_token=" + access_token
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'recognize_granularity': 'small'
                   }

        response = requests.post(request_url, data=params, headers=headers)
        f.close()
        response = response.json()
        return response

    def get_loc(self, img_target_path, img_temp_path):
        """
        获取对应文字的位置
        :param img_target_path 待点击的文字
        :param img_temp_path   模板背景，点击位置
        :output loc_json 对应文字的位置信息
        """
        res_target = self.reco_by_baiduapi(img_path=img_target_path)
        res_temp = self.reco_by_baiduapi(img_path=img_temp_path)
        target_words = res_target['words_result'][0]['words'] # 待点击的文字
        res_loc = []
        for word in target_words:
            for temp in res_temp['words_result']:
                if(word == temp['words']):
                    res_loc.append({word: temp['location']})
                    break
        return res_loc

    # 按顺序点击文字
    def click_words(self, browser, wordsPosInfo, temp_xpath):
        # 获取模板图位置
        temp_img_Element = browser.find_element_by_xpath(temp_xpath)
        # 根据文字位置信息依次点击
        for info in wordsPosInfo:
            ActionChains(browser).move_to_element_with_offset(
                to_element=temp_img_Element, xoffset=info['location']['left'] + 20,
                yoffset=info['location']['top']+20
            ).click().perform()
            time.sleep(1)
