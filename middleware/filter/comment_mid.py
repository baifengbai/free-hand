from core.base.middleware.mid_filter.base import BaseFilter
from middleware.cleaner.comment_mid import CommentMiddleware

class Filter_Comment(BaseFilter):
    # -> 评论内容的集成操作方法
    def integratedOp(self, commentList, keywordList):
        result = []
        cleanerInstance = CommentMiddleware()
        for item in commentList:
            # 1 进行清洗操作(评论不用清洗 去除两边空格就可了)
            item[1] = cleanerInstance.integratedOp(item[1])
            item[1] = item[1].strip('1.').strip('2.').strip('3.').strip('4.').strip('5.').strip('6.').strip('7.').strip('8.').strip()
            for keyword in keywordList:
                # 2 根据字符串长度25-250间进行筛选
                if (not self.filter_BetweenNumberOfWords(item[1], whichKind='articleComment')):
                    # 段落字数再25-250间，有用可传
                    continue
                # 3 对每个段落进行关键词筛选 若有关键词则跳出当前循环
                if (self.checkIfHasKeyword_comment(item[1], keyword)):
                    # 4 根据筛选结果导入可上传的数据
                    result.append(
                        (
                            item[1],  # 评论内容
                            keyword,  # 相关关键词
                        )
                    )
                    break
        return result