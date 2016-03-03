from data.posts import Posts
from data.log import Log
from spyders.gagspyder import GagSpyder
from spyders.quickspyder import QuickSpyder
from spyders.redspyder import RedSpyder
import sys
from datetime import datetime
from models.logdata import LogData

#for printing purposes
#CURSOR_UP_ONE = '\x1b[1A'
#ERASE_LINE = '\x1b[2K'


def spyder_nest_init(chosen_spyder, numberOfPagesOrScrolls, minimumUpvotes, minimumComments):

    f = open('spyder-args-' + str(datetime.now()).replace(' ', '-').replace(':', '-').replace('.', '-'), 'w')
    f.write(chosen_spyder + ' '+ numberOfPagesOrScrolls + ' ' + minimumUpvotes + '\n')
    f.close()
    spyders = []
    spyders = get_spyders()

    #if the application is user started and no arguments are provided
    if chosen_spyder is None and numberOfPagesOrScrolls is None and minimumUpvotes is None:
        chosen_spyder = prompt_spyders(spyders)
        numberOfPagesOrScrolls = prompt_scroll_pages()
        minimumUpvotes = prompt_minimum_upvotes()
        minimumComments = prompt_minimum_comments()

    spyder = spyders[int(chosen_spyder)-1]
    posts = spyder.crawl(int(numberOfPagesOrScrolls), int(minimumUpvotes), int(minimumComments))

    print('Writing to database...')
    total_inputs = Posts().insert_posts(posts)
    print('Done!')
    print('Total number of inserted rows: ' + str(total_inputs))
    f = open('spyder-report-' + str(datetime.now()).replace(' ', '-').replace(':', '-').replace('.', '-'), 'w')
    f.write('Total number of inserted rows: ' + str(total_inputs) + '\n')
    f.close()


def get_spyders():
    spyders = []
    spyders.append(GagSpyder())
    spyders.append(QuickSpyder())
    spyders.append(RedSpyder())
    return spyders


def prompt_spyders(spyders):
    i=1
    for spyder in spyders:
        print(str(i) + ": " + spyder.name)
        i = i+1
    chosen_spyder = input("Select spyder:")
    return chosen_spyder


def prompt_scroll_pages():
    return input("Enter number of pages:")


def prompt_minimum_upvotes():
    return input("Enter required number of upvotes:")


def prompt_minimum_comments():
    return input("Enter required number of comments:")

if __name__ == "__main__":
    try:
        #if arguments are provided on start
        if len(sys.argv) > 1:
            spyder_nest_init(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            spyder_nest_init(None, None, None, None)
    except Exception as ex:
        error = LogData("High", str(ex), "critical", "main", datetime.now())
        log = Log()
        log.write_error(error)


#spyder_nest_init()
