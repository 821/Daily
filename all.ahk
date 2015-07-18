;EE 自動保存，不保存 EE 新建的「无标题」文件
SetTitleMatchMode RegEx
loop{
	MyLable:
	Sleep, 10000
	GetKeyState, state, Shift
	GetKeyState, statea, Alt
	GetKeyState, statec, Ctrl
	if statec != D
	{
		if statea != D
		{
			if state != D
			{
				If WinActive("^[^标]+ \* - EverEdit")
				{
					Send ^s
					Goto, MyLable
				}
			}
		}
	}
}

; Ctrl 和 Shift 的變形
*$RCTRL::
key = 0
Input, key, L1 M
SendInput {CTRL Down}{%key%}{CTRL Up}
return

*$RShift::
key = 0
Input, key, L1 M
SendInput {CTRL Down}{%key%}{CTRL Up}
return