from core.base.tasksmixin.tasks_postdata.base import Base_Task_Post
from db.backends.mysql.operations import OperatorMysql
from contrib.poster import poster_article
from middleware.cleaner.article_mid import ArticleMiddleware


"""
    文章上传
    筛选条件：
        完整清洗过后的 文章内容 content 字数>500
        完整清洗过后的 标题 title 字数>10
    清洗条件：
"""
class Task_Post_Article(Base_Task_Post):
    def handle_article_lis(self, lis):
        res_lis = []
        cleaner_Article = ArticleMiddleware()
        for article in lis:
            title = cleaner_Article.clean_title(title=article[0])
            content = cleaner_Article.clean_content(content=article[1])
            if(len(title)>=10 and len(content)>550):
                res_lis.append((title, content))
        return res_lis

    def run(self, db_user, db_pwd, database_name, table_name):
        """
            主要针对 段落、文章、评论 且保存在数据路里的这类数据（字符串类型）的处理和上传， 图片、视频等类型数据不适合本类方法
            注意：
                本类方法不做任何过滤操作和其它数据清洗操作，特殊操作根据不同task_type选择不同task 如 task_post_articles.py
        """
        sql = 'SELECT `title`, `content` FROM {};'.format(table_name)
        # 2 获取 从数据库获取数据列表
        params = {
            'USER': db_user,
            'DBNAME': database_name,
            'PASSWORD': db_pwd,
            'HOST': '',
            'PORT': '',
        }
        dbOperator = OperatorMysql(params)
        dataList = dbOperator.getAllDataFromDB(sql)
        # 3 去重
        dataList = self.del_repeatdata(task_type='articles', lis=dataList)
        # 4 清洗 根据不同 task_type 通用数据清洗操作 作为上传数据前的最后一步清洗
        dataList = self.handle_article_lis(lis=dataList)
        # 5 上传 处理后的列表
        if(dataList):
            posterInstance = poster_article.Poster_Article(interface='http://121.40.187.51:8088/api/article_get')
            posterInstance.post_auto(dataList, task_type='article')
        # 6 更新 将上传过的数据放到postedurldatabase中

