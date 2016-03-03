from datetime import datetime
from data import log

class logger(object):
    def __init__(self):
        self.error_message = ''
        self.level = ''
        self.source = ''
        self.date_created = datetime.now()

    def write_error(self):
        '''do nothing'''


