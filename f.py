#coding:utf-8#

import os,re
import win32clipboard as w
import win32con

rootDir = "E:\\Jekyll"

w.OpenClipboard()
strFind=re.compile(b'(?<=\/)[^/]+(?=/[^/]*$)')
ty=w.GetClipboardData(win32con.CF_TEXT)
c=strFind.search(ty).group().decode(encoding="UTF-8")
w.CloseClipboard()

fileList = []

for root, subFolders, files in os.walk(rootDir):
	if 'done!' in subFolders:
		subFolders.remove('done!')
	for f in files:
		if f.find(c) != -1:
			fileList.append(os.path.join(root, f))

os.system("Everedit.exe "+fileList[0])