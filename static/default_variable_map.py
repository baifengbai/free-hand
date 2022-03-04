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
#   数据表操作        #
#  tb_      #
#####################
COMMENT_SQL_GET = 'SELECT `comment` FROM commentdatabase.tb_comment_aigupiao_content;'