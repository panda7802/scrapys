# coding=utf-8
import commands
import time
from scrapy import cmdline

import django.core.handlers.wsgi
import sys
import os

from subprocess import Popen, PIPE

if __name__ == "__main__":
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
