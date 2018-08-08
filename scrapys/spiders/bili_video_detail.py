# -*- coding: utf-8 -*-
import scrapy


class BiliVideoDetailSpider(scrapy.Spider):
    name = 'bili_video_detail'
    allowed_domains = ['space.bilibili.com']
    start_urls = ['http://space.bilibili.com/']

    def parse(self, response):
        pass
