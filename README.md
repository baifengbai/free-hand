# freehand
    数据（段落、评论、图片、视频）的自动化处理  在旧项目packageDIY的基础上进行代码的简化和整合
    1、 需求说明
        1. 涉及的数据类型： 关键词段落、关联词段落、缩略图、内容图、评论、财经文章
        2. 主要任务： 定时自动化数据爬取任务 + 数据处理任务 + 定时自动化数据上传任务
            数据处理包括： 
                字符串相关：
                    数据过滤 数据清洗 数据替换 等
                其它类型
                    图片识别
                    图片md5修改
                    图片比例修改
                    ..
                    视频处理
    2、 项目思路：
        1.整体思路最初设想 ———— packageDIY 已不再维护
            1 自动化定时方面 分别设置三类定时器 
                定时爬取定时器、 定时上传定时器、 定时清空数据库定时器
                - 测试：实现后经过测试发现任务启动时间上不好控制，出现了误清空数据库的问题
                - 问题：三类任务应该是顺序执行的才行，但是由于是分别启动的定时器，因此运行时间上有出入
                    因此取消了清空数据库的定时器，而是把清空数据库的任务 嵌入了 上传数据任务完成之后
            2 数据处理方面
                分别根据 不同的数据类型 单独开发不同的模块 包括 Filter模块 Cleaner模块 Poster模块 等等
                    |-packageDIY
                    |--articlesRef
                        |----Cleaner
                        |----Poster
                        |----Filter
                        |----...
                    |--commentsRef
                        |----Cleaner
                        |----Poster
                        |----Filter
                        |----...
                    |--videoRef
                    |...
                问题： 后面发现代码太冗余了，改动太麻烦，太多重复的
       2. 经过完善的新思路 ———— auto_datahandler 继续维护
            - 主要完善方向：
                将冗余的代码全部提出来单独成立一个 全局通用模块 basement
                新增了一个spider模块用于 selenium爬取任务 的开发
                集成了通用验证码处理模块 
            - 完善的核心体现在 
                项目结构的组织上 如 将数据清洗单独作为一个模块放在了自定义方法模块 customFunction 里等 
                任务进行的流程上 如 优化了抖音视频爬取流程，删除了一些不必要的重复的流程
                解耦了复杂逻辑（将关键且常用的流程提纯成一个单独的方法，如滑块验证 解耦主要体现在selenium爬取视频上）
       3. 数据结构层面优化了定时爬取任务
            过去：auto_datahandler的定时任务分别单独开启爬取任务，依据不同的爬取源创建不同的定时爬取任务文件
                如： 在爬取文章时,分别启动下面的每一份定时器 
                    财联社         cailianshe_Spider.py
                    每日经济新闻    cfi_Spider.py
                    虎嗅           huxiu_Spider.py
                问题：这样导致了太多的python脚本的运行，不太好管理，scrapy爬取还好，遇到selenium爬取的若是刚好同时运行，chromedriver启动太多占用内存不小
            解决： 使用队列这种数据结构 将同一类的任务以方法的形式压入队列中，定时任务定位调用队列 先入先出
                好处： 避免了任务同时进行这种情况的出现
                ps: 这种方式只用在数据爬去的任务上，定时上传的任务不采用这种方案，原因是 定时上传 偶尔管理的时候需要查看对应上传了些什么东西，需要查看控制台，多份脚本这样好查看
    3、 数据库的设计
        1. 当前数据库创建格式 及 命名格式
            根据不同的任务类型 task_type 创建不同的数据库
            - articledatabase     存放文章的数据库
                基本格式 tb_article_站点名_content
                + tb_article_aigupiao_content
                + tb_article_cailianshe_content
                + tb_article_toutiao_articleinfo    少数需要涉及到这类表
                + tb_article_toutiao_content
                + ...
            - commentdatabase     存放评论数据的数据库
                + tb_comment_gelonghui_content
                + tb_comemnt_guba_content
            - imgsdatabase        存放图片的数据库
                基本格式 tb_任务类型_站点名
                + tb_contentimg_cbnweek
                + tb_thumbnail_huxiu
            - paragraphdatabse    存放段落内容的数据库
                少数需要涉及该类表 能不要则不要吧
                + tb_keyparagraph_selfsites_content
                + tb_relativeparagraph_cngold_articlecontent
                + tb_relativeparagraph_cngold_articleinfo
            - videodatabase       存放视频信息的数据库
                + tb_douyin_videoinfo
                + tb_bilibili_videoinfo
            - postedurldatabase   存放上传过的数据的数据库
                + tb_article_posted
                + tb_comment_posted
                + tb_contentimgs_posted
                + tb_paragraph_posted
                + tb_thumbnailimgs_posted
                + tb_video_posted
            - stocksnamecode      存放股票对应的数据库
                + tb_namecode
        2. 有空再优化一下数据库设计
        3. 更新一下数据库表的设计
            简化策略： 
                不用上传的字段都删去，留下的都是要处理的字段
                每个源一张表完成，尽量不要多张表
            - keyparagragh 表的字段
                id paragraph tag_ori
            - relativeparagraph 
                id paragraph 
    4、 未来任务方向
        开发一套爬虫站点 主要包括 启动爬虫 定时 以及各种日志查看的功能
## 一、 依赖库（需下载）:
    requests
    pymysql
    opencv-python
    shutil
    pyexecjs
    opencv-python
    selenium
    scrapy
    baidu-aip
    requests-toolbelt
    fake_useragent
    pillow
    PyPDF2
    pdf2image
    psutil      判断进程是否存在

## 二、 timerConfig 配置参数
    1. 参数说明
    - 关键配置参数
        + 'crawler_method'      爬 取 方 式   只在定时爬去任务定时器里有该参数
            'scrapy'            基本都采用该方式
            'selenium'          除了 抖音 今日头条 这种特别麻烦的采用selenium
        + 'task_type'           任 务 种 类 
            'articles'          财经文章
            'keyParagraph'      关键词段落
            'relativeParagraph' 关联词段落
            'thumbnailImgs'     缩略图
            'contentImgs'       内容图
            'articleComment'    文章评论
        + 'keywordList'         这个在不同task_type中有不同含义
    - 涉及视频、图片的保存路径上
        + 'proj_absPath' : proj_absPath,   # 当前环境路径  用于设置保存路径
        + 'origin' : origin,     # 对应源名 如 douyin 主要用在  根据日期和origin创建的目录
        scrapy爬虫任务的关键参数
        + 'spiderPath'          scrapy爬虫项目的项目路径
        + 'spiderName'          scrapy爬虫项目的爬虫名
        + 'command'             scrapy爬虫项目的命令
            "Scrapy crawl aitouyanSpider"
    - 其它
        + 'databaseUser' : 'root'
        + 'databasePasswd' : 'root'
        + 'databaseName': 'commentdatabase',  # 对应的数据库名
        + 'tableName': ['tb_comment_stockstar_content'],  # 待处理的表名——存放图片url信息的表
        + 'table_wait2bclean'   待清空的数据库表名
            
    2. 定时配置
        {
            "beginTime": '08:03:00',  # 注意表示 一位数字的要0开头
            "endTime": '09:00:00',
            "taskExcuteDelta": 3600,  # 任务间隔1h
            "timeExcuteDelta": 86400*100,  # 定时器间隔 每个一天运行一次
        }
        ps: timeExcuteDelta *100是为了避免定时器启用太多个
    3. 爬虫定时任务（默认都要加上定时配置，下面就省略了）
        - 【selenium爬取+上传一体】视频
            {   
                "crawler_method": "selenium"
                "task_type": 'video',
                "proj_absPath": proj_absPath,  # 当前环境路径
                "origin": 'douyin',  # 对应域名
                "crawlUrl_list" : [
                    "https://www.douyin.com/search/%E8%82%A1?publish_time=1&sort_type=2&source=normal_search&type=video",
                    "https://www.douyin.com/search/%E8%82%A1%E7%A5%A8?publish_time=1&sort_type=2&source=normal_search&type=video",
                    "https://www.douyin.com/search/%E6%B6%A8%E8%B7%8C?publish_time=1&sort_type=2&source=normal_search&type=video",
                    "https://www.douyin.com/search/%E5%A4%A7%E7%9B%98?publish_time=1&sort_type=2&source=normal_search&type=video",
                    "https://www.douyin.com/search/B%E8%82%A1?publish_time=1&sort_type=2&source=normal_search&type=video",
                    "https://www.douyin.com/search/%E7%9F%AD%E7%BA%BF?publish_time=1&sort_type=2&source=normal_search&type=video",
                    "https://www.douyin.com/search/%E6%8C%87%E6%95%B0?publish_time=1&sort_type=2&source=normal_search&type=video"
                ],
                'databaseName': 'videodatabase', # 数据库名
                'table_wait2bclean' : 'tb_douyin_videoinfo'  # 待清空的数据库表名
            }
        - 【scrapy爬取】文章、关键词段落、关联词段落、内容图、缩略图、评论 统一配置
            {
                "crawler_method": "scrapy"
                "spiderPath": "E:\\Projects\\Crawl_Dealwith_Post_Auto\\commentStockstar\\commentStockstar",
                "spiderName": "stockstarSpider",
                "command": "Scrapy crawl stockstarSpider"
            }
    4. 自动化上传定时任务（默认都要加上定时配置，下面就省略了）
        - 视频 视频任务由于是采用selenium完成，不涉及scrapy，所以自动化上传也再爬取的任务里面完成，无需额外开启上传任务
        - 文章
            {   
                'task_type': 'articles',
                'databaseUser' : 'root',
                'databasePasswd' : 'root',
                'databaseName': 'articledatabase',  # 对应的数据库名
                'tableName': ['tb_article_aigupiao_content'],  # 待处理的表名——存放图片url信息的表
                'sql': 'SELECT * FROM `articledatabase`.`tb_article_aigupiao_content`;',
                'crawler_method': 'scrapy'
            }
        - 关键词段落
            {   
                "task_type": 'keyParagraph',
                'databaseName': 'paragraphdatabase',
                'databaseUser': 'root',
                'databasePasswd': 'root',
                'tableName': 'tb_keyparagraph_anxinsc_articlecontent',
                'tableName2Clear': [
                    'tb_keyparagraph_anxinsc_articleinfo',
                    'tb_keyparagraph_anxinsc_articlecontent'
                ]
            }
        - 关联词段落
            {
                'databaseName' : 'paragraphdatabase',
                'databaseUser' : 'root',
                'databasePasswd' : 'root',
                'keywordList' : ['个股', '股市', 'A股', '港股', '新股', '美股', '创业板', '证券股', '炒股', '散户', '短线', '操盘', '波段', '股票'],
                "task_type": 'relativeParagraph',
                'tableName2Clear': [
                    'tb_relativeparagraph_cngold_articleinfo',
                    'tb_relativeparagraph_cngold_articlecontent'
                ]
            }
        - 内容图
            {
                "task_type": 'contentImgs',
                "maskFilt" : False, # 是否需要处理水印
                "databaseName": 'imgsdatabase',  # 对应的数据库名
                "tableName": ['tb_contentimg_cbnweek'],  # 待处理的表名——存放图片url信息的表
                "proj_absPath" : proj_absPath,   # 当前环境路径   只有图片才需要这个
                "origin" : origin,     # 对应域名  只有图片才需要这个
                "tableName2Clear": ['tb_contentimg_cbnweek']
            }
        - 缩略图
            {
                "task_type": 'thumbnailImgs',
                "databaseName": 'imgsdatabase',  # 对应的数据库名
                "tableName": ['tb_thumbnail_huxiu'],  # 待处理的表名——存放图片url信息的表
                "proj_absPath" : proj_absPath,   # 当前环境路径   
                "origin" : origin,     
                "tableName2Clear": ['tb_thumbnail_huxiu']
            }
        - 评论
            {
                "task_type": 'articleComment',
                'keywordList' : ['个股', '股市', 'A股', '港股', '新股', '炒股', '散户', '短线', '操盘', '波段', '股票'],
                'databaseUser' : 'root',
                'databasePasswd' : 'root',
                "databaseName": 'commentdatabase',  # 对应的数据库名
                "tableName": ['tb_comment_stockstar_content'],  # 待处理的表名——存放图片url信息的表
                "tableName2Clear": ['tb_comment_stockstar_content'],
                "sql": 'SELECT id, comment FROM `commentdatabase`.`tb_comment_stockstar_content`;'
            }
## 三、 爬取内容处理思路
    1. 文章 换成思路一
        首先，对标题进行判断，判断是否是疑问句，是的话再进行以下的步骤
        思路一：
            在scrapy爬虫项目中，
            针对每个段落（for循环）：
                · 过滤
                · 清洗
                · 拼接合成
                · 进入pipeline 录入数据库。
        思路二：经过过滤筛选的段落合成之后录入数据库，在上传前再做一次清洗，这样的话需要分段处理，就需要多一步split。（旧思路）
        关于段落的清洗：
            用clean_paragraph.Cleaner_Paragraph 类下的方法 integratedOp()
            注意：不要再合成的时候创建对象清洗段落，虽然能达到目的但是耗时很大。
            由于段落的处理在for循环内部，若是在拼接合成的时候直接用 clean_paragraph.Cleaner_Paragraph().integratedOp()
                等同于每循环一个段落创建一个对象，资源耗费也很大
            正确做法：
                在for循环外部创建一个对象，for循环内部调用对象的方法 integratedOp()
## 四、 使用示例
    1. 导入特定定时器
        from auto_datahandler.basement__ import Timer
    2. 设置好配置 timeConfig
        timeConfig = {
                "beginTime": '08:03:00',  # 注意表示 一位数字的要0开头
                "endTime": '09:00:00',
                "taskExcuteDelta": 3600,  # 任务间隔1h
                "timeExcuteDelta": 86400*100,  # 定时器间隔 每个一天运行一次
                "spiderPath": "E:\\Projects\\Crawl_Dealwith_Post_Auto\\commentStockstar\\commentStockstar",
                "spiderName": "stockstarSpider",
                "command": "Scrapy crawl stockstarSpider",
                'crawler_method' : 'scrapy'
            }
    3. 创建对应定时器对象
        spider_timer = Timer.TaskTimer_Spider(timerConfig=timerConfig)
    4. 启动定时器
        spider_timer.timerTaskRun()
    5. 关于进程运行状态检查
        需要提前设置好数据库 及各个task_type 的映射关系
        - 示例
        主要字段 id pid      task_type         execute_command             task        origin
                0  XXX      comments        python E:\XXX\XX\...\XX.py    spider    stockstar
        - 字段说明
            id              映射id
            pid             进程id
            task_type       同前面的task_type
            execute_command 命令执行语句
            task            任务类型            spider/poster
            origin          源站点名 便于分类

## 五、版本
    freehand 版本主要有三大版本：
        最初版本        基本操作流程               packageDIY
        第二版本    基于packageDIY的第一次架构      auto_handler
        第三版本    基于auto_handler的第二次架构    freehand
    当前处在第三版本 为架构比较合理的版本 历史版本已设私密
    查看历史版本或是技术交流请联系 18898670632
      