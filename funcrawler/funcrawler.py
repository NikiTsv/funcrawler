from gagspyder import gagspyder
from dataaccess import dataaccess
#for printing purposes
#CURSOR_UP_ONE = '\x1b[1A'
#ERASE_LINE = '\x1b[2K'

def init():
   
    spider = gagspyder()
    posts = spider.crawl(90,15000)
   
    print('Writing to database...')
    total_inputs = dataaccess().insert_posts(posts)
    print('Done!')
    print('Total number of inserted rows: ' + str(total_inputs))

init()