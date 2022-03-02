import threading

import psutil
import os

class Process_Handler:
    """
    思路：
        设置好数据库中每条记录对应的 task_type execute_command
        从数据库表中获取 pid、 execute_command
        判断pid是否在运行，若运行则等待一段时间再判断
        否则执行execute_command命令， 更新数据库中对应的pid字段 继续等待一段时间判断
    """
    @staticmethod
    def check_if_alive(pid:int):
        """
        判断进程是否在运行
        :param pid 进程编号 通过 os.getpit()获取
        """
        pid_alive_lis = psutil.pids()
        if(pid in pid_alive_lis):
            return True
        else:
            return False

    @staticmethod
    def start_process(command:str):
        """
        运行指定路径python文件
        """
        os.system(command)
    @staticmethod
    def kill_process(pid:int):
        """
        杀死进程
        :param pid 进程pid
        """
        if(os.name=='nt'):
            # Windows系统
            cmd = 'taskkill /pid ' + str(pid) + ' /f'
            try:
                os.system(cmd)
                print(pid, 'killed')
            except Exception as e:
                print(e)
        elif(os.name == 'posix'):
            # Linux 系统
            cmd = 'kill' + str(pid)
            try:
                os.system(cmd)
                print(pid, 'killed')
            except Exception as e:
                print(e)
        else:
            print('Undefined os.name')

    threading.Thread.join()