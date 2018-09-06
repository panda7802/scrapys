# coding=utf-8

from scrapy import cmdline

import django.core.handlers.wsgi
import sys
import os

if __name__ == "__main__":
    # DJANGO_PROJECT_SCRAPY_PATH = 'D:\lxdzx\lxdzx_server\scrapys'
    DJANGO_PROJECT_PATH = '../../lxdzx_server'
    DJANGO_SETTINGS_MODULE = 'lxdzx_server.settings'

    sys.path.insert(0, DJANGO_PROJECT_PATH)
    # sys.path.insert(0, DJANGO_PROJECT_SCRAPY_PATH)
    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    # application = django.core.handlers.wsgi.WSGIHandler()
    print "===========setting over==========="
    django.setup()
    cmdline.execute("scrapy crawl bili_statistics".split())

    # cmdline.execute("scrapy crawl lxdzx_bili -o obj.csv".split())
    # cmdline.execute("scrapy crawl bili_video".split())
    # cmdline.execute("scrapy crawl bili_video".split())
    # cmdline.execute("scrapy crawl bili_video_detail".split())

    # cmdline.execute("scrapy crawl bili_video_list ".split())

    # cmdline.execute("scrapy crawl bili_video_list -a names=黑马,".split())
    # cmdline.execute("scrapy crawl bili_get_mid -a names=黑马,".split())
    # cmdline.execute("scrapy crawl bili_video_list -a mids=37974444,284797409".split())
