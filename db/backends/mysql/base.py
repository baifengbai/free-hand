from conf import setting
import pymysql

class BaseDatabase:
    """数据库连接基类 默认连接配置文件中的数据库"""
    def __init__(self):
        self.connection = None
        self._cur_conn_params = self.get_connection_params()
        self.connect(self._cur_conn_params)
        self.cursor = self.get_cursor()

    @property
    def cur_conn_params(self):
        """当前数据库连接的参数"""
        return self._cur_conn_params

    @cur_conn_params.setter
    def cur_conn_params(self, dic:dict):
        print('数据库参数改动了,重新连接数据库')
        self._cur_conn_params = dic
        self.connect(self._cur_conn_params)
        self.cursor = self.get_cursor()
        pass

    def get_connection_params(self):
        """从默认配置中获取参数"""
        kwargs = {}
        kwargs['user']  = setting.DATABASES['USER']
        kwargs['database'] = setting.DATABASES['DBNAME']
        kwargs['password'] = setting.DATABASES['PASSWORD']
        kwargs['unix_socket'] = setting.DATABASES['HOST']
        kwargs['host'] = setting.DATABASES['HOST']
        kwargs['port'] = int(setting.DATABASES['PORT'])
        return kwargs

    def get_new_connection(self, params):
        """创建自定义的数据库连接"""
        conn = pymysql.connect(
            host=params['host'],
            user=params['user'],
            passwd=params['password'],
            db=params['database'],
            autocommit=True
        )
        return conn

    def connect(self, _cur_conn_params):
        self.connection = self.get_new_connection(_cur_conn_params)

    def get_conn(self):
        if(self.connection):
            return self.connection
        else:
            assert '数据库未连接，清调用connect方法连接数据库'

    def get_cursor(self):
        if(self.connection):
            return self.connection.cursor()
        else:
            assert '数据库未连接，清调用connect方法连接数据库'

    def close_db(self):
        try:
            self.connection.close()
        except Exception as e:
            assert '数据库关闭失败'

    def closeDb(self):
        try:
            self.cursor.close()
            self.conn.close()
            return "数据库 ", self.databaseName, " 关闭成功"
        except Exception as e:
            print("数据库 ", self.databaseName, " 关闭失败")
            return -1
