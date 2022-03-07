"""
    定时器相关的基类和方法
"""
import datetime
import time
import threading
import ctypes
import inspect
from db.backends.mysql.operations import OperatorMysql
from core.base.utils.u_process import Process_Handler

# 定时任务器基类(设计多个基类)
class Base_Timer_0:
    """每隔指定间隔时间，在指定时间段内，指定时间间隔执行一次任务"""
    def __init__(self, timerConfig):
        self.timerConfig = timerConfig
        self.beginTime = self.timerConfig['beginTime']  # 定时任务每天的启动时间 例子早上8点 08:00:00
        self.endTime = self.timerConfig['endTime']  # 定时任务执行在几点之前 例子早上9点 09:00:00
        self.taskExcuteDelta = self.timerConfig['taskExcuteDelta']  # 定时任务间隔几秒执行一次
        self.timeExcuteDelta = self.timerConfig['timeExcuteDelta']

    def timer_entrance(self):
        '''
        定时器入口，设置每隔指定时间间隔，执行一次定时器
        :param
        :return
        '''
        self.timer_interval() # 入口执行一次函数，从此刻开始计时
        t = threading.Timer(self.timeExcuteDelta, self.timer_entrance)
        t.start()


    def timer_interval(self):
        '''
        定时器间隔函数 8点-9点，隔3600秒执行一次任务task
        :return:
        '''
        self.task()
        now_time = datetime.datetime.now()
        today_9 = datetime.datetime.strptime(
            str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month) + '-' + str(
                datetime.datetime.now().day) + ' ' + str(self.endTime), '%Y-%m-%d %H:%M:%S')
        # 因为定时任务会延后10秒钟执行，所以设置终止条件时，需要提前10秒钟
        if (now_time <= today_9 - datetime.timedelta(seconds=10)):
            print("当前时间 " + str(now_time) + " ,该时间在任务执行时段内，继续间隔 " + str(self.taskExcuteDelta) + " 执行任务")
            t = threading.Timer(self.taskExcuteDelta, self.timer_interval)
            t.start()
        else:
            print("当前时间 " + str(now_time) + " ,该时间不在任务执行时段内，等待 " + str(self.timeExcuteDelta) + " 后再重新开启执行任务定时器")

    def task(self):
        '''
        定时任务内容，通过继承重写
        :return:
        '''
        print(' ---------- task任务开始执行 ---------- ')
        print("本定时器未设置定时任务内容")
        time.sleep(1)
        print(' ---------- task任务执行完毕 ---------- ')

    def timerTaskRun(self):
        # 获取当前时间
        now_time = datetime.datetime.now()
        # 获取当前年月日
        now_year = now_time.year
        now_month = now_time.month
        now_day = now_time.day

        # 今天早上8点时间表示
        # today_8 = datetime.datetime.strptime(str(now_year)+'-'+str(now_month)+'-'+str(now_day)+' '+'08:00:00','%Y-%m-%d %H:%M:%S')
        today_8 = datetime.datetime.strptime(str(now_year) + '-' + str(now_month) + '-' + str(now_day) + ' ' + str(self.beginTime), '%Y-%m-%d %H:%M:%S')
        # 明天早上8点时间表示
        tomorrow_8 = datetime.datetime.strptime(str(now_year) + '-' + str(now_month) + '-' + str(now_day) + ' ' + str(self.beginTime), '%Y-%m-%d %H:%M:%S')

        # 判断当前时间是否过了今天凌晨8点,如果没过，则今天早上8点开始执行，过了则从明天早上8点开始执行，计算程序等待执行的时间
        if (now_time <= today_8):
            wait_time = (today_8 - now_time).total_seconds()
        else:
            wait_time = (tomorrow_8 - now_time).total_seconds()

        # 等待wait_time秒后（今天早上8点或明天早上8点），开启线程去执行func函数
        self.thread = threading.Timer(wait_time, self.timer_entrance)  # 当前线程
        self.thread.start()

    @classmethod
    def permanent_runner(cls, process_recordintb_id, origin, whatkind):
        """
        让定时器永久运行
        注意：要使用此方法需要让对应执行的爬虫项目文件在启动后 在对应数据表里对应记录更新pid值
        :param process_recordintb_id 数据库表里面对应的id编号，以获取对应的pid
        :param origin 站点名
        :param whatkind 爬虫还是上传器
        """
        while(True):
            param = {
                'USER': 'root',
                'DBNAME': 'resourcedatabase',
                'PASSWORD': 'root',
                'HOST': '',
                'PORT': '',
            }
            cdb = OperatorMysql(param)
            command = cdb.getOneDataFromDB('SELECT `execute_command` FROM `tb_process_info` WHERE `id` = {};'.format(str(process_recordintb_id)))
            pid = cdb.getOneDataFromDB('SELECT `pid` FROM `tb_process_info` WHERE `id` = 2;')
            if (not Process_Handler.check_if_alive(pid=pid[0])):
                print('{}{}停止了，重启{}{}'.format(origin, whatkind,origin, whatkind))
                Process_Handler.start_process(command[0])
            else:
                print('{}运行良好'.format(origin, whatkind))
            time.sleep(5)


# 结束线程的类没有用到
class StopThread():
    '''结束线程的类'''
    def _async_raise(self,tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if(not inspect.isclass(exctype)):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if(res == 0):
            raise ValueError("invalid thread id")
        elif(res != 1):
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    # 任务自动执行结束 结束本线程实例，在调用本方法之前得先调用 timedTaskRun()
    def stopCurThread(self, thread):
        self._async_raise(thread.ident, SystemExit)
