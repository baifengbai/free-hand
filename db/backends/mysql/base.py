import pymysql

class BaseDatabase:
    """数据库连接基类"""
    def __init__(self, settings_dict):
        self.connection = None
        self.settings_dict = settings_dict
        self.connect()
        self.cursor = self.get_cursor()

    def get_connection_params(self):
        kwargs = {}
        settings_dict = self.settings_dict
        if(settings_dict['USER']):
            kwargs['user']  = settings_dict['USER']
        if(settings_dict['DBNAME']):
            kwargs['database'] = settings_dict['DBNAME']
        if(settings_dict['PASSWORD']):
            kwargs['password'] = settings_dict['PASSWORD']
        if( settings_dict['HOST'].startswith('/')):
            kwargs['unix_socket'] = settings_dict['HOST']
        elif(settings_dict['HOST']):
            kwargs['host'] = settings_dict['HOST']
        if(settings_dict['PORT']):
            kwargs['port'] = int(settings_dict['PORT'])
        return kwargs

    def get_new_connection(self, params):
        conn = pymysql.connect(
            host=params['host'],
            user=params['user'],
            passwd=params['password'],
            db=params['database'],
            autocommit=True
        )
        return conn

    def connect(self):
        conn_params = self.get_connection_params()
        self.connection = self.get_new_connection(conn_params)

    def get_conn(self):
        if(self.connection):
            return self.connection
        else:
            assert '数据库未连接，清调用connect方法连接数据库'

    def get_cursor(self):
        if (self.connection):
            return self.connection.cursor
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
