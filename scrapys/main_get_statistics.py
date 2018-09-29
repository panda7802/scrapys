# coding=utf-8
import os
import time

if __name__ == "__main__":
    while True:
        print "------1------"
        os.system("python single_get_bili_statistics.py &")
        os.system("python single_get_toutiao_statistics.py &")
        time.sleep(3600)
        print "------2------"
