"""
    全局使用的默认变量
        如 内置的表对应的操作SQL语句
"""

#######################
#  重用selenium引擎    #
#  tb_selenium_info  #
#####################
"""
CREATE TABLE `tb_selenium_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `executor` varchar(250) DEFAULT NULL,
  `session_id` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""
SELENIUM_REUSE_SQL_INSERT = "INSERT INTO `data_usable_database`.`tb_selenium_info` (`executor`, `session_id`) VALUES ('{}', '{}');"
SELENIUM_REUSE_SQL_UPDATE = "UPDATE `data_usable_database`.`tb_selenium_info` SET `executor` = '{}', `session_id` = '{}' WHERE (`id` = '{}');"


##########################
#   进程信息操作           #
#   主要用于自动化任务的操作 #
#   tb_process_info     #
########################
"""
CREATE TABLE `tb_process_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pid` int DEFAULT NULL,
  `task_type` varchar(45) DEFAULT NULL,
  `execute_command` text,
  `task` varchar(45) DEFAULT NULL,
  `origin` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='进程控制'
"""




#######################
#   站点信息操作        #
#  tb_site_info      #
#####################
"""
CREATE TABLE `site_infos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `crawl_type` varchar(45) DEFAULT NULL,
  `site_name` varchar(120) DEFAULT NULL,
  `site_url` longtext,
  `site_usable` varchar(45) DEFAULT NULL,
  `comment` longtext,
  `classification` varchar(45) DEFAULT NULL COMMENT '数据传到哪个平台',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='关于站点的选择爬取情况\n'
"""


#######################
#   数据表 创建及操作    #
#  tb_      #
#####################
"""
评论内容的表
CREATE TABLE `tb_comment_aigupiao_content` (
  `id` int NOT NULL AUTO_INCREMENT,
  `comment` longtext,
  `publishTime` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存放爱股票文章评论内容'
"""
COMMENT_SQL_GET = 'SELECT `comment` FROM commentdatabase.tb_comment_aigupiao_content;'

"""
关键词段落内容的表
CREATE TABLE `tb_keyparagraph_anxinsc_content` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paragraph` longtext,
  `tag_ori` varchar(60) DEFAULT NULL COMMENT '该段落包含的标签内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存放文章的段落内容'
"""

"""
关联词段落
CREATE TABLE `tb_relativeparagraph_cngold_articlecontent` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paragraph` longtext,
  `referArticleUrl` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='金投网的文章内容'
"""

"""
内容图片表
CREATE TABLE `tb_contentimg_zhidx` (
  `id` int NOT NULL AUTO_INCREMENT,
  `origin_pic_path` longtext,
  `from_url` longtext,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='https://zhidx.com/ 内容图'
"""

"""
缩略图片表
CREATE TABLE `tb_thumbnail_huxiu` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dateline` varchar(45) DEFAULT NULL,
  `formatDate` varchar(45) DEFAULT NULL,
  `origin_pic_path` longtext,
  `pic_path` longtext,
  `title` longtext,
  `user_name` varchar(45) DEFAULT NULL,
  `user_uid` varchar(45) DEFAULT NULL,
  `user_avatar` longtext,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='存放虎嗅网金融地产下的文章信息，包括图片的路径信息'
"""
