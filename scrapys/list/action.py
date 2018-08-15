# coding=utf-8
import sqlite3
import traceback

import openpyxl
import time

import os

from openpyxl import Workbook

from tutils import t_global_data
from tutils.t_err_info import err_urls
from tutils.t_global_data import obj_projects, bili_show_list


def get_file_name(name):
    """
    获取文件名
    :param name:
    :return:
    """
    obj_dir = "result"
    is_exists = os.path.exists(obj_dir)
    # 判断结果
    if not is_exists:
        # 如果不存在则创建目录
        os.makedirs(obj_dir)
    file_name = obj_dir + "/" + name.decode('utf-8').encode('gbk') + ".xlsx"
    return file_name


def write_list(item):
    """
     # 写List
    :param item:
    :return:
    """
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


def write_list2db(item):
    """
     # 写List到数据库
    :param item:
    :return:
    """
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

    sql_sel = "SELECT id FROM t_video_detail WHERE 1 = 1 AND aid = '" + item['aid'] + "'"
    cursor = t_global_data.db_conn.execute(sql_sel)
    have_data = False
    for row in cursor:
        have_data = True
        break
    if have_data:
        print "do update"
    else:
        print "do ins"
        # sql_ins = "INSERT INTO t_video_detail ("
        # sql_ins +=
        # sql_ins += ")"


def write_list_title():
    """
     # 写excel标题
    :return:
    """
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


def create_tables():
    """
    # 建表
    :return:
    """
    print "=======start create tables=========="
    # t_global_data.db_conn = sqlite3.connect("result/res.db")
    # cur = t_global_data.db_conn.cursor()
    # sql_create_video_detail = "CREATE TABLE IF NOT EXISTS t_video_detail (" \
    #                           "id INTEGER PRIMARY KEY AUTO_INCREMENT," \
    #                           "title CHAR(512), subtitle CHAR(512), COMMENT INTEGER," \
    #                           "created CHAR(512), video_review INTEGER, favorites INTEGER," \
    #                           "video_length INTEGER, play INTEGER,  author CHAR(512)," \
    #                           "review CHAR(512), typeid CHAR(512)," \
    #                           "pic CHAR(512), description CHAR(512), aid CHAR(512)," \
    #                           "mid CHAR(512), copyright CHAR(512)," \
    #                           "bak CHAR(2048));"
    # print sql_create_video_detail
    # cur.execute(sql_create_video_detail)
    # t_global_data.db_conn.commit()


def write_mid(item):
    """
     写视频序号
    :param item:
    :return:
    """
    # FIXME 插入数据库
    pass
