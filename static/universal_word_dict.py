
# 通用词列表
UNIVERSAL_CLEANWORD_DICT = {
    ########################################
    # 通用的待组合清洗字符字典列表，如数字、字母等 #
    ########################################
    'alphabeticList':[
        'A','B','C','D','E','F','G','H','I','J','K','L','M','N',
        'a','b','c','d','e','f','g','h','i','j','k','l','m','n'
    ],
    'numList1':['一','二','三','四','五','六','七','八','九','十'],
    'numList2':['第一','第二','第三','第四','第五','第六','第七','第八','第九','第十'],
    ########################################
    # 通用标点符号、 空白                     #
    ########################################
    'symbol': ['.', '。', ',', '，', '、', '：', ':', '|', '｜', '丨'],
    'space': [' ', '\u3000', '\xa0', '\r', '\n', '\t'],
    'paragraph_key_or_rel': [
        '●', '但是，', '所以，', '再说，', '虽然说，', '另外，', '最后，', '而且，',
        '其次，', '首先，', '再者，', '同时，', '不过，', '当然，', '当然啦，', '那么，', '虽然，',
        '其实，', '通常，', '接着，', '综上所述，', '因此，'
    ],
    'startwith': [',','，','.','。','、'],
    'xuhao1': ['问题1', '问题2'],
    'xuhao2': ['①','②','③','④','⑤','⑥'],
    'xuhao3': []
}

for i in range(1,100):
    UNIVERSAL_CLEANWORD_DICT['xuhao1'].extend(
        [
            '({})'.format(str(i)), '（{}）'.format(str(i)),
            '{}）'.format(str(i)), ')'.format(str(i)),
            '[{}]'.format(str(i)), '【{}】'.format(str(i)),
        ]
    )

for x in UNIVERSAL_CLEANWORD_DICT['numList1']:
    UNIVERSAL_CLEANWORD_DICT['xuhao2'].extend(
        [
            x + '.', x + '、', x + '，'
        ]
    )

for x in UNIVERSAL_CLEANWORD_DICT['alphabeticList']:
    UNIVERSAL_CLEANWORD_DICT['xuhao3'].extend(
        [
            x + '.', x + ')', x + '）'
        ]
    )