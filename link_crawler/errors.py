
import traceback as tb
import time

def NO_SITE_FOUND(url, tb):

    print("SITE NOT FOUND ERROR")
    t = time.localtime()
    current_time = time.strftime("Date: %d %b %Y Time: %H:%M:%S", t)

    print("SITE NOT FOUND ERROR")

def UNKNOWN_PAGE(url):

    print("UNKNOWN_PAGE ERROR")
