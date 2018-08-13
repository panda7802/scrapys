# -*- coding: utf-8 -*-
import json
import logging
import traceback

import scrapy
import sys

from scrapys.list.items_list import TBiliVideoListItem
from tutils.t_err_info import err_urls
from tutils.t_global_data import *

reload(sys)
sys.setdefaultencoding("utf-8")

LIST_PAGE_SIZE = 30


# 获取当前页面
def get_curr_url(page_index=1, page_size=LIST_PAGE_SIZE, mid="22500342", order="pubdate"):
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

    def start_requests(self):
        for key in obj_projects:
            yield scrapy.Request(url=get_curr_url(mid=key), headers=BASE_HEAD, dont_filter=True,
                                 cookies=BASE_COOKIES,  # 似乎只要有就行
                                 meta={FLAG_PAGE_INDEX: 1, FLAG_KEY_WORD: key})

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

        # 下一页
        page_index += 1
        print "page_index : ", page_index
        if len(vlist) >= LIST_PAGE_SIZE:
            next_url = get_curr_url(page_index=page_index, mid=mid)
            print "next_url:", next_url
            yield scrapy.Request(url=next_url, headers=BASE_HEAD, dont_filter=True,
                                 cookies=BASE_COOKIES,
                                 meta={FLAG_PAGE_INDEX: page_index, FLAG_KEY_WORD: mid}, callback=self.parse)
