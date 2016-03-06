import datetime
from datetime import datetime

class PostModel(object):
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
        self.date_created = datetime.now().date()


class PostWpModel(object):
    '''post'''

    #might be overridden in dataaccess generate wpmodel method
    post_author = ""
    post_date = ""
    post_date_gmt = datetime.now()
    #converts imageUrl to html image
    post_content = ""
    post_title =""
    post_excerpt = ""
    ping_status = "closed"
    post_status = "publish"
    comment_status = "open"
    post_password = ""
    post_name =""
    to_ping = ""
    pinged = ""
    post_modified = datetime.now()
    post_modified_gmt = datetime.now()
    post_content_filtered = ""
    post_parent = 0 #??
    guid = "http://www.4dlols.com/?p=" #insert id after =
    menu_order = 1
    post_type = "post"
    post_mime_type = "" #??
    comment_count = ""

    #TODO INIT METHOD

