from ..base import Base_Task

class Base_Task_Post(Base_Task):
    @classmethod
    def get_by_tasktype_config(cls, task_type, table_name):
        """根据不同的任务类型选择对应的数据获取方式"""
        if(task_type == 'articles' ):
            return {
                'sql_getdata': 'SELECT `title`, `content` FROM {};'.format(table_name),
                'interface': ''
            }
        elif(task_type == 'relativeParagraph'):
            return {
                'sql_getdata': 'SELECT `id`, `paragraph` FROM {};'.format(table_name),
                'interface': 'http://121.40.187.51:8088/api/relation_paragraph_api'
            }
        elif (task_type == 'keyParagraph'):
            return {
                'sql_getdata': 'SELECT * FROM {};'.format(table_name),
                'interface': 'http://121.40.187.51:8088/api/key_paragraph_api'
            }
        elif (task_type == 'thumbnailImgs'):
            return {
                'sql_getdata': '',
                'interface': ''
            }
        elif (task_type == 'contentImgs'):
            return {
                'sql_getdata': '',
                'interface': ''
            }
        elif (task_type == 'articleComment'):
            return {
                'sql_getdata': 'select `id`,`comment` from {};'.format(table_name),
                'interface': 'http://121.40.187.51:8088/api/articlecomment_api'
            }
        else:
            print('task_type出错：', task_type)
            return None

    def del_repeatdata(self,task_type, lis):
        """由于不同任务类型从数据库获取的数据列表的格式都不一样，因此需要针对不同任务进行去重处理"""
        if (task_type == 'articles'):
            """
            格式：
                [(title, content),(title, content)]
            """
            has_title_lis = []
            res_lis = []
            for i in lis:
                if(i[0] not in has_title_lis):
                    res_lis.append(i)
                    has_title_lis.append(i[0])
            del has_title_lis
            return res_lis
        elif (task_type == 'relativeParagraph'):
            """
            格式：
                [(id, paragraph),(id, paragraph)]
            """
            has_para_lis = []
            res_lis = []
            for i in lis:
                if(i[1] not in has_para_lis):
                    res_lis.append(i)
                    has_para_lis.append(i[1])
            del has_para_lis
            return res_lis
        elif (task_type == 'keyParagraph'):
            res_lis = lis
            return res_lis
        elif (task_type == 'thumbnailImgs'):
            res_lis = lis
            return res_lis
        elif (task_type == 'contentImgs'):
            res_lis = lis
            return res_lis
        elif (task_type == 'articleComment'):
            """
            格式：
                [(id, comment),(id, comment)]
            """
            has_comment_lis = []
            res_lis = []
            for i in lis:
                if (i[1] not in has_comment_lis):
                    res_lis.append(i)
                    has_comment_lis.append(i[1])
            del has_comment_lis
            return res_lis
        else:
            print('task_type出错：', task_type)
            return None