import requests

class Baidu_Api:
    __APP_ID = '24654559'
    __API_KEY = 'Pnexi1A99Eobsb1iX7xiBTsE'
    __SECRET_KEY = 'qYYXNhsGLrnAwAWkmHPFOEofQHPRqSYL'

    # 获取accessToken的方法
    @staticmethod
    def getAccessToken(AK, SK):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(AK, SK)
        response = requests.get(host)
        if response:
            return response.json()['access_token']

    @classmethod
    def set_APPID(cls, appid):
        cls.__APP_ID = appid

    @classmethod
    def set_API_KEY(cls, api_key):
        cls.__API_KEY = api_key

    @classmethod
    def set_SECRET_KEY(cls, secret_key):
        cls.__SECRET_KEY = secret_key

    @classmethod
    def get_APPID(cls):
        return cls.__APP_ID

    @classmethod
    def get_API_KEY(cls):
        return cls.__API_KEY

    @classmethod
    def get_SECRET_KEY(cls):
        return cls.__SECRET_KEY
