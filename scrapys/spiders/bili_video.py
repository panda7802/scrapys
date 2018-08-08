# -*- coding: utf-8 -*-
import json
import traceback

import scrapy
import sys

from scrapys.items import LxdzxBiliItem
from tutils.tglobal_data import lxdzx_bili_show_list

reload(sys)
sys.setdefaultencoding("utf-8")


# 获取当前页面
def get_curr_url(page_index=1, page_size=30):
    curr_url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid=22500342&" \
               "pagesize=" + str(page_size) + "&tid=0&page=" + str(page_index) + "&keyword=&order=pubdate"
    return curr_url


class BiliVideoSpider(scrapy.Spider):
    name = 'bili_video'
    allowed_domains = ['space.bilibili.com']
    page_index = 1
    page_size = 30

    start_urls = [get_curr_url(page_index)]

    def parse(self, response):
        print "+++++++++++++++ start parse " + str(self.page_index) + "+++++++++++++++\n"
        s_json = response.text  # .decode('unicode_escape')

        # print "s_json : ", s_json
        vlist = json.loads(s_json)['data']['vlist']
        len_vlist = len(vlist)

        # 处理
        for item in vlist:
            bili_item = LxdzxBiliItem()
            for show_item in lxdzx_bili_show_list:
                try:
                    key = show_item[0]
                    bili_item[key] = str(item[key])  # .decode('unicode_escape').encode("gbk", "ignore")
                except Exception, e:
                    traceback.print_exc()
            yield bili_item

        # FIXME 单页
        # # 下一页
        # self.page_index += 1
        # if len_vlist >= self.page_size:
        #     next_url = get_curr_url(self.page_index)
        #     print "next_url:", next_url
        #     yield scrapy.Request(next_url, callback=self.parse)
