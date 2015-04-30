import os,re,clipboard
from tkinter import *

rootdir = "E:\\Jekyll"

wd = Tk()
wd.title('開文件')

ent = Entry(wd,width=50)
ent.grid(row=1,column=0)
def newText():
	ent.delete(0,END)
	ent.insert(0,clipboard.paste())
but = Button(wd, text="Paste",command=newText)
but.grid(row=1,column=1)

def openit():
	FileList = []
	for root, subFolders, files in os.walk(rootdir):
		for f in files:
			if f.find(ent.get()) != -1:
				FileList.append(os.path.join(root, f))
	os.system("Everedit.exe "+FileList[0])

but = Button(wd,text='Open',command=openit)
but.grid(row=2,column=0)

wd.update()
wd.mainloop()