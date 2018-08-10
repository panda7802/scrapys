# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback

import time

from tutils.err_info import err_urls
from tutils.tglobal_data import lxdzx_bili_show_list
from openpyxl import Workbook


class ScrapysPipeline(object):
    filename = "obj.xls"

    def __init__(self):
        print "------__init__ ScrapysPipeline------"
        del err_urls[:]
        title_list = []
        for item in lxdzx_bili_show_list:
            title_list.append(item[1])
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(title_list)  # 设置表头
        self.start_row = 1
        self.end_row = 1  # len(lxdzx_bili_show_list)
        self.start_column = 1
        self.end_column = self.start_column

    def process_item(self, item, spider):
        print "======process_item==========="
        line = []
        for show_item in lxdzx_bili_show_list:
            try:
                key = show_item[0]
                value = item[key].replace("\n", " ").replace("\r", " ").replace(",", " ").strip()
                if key == 'created':  # 时间转换
                    value = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(long(value)))
                line.append(value)
            except Exception, e:
                traceback.print_exc()

        Li = []
        Li.append(line)
        Li.append(line)
        Li.append(line)
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        # self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        # self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        # while item in Li:
        #     self.ws.append(item)
        # # 合并
        # for each in Li:
        #     self.end_row = self.start_row + len(each) - 1
        #     self.ws.merge_cells(start_row=self.start_row, end_row=self.end_row, start_column=self.start_column,
        #                         end_column=self.end_column)
        #     self.start_column = self.end_column + 1

        self.wb.save(self.filename)  # 保存xlsx文件
        return item

    def close_spider(self, sqider):
        print "------close_spider ScrapysPipeline------"
        print "err urls:"
        for err_url in err_urls:
            print err_url + "\n"


class LxdzxBiliPipeline(object):
    def __init__(self):
        print "------__init__ LxdzxBiliPipeline------"
        del err_urls[:]
        self.filename = open("lxdzx_bili.csv", "wb")
        for show_item in lxdzx_bili_show_list:
            try:
                key = show_item[1]
                self.filename.write(key + ",")
            except Exception, e:
                traceback.print_exc()
        self.filename.write("\n")

    def process_item(self, item, spider):
        value = ""
        for show_item in lxdzx_bili_show_list:
            try:
                key = show_item[0]
                value = item[key].replace("\n", " ").replace("\r", " ").replace(",", " ").strip()
                if key == 'created':  # 时间转换
                    self.filename.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(long(value))) + ",")
                else:
                    self.filename.write(value + ",")
            except Exception, e:
                traceback.print_exc()
        self.filename.write("\n")
        return item

    def close_spider(self, sqider):
        print "------close_spider LxdzxBiliPipeline------"
        print "err urls:"
        for err_url in err_urls:
            print err_url + "\n"
        self.filename.close()
