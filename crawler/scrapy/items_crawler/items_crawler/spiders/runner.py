import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    execute(
        [
            'scrapy',
            'crawl',
            'bhid_crawler',
            '-t',
            'csv',
            '-o',
            'items.csv',
        ]
    )
except SystemExit:
    pass