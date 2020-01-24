from database import db
import htb


class NullUser(object):

    def __init__(self, userId):
        self.userId = userId