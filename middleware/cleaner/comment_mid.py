from core.base.middleware.mid_string.mid_string_clean import StringMiddleware

class CommentMiddleware(StringMiddleware):
    @classmethod
    def process_operation(self, comment:str):
        """
        段落清洗操作
        """
        # 1 有统一前奏操作
        comment = self.process_default(comment)
        # 2 清标签
        comment = self.clean_webTag(comment)
        for i in range(1,10):
            if(comment.startswith(str(i))):
                comment = comment[1:]
        # 3 判断起始位置
        if (comment.startswith('，') or comment.startswith(',')):
            comment = comment[1:]
        return comment