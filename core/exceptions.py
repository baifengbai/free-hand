"""
Global exception and warning classes.
"""


class DBConfigError(Exception):
    """数据库配置错误"""
    pass


class ImproperlyConfigured(Exception):
    """配置错误"""
    pass