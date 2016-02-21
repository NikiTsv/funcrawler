from data.posts import Posts
from gagspyder import GagSpyder


#for printing purposes
#CURSOR_UP_ONE = '\x1b[1A'
#ERASE_LINE = '\x1b[2K'

def init():
   
    spider = GagSpyder()
    posts = spider.crawl(10,8000)
   
    print('Writing to database...')
    total_inputs = Posts().insert_posts(posts)
    print('Done!')
    print('Total number of inserted rows: ' + str(total_inputs))

init()