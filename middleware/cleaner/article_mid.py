from core.base.middleware.mid_string.mid_string_clean import StringMiddleware
from . import paragraph_mid

class ArticleMiddleware(StringMiddleware):
    """
            文章内容 清洗需求
                1 只保留p标签和img标签
                2 清掉所有样式属性 img保留src
        """
    cleanWords_huxiu_lis = [
        '本文不构成', '本文来自', '作者：', '未经允许不得转载', '原文链接', '出品｜', '作者｜', '题图｜', '作者 |', '出品 |', '头图 |', '扫描图末二维码', '虎嗅注'  # 过滤词
                                                                                                            '（应受访者要求，文中均为化名）',
        '（via Anna Team）'  # 提取 （via ） 、 （化名）   规则
    ]

    def __init__(self):
        self.cleanWordList = [
            '本报记者 ', '友情提示：'
        ]
        self.irrelevantWordList = ['图']
        self.baseClass = StringMiddleware  # 父类

    def clean_tag(self, content):
        pass

    def clean_title(self, title):
        """
            有品牌或者前置声明的   把他替换为空
            替换后标题数目<10个字则过滤掉
            清洗过后的标题中含有的诸如 逗号、引号 之类的符号，将其替换
                逗号 换 空格
                其它符号 替换为空
        """
        symple_lis = [
            ':', '：', '|', '｜', '［', '丨'
        ]
        symple_4replace_lis = [
            '“', '”', '；', '！', '「', '」', '—', '《', '》', '*', '...', '..',
            '；', ';', '：', ':', '（', '）', '。', '【', '】', '|', '-', '、', '&'
        ]
        origin_lis = [
            '每日经济新闻', '财联社', '资本邦', '新华社', '虎嗅', '每经AI', '每经', '新华网'
        ]
        for symple in symple_lis:
            if (symple in title):
                title = self.del_content_symple(title, symple=symple, del_direction='left')
        for originName in origin_lis:
            if (originName in title):
                title = title.replace(originName, '')
        res = self.del_content_brackets(title, delAll=True)
        res = res.replace('，', ' ').replace(',', ' ')
        for symple in symple_4replace_lis:
            res = res.replace(symple, '')
        return res

    def clean_content(self, content):
        """对文章内容整体的清洗"""
        origin_lis = [
            '每日经济新闻', '财联社', '资本邦', '新华社', '虎嗅', '每经AI', '每经', '新华网'
        ]
        if (content.startswith('，') or content.startswith(',')):
            content = content[1:]
        for origin in origin_lis:
            content = self.del_content_between(content, s_left='(' + origin, s_right=')')  # 正则 直接小括号会报错
            content = self.del_content_between(content, s_left='（' + origin, s_right='）')
            content = self.del_content_between(content, s_left=origin, s_right='讯')
            content = content.replace(origin, '')
        return content

    def clean_baseon_origin(self, origin):
        """根据不同站点文章内容的情况针对性清洗"""
        if (origin == 'huxiu'):
            pass
        elif (origin == 'nbd'):
            pass
        else:
            print('站点 origin 不存在：', origin)
            pass

    def split_content(self, content) -> list:
        """
        拆分经过拼接合成的content
        :param content
            格式：
            <p>...</p>...<img src='xxx' />...
        :output 按原先顺序 输出段落内容和链接
            ['段落内容', '链接']
        """
        lis = content.split('</p>')
        res = []
        for i in lis:
            if ('img' in i):
                temp_lis = i.split(' />')
                for t in temp_lis:
                    if ('img' in t):
                        src = t.split('src=')[-1][1:-1]
                        res.append(src)
                    else:
                        res.append(t.replace('<p>', ''))
            else:
                res.append(i.replace('<p>', ''))
        return res

    def process_operation(self, content_ori):
        content = ''
        p_lis = self.split_content(content_ori)
        for p in p_lis:
            if ('http' not in p):
                content = content + '<p>' + paragraph_mid.ParagraphMiddleware().process_operation(p) + '</p>'
            else:
                content = content + '<img src=\'' + p + '\' />'
        return content