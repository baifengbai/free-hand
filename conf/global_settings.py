# 浏览器引擎位置 全局通用
DRIVER_SELENIUM_PATH = r'E:\Projects\webDriver\chrome\chromedriver.exe'

"""
Default FREEHAND settings. Override these with settings in the module pointed to
by the FREEHAND_SETTINGS_MODULE environment variable.
"""
####################
# AUTHENTICATION   #
####################
AUTHENTICATION = {
    'userName':'qin',
    'password':'qin123456',
    'key': ''
}

# 待上传的资源的目录路径 注意这里的路径最后加\\的
RESOURCEPATH = {
    'thumbnail_dir_path': '',
    'contentimgs_dit_path': ''
}

#########################################
#           数据库表命名的规范             #
#   tb_ + 类型 + _ + 站点名 + _content    #
#   如： tb_comment_xueqiu_content       #
#   涉及主要字段如下：                     #
#   title                               #
#   content/comment              #
#   keyword                      #
#   rekeyword                    #
#   question                     #
#   answer                       #
#########################################



#########################################
#           API_Params                  #
#   做一个统一的规范                       #
#   对于从数据库获取的记录，指定好对应字段位置  #
#   SQL语句也要写明对应要获取的字段名         #
#   涉及字段如下：                         #
#   title                   item[0]     #
#   content/comment         item[1]     #
#   keyword                 item[2]     #
#   rekeyword               item[3]     #
#   question                item[4]     #
#   answer                  item[5]     #
#########################################
API_PARAMS_DICT = {
    'default':{
        "account": AUTHENTICATION['userName'],
        "password": AUTHENTICATION['password'],
        "key": ''
    },
    'keyParagraph':{
        "key": '',
        "account": '',
        "password": '',
        'content': '',
        'keyword': '',
        'rekeyword': '配资'
    },
    'relativeParagraph':{
        "key": '',
        "account": '',
        "password": '',
        'content': '',
        'keyword': ''
    },
    'articleComment':{
        "key": '',
        "account": '',
        "password": '',
        'title': '',
        'content': ''
    },
    'question':{
        "key": '',
        "account": '',
        "password": '',
        'question': '',
        'answer': ''
    }
}

####################
# CORE             #
####################
# Database connection info. If left empty, will default to the dummy backend.
DATABASES = {
    'USER':'root',
    'PASSWORD':'root',
    'HOST': 'localhost',
    'PORT': '3306',
    'DBNAME': 'data_usable_database',
}

# Classes used to implement DB routing behavior.
DATABASE_ROUTERS = []

# List of strings representing installed apps.
INSTALLED_APPS = []


# Default file storage mechanism that holds media.
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


# Default formats to be used when parsing dates from input boxes, in order
# See all available format string here:
# https://docs.python.org/library/datetime.html#strftime-behavior
# * Note that these format strings are different from the ones to display dates
DATE_INPUT_FORMATS = [
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',             # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',             # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',             # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',             # '25 October 2006', '25 October, 2006'
]

# Default formats to be used when parsing times from input boxes, in order
# See all available format string here:
# https://docs.python.org/library/datetime.html#strftime-behavior
# * Note that these format strings are different from the ones to display dates
TIME_INPUT_FORMATS = [
    '%H:%M:%S',     # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
    '%H:%M',        # '14:30'
]

# Default formats to be used when parsing dates and times from input boxes,
# in order
# See all available format string here:
# https://docs.python.org/library/datetime.html#strftime-behavior
# * Note that these format strings are different from the ones to display dates
DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
]


##############
# MIDDLEWARE #
##############

# List of middleware to use. Order is important; these
# middleware will be applied in the order given
MIDDLEWARE = []


###########
# LOGGING #
###########
# The callable to use to configure logging
LOGGING_CONFIG = 'logging.config.dictConfig'

# Custom logging configuration.
LOGGING = {}

# Default exception reporter class used in case none has been
# specifically assigned to the HttpRequest instance.
DEFAULT_EXCEPTION_REPORTER = 'django.views.debug.ExceptionReporter'

# Default exception reporter filter class used in case none has been
# specifically assigned to the HttpRequest instance.
DEFAULT_EXCEPTION_REPORTER_FILTER = 'django.views.debug.SafeExceptionReporterFilter'

###########
# TESTING #
###########

# The name of the class to use to run the test suite
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Apps that don't need to be serialized at test database creation time
# (only apps with migrations are to start with)
TEST_NON_SERIALIZED_APPS = []



