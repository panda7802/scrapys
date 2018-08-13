# -*- coding: utf-8 -*-
import json
import logging
import traceback

import scrapy
import sys

from scrapys.items import LxdzxBiliItem
from tutils.t_err_info import err_urls
from tutils.t_global_data import *

reload(sys)
sys.setdefaultencoding("utf-8")


# 获取当前页面
def get_curr_url(page_index=1, page_size=30, mid="22500342"):
    # FIXME
    # mid = "37974444"
    curr_url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + str(mid) \
               + "&pagesize=" + str(page_size) \
               + "&tid=0&page=" + str(page_index) + "&keyword=&order=pubdate"
    return curr_url


def get_view_url(aid="0"):
    # curr_url = "https://www.bilibili.com/video/" + aid
    curr_url = "https://comment.bilibili.com/playtag,49971844-" + str(aid) + "?html5=1"
    return curr_url


class BiliVideoSpider(scrapy.Spider):
    name = 'bili_video'
    allowed_domains = ['space.bilibili.com']
    page_index = 1
    page_size = 50

    start_urls = [get_curr_url(page_index)]

    # start_urls = [get_view_url("28834788")]

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=BASE_HEAD, dont_filter=True,
                             cookies=BASE_COOKIES,  # 似乎只要有就行
                             meta={'cookiejar': True})  # 这里带着cookie发出请求

    def get_detail(self, response):  # 关联
        if response.status != 200:
            req_url = response.request.url
            err_urls.append(req_url)
            print "get_detail请求错误 : ", req_url, " 错误码 : ", response.status
            return

        parent_item = response.meta['item']
        s_json = response.text.decode('unicode_escape')
        if len(s_json) <= 10:
            yield parent_item
            return

        gl_list = json.loads(s_json)  # 关联list
        if len(gl_list):
            for item in gl_list:
                try:
                    s_items = str(item).split(",")
                    parent_item["gl_title"] = eval(str(s_items[2]))  # 标题
                    parent_item["gl_url"] = "https://www.bilibili.com/video/av" + (s_items[1]).strip()
                    yield parent_item
                except Exception, e:
                    traceback.print_exc()
        else:
            yield parent_item

    def parse(self, response):
        print "+++++++++++++++ start parse " + str(self.page_index) + "+++++++++++++++\n"

        if response.status != 200:
            req_url = response.request.url
            err_urls.append(req_url)
            print "请求错误 : ", req_url, " 错误码 : ", response.status
            return

        s_json = response.text  # .decode('unicode_escape')
        # print "response : ", s_json
        status = json.loads(s_json)['status']
        if not status:
            logging.error("==========状态异常 status is err ==========")
            return

        # 视频列表
        vlist = json.loads(s_json)['data']['vlist']
        # 处理
        for item in vlist:
            bili_item = LxdzxBiliItem()
            for show_item in bili_show_list:
                try:
                    key = show_item[0]
                    bili_item[key] = str(item[key])
                except Exception, e:
                    traceback.print_exc()
            yield bili_item
            # aid = bili_item['aid']
            # detal_url = get_view_url(aid)
            # print "detal_url:", detal_url
            # yield scrapy.Request(url=detal_url, headers=BASE_HEAD, dont_filter=True,
            #                      cookies=BASE_COOKIES,
            #                      meta={'item': bili_item}, callback=self.get_detail)
        # return
        # 下一页
        self.page_index += 1
        print "page_index : ", self.page_index
        if len(vlist) >= self.page_size:
            if self.page_index > 2:
                return
            next_url = get_curr_url(self.page_index)
            print "next_url:", next_url
            yield scrapy.Request(url=next_url, headers=BASE_HEAD, dont_filter=True,
                                 cookies=BASE_COOKIES,
                                 meta={'item': bili_item}, callback=self.parse)
