# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapys.list import action
from scrapys.list.items_list import TBiliVideoListItem, TBiliMidItem
from tutils.t_err_info import err_urls


class TBiliVideoListPipeline(object):
    def __init__(self):
        print "------__init__ BiliVideoListPipeline------"
        action.write_list_title()
        # action.create_tables()

    def process_item(self, item, spider):
        if isinstance(item, TBiliVideoListItem):
            action.write_list(item)
            # action.write_list2db(item)
        if isinstance(item, TBiliMidItem):
            action.write_mid(item)

        return item

    def close_spider(self, sqider):
        print "------close_spider ScrapysPipeline------"
        # 打印错误
        print "err urls:"
        for err_url in err_urls:
            print err_url + "\n"
