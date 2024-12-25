
# powershell是cmd调用:
#     Add-Type是powershell调用:
#         DllImport extern是C#代码
#     SendMessage是ps1执行

function Main() {
(Add-Type '[DllImport("user32.dll")]public static extern int SendMessage(int hWnd, int hMsg, int wParam, int lParam);' -Name a -Pas)::SendMessage(-1, 0x0112, 0xF170, 2)
}


# 引入Task类所在的命名空间
Add-Type -AssemblyName System.Threading.Tasks


$Throttle = 20  #threads

#脚本块，对指定的计算机发送一个ICMP包测试，结果保存在一个对象里面

$ScriptBlock = {
    (Add-Type '[DllImport("user32.dll")]public static extern int SendMessage(int hWnd, int hMsg, int wParam, int lParam);' -Name a -Pas)::SendMessage(-1, 0x0112, 0xF170, 2)
}


#创建一个资源池，指定多少个runspace可以同时执行
$RunspacePool = [RunspaceFactory]::CreateRunspacePool(1, $Throttle )
$RunspacePool.Open()
$Jobs = @()


#获取Windows 2012服务器的信息，对每一个服务器单独创建一个job，该job执行ICMP的测试，并把结果保存在一个PS对象中


#Start-Sleep -Seconds 1
$Job = [powershell]::Create().AddScript( $ScriptBlock )
$Job.RunspacePool = $RunspacePool
$Jobs += New-Object  PSObject -Property @{
    Server = $_
    Pipe   = $Job
    Result = $Job.BeginInvoke()
}





# Get-Process -Name PowerShell | Format-Table -Property ID, ProcessName, MachineName
# taskkill.exe /IM powershell.exe /F
Start-Sleep -seconds 6
# exit
Stop-Process -Id $PID -Force



