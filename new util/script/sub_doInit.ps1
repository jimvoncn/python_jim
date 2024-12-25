#! /usr/bin/env powershell
# -*-coding:utf-8-sig -*-
# @Created on   : "Thursday June 27 2024 19:11:10 GMT+0800 (China Standard Time)"
# @Author       : github.com/jimvoncn
# @File         : onInit-0627.ps1
# @Description  : <div>
# 1.做什么?: 重启和开机后自动打开五常[文件夹、vscode、python、浏览器、任务管理器]
# 2.utf-8-sig <<特别注意>>这个文件的编码必须是utf-8-sig


echo "如果卡住了，请右击鼠标(刷新)"


# 普通软件
start "C:\D\python idle.pyw.lnk"
start "C:\D\WeChat.exe.lnk"
start "C:\D\Outlook.exe.lnk"

# 浏览器与文件夹
sleep 0.2
start "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "https://fanyi.baidu.com" 
sleep 0.4
start "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "https://www.baidu.com"
sleep 0.2
start "C:\E\Download"
sleep 4
start "C:\Users\jimvoncn\Desktop"


# 音量设置为2%
start "./sub_doInitSound.vbs"

# 以管理员身份启动：任务管理器、everything、关闭软件
powershell "./sub_doInitAdmin.ps1"
sleep 20




# 关闭当前命令行窗口
echo "All done..."
taskkill /im cmd.exe /f
exit
taskkill /im powershell.exe /f


