# coding=utf-8
import commands
import time
from scrapy import cmdline

import django.core.handlers.wsgi
import sys
import os

from subprocess import Popen, PIPE

if __name__ == "__main__":
    while True:
        print "------1------"
        os.system("python single_get_statistics.py")
        time.sleep(5)
        print "------2------"
