from datetime import datetime


class LogData(object):
    level = ''
    message = ''
    source = ''
    date_created = datetime.now()

    def __init__(self, message, source):
        self.message = message
        self.source = source


