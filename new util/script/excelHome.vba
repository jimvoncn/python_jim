
Sub sub_goHome()
    '所有Sheet页移动到A1单元格

    Dim iSheet As Long

    For iSheet = Sheets.Count To 1 Step -1

        Sheets(iSheet).Activate
        'ActiveWindow.Zoom = 100  'Sheet页缩放
        ActiveWindow.ScrollRow = 1
        ActiveWindow.ScrollColumn = 1
        Sheets(iSheet).Range("A1").Activate

    Next iSheet
End Sub

