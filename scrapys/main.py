# coding=utf-8

from scrapy import cmdline

# cmdline.execute("scrapy crawl lxdzx_bili -o obj.csv".split())
# cmdline.execute("scrapy crawl bili_video".split())
# cmdline.execute("scrapy crawl bili_video".split())
# cmdline.execute("scrapy crawl bili_video_detail".split())

# cmdline.execute("scrapy crawl bili_video_list ".split())

# cmdline.execute("scrapy crawl bili_video_list -a names=黑马,".split())
# cmdline.execute("scrapy crawl bili_get_mid -a names=黑马,".split())
cmdline.execute("scrapy crawl bili_video_list -a mids=37974444,284797409".split())
