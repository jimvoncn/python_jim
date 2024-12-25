#! /usr/bin/env python3
# -*-coding:utf-8 -*-

"""
创建、删除、修改、查看文件夹
读写文件
"""


def sub_getDesktop():
    import winreg

    lv_regedit = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
    lo_regKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, lv_regedit)
    lv_desktop = winreg.QueryValueEx(lo_regKey, "Desktop")[0]

    return lv_desktop


def sub_getIP():
    import scapy
    import scapy.all

    ev_ip = "127.0.0.1"
    for i in scapy.all.conf.ifaces.items():
        # ip of all Network Adapter
        lv_adapterName = str(i[1].name)
        lv_ip = scapy.all.get_if_addr(lv_adapterName)

        if lv_ip == "0.0.0.0":
            continue
        if scapy.all.conf.iface == i[1]:
            ev_ip = lv_ip
    return ev_ip


if True:
    import math
    import re
    import random
    import os
    import shutil
    import sys

    iv_file = r"C:\E\code\python\202412learn"

    # 1.创建空文件夹
    if not os.path.exists(iv_file):
        # 如果这个文件夹不存在 则创建
        os.makedirs(iv_file)
    else:
        if os.path.isfile(iv_file):
            # 如果恰好是文件则删除文件 再创建文件夹
            os.remove(iv_file)
            os.makedirs(iv_file)
        else:
            shutil.rmtree(iv_file)
            os.makedirs(iv_file)

    # 2.创建10个文件
    lv_index = 0
    while lv_index <= 10:
        lv_index = lv_index + 1
        lv_file = os.path.join(iv_file, f"rand-{lv_index}.txt")
        lv_floatNumber = random.random() * 100
        with open(lv_file, "wb") as fileOutputStream:
            lv_str = str(lv_floatNumber)
            lv_byte = lv_str.encode("utf-8")
            lv_return = fileOutputStream.write(lv_byte)

    # 3.打开文件夹窗口看效果
    lv_return = os.startfile(iv_file)

    # 4.创建、复制、循环子文件夹
    lv_subFolder = os.path.join(iv_file, "子文件夹")
    os.makedirs(lv_subFolder)
    for lv_filename in os.listdir(iv_file):  # 循环-逐个复制
        lv_fi = os.path.join(iv_file, lv_filename)
        lv_copyFile = os.path.join(lv_subFolder, lv_filename)
        if os.path.isfile(lv_fi):
            shutil.copy2(lv_fi, lv_copyFile)
    lv_copyFolder = os.path.join(iv_file, "New Folder")
    shutil.copytree(lv_subFolder, lv_copyFolder)  # 全部复制

    # 5.循环、统计所有子文件
    lv_size = 0
    lv_count = 0
    lt_fileList = []
    for lv_parentFolder, lt_subFolder, lt_subFile in os.walk(iv_file):
        for lv_name in lt_subFile:
            lv_count = lv_count + 1
            lv_fi = os.path.join(lv_parentFolder, lv_name)
            ls_info = os.stat(lv_fi)
            lv_size = lv_size + ls_info.st_size
            lt_fileList.append(lv_fi)
        for lv_name in lt_subFolder:
            print(f"subFolder: {lv_name}")
    print(f"文件总数量={lv_count}个, 文件总大小={lv_size}B")
    # 但是python和文件管理器的速度太慢，广告：想极速搜文件就用everything.exe

    # 6.读写文件，又名：解析文件
    # 读写.txt
    with open(lv_fi, "wb") as fileOutputStream:
        lv_return = fileOutputStream.write("文件内容...".encode("utf-8"))
        print(lv_fi)
    with open(lv_fi, "rb") as fileInputStream:
        lv_data = fileInputStream.read()
        print(lv_data.decode("utf-8"))  # 你凭什么知道一定是utf-8

    # 6.读写.xml、.xlsx、.html、.jpg 则需要安装对应的python依赖包

    # 7.取桌面文件夹的文件路径
    lv_str = sub_getDesktop()

    # 8.强制删除202412learn文件夹，但是删除文件夹有可能会报错
    # shutil.rmtree(iv_file)

    # 9.这，没个几年专业编程经验，一般人建议放弃：
    #     因为与其一知半解还不如完全不懂，
    #     不懂就不要勉强，自然有专业人士做，社会分工的意义就在于专注于做好一件小事。
    #     但即使不懂，了解了解、双击运行(/test/main.py)文件还是可以的
    #     进一步思考，一知半解并不是重点，重点是不要高估、低估、自不量力
    #     再进一步，明白、不明白，认识、不认识，世界观
    input("ENTER to exit...")
