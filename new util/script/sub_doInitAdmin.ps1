
# 以管理员身份启动

function zfunc_runAdmin {
    # 以管理员身份启动
    Start-Process -FilePath "taskmgr.exe" -Verb RunAs
    Start-Process -FilePath "C:\D\everything.exe.lnk" -Verb RunAs  -WindowStyle hidden

    # 强行关闭开机自启动的软件
    taskkill /im wps.exe /f
    taskkill /im QiyiService.exe /f
    # taskkill /im ms-teams.exe /f
}


if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    # 不是管理员，则以管理员身份重新运行本脚本
    Start-Process PowerShell -Verb RunAs -ArgumentList ('-NoProfile -ExecutionPolicy Bypass -File "{0}" -Elevated' -f $myInvocation.MyCommand.Definition)
    exit
}


zfunc_runAdmin

