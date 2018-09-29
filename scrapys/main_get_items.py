# coding=utf-8
import os
import time

if __name__ == "__main__":
    while True:
        print "------1 video ------"
        os.system("python single_get_bili_video.py &")
        time.sleep(3600)
        print "------2 video ------"
