from core.base.poster.base import BasePoster

class Poster_Question(BasePoster):
    def __init__(self, interface='http://121.40.187.51:8088/api/question_get'):
        self.interface = interface