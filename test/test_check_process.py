import time
from core.base.utils.u_process import Process_Handler
from basement__.ContralerDatabase import Contraler_Database

if __name__=='__main__':
    """�������Ƿ������У������̽�������������"""
    while(1):
        cdb = Contraler_Database('resourcedatabase')
        command = cdb.getOneDataFromDB('SELECT `execute_command` FROM `tb_process_info` WHERE `id` = 2;')
        pid = cdb.getOneDataFromDB('SELECT `pid` FROM `tb_process_info` WHERE `id` = 2;')
        if(not Process_Handler.check_if_alive(pid=pid[0])):
            print('����ֹͣ�ˣ�������������')
            Process_Handler.start_process(command[0])
        else:
            print('������������')
        time.sleep(5)