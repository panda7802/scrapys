# -*- coding: utf-8 -*-
import traceback

import scrapy

from scrapys.list.items_list import TBiliMidItem
from tscrapy_utils import t_global_data
from tscrapy_utils.t_global_data import BASE_HEAD, BASE_COOKIES, FLAG_KEY_WORD


def get_mid_url(keyword=""):
    """
    获取mid
    """
    get_mid_url = "https://search.bilibili.com/upuser?keyword=%s" % keyword
    return get_mid_url


class BiliGetMidSpider(scrapy.Spider):
    name = 'bili_get_mid'
    allowed_domains = ['space.bilibili.com']
    start_urls = ['http://space.bilibili.com/']

    def __init__(self, names=None, *args, **kwargs):
        super(BiliGetMidSpider, self).__init__(*args, **kwargs)
        self.obj_names = names
        if None is self.obj_names:
            self.obj_names = ""

    def start_requests(self):
        if self.obj_names.find(",") <= 0:
            return
        t_global_data.obj_projects.clear()
        keywords = self.obj_names.split(",")
        print "======= 开始获取mids ======="
        for keyword in keywords:
            if keyword.__len__() <= 0:
                continue
            url = get_mid_url(keyword)
            yield scrapy.Request(url=url, headers=BASE_HEAD, dont_filter=True,
                                 cookies=BASE_COOKIES,  # 似乎只要有就行
                                 meta={FLAG_KEY_WORD: keyword})

    def parse(self, response):
        """
        接下获取mid
        :param response:
        :return:
        """
        keyword = response.meta[FLAG_KEY_WORD]
        value = ""
        try:
            mid_list = response.xpath(".//*[@class='user-list']/li")
            for item in mid_list:
                href = str(item.xpath("./div[@class='up-face']/a/@href").extract_first())
                mid = str(href.split("?")[0].split("com/")[1])
                name = str(item.xpath("./div[@class='up-face']/a/@title").extract_first())
                if name.__len__() <= 0:
                    continue
                mid_item = TBiliMidItem()
                mid_item['mid'] = mid
                mid_item['name'] = name
                yield mid_item
        except Exception, e:
            traceback.print_exc()
