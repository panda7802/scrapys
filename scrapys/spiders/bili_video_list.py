# -*- coding: utf-8 -*-
import json
import logging
import traceback

import scrapy
import sys

from scrapys.list.items_list import TBiliVideoListItem
from tutils import t_global_data
from tutils.t_err_info import err_urls
from tutils.t_global_data import *

reload(sys)
sys.setdefaultencoding("utf-8")

LIST_PAGE_SIZE = 30


def get_list_url(page_index=1, page_size=LIST_PAGE_SIZE, mid="22500342", order="pubdate"):
    """
    获取当前页面
    :param page_index:
    :param page_size:
    :param mid:
    :param order:
    :return:
    """
    curr_url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + str(mid) \
               + "&pagesize=" + str(page_size) \
               + "&tid=0&page=" + str(page_index) + "&keyword=&order=" + order
    return curr_url


def get_view_url(aid="0"):
    # curr_url = "https://www.bilibili.com/video/" + aid
    curr_url = "https://comment.bilibili.com/playtag,49971844-" + str(aid) + "?html5=1"
    return curr_url


def is_err_url(response):  # 是否为错误URL
    if response.status != 200:
        req_url = response.request.url
        err_urls.append(req_url)
        print "请求错误 : ", req_url, " 错误码 : ", response.status
        return True
    else:
        return False


class BiliVideoListSpider(scrapy.Spider):
    name = 'bili_video_list'
    allowed_domains = ['space.bilibili.com']
    start_urls = [""]

    def __init__(self, mids=None, *args, **kwargs):
        super(BiliVideoListSpider, self).__init__(*args, **kwargs)
        self.mids = mids
        if None is self.mids:
            self.mids = ""

    def start_requests(self):
        print "开始获取列表 : ", self.mids
        s_mid = str(self.mids)
        if len(s_mid) <= 1 and s_mid.find(",") <= 0:
            print "没有mid，无需爬虫"
            return
        self.mids = s_mid.split(",")

        for mid in self.mids:
            if len(mid) <= 0:
                continue
            print "开始解析 ： ", get_list_url(mid=mid)
            yield scrapy.Request(url=get_list_url(mid=mid), headers=BASE_HEAD, dont_filter=True,
                                 cookies=BASE_COOKIES,  # 似乎只要有就行
                                 meta={FLAG_PAGE_INDEX: 1, FLAG_KEY_WORD: mid})

    def parse(self, response):
        page_index = response.meta[FLAG_PAGE_INDEX]
        mid = response.meta[FLAG_KEY_WORD]
        print "+++++++++++++++ start parse ", mid \
            , " index : ", str(response.meta[FLAG_PAGE_INDEX]), "+++++++++++++++\n"

        if is_err_url(response):
            return

        s_json = response.text  # .decode('unicode_escape')
        status = json.loads(s_json)['status']
        if not status:
            logging.error("==========状态异常 status is err ==========")
            return

        # 视频列表
        vlist = json.loads(s_json)['data']['vlist']
        # 处理
        for item in vlist:
            list_item = TBiliVideoListItem()
            for show_item in bili_show_list:
                try:
                    key = show_item[0]
                    list_item[key] = str(item[key])
                except Exception, e:
                    traceback.print_exc()
            yield list_item
        page_index += 1  # 下一页
        print "page_index : ", page_index
        # if len(vlist) >= LIST_PAGE_SIZE:
        #     next_url = get_mid_url(page_index=page_index, mid=mid)
        #     print "next_url:", next_url
        #     yield scrapy.Request(url=next_url, headers=BASE_HEAD, dont_filter=True,
        #                          cookies=BASE_COOKIES,
        #                          meta={FLAG_PAGE_INDEX: page_index, FLAG_KEY_WORD: mid}, callback=self.parse)
