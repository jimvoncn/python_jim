#! /usr/bin/env python3
# -*-coding:utf-8 -*-
# @Created on   : "Friday December 06 2024 19:15:02 GMT+0800 (China Standard Time)"
# @Author       : github.com/jimvoncn
# @File         : 04. string.py
# @Description  :


r"""
04. string.py
质变：假设你开局即满级
"""


'''
文件结构讲解：
    1.本文件开头6行#注释，(#开头的是注释，作用是注释说明代码为什么要这么写)
    2.然后是r"""注释说明本文件是做什么的，
    3.然后是import导入需要用到的依赖包、命名空间，
    4.然后在main()函数中写代码，
        推论：所以重点是main()
        推论：所以可以把1.2.5.的注释和代码去掉看起来更清爽
    5.最后是执行：调用main()函数
'''


if True:
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

    # pip install *


def main():
    """
    @description public static void main(String[] args){}
    @param iv_file  absolute path of input file or folder
    """
    print(__doc__)
    print("------------ <begin> time: " + time.ctime() + " ------------")
    ############
    iv_file = r""

    lv_str = "L:局部变量, V:单值, _, str:字符串"
    lv_str2 = "String 2"

    # 字符串处理：长度、拼接、截取
    lv_length = len(lv_str)
    lv_concat = lv_str + lv_str2
    lv_substring = lv_concat[0:lv_length]
    if lv_str in lv_concat:
        print(lv_substring)

    # 正则表达式：匹配、分割、替换
    lv_isMatch = re.search("^L:", lv_str)
    lt_split = re.split("[,，]", lv_str)
    lv_replace = re.sub("L", "local", lv_str)

    # 本质：字符就是数字，数字就是二进制的字节流
    lv_trimSpace = lv_str.strip()
    lv_lowerCase = lv_str.lower()
    lv_char = lv_str[0]
    lv_UnicodeNumber = ord(lv_char)
    lv_byte = lv_char.encode("utf-8")

    ############
    print("------------ <end> time: " + time.ctime() + " ------------")


# 程序入口-这里是执行主程序的起点
if __name__ == "__main__":
    main()
    input("ENTER to exit...")
