# -*- coding: utf-8 -*-
import urllib
import urllib2

import scrapy
from scrapy.conf import settings

from scrapys.items import LxdzxBiliItem


def get_curr_url(page_index=1, page_size=30, keyword="留学的真相"):  # 获取当前页面
    # curr_url = "https://search.bilibili.com/all?keyword=" + str(urllib.quote(keyword)) \
    #            + "&from_source=banner_search&page=" + str(page_index)
    curr_url = "https://search.bilibili.com/all?keyword=" + str(urllib.quote(keyword)) \
               + "&from_source=banner_search&page=" + str(page_index)
    return curr_url


class BiliVideoDetailSpider(scrapy.Spider):
    name = 'bili_video_detail'
    allowed_domains = ['search.bilibili.com']

    page_index = 1
    page_size = 30
    start_urls = [get_curr_url(keyword="黑马程序员")]
    video_cookie = ""

    # cookie = settings['COOKIE']
    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Host': 'search.bilibili.com',
        'Upgrade-Insecure-Requests': '1',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0',
        # 'Cookie': 'finger=203273ea; buvid3=C4F974E7-9CDC-4656-B3B5-A47C52F993B112117infoc'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=self.headers, dont_filter=True,
                             cookies={'a': 'b'},  # 似乎只要有就行
                             meta={'cookiejar': True})  # 这里带着cookie发出请求

    def get_list(self, response):
        print "get_list-------------------"
        print 'Cookie', response.request.headers.getlist('Cookie')
        print 'Host', response.request.headers.getlist('Host')
        print 'User-Agent', response.request.headers.getlist('User-Agent')
        print 'Accept', response.request.headers.getlist('Accept')
        print 'recv Cookie ', response.headers.getlist('Set-Cookie')

    def parse(self, response):
        # print response.text
        # "video-contain clearfix"
        video_list = response.xpath(".//*[@class='video-contain clearfix']/li")
        for item in video_list:
            href = str(item.xpath("./a/@href").extract_first())
            title = str(item.xpath("./a/@title").extract_first())
            av_id = str(item.xpath("./div[@class='info']/div[@class='tags']/span[@class='so-icon watch-num']/text()").extract_first())
            print "h : ", href
            print "t : ", title
            print "av_id : ", av_id

            # print "+++++++++" + str(item.xpath(".//*[@class='title']")) + "=====\n"
            # list_item = LxdzxBiliItem()
            # db_item['serial_num'] = item.xpath("./div/div[1]/em/text()").extract_first()

            # print "vl ", video_list
            # err_txt_xpath = ".//div[2]/div[2]/div[2]/div/div[2]/p/text()"
            # err_txt = movie_list = response.xpath(err_txt_xpath).extract_first().strip()
            # print "err_txt : " + err_txt
            # print 'Cookie', response.request.headers.getlist('Cookie')
            # print 'Host', response.request.headers.getlist('Host')
            # print 'User-Agent', response.request.headers.getlist('User-Agent')
            # print 'Accept', response.request.headers.getlist('Accept')
            #
            # recv_cookie = response.headers.getlist('Set-Cookie')
            # print 'recv Cookie ', recv_cookie  # 查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
            # if str(err_txt).index("出错") >= 0:
            #     print "prepare get list"
            # yield scrapy.Request(get_curr_url(), callback=self.get_list,
            #                      cookies=recv_cookie)

            # print "+++++++++++++++++++", response.text
            # s = urllib2.urlopen(get_curr_url()).read()
            # print "==========", s,
