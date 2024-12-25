
Sub sub_insertCopyDown()
    '连续插入几十行

    Dim currentRow As Long
    Dim i As Long

    currentRow = ActiveCell.Row

    Application.ScreenUpdating = False

    ' 从当前行开始往下插入20行，内容都复制当前行的内容
    For i = 1 To 20
        Rows(currentRow).Copy
        Rows(currentRow).Insert Shift:=xlDown
    Next i

    Application.ScreenUpdating = True
End Sub
