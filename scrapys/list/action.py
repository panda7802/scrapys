# coding=utf-8
import traceback

import openpyxl
import time

import os

from openpyxl import Workbook

from tutils.t_err_info import err_urls
from tutils.t_global_data import obj_projects, bili_show_list


def get_file_name(name):
    obj_dir = "result"
    is_exists = os.path.exists(obj_dir)
    # 判断结果
    if not is_exists:
        # 如果不存在则创建目录
        os.makedirs(obj_dir)
    file_name = obj_dir + "/" + name.decode('utf-8').encode('gbk') + ".xlsx"
    return file_name


def write_list(item):  # 写List
    line = []
    for show_item in bili_show_list:
        try:
            key = show_item[0]
            value = item[key].replace("\n", " ").replace("\r", " ").replace(",", " ").strip()
            if key == 'created':  # 时间转换
                value = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(long(value)))
            line.append(value)
        except Exception, e:
            traceback.print_exc()

    wb = openpyxl.load_workbook(get_file_name(obj_projects[item["mid"]]))
    ws = wb.active
    ws.append(line)  # 将数据以行的形式添加到xlsx中
    wb.save(get_file_name(obj_projects[item["mid"]]))  # 保存xlsx文件


def write_list_title():  # 写excel标题
    for key in obj_projects:
        del err_urls[:]
        title_list = []
        # 打印表头
        for item in bili_show_list:
            title_list.append(item[1])

        wb = Workbook()
        ws = wb.active
        ws.append(title_list)  # 设置表头
        wb.save(get_file_name(obj_projects[key]))  # 保存xlsx文件
