# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback

import time

from openpyxl.styles import Alignment

from tutils.err_info import err_urls
from tutils.tglobal_data import *
from openpyxl import Workbook


class ScrapysPipeline(object):
    filename = "obj.xls"

    def __init__(self):
        print "------__init__ ScrapysPipeline------"
        del err_urls[:]
        title_list = []
        # 打印表头
        for item in lxdzx_bili_show_list:
            title_list.append(item[1])
        for item in lxdzx_bili_detail_list:
            title_list.append(item[1])

        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(title_list)  # 设置表头
        self.start_row = 1
        self.end_row = 1  # len(lxdzx_bili_show_list)
        self.start_column = 1
        self.end_column = self.start_column
        self.wb.save(self.filename)  # 保存xlsx文件

    def process_item(self, item, spider):
        # print "======process_item==========="
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

        for show_item in lxdzx_bili_detail_list:
            try:
                key = show_item[0]
                value = item[key].replace("\n", " ").replace("\r", " ").replace(",", " ").strip()
                line.append(value)
            except Exception, e:
                traceback.print_exc()

        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
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

        last_title = ""
        curr_index = 0  # 当前合并的行号
        start_index = 0  # 开始合并的行号
        # 合并单元格
        print "=======合并单元格======="
        # for row in self.ws.rows:
        #     if 0 == curr_index:
        #         curr_index += 1
        #         continue
        #     curr_index += 1
        #     title = row[0].value
        #     if title == last_title:
        #         for index in range(len(lxdzx_bili_show_list)):
        #             self.ws.merge_cells(start_row=start_index, start_column=index + 1,
        #                                 end_row=curr_index, end_column=index + 1)
        #     else:
        #         last_title = title
        #         start_index = curr_index
        # self.wb.save(self.filename)  # 保存xlsx文件

        # 打印错误
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
