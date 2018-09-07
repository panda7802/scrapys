# -*- coding: utf-8 -*-
import json
import logging
import traceback

import scrapy

from get_web_data.models import VideoNameInfos
from get_web_data.t_video_enums import TSides
from scrapys.items import PlatformStatisticsItem
from tscrapy_utils import t_global_data
from tscrapy_utils.t_err_info import err_urls
from tscrapy_utils.t_global_data import BASE_HEAD, BASE_COOKIES, FLAG_KEY_WORD, FLAG_DATA_ITEM, FLAG_KEY_MID, FLAG_VIDEO

WEB_SIDE = TSides.SIDE_BILI


def get_follows_fans(mid=""):
    """
    获取关注和粉丝
    """
    res = "https://api.bilibili.com/x/relation/stat?vmid=" + mid
    return res


def get_play_article(mid=""):
    """
    获取点击量和阅读数
    """
    res = "https://api.bilibili.com/x/space/upstat?mid=" + mid
    return res


class BiliStatisticSpider(scrapy.Spider):
    """
    B站基本统计
    """
    name = 'bili_statistics'
    allowed_domains = ['space.bilibili.com']
    start_urls = ['http://space.bilibili.com/']

    def __init__(self, *args, **kwargs):
        super(BiliStatisticSpider, self).__init__(*args, **kwargs)
        # 从数据库获取要爬取的项
        self.get_items = VideoNameInfos.objects.filter(get_data=0, platform=1)

    def start_requests(self):
        print "======= 开始获取B站概况 ======="
        # print self.get_items
        for item in self.get_items:
            mid = item.mid
            url = get_follows_fans(mid)  # 获取粉丝数等信息
            data_item = PlatformStatisticsItem()
            data_item['vid'] = item
            print "url : ", url
            yield scrapy.Request(url=url, headers=BASE_HEAD, dont_filter=True,
                                 cookies=BASE_COOKIES,
                                 meta={FLAG_DATA_ITEM: data_item, FLAG_KEY_MID: mid})

    def parse(self, response):
        """
        解析关注、粉丝
        :param response:
        :return:
        """
        try:
            if response.status != 200:
                req_url = response.request.url
                err_urls.append(req_url)
                print "请求错误 : ", req_url, " 错误码 : ", response.status
                return

            data_item = response.meta[FLAG_DATA_ITEM]
            mid = response.meta[FLAG_KEY_MID]

            # 拿到JSON进行解析
            s_json = response.text
            json_data = json.loads(s_json)
            data_item['follows'] = json_data['data']['following']  # 关注
            data_item['fans'] = json_data['data']['follower']  # 粉丝
            url = get_play_article(mid)
            yield scrapy.Request(url=url, headers=BASE_HEAD, dont_filter=True,
                                 cookies=BASE_COOKIES,
                                 meta={FLAG_DATA_ITEM: data_item, FLAG_KEY_MID: mid}, callback=self.parse_play_article)
        except Exception, e:
            traceback.print_exc()

    def parse_play_article(self, response):
        """
        解析阅读、播放
        :param response:
        :return:
        """
        try:
            if response.status != 200:
                req_url = response.request.url
                err_urls.append(req_url)
                print "请求错误 : ", req_url, " 错误码 : ", response.status
                return

            data_item = response.meta[FLAG_DATA_ITEM]
            mid = response.meta[FLAG_KEY_MID]

            # 拿到JSON进行解析
            s_json = response.text
            json_data = json.loads(s_json)
            data_item['clicks'] = json_data['data']['archive']['view']  # 点击量
            data_item['reads'] = json_data['data']['article']['view']  # 阅读数

            # 保存
            # print data_item
            data_item.save()
        except Exception, e:
            traceback.print_exc()
