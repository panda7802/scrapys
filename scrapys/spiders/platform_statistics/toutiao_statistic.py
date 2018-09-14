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
from tscrapy_utils.t_global_data import BASE_HEAD, BASE_COOKIES, FLAG_KEY_WORD, FLAG_DATA_ITEM, FLAG_KEY_MID, \
    FLAG_VIDEO, FLAG_COOKIE

WEB_SIDE = TSides.SIDE_BILI


def get_video_count():
    """
    获取播放量和视频数
    """
    res = "https://mp.toutiao.com/xigua/api/data/get-data"
    return res


def get_fans_count():
    """
    获取粉丝数
    :return:
    """
    res = "https://mp.toutiao.com/statistic/profile_stat/"
    return res


def get_cookie_from_str(str=""):
    cookies = {}
    try:
        cookie_items = str.split(";")
        for item in cookie_items:
            kv = item.split("=")
            cookies[kv[0].strip()] = kv[1].strip()
    except Exception, e:
        traceback.print_exc()
    return cookies


class BiliStatisticSpider(scrapy.Spider):
    """
    B站基本统计
    """
    name = 'toutiao_statistics'
    allowed_domains = ['space.bilibili.com']
    start_urls = ['http://space.bilibili.com/']

    def __init__(self, *args, **kwargs):
        super(BiliStatisticSpider, self).__init__(*args, **kwargs)
        # 从数据库获取要爬取的项
        self.get_items = VideoNameInfos.objects.filter(get_data=0, platform=2)

    def start_requests(self):
        print "======= 开始获取头条概况 ======="
        for item in self.get_items:
            data_item = PlatformStatisticsItem()
            data_item['vid'] = item
            s_cookie = 'UM_distinctid=165adc7e71711-0b35612dd6f3a88-16347940-1fa400-165adc7e718645; tt_webid=6598009680210707971; ccid=f9edb1ae7545d9ccc8a8ad20cc85da32; sso_uid_tt=3ce44faae230094f7f6b927e491c0489; toutiao_sso_user=d1a0a66054a78e9b10b770f633dbe86e; sso_login_status=1; login_flag=a01cce2fd70988b136d8b39e4f6d889f; uid_tt=d34ee18a99085da284d107e58484b73d; sid_guard="d254f79b9ee58eb8cacf9336621d99ff|1536218916|15552000|Tue\054 05-Mar-2019 07:28:36 GMT"; uuid="w:f3a93bfdc45846c1977cec12aedce56a"; __tea_sdk__ssid=a1327d39-5b0c-4f4b-83c5-64bcd9f0d303; _mp_test_key_1=5bbf0577fff3abc5775c0fc6e0e4536e; tt_im_token=1536904286437629942738282838299430575624416090630086523993925706; sessionid=b3612d4303a7c97fc09a62bc325c5428'
            cookies = get_cookie_from_str(s_cookie)
            url = get_fans_count()
            yield scrapy.Request(url=url, headers=BASE_HEAD, dont_filter=True,
                                 cookies=cookies,
                                 meta={FLAG_DATA_ITEM: data_item, FLAG_COOKIE: cookies})

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
            cookies = response.meta[FLAG_COOKIE]

            # 拿到JSON进行解析
            s_json = response.text
            json_data = json.loads(s_json)
            data_item['fans'] = json_data['data']['total_subscribe_count']
            data_item['clicks'] = json_data['data']['play_effective_count']
            data_item['reads'] = json_data['data']['go_detail_count']
            data_item.save()
            # url=get_video_count()
            # yield scrapy.Request(url=url, headers=BASE_HEAD, dont_filter=True,
            #                      cookies=BASE_COOKIES,
            #                      meta={FLAG_DATA_ITEM: data_item, FLAG_COOKIE: cookies}), callback=self.parse_play_article)
        except Exception, e:
            traceback.print_exc()
