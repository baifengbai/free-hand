from core.base.selenium.base import BaseSelenium
from selenium import webdriver
import string
import zipfile

class Contraler_Selenium(BaseSelenium):
    """定制Selenium特定功能"""
    def add_agent(self, proxyHost="u7125.5.tp.16yun.cn", proxyPort= "6445", proxyUser="16OINIUS", proxyPass= "971935", plugin_path_dir='E:/yiniuyun/', browser_driver_path="E:\Projects\webDriver\\chrome\\chromedriver.exe"):
        """
        创建添加爬虫代理的browser 此处采用的爬虫代理使用代码来源于 亿牛云
        """
        def create_proxy_auth_extension(proxyHost, proxyPort, proxyUser, proxyPass, scheme='http', plugin_path=None, plugin_path_dir=plugin_path_dir):
            if plugin_path is None:
                plugin_path = plugin_path_dir + 'tmp/{}_{}@t.16yun.zip'.format(proxyUser, proxyPass)

            manifest_json = """
                        {
                            "version": "1.0.0",
                            "manifest_version": 2,
                            "name": "16YUN Proxy",
                            "permissions": [
                                "proxy",
                                "tabs",
                                "unlimitedStorage",
                                "storage",
                                "<all_urls>",
                                "webRequest",
                                "webRequestBlocking"
                            ],
                            "background": {
                                "scripts": ["background.js"]
                            },
                            "minimum_chrome_version":"22.0.0"
                        }
                        """

            background_js = string.Template(
                """
                var config = {
                    mode: "fixed_servers",
                    rules: {
                        singleProxy: {
                            scheme: "${scheme}",
                            host: "${host}",
                            port: parseInt(${port})
                        },
                        bypassList: ["localhost"]
                    }
                  };

                chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: "${username}",
                            password: "${password}"
                        }
                    };
                }

                chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
                );
                """
            ).substitute(
                host=proxyHost,
                port=proxyPort,
                username=proxyUser,
                password=proxyPass,
                scheme=scheme,
            )
            with zipfile.ZipFile(plugin_path, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            return plugin_path

        proxy_auth_plugin_path = create_proxy_auth_extension(
            proxyHost=proxyHost, proxyPort=proxyPort, proxyUser=proxyUser, proxyPass=proxyPass
        )
        option = webdriver.ChromeOptions()
        # 如报错 chrome-extensions
        # option.add_argument("--disable-extensions")
        option.add_extension(proxy_auth_plugin_path)
        # 关闭webdriver的一些标志
        # option.add_experimental_option('excludeSwitches', ['enable-automation'])
        browser = webdriver.Chrome(
            chrome_options=option,
            executable_path=browser_driver_path
        )
        return browser

    def test_agent(self, browser):
        """测试爬虫代理ip 输出ip地址"""
        return browser.get('http://httpbin.org/ip')

    def run(self):
        self.browser = self.add_agent(proxyHost="u7125.5.tp.16yun.cn", proxyPort= "6445", proxyUser="16OINIUS", proxyPass= "971935", browser_driver_path="E:\Projects\webDriver\\chrome\\chromedriver.exe")