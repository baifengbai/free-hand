import time
from core.base.utils.u_process import Process_Handler
from basement__.ContralerDatabase import Contraler_Database

if __name__=='__main__':
    """检查进程是否还在运行，若进程结束则重启进程"""
    while(1):
        cdb = Contraler_Database('resourcedatabase')
        command = cdb.getOneDataFromDB('SELECT `execute_command` FROM `tb_process_info` WHERE `id` = 2;')
        pid = cdb.getOneDataFromDB('SELECT `pid` FROM `tb_process_info` WHERE `id` = 2;')
        if(not Process_Handler.check_if_alive(pid=pid[0])):
            print('抖音停止了，重启抖音爬虫')
            Process_Handler.start_process(command[0])
        else:
            print('抖音还在运行')
        time.sleep(5)