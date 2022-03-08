"""初始化数据库 创建默认数据库及对应数据表"""
from .base import BaseDatabase
from static import default_variable_map
from core.utils.module_loading import import_string

default_variable_map_path = 'static.default_variable_map'

"""本类只在初始化基于本框架项目的时候调用一次"""
class Init_DB(BaseDatabase):
    def __init__(self):
        self.connection = None
        self._cur_conn_params = self.get_connection_params()
        self._cur_conn_params = self.get_connection_params()
        self._cur_conn_params.pop('database')
        self.connect(self._cur_conn_params)
        self.cursor = self.get_cursor()

    def _create_db(self):
        """创建默认的数据库"""
        self.cursor.execute(default_variable_map.CREATE_DEFAULT_DATABASE)

    def _create_table_default(self):
        table_lis = default_variable_map.DEFAULT_TABLE_LIS
        for table_name in table_lis:
            sql = import_string(default_variable_map_path + '.' + table_name)
            self.cursor.execute(sql)


    def _connect_db(self):
        """连接进入默认创建的数据库"""
        self.cur_conn_params['database'] = default_variable_map.DATABASE
        self.connect(self.cur_conn_params)

    def run_default(self):
        """创建内置默认数据库和表的流程"""
        self._create_db()   # 创建数据库
        self._connect_db()  # 连接数据库
        self._create_table_default()

