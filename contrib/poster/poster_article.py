from core.base.poster.base import BasePoster

class Poster_Article(BasePoster):
    def __init__(self, interface='http://121.40.187.51:8088/api/article_get'):
        self.interface = interface