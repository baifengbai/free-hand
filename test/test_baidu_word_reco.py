"""测试百度识别图片文字"""
from core.base.cracker.base_captchaword_reco import Captcha_Word_Reco

def test_word_reco(imgsrc=r'E:\1.jpeg'):
    cwr = Captcha_Word_Reco()
    return cwr.reco_by_baiduapi(imgSrc=imgsrc)



if __name__ == '__main__':
    print("测试百度识别图片文字")
    print(test_word_reco())