from basement__.ContralSelenium import Base_Selenium
from basement__.ContralerDatabase import Contraler_Database
from basement__ import Timer
from basement__.ContralSelenium import ReuseChrome
import time

def start_chrome(chromeDriverPath):
    c = Base_Selenium()
    driver = c.init_webdriver(chromeDriverPath=chromeDriverPath)
    executor = driver.command_executor._url
    session_id = driver.session_id
    print("driver executor : ", executor)
    print("driver session id: ", session_id)
    return {
        "executor": executor,
        "session_id": session_id
    }

class C(Timer.Base_Timer_0):
    def task(self):
        self.setting = self.timerConfig
        dbOperator = Contraler_Database(databaseName='data_usable_database')
        sql_get = 'SELECT * FROM `tb_selenium_info` WHERE `id`=\'1\';'
        driver_info = dbOperator.getOneDataFromDB(sql_get)
        if(driver_info[1]!=''):
            print("上一个chrome driver信息：", driver_info)
            try:
                browser_toutiao = ReuseChrome(command_executor=driver_info[1], session_id=driver_info[2])
                browser_toutiao.current_url
            except Exception as e:
                browser_toutiao = None
                dbOperator.cursor.execute(
                    "UPDATE `tb_selenium_info` SET `executor` = '', `session_id` = '' WHERE (`id` = '1');")
            if (browser_toutiao):
                while (1):
                    if (browser_toutiao.current_url != r'chrome://version/'):
                        print("browser is being using now...")
                        time.sleep(10)
                        continue
                    else:
                        time.sleep(1)
                        break
                browser_toutiao.close()
        c = Base_Selenium()
        driver = c.init_webdriver(chromeDriverPath=r'E:\Projects\webDriver\chrome\chromedriver.exe')
        driver.get('chrome://version/')
        dbOperator = Contraler_Database(databaseName='data_usable_database')
        executor = driver.command_executor._url
        session_id = driver.session_id
        sql_update = 'UPDATE `data_usable_database`.`tb_selenium_info` SET `executor` = \'{}\', `session_id` = \'{}\' WHERE (`id` = \'1\');'.format(
            executor,
            session_id
        )
        dbOperator.cursor.execute(sql_update)
        print("driver executor : ", executor)
        print("driver session id: ", session_id)

if __name__ == '__main__':
    setting = {
        "beginTime": '00:01:59',  # 注意表示 一位数字的要0开头
        "endTime": '23:59:59',
        "taskExcuteDelta": 1200,  # 任务间隔1h
        "timeExcuteDelta": 604800*100  # 定时器间隔 每个一周运行一次
    }
    m = C(
        timerConfig = setting
    )
    m.timerTaskRun()