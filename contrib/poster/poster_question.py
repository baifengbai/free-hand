from core.base.poster.base import BasePoster

class Poster_Question(base_poster.Base_Poster):
    def __init__(self, interface='http://121.40.187.51:8088/api/question_get'):
        self.interface = interface