# coding=utf-8

from scrapy import cmdline

# cmdline.execute("scrapy crawl douban_spider".split())
# cmdline.execute("scrapy crawl douban_spider -o obj.json".split())
# cmdline.execute("scrapy crawl douban_spider -o obj.csv".split())
# cmdline.execute("scrapy crawl lxdzx_bili -o obj.csv".split())
cmdline.execute("scrapy crawl bili_video".split())


# s = "1:1:30"
# s1 = "1:0"
# print s[0:s.index(":", 3)]
# print s1.index(":",2)
