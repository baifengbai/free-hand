from core.base.middleware.mid_string.mid_string_clean import StringMiddleware

class ParagraphMiddleware(StringMiddleware):
    @classmethod
    def process_operation(self, paragraph:str):
        """
        段落清洗操作
        """
        # 1 有统一前奏操作
        paragraph = self.process_default(paragraph)

        # 2 判断起始位置
        if (paragraph.startswith('，') or paragraph.startswith(',')):
            paragraph = paragraph[1:]
        for i in range(1,10):
            if(paragraph.startswith(str(i))):
                paragraph = paragraph[1:]

        return paragraph