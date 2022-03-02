from core.base.middleware.mid_filter.base import BaseFilter
from middleware.cleaner.paragraph_mid import ParagraphMiddleware

class Filter_Keyparagraph(BaseFilter):
    def integratedOp(self, paragraphList):
        result = []
        cleanerInstance = ParagraphMiddleware()
        for item in paragraphList:
            paragraph = item[0]
            tag_ori = item[1]
            # 筛选有标签的
            if (self.filter_hasTag_keyParagraph(paragraph, tag_ori)):
                # 进行清洗操作
                paragraph = cleanerInstance.integratedOp(paragraph)
                # 筛选判断 ：
                #   1 字符串长度不在125-250之间；
                #   2 段落含有股票名或代码
                #   3 段落包含日期关键词
                ##  但凡满足上面任何一个的段落筛选条件的段落都过滤掉
                check = (not self.filter_BetweenNumberOfWords(paragraph, whichKind='keyParagraph')) or self.filter_hasStockCode(paragraph, self.stocksNameCodeList) or self.filter_dateRef(paragraph, self.dateRefList)
                if (check):
                    # 进入该判断条件说明对应段落无效跳过， 因此希望有效段落的check最终为false
                    continue
                result.append(
                    (
                        paragraph,  # 段落内容
                        tag_ori
                    )
                )
            else:
                continue
        return result