from customFunction__.Manager.article_manager import Article_Manager
from taskLibrary__.scrapy_tasks.task_articles import Article_Task
"""测试任务管理器 """
articles_configs = {
    'gelonghui': {
        "spiderPath": "C:\\Users\\Administrator\\Desktop\\Projects\\Crawl_Dealwith_Post_Auto\\commentGelonghui_Crawl_Dealwith_Post_Auto\\commentGelonghui_Crawl_Dealwith_Post_Auto",
        "spiderName": "gelonghuiSpider",
        "command": "Scrapy crawl gelonghuiSpider"
        },
    'guba': {
        "spiderPath": "C:\\Users\\Administrator\\Desktop\\Projects\\Crawl_Dealwith_Post_Auto\\commentGuba_Crawl_Dealwith_Post_Auto\\commentGuba_Crawl_Dealwith_Post_Auto",
        "spiderName": "gubaSpider",
        "command": "Scrapy crawl gubaSpider"
        },
    'stockstar':{
        "spiderPath": "C:\\Users\\Administrator\\Desktop\\Projects\\Crawl_Dealwith_Post_Auto\\commentStockstar\\commentStockstar",
        "spiderName": "gubaSpider",
        "command": "Scrapy crawl stockstarSpider"
        },
    'xueqiu':{
        "spiderPath": "C:\\Users\\Administrator\\Desktop\\Projects\\Crawl_Dealwith_Post_Auto\\commentXueqiu_Crawl_Dealwith_Post_Auto\\commentXueqiu_Crawl_Dealwith_Post_Auto",
        "spiderName": "xueqiuSpider",
        "command": "Scrapy crawl xueqiuSpider"
    }
}
manager_articles = Article_Manager()
task_queue = manager_articles.init_queue('articles')
for item in articles_configs.values():
    article_task = Article_Task()
    article_task.env_config = item
    manager_articles.push_task(task_queue, article_task.run)
# 文章对象需要创建多个 不同站点 不同对象
while(task_queue.qsize()!=0):
    """间隔60s执行任务"""
    task_queue.get()()
    # time.sleep(60)
print('任务执行完毕')
