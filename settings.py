from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTHENTICATION = {
    'userName':'qin',
    'password':'qin123456',
    'key': ''
}


# Application definition
INSTALLED_APPS = [

]

MIDDLEWARE = [

]


# Database
DATABASES = {
    'default': {
        'ENGINE': 'freehand.db.backends.mysql',
        'NAME': 'spider_visualpanel_database',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'root'
    }
}