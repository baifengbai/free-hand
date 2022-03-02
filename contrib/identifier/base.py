from static.intterrogative_dict import INTERROGATIVE_WORD_DICT

class Base_Identifier:
    def __init__(self):
        pass

    @staticmethod
    def is_intterrogative(s:str):
        check = False
        word_lis = INTERROGATIVE_WORD_DICT['symple_value_100']
        word_lis.extend(INTERROGATIVE_WORD_DICT['yiwenci_value_99'])
        word_lis.extend(INTERROGATIVE_WORD_DICT['yiwenci_value_98'])
        word_lis.extend(INTERROGATIVE_WORD_DICT['yiwenci_value_97'])
        word_lis.extend(INTERROGATIVE_WORD_DICT['yiwenci_value_96'])
        word_lis.extend(INTERROGATIVE_WORD_DICT['tongyong'])
        for i in word_lis:
            if (i in s):
                check = True
                return check
            else:
                continue
        return check

