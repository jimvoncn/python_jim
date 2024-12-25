
@REM 切换WiFi
netsh wlan connect name="ChinaNet-jv"


exit

@REM ------------------------------------------------
@REM 1.导出WiFi密码，并把xml文件发给项目组其他成员
netsh wlan export profile name="ChinaNet-jv"  key=clear  folder="C:\E\wifi"
@REM 2.导入WiFi密码
netsh wlan add profile filename="C:\E\WeChat Files\2024-12\Wi-Fi-ChinaNet-jv.xml"
@REM 3.切换WiFi
netsh wlan connect name="ChinaNet-jv"
@REM ------------------------------------------------
