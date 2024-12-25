#! /usr/bin/env python3

# 点击屏幕 每59秒点一次以防止锁屏

while True:
    import time
    import os

    try:
        import pyautogui

        pyautogui.FAILSAFE = False
        pyautogui.click(x=100, y=120)
    except Exception as ex:
        print(time.ctime())
        print(ex)

    time.sleep(59)
