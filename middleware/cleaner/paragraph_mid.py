from core.base.middleware.mid_string_clean import StringMiddleware

class ParagraphMiddleware(StringMiddleware):
    @classmethod
    def process_operation(self, paragrph:str):
        """
        段落清洗操作
        """
        # 1 清空白
        paragraph = self.clean_space(paragrph)
        # 2 清括号内容
        paragraph = self.clean_content_brackets(paragraph, delAll=True)
        # 3 清序号
        for k in ['xuhao1', 'xuhao2', 'xuhao3']:
            paragraph = self.clean_headnum(paragraph, k)

        for i in range(1,10):
            if(paragraph.startswith(str(i))):
                paragraph = paragraph[1:]
        return paragraph