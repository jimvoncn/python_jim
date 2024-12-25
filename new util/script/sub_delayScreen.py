#! /usr/bin/env python3

# 先息屏再锁屏

if True:
    import os
    import time

    lv_cmd = 'powershell "./sub_doBlack.ps1"'  # 先息屏
    os.system(lv_cmd)

    time.sleep(65)

    # 65秒后 再锁屏
    # 应用场景：中午吃午饭，担心直接锁屏会不会停止下载，所以想先息屏再锁屏
    # 推论：所以息屏只是关闭显示器、省电，不会产生其他任何影响；鼠标一动就亮屏。
    lv_cmd = "rundll32.exe user32.dll,LockWorkStation"
    os.system(lv_cmd)
