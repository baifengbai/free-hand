from core.base.poster.base import BasePoster

class Poster_Comment(BasePoster):
    def __init__(self, interface):
        self.interface = interface

    def update_postedurldb(self, item):
        sql = "INSERT INTO `postedurldatabase`.`tb_comment_posted` (`comment`) VALUES (\'{}\');".format(item[0].strip())
        return self.dbOperator.insertData2DB(sql)

