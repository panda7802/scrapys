# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EmptyItem(scrapy.Item):
    pass


class TBiliVideoListItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    subtitle = scrapy.Field()  # 子标题
    comment = scrapy.Field()  # 评论数
    created = scrapy.Field()  # 创建时间
    video_review = scrapy.Field()  # 弹幕数
    favorites = scrapy.Field()  # 收藏量
    length = scrapy.Field()  # 长度
    play = scrapy.Field()  # 播放量
    author = scrapy.Field()  # 作者
    review = scrapy.Field()
    typeid = scrapy.Field()  # 类型
    pic = scrapy.Field()  # 图片
    description = scrapy.Field()  # 描述
    aid = scrapy.Field()  # 详细信息id
    mid = scrapy.Field()  # 当前id
    copyright = scrapy.Field()  # 版权
    hide_click = scrapy.Field()  # 不可点击
