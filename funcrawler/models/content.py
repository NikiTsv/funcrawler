

class Content(object):

    type = ''
    src = ''
    thumbnail = ''

    def __init__(self, type, src, thumbnail):
        self.type = type
        self.src = src
        self.thumbnail = thumbnail

    def __init__(self):
        type = ''
        src = ''
        thumbnail = ''
