# coding=utf-8

from scrapy import cmdline

# cmdline.execute("scrapy crawl lxdzx_bili -o obj.csv".split())
# cmdline.execute("scrapy crawl bili_video".split())
cmdline.execute("scrapy crawl bili_video".split())
# cmdline.execute("scrapy crawl bili_video_detail".split())

# print str("出错啦").index("出错") >= 0

