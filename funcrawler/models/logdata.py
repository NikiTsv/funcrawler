from datetime import datetime


class LogData(object):
    level = ''
    message = ''
    source = ''
    date_created = datetime.now()

    def __init__(self, level, message, source, date_created):
        self.level = level
        self.message = message
        self.source = source
        self.date_created = date_created

