#! /usr/bin/env python3
# -*-coding:utf-8 -*-
# @Created on   : "Monday December 18 2023 19:51:42 GMT+0800 (China Standard Time)"
# @Author       : zorrow2017
# @Thanks to    : https://zhuanlan.zhihu.com/p/657981553
# @File         : printScreen-1218.py
# @Description  : <div>
#   注：[2024-12-25]此功能已成功集成到zserver81了，不用再单独点了
#   Ctrl+PrtScr 截图快捷键 python3版
# </div>


r"""
printScreen-1218.py
Ctrl+PrtScr 截图快捷键, python3版

* 前提: 安装依赖包3个，改源代码以指定文件夹 (安装依赖失败或装了仍然报错，则，跳楼)

* 用法: Ctrl+PrtScr 后台立即全屏截图并保存文件，不会有弹出框，(保证本.py文件一直运行)
针对：在会议中对方分享屏幕切得很快，某截图软件在按PrtScr后电脑卡时会隔一两秒才能弹出截图界面追不上，所以可以用我的Ctrl+PrtScr截屏

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
from pynput import mouse
from pynput import keyboard  # 核心技术1.监听键盘 #监听Windows全局的键盘按键的py依赖库
from pynput.keyboard import Key
from pynput.keyboard import Controller

# pip install pyautogui
# pip install pillow
import pyautogui  # 核心技术2.截屏

# # pip install openpyxl
# import openpyxl  # 核心技术3.读写Excel文件 没必要用


gt_log = []  # 全局变量以定时写日志者，以防程序停了都还不知道
gv_lastKey = ""  # 上一个键盘按键
gv_folder = r"C:\E\heavy\screenshot"
go_time1 = time.time()


def main():
    """
    @description To do
    @dependence  pip install *
    @param iv_file is gv_folder
    """
    print(__doc__)
    print("<begin> time: " + time.ctime())
    ############
    # 每隔多少秒存日志sub_saveLog()
    lo_thread = threading.Thread(target=sub_saveLog, args=())
    lo_thread.start()

    # 注册监听器 pip install pynput
    lo_listener = keyboard.Listener(on_press=sub_on_press)
    # lo_listener.join() #阻塞/非阻塞
    lo_listener.start()  # 阻塞/非阻塞
    ############
    print("<end> time: " + time.ctime())


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
        if lv_keyval == Key.print_screen.value or (
            gv_lastKey == Key.ctrl_l and io_key == Key.ctrl_r
        ):  # 如果是截屏键则截屏，不能录屏
            lo_time = time.time()
            # 执行
            sub_save_screen_picture(lo_time, lv_keyval, gv_lastKey, io_key)
            # 执行后日志-2
            lv_timeformat = '"%A %B %d %Y %H:%M:%S GMT%z"'
            # print(time.strftime(lv_timeformat, time.localtime(lo_time)))
    except Exception as ex:
        # 执行后日志-3 如果报错
        ev_log = str(ex)
        print(ev_log)
        gt_log.append(ev_log)
    lv_str = ""  # 空语句，防debug跳太快了
    gv_lastKey = io_key

    try:
        ev_log = "Key %s press" % (io_key.char)
        # print(ev_log)
    except Exception:  # AttributeError:
        ev_log = "SpecialKey: %s press" % str(io_key)
        # print(ev_log)
    # 这里是配合函数sub_clickSum()统计键盘各按键的使用频率
    gt_log.append([str(io_key), "true"])


def sub_save_screen_picture(io_time, io_keyval, iv_lastKey, io_thisKey=None):
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
    lv_folder = gv_folder
    # @var lv_foldergar 垃圾文件夹，意思是如果只按PrtScr而不是Ctrl+PrtScr则也截图但存到这里
    lv_foldergar = os.path.join(gv_folder, "garbage")

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
    if (
        iv_lastKey == Key.ctrl_l
        or iv_lastKey == Key.ctrl_r
        or iv_lastKey == Key.shift_l
        or iv_lastKey == Key.shift_r
    ) or (iv_lastKey == Key.ctrl_l and io_thisKey == Key.ctrl_r):
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
    lv_wait = 20  # 等20秒
    lv_folder = os.path.join(gv_folder, "log")
    if not os.path.exists(lv_folder):
        os.mkdir(lv_folder)
    lv_file = ""
    lv_charset = "utf-8"
    global gt_log
    while True:
        time.sleep(lv_wait)
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

    iv_file = r"C:\E\heavy\screenshot\log\2024-07-22Monday(30).log.txt"
    lv_folder = os.path.dirname(os.path.dirname(iv_file))  # ../../
    # lv_folder = r"C:\E\heavy\screenshot"
    # iv_file = os.path.join(lv_folder, "log", "2024-07-22Monday(30).log.txt")

    lv_folder_log = os.path.dirname(iv_file)  # 考虑统计所有log文件记载的按键频率
    # 输出.csv文件，虽然.xlsx文件也行但要依赖openpyxl库
    ev_csv = os.path.join(lv_folder, "calc.csv")
    lv_charset = "utf-8"
    # 读日志文件
    ls_dc = {}
    lv_len = 0
    lv_fi = iv_file
    for lv_fi in os.listdir(lv_folder_log):
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
        print(i)
        lv_count -= 1
        if lv_count <= 0:
            break
    # 结果另存为.csv Excel文件
    if ev_csv == None or len(ev_csv) == 0:
        return
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
    print("这个期间中你总共敲了 %d 次键盘，可谓是只老程序员了" % lv_len)
    return True


# 主程序入口
if __name__ == "__main__":
    main()
    input("ENTER to exit...")
