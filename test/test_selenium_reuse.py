from basement__.ContralSelenium import ReuseChrome
from basement__.ContralerDatabase import Contraler_Database
setting = {

}

dbOperator = Contraler_Database(databaseName='data_usable_database')
sql_get = 'SELECT * FROM `tb_selenium_info` WHERE `id`=\'1\';'
driver_info = dbOperator.getOneDataFromDB(sql_get)
browser_toutiao = ReuseChrome(command_executor=driver_info[1], session_id=driver_info[2])
browser_toutiao.refresh()
# driver_reuse = ReuseChrome(command_executor=setting['command_executor'], session_id=setting['session_id'])