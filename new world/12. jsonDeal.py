#! /usr/bin/env python3
# -*-coding:utf-8 -*-
# @Created on   : "Thursday December 19 2024 19:27:13 GMT+0800 (China Standard Time)"
# @Author       : github.com/jimvoncn
# @File         : 12. jsonDeal.py
# @Description  :


r"""
12. jsonDeal.py
json是一个遵循一定的格式和规范的txt纯文本文件，比如：
{
    "Key": "Value",
    "时间": "2024-12-19",
    "地点": "Windows10 vscode",
    "人物": ["我", "你", "他"]
}

所有json就是一个配置文件而已

json与xml
json与xml excel html
json与txt
json与pickle
json与pickle toml

"""


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

    ls_json = {
        "亮度": "80%",
        "音量": 2,
        "字体大小": "12",
        "Font": "宋体",
        "screenWidth": 1920,
        "screenHight": 1080,
        "software": [
            {"id": "vscode.exe", "info": "什么什么的"}, 
            {"id": "python.exe", "info": ""}
        ]
    }

    print("所有json就是一个配置文件而已")

    ############
    print("------------ <end> time: " + time.ctime() + " ------------")


# 程序入口-这里是执行主程序的起点
if __name__ == "__main__":
    main()
    input("ENTER to exit...")
