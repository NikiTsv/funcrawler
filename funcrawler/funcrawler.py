from gagspyder import gagspyder
from dataaccess import dataaccess
#for printing purposes
#CURSOR_UP_ONE = '\x1b[1A'
#ERASE_LINE = '\x1b[2K'

def init():
    #make this return list of PostData
    spider = gagspyder()
    posts = spider.crawl(2)
    #save post data
    #try:
    print('Writing to database...')
    dataaccess().insert_posts(posts)
    print('Done!')
    #except: 
    #    raise
        #print('There was an error when writing to database')
init()