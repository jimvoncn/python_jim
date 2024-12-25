#! /usr/bin/env python3
# -*-coding:utf-8 -*-
# @Created on   : "Monday December 18 2023 19:51:42 GMT+0800 (China Standard Time)"
# @Author       : zorrow2017
# @Thanks to    : https://zhuanlan.zhihu.com/p/657981553
# @File         : printScreen-1218.py
# @Description  : <div> Ctrl+PrtScr 截图快捷键 python3版 </div>


r"""
printScreen-1218.py
Ctrl+PrtScr 截图快捷键, python3版

* 前提: 安装依赖包3个，改源代码以指定文件夹

* 用法: Ctrl+PrtScr 截图
* 功能1.截图
main()  监听键盘 -> 写日志 -> 截屏 -> 存文件

* 功能2.统计键盘各按键的使用频率顺便
sub_clickSum()  读日志 -> 统计 -> 写Excel
"""


if True:  # 自带依赖包常用版，封装成块，方便一起复制粘贴
    import base64
    import datetime
    import hashlib
    import json
    import math
    import os
    import random
    import re
    import shutil
    import sys
    import time

# 自带依赖包-不常用的
import collections
import importlib
import itertools
import threading
import uuid

# 共计2、3个依赖包
# pip install pynput
# pip install pyautogui
# pip install pillow
import pynput
import pynput.mouse
import pynput.keyboard  # 核心技术1.监听键盘 #监听Windows全局的键盘按键的py依赖库

import pyautogui  # 核心技术2.截屏


Key = pynput.keyboard.Key
gt_log = []  # 全局变量以定时写日志者，以防程序停了都还不知道
gv_lastKey = ""  # 上一个键盘按键
gv_baseScreenshotFolder = r"C:\E\heavy\screenshot"
go_time1 = time.time()


def main():
    """
    @description To do
    @dependence  pip install *
    """
    print(__doc__)
    print("<begin> time: " + time.ctime())
    ############
    # 注册监听器 pip install pynput
    lo_listener = pynput.keyboard.Listener(on_press=sub_on_press)
    lo_listener.start()  # 阻塞/非阻塞
    ############
    # print("<end> time: " + time.ctime())
    return lo_listener


def sub_on_press(io_key):
    """
    listener 监听Windows所有键盘事件(按住不放则反复触发)
    @param io_key 这一次按的哪个键
    @param gv_lastKey 上一次按的哪个键
    """
    ev_log = ""
    # 获取按的键
    try:
        lv_keyval = io_key.value
    except Exception as ex:
        lv_keyval = str(io_key)

    # PrtScr
    global gv_lastKey
    try:
        # 截屏快捷键：Ctrl+printScreen、左Ctrl+右Ctrl、或自定义
        if (
            io_key == Key.print_screen
            or (gv_lastKey == Key.ctrl_l and io_key == Key.print_screen)
            or (gv_lastKey == Key.ctrl_l and io_key == Key.ctrl_r)
        ):
            lo_time = time.time()

            # 执行:保存并弹出截图
            sub_save_screen_picture(lo_time, lv_keyval, gv_lastKey)

            # 执行后日志
            lv_timeformat = '"%A %B %d %Y %H:%M:%S GMT%z"'
            # print(time.strftime(lv_timeformat, time.localtime(lo_time)))
    except Exception as ex:
        # 报错日志
        ev_log = str(ex)
        print(ev_log)
        gt_log.append(ev_log)
    gv_lastKey = io_key

    try:
        ev_log = "Key %s press" % (io_key.char)
        # print(ev_log)
    except Exception:  # AttributeError:
        ev_log = "SpecialKey: %s press" % str(io_key)
        # print(ev_log)
    # 这里是配合函数sub_clickSum()统计键盘各按键的使用频率
    gt_log.append([str(io_key), "true"])
    sub_saveLog()


def sub_save_screen_picture(io_time, io_keyval, iv_lastKey):
    """
    截图，保存到文件夹
    @param io_time 截图时间
    @param io_keyval 这一次按的哪个键
    @param iv_lastKey 上一次按的哪个键
    @param lv_folder 保存截图文件的父文件夹
    """
    # 截图代码：仅一行 pip install pyautogui (尽量减少从按快捷键到执行截图的间隔时间)
    lo_jpg = pyautogui.screenshot()

    # 文件夹和文件名
    # TODO 指定文件夹
    lv_folder = gv_baseScreenshotFolder
    if os.path.exists(gv_baseScreenshotFolder) == False:
        os.makedirs(gv_baseScreenshotFolder)
    # @var lv_foldergar 垃圾文件夹，意思是如果只按PrtScr而不是Ctrl+PrtScr则也截图但存到这里
    lv_foldergar = os.path.join(gv_baseScreenshotFolder, "garbage")

    lv_subfolder = sub_get_subfolder(go_time1)  # 每周存一个文件夹
    lv_folder2 = os.path.join(lv_folder, lv_subfolder)
    if not os.path.exists(lv_folder):
        os.mkdir(lv_folder)
    if not os.path.exists(lv_foldergar):
        os.mkdir(lv_foldergar)
    if not os.path.exists(lv_folder2):
        os.mkdir(lv_folder2)
    lv_timeformat = "%Y-%m-%dT%H_%M_%S"  # .jpg 文件名
    lv_name = time.strftime(lv_timeformat, time.localtime(io_time))
    # lv_filename = os.path.join(lv_folder2, lv_name + ".jpg")
    if iv_lastKey == Key.ctrl_l or iv_lastKey == Key.ctrl_r:
        # Ctrl+PrtScn 表示有用的截图
        # print(iv_lastKey)
        lv_filename = os.path.join(lv_folder2, lv_name + ".jpg")
    else:
        # 非ctrl则认为是随便的截图，存垃圾文件夹
        lv_filename = os.path.join(lv_foldergar, lv_name + ".jpg")
    if os.path.exists(lv_filename):
        lv_int = int((random.random() * 900) + 100)  # 毫秒随机版，1秒最多1000个
        lo_uuid = uuid.uuid1()
        lv_name2 = lv_name + "-" + str(lo_uuid.hex)
        lv_filename = os.path.join(lv_folder2, lv_name2 + ".jpg")
        if os.path.exists(lv_filename):
            # 这怎么可能
            lo_ex = Exception('"%s" 这个uuid竟然重复了，这怎么可能!?' % lv_filename)
            raise lo_ex

    # 保存截图
    with open(lv_filename, "wb") as fos:
        lo_jpg.save(fos)
    if iv_lastKey == Key.ctrl_l or iv_lastKey == Key.ctrl_r:
        # 显示截图
        sub_open_paint(True, lv_filename)

    # 执行后日志-1, datetime在日志2
    ev_log = "file=%s, datetime=" % lv_filename
    print(ev_log)
    gt_log.append(ev_log)


def sub_get_subfolder(io_time):
    """
    YYYY-mm-DDMonday(本年的第几周)
    '2024-07-15Monday(%d)'
    以本周星期一的日期为文件夹名
    """
    lo_time = datetime.datetime.fromtimestamp(io_time)
    lo_week = lo_time.isocalendar()
    lv_yearweek = lo_week.week
    lv_weekday = lo_week.weekday
    # 往前减几天以取星期一为文件夹名
    lo_backday = datetime.timedelta(days=lv_weekday - 1)
    lo_time2 = lo_time - lo_backday
    # /2023-12-18week/aaa.jpg
    # ev_folder2 = lo_time2.strftime("%Y-%m-%d") + "Monday"
    ev_folder2 = lo_time2.strftime("%Y-%m-%d%A")
    ev_folder2 = ev_folder2 + "(%2d)" % lv_yearweek  # 本年第几周
    return ev_folder2


def sub_open_paint(iv_is_async, iv_file):
    if iv_is_async == True:
        lo_thread = threading.Thread(
            target=sub_open_paint, kwargs={"iv_is_async": False, "iv_file": iv_file}
        )
        lo_thread.start()
    else:
        # 命令行同步查看图片，用Windows自带的画图 因为快
        lv_cmd = 'mspaint.exe "%s"' % iv_file
        lv_ret = os.system(lv_cmd)


def sub_saveLog(iv_arg=None):
    # lv_wait = 20  # 等20秒
    lv_folder = os.path.join(gv_baseScreenshotFolder, "log")
    if not os.path.exists(lv_folder):
        os.makedirs(lv_folder)
    lv_file = ""
    lv_charset = "utf-8"
    global gt_log
    if True:
        # time.sleep(lv_wait)
        if len(gt_log) > 0:
            # lt_log=gt_log.copy()
            # lt_log=json.loads(json.dumps(gt_log))
            if lv_file == None or lv_file.strip() == "":
                lo_time = time.time()
                # lv_name=sub_get_subfolder(lo_time)
                lv_name = sub_get_subfolder(go_time1)
                lv_file = os.path.join(lv_folder, lv_name + ".log.txt")

            # 写文件
            lv_end = "\r\n"
            with open(lv_file, "a", encoding=lv_charset) as fos:
                while len(gt_log) > 0:
                    lv_front = gt_log.pop(0)  # 删除第0个 可用线程安全的队列

                    lv_micro = time.time()  # 精确到微秒 1721273733.9333043
                    lv_dec = ("%.3f" % lv_micro)[-4:]
                    lv_ts = time.strftime("%Y-%m-%dT%H_%M_%S", time.localtime(lv_micro)) + lv_dec
                    # abs(lv_micro)%1
                    lv_beg = "[%s] " % lv_ts

                    if type(lv_front) == list:
                        lv_ret = fos.write(str(lv_front[0]))
                        lv_ret = fos.write("\n")
                        continue
                    lv_ret = fos.write(lv_beg)
                    lv_ret = fos.write(str(lv_front))
                    lv_ret = fos.write(lv_end)
    ev_return = True


def sub_clickSum(iv_isall=False, iv_file=None):
    """
    广告：用此函数配合本程序(.log.txt文件)运行，可以统计按键的使用频率 到Excel然后自己分析数据
    本函数有相当的独立性，故自带import、坚决拒绝全局变量、不依赖其他函数，可拎到python IDLE独立运行、可另存为.py文件独立运行
    """
    import os
    import re

    ev_result = ""
    if iv_file == None:
        iv_file = r"C:\E\heavy\screenshot\log\2024-07-22Monday(30).log.txt"
    lv_folder = os.path.dirname(os.path.dirname(iv_file))  # ../../

    lv_folder_log = os.path.dirname(iv_file)  # 考虑统计所有log文件记载的按键频率
    # 输出.csv文件，虽然.xlsx文件也行但要依赖openpyxl库
    ev_csv = os.path.join(lv_folder, "calc.csv")
    lv_charset = "utf-8"
    # 读日志文件
    ls_dc = {}
    lv_len = 0
    lt_time = []
    for lv_fi in os.listdir(lv_folder_log):
        if re.search(r"^\d+-\d{2}", lv_fi):
            lt_time.append(lv_fi[0:10])
        lv_fi = os.path.join(lv_folder_log, lv_fi)
        if iv_isall == False:
            if lv_fi != iv_file:
                continue
        with open(lv_fi, "rb") as fis:
            lv_byte = fis.read()
        lv_str = lv_byte.decode(lv_charset)
        lt_str = re.split("[\r\n]+", lv_str)
        # 统计按键频率
        for i in lt_str:
            lv_key = i.strip()
            if lv_key == "" or len(lv_key) > 30:  # 或匹配不是key样子
                continue
            ls_dc[lv_key] = ls_dc.get(lv_key, 0) + 1
            lv_len += 1

    # 结果展示(报表)
    lt_output = []
    for i in ls_dc.keys():
        lv_val = ls_dc[i]
        ls_output = {
            "key": i,
            "time": lv_val,
            "percent": "%.4f%%" % (100 * lv_val / lv_len),
        }
        lt_output.append(ls_output)
    # 排序，取前10名
    lt_output.sort(key=lambda x: x["time"], reverse=True)
    lv_count = 10
    for i in lt_output:
        # print(i)
        ev_result += str(i) + "\n"
        lv_count -= 1
        if lv_count <= 0:
            break
    # 结果另存为.csv Excel文件
    if ev_csv == None or len(ev_csv) == 0:
        pass
    else:
        lv_sep = ","
        with open(ev_csv, "w", encoding=lv_charset) as fos:
            lt_title = ["key", "percent", "time"]
            lv_ret = fos.write(lv_sep.join(lt_title))
            lv_ret = fos.write("\n")
            for i in lt_output:
                lt_row = []
                for lv_key2 in lt_title:
                    lv_val = str(i[lv_key2])
                    # if lv_val.find(",")>=0:
                    lv_val = lv_val.replace(",", "comma")  # 逗号
                    lt_row.append(lv_val)
                lv_ret = fos.write(lv_sep.join(lt_row))
                lv_ret = fos.write("\n")

    lv_period = f"{min(lt_time)}, {max(lt_time)}周一至周末"
    ev_result += "这个期间(%s)中你总共敲了 %d 次键盘，可谓是只老程序员了" % (lv_period, lv_len)
    ev_result += "\n" + r"(更多详情见C:\E\heavy\screenshot\calc.csv)"
    print(ev_result)
    return ev_result


# 主程序入口
if __name__ == "__main__":
    main()
    input("ENTER to exit...")
