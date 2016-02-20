import datetime
from datetime import datetime

class PostData(object):
    '''post'''
    title = ''
    content =''
    contentType = ''
    contentUrl = ''
    points = 0
    date_created = datetime.now().date()
    
    def __init__(self, title, content, contentType, contentUrl, points):
        self.title = title        
        self.content = content
        self.contentType = contentType
        self.contentUrl = contentUrl
        self.points = points
        self.date_created =  datetime.now().date()

