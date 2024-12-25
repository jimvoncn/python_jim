#! /usr/bin/env python3
# -*-coding:utf-8 -*-
# 实际上就是调用/new util/zserver81/Control/ZServer81.py而已


def main():
    try:
        import tornado.ioloop
        import tornado.web
    except Exception as ex:
        lv_msg = str(ex)
        print("检查1. 未安装python的tornado依赖包，请务必要安装")

    try:
        import os

        gs_config = {}
        gs_config["base"] = "C:\\E\\code\\python_jim"
        lv_baseFolder = os.path.join(gs_config["base"], "new util/zserver81/Control")
        for i in os.listdir(lv_baseFolder):
            pass
    except Exception as ex:
        lv_msg = str(ex)
        print('检查2. 路径不存在，请用记事本打开和修改main.py里面的"base"文件路径')

    # 检查3. 防命令行窗口卡住了
    sub_cmdDisableQuickEditMode()

    # 先临时添加ZServer81.py所在文件夹，然后import ZServer81
    import os
    import sys

    sys.path.append(lv_baseFolder)

    import ZServer81  # type: ignore

    # 见(/new util/zserver81/Control/ZServer81.py)
    ZServer81.main(gs_config["base"])


def sub_cmdDisableQuickEditMode():
    """
    python双击执行的命令行窗口卡住了，必须鼠标右击(刷新)才能继续执行，怎么办？
    见 https://blog.csdn.net/u013314786/article/details/109367405
    """
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
    except Exception as ex:
        lv_msg = str(ex)
        print(lv_msg)


# 主程序入口
if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        lv_msg = str(ex)
        print(lv_msg)

    input("ENTER to exit...")
