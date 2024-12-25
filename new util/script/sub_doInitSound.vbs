
'音量设置为2%

set lo_ws = WScript.CreateObject("WScript.Shell")

'音量减
For i = 0 To 100
    lo_ws.SendKeys chr(&H88AE)
Next

lo_ws.SendKeys chr(&H88AF) '音量加
'lo_ws.SendKeys chr(&H88AD) '静音

WScript.quit
