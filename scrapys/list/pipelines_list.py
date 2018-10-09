# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from get_web_data.models import VideoList, VideoDetail
from scrapys.items import LxdzxBiliItem
from scrapys.list import action
from scrapys.list.items_list import TBiliVideoListItem, TBiliMidItem
from tscrapy_utils.t_err_info import err_urls


class TBiliVideoListPipeline(object):
    def __init__(self):
        print "------__init__ BiliVideoListPipeline------"
        # action.write_list_title()
        # action.create_tables()

    def process_item(self, item, spider):
        if isinstance(item, TBiliVideoListItem):
            # action.write_list(item)
            item.save()
        if isinstance(item, TBiliMidItem):
            action.write_mid(item)
        if isinstance(item, LxdzxBiliItem):
            # 判断库中是否有
            # item.save()
            try:
                pre_2_save = VideoList.objects.filter(aid=item['aid']).first()
            except Exception, e:
                logging.error(str(e))

            # 如果数据库存在，则不再添加
            if None is pre_2_save:
                item.save()
                pre_2_save = VideoList.objects.filter(aid=item['aid']).first()

            # 更新详细
            video_detail = VideoDetail()
            video_detail.video = pre_2_save
            video_detail.comment = item['comment']
            video_detail.video_review = item['video_review']
            video_detail.favorites = item['favorites']
            video_detail.play = item['play']
            # print video_detail
            video_detail.save()

        return item

    def close_spider(self, sqider):
        print "------close_spider ScrapysPipeline------"
        # 打印错误
        print "err urls:"
        for err_url in err_urls:
            print err_url + "\n"
