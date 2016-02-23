from data.posts import Posts
from spyders.gagspyder import GagSpyder
from spyders.quickspyder import QuickSpyder


#for printing purposes
#CURSOR_UP_ONE = '\x1b[1A'
#ERASE_LINE = '\x1b[2K'

def spyder_nest_init():

    spyders = []
    spyders = get_spyders()

    i=1
    for spyder in spyders:
        print(str(i) + ": " + spyder.name)
        i = i+1

    chosen_spyder = input("Select spyder:")
    spyder = spyders[int(chosen_spyder)-1]
    posts = spyder.crawl(10,8000,500)
   
    print('Writing to database...')
    total_inputs = Posts().insert_posts(posts)
    print('Done!')
    print('Total number of inserted rows: ' + str(total_inputs))

def get_spyders():
    spyders = []
    spyders.append(GagSpyder())
    spyders.append(QuickSpyder())
    return spyders

spyder_nest_init()