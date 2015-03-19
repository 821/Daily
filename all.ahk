;EE 自動保存
loop{
	MyLable:
	Sleep, 1000
	GetKeyState, state, Shift
	GetKeyState, statea, Alt
	GetKeyState, statec, Ctrl
	if statec != D
	{
		if statea != D
		{
			if state != D
			{
				IfWinActive, ahk_class EverEdit
				{
					Send {F9}
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