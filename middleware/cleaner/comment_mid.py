from core.base.middleware.mid_string.mid_string_clean import StringMiddleware

class CommentMiddleware(StringMiddleware):
    @classmethod
    def process_operation(self, comment:str):
        """
        段落清洗操作
        """
        # 1 清空白
        comment = self.clean_space(comment)
        # 2 清括号内容
        comment = self.clean_content_brackets(comment, delAll=True)
        # 3 清序号
        for k in ['xuhao1', 'xuhao2', 'xuhao3']:
            comment = self.clean_headnum(comment, k)
        # 4 清标签
        comment = self.clean_webTag(comment)
        for i in range(1,10):
            if(comment.startswith(str(i))):
                comment = comment[1:]
        return comment