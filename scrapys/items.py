# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem

from get_web_data.models import VideoList, PlatformStatistics, VideoDetail


class ScrapysItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LxdzxBiliItem(DjangoItem):
    django_model = VideoList


class LxdzxBiliItemDetail(DjangoItem):
    django_model = VideoDetail


class PlatformStatisticsItem(DjangoItem):
    django_model = PlatformStatistics

# class LxdzxBiliItem(scrapy.Item):
#     title = scrapy.Field()  # 标题
#     subtitle = scrapy.Field()  # 子标题
#     comment = scrapy.Field()  # 评论数
#     created = scrapy.Field()  # 创建时间
#     video_review = scrapy.Field()  # 弹幕数
#     favorites = scrapy.Field()  # 收藏量
#     length = scrapy.Field()  # 长度
#     play = scrapy.Field()  # 播放量
#     author = scrapy.Field()  # 作者
#     review = scrapy.Field()
#     typeid = scrapy.Field()  # 类型
#     pic = scrapy.Field()  # 图片
#     description = scrapy.Field()  # 描述
#     aid = scrapy.Field()  # 详细信息id
#     mid = scrapy.Field()  # 当前id
#     copyright = scrapy.Field()  # 版权
#     hide_click = scrapy.Field()  # 不可点击
#     #
#     gl_title = scrapy.Field()  # 关联标题
#     gl_url = scrapy.Field()  # 关联url
