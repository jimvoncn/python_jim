#! /usr/bin/env python3
# -*-coding:utf-8 -*-

"""
这里拖拖拉拉、婆婆妈妈，讨论：
    数学运算与字符串处理
    依赖包与命名空间
    单值、列表、结构
    顺序、条件、循环
    面向过程、面向对象
    封装、继承、多态
"""


if True:
    # if True的代码既能直接复制粘贴到Python IDLE回车执行、又能.py文件
    # 这2个命名空间代表数学运算与字符串处理，强烈建议要、虽然不要也行
    import math
    import re

    # 这几个是http网络相关的，不要也行
    import base64
    import hashlib
    import json

    # 这几个是文件、文件夹相关的，不要也行
    import random
    import os
    import shutil
    import sys

    # 这几个是时间日期相关的，不要也行
    import datetime
    import time

    # pip install *
    # math命名空间，不用安装依赖包 因为math是自带的，可以直接import
    # requests命名空间，必须先手动安装requests依赖包，然后才能import
    # import requests

    # def main():
    # 程序=数据结构+算法

    # 数据结构分为：单值、数组、结构
    lv = "单值：整数、小数、字符串、null值"
    lt = ["数组", "列表", "表格", "序列"]
    ls = {"1": "结构", "2": "结构体", "3": "字典", "4.嵌套": lt}

    # 算法：循环
    lv_int = 0
    for lv_item in lt:  # 循环语句
        if lv_item == lv:  # 条件语句
            # 顺序语句
            a = 0
            c = str(a) + "b"
        else:
            lv_int = lv_int + 1
            print(f"lv_int={lv_int}")

    # 其他的经验做多了自然就知道了，比如：避免多层循环、值传递、全局变量、命名规范


# if True：面向过程，
# 函数：面向过程，
# 类与对象：面向对象 --只有Java的面向对象才是正宗的面向对象，python面向对象是渣渣
def sub_function(iv):
    ev = iv + 100
    return ev


class cl_Object(object):
    def __init__(self):
        self.mv = ""

    def sub_function(self, iv: float):
        ev = iv + 100
        return ev

    def sub_inheritAndOverwrite(self):
        return "封装，继承，多态"


class cl_儿子OfObject(cl_Object):
    def sub_function(self, iv_bigChange: bool, iv_22):
        # @Override
        print("子类的sub_function方法已经被重载重写大变样了")

        import this  # The Zen of Python

        return None


if __name__ == "__main__":
    go_obj = cl_儿子OfObject()  # 建议：不要像这样用中文变量名
    print(go_obj.sub_inheritAndOverwrite())
    # input("ENTER to exit...")


# <<恭喜你毕业了！>>

# 下一篇：python真正干活的实用脚本代码(/new util/z01_newUtil.md.txt)
# 或继续深造：文件处理教程(/new world/11. fileDeal.py)
