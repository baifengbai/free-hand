"""基类"""
class MiddlewareMixin:
    """
    中间件元基类内部基本方法， 定义了中间件需要重写的方法
    """
    def process_default(self, obj):
        """
        定义统一需要执行的操作
        若无统一操作则直接pass
        子类必须重写
        """
        return obj

    def process_operation(self, obj):
        """集成操作，子类需要重写该方法"""
        obj = self.process_default(obj)
        return obj
