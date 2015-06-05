import sys,re,os,shutil
from PyQt4.QtGui import *; from PyQt4.QtWebKit import QWebView; from PyQt4.QtCore import Qt,QObject, QUrl
from conf import * # import settings

# open the list
def initialize():
	listWidget.clear()
	global filedict
	add2list('All Files')
	add2list('Style')
	filedict = {'All Files': listfile, 'Style': cssjs}
	with open(listfile, 'r', encoding='utf-8') as f:
		filelist = f.read().splitlines()
	for i in filelist:
		name = re.sub(r'    .+$', '', i)
		path = re.sub(r'^.+    ', '', i)
		filedict[name] = path
		add2list(name)

# check existence and create
def foldercreate(path):
	folderexist = os.path.isdir(path)
	if folderexist == False:
		os.mkdir(path)

# add item to listWidget with format
def add2list(name):
	lItem = QListWidgetItem(name)
	lItem.setBackgroundColor(QColor('black'))
	lItem.setTextColor(QColor('white'))
	listWidget.addItem(lItem)

# convinience functions
def getname(fullpath):
	reget = re.compile(u'(?<=/)[^/]+$')
	return reget.search(fullpath).group()
def outpath(inpath):
	return outfolder + getname(inpath) + '.html'
def getCurrentListItem():
	return listWidget.currentItem().text()
def alldo(func):
	for v in filedict.values():
		func(v)

# view button
def view():
	with open(outpath(filedict[getCurrentListItem()]), 'r', encoding='utf-8') as visit:
		tabWidget.setTabText(tabWidget.currentIndex(), getCurrentListItem())
		tabWidget.currentWidget().setHtml(visit.read())

# create and view in new tab button
def newtab():
	tabWidget.addNewTab()
	view()

# generate from input files and view output
def html(infile, informat):
	os.system(pandoc + ' ' + infile + ' -f ' + informat + ' -t html --highlight-style=pygments -H ' + cssjs + ' -s -o ' + outpath(infile))
def generate(itempath):
	if itempath[-2:] == 'md' or itempath[-3:] == 'txt':
		html(itempath, 'markdown_github')
	elif itempath[-7:] == 'textile':
		html(itempath, 'textile')
	elif itempath[-3:] == 'tex':
		html(itempath, 'latex')
	elif itempath[-3:] == 'rst':
		html(itempath, 'rst')
	else:
		html(itempath, 'html')
def regenerate():
	generate(filedict[getCurrentListItem()])
	view()

# edit selected item and the item being viewed
def edit():
	os.system(te + ' ' + filedict[getCurrentListItem()])
def editview():
	tabtitle = tabWidget.tabText(tabWidget.currentIndex())
	os.system(te + ' ' + filedict[tabtitle])

# backup
def ftp(path):
	os.system(WinSCP + ' /command "open ' + server + '" "put ' + re.sub(r'\/', r'\\', path) + ' ' + upfolder + '" "exit"')
def centralize():
	foldercreate(localbackupfolder)
	for v in filedict.values():
		shutil.copyfile(v, localbackupfolder + getname(v))
def decentralize():
	for v in filedict.values():
		shutil.copyfile(localbackupfolder + getname(v), v)
def dropbox():
	dbclient = dropbox.client.DropboxClient(oauth2)
	fullpath = filedict[getCurrentListItem()]
	dbpath = re.search(u'/[^/]+$', fullpath)
	with open(fullpath, 'rb') as f:
		response = dbclient.put_file(dbpath.group(), f, overwrite=True)

# find next
def findnext():
	crtabwd = tabWidget.currentWidget()
	next = crtabwd.findText(blineEdit.text())
	crtabwd.focusNextChild(next)

# find in list
def fil():
	initialize()
	global founditems, foundindex
	foundindex = 0
	founditems = listWidget.findItems(llineEdit.text(), Qt.MatchFlag(16) and Qt.MatchFlag(1)) # 1: partial search, 4:regex, 16: case insensitive
	for item in founditems:
		item.setBackgroundColor(QColor('blue'))
	listWidget.setCurrentItem(founditems[0])
def nextitem():
	global foundindex
	if foundindex == len(founditems) - 1:
		foundindex = 0
	else:
		foundindex += 1
	listWidget.setCurrentItem(founditems[foundindex])

# apply some changes to QTabWidget
class TabWidget(QTabWidget):
	def __init__(self, parent=None):
		super (TabWidget, self).__init__(parent)
		self.setTabsClosable(True)
		self.tabCloseRequested.connect(self.closeTab)
		self.setMovable(True)
	def closeTab(self,index):
		self.last_closed_doc = self.widget(index)
		self.removeTab(index)
	def addNewTab(self,title = "Untitled"):
		self.insertTab(0, QWebView(), title)
		self.setCurrentIndex(0)

# start here
foldercreate(outfolder)
app = QApplication(sys.argv)
widget = QWidget()
icon = QIcon(widget.style().standardIcon(QStyle.SP_CommandLink)) # generate icon
widget.setWindowIcon(icon)
widget.setWindowTitle('Note-')
tabWidget = TabWidget()
listWidget = QListWidget()
listWidget.setFixedWidth(150)
llineEdit, blineEdit = QLineEdit(), QLineEdit()
buttonLayout = QGridLayout()
buttonLayout.addWidget(llineEdit, 0, 3)
buttonLayout.addWidget(blineEdit, 0, 16)
for text, func, column in (("Reload List", initialize, 0),
					("Find in List", fil, 1),
					("Next Item", nextitem, 2),
					("View", view, 4),
					("New Tab", newtab, 5),
					("Regenerate", regenerate, 6),
					("Generate All", lambda:alldo(generate), 7),
					("Edit", edit, 8),
					("Edit Viewed", editview, 9),
					("FTP", lambda:ftp(filedict[getCurrentListItem()]), 11),
					("FTP All", lambda:alldo(ftp), 12),
					("Dropbox", dropbox, 13),
					("Centralize", centralize, 14),
					("Decentralize", decentralize, 15),
					("Find Next", findnext, 17)):
	button = QPushButton(text)
	button.clicked.connect(func)
	buttonLayout.addWidget(button, 0, column)
rightHalf = QVBoxLayout()
rightHalf.addWidget(tabWidget)
rightHalf.addLayout(buttonLayout)
fullLayout = QHBoxLayout()
fullLayout.addWidget(listWidget)
fullLayout.addLayout(rightHalf)
widget.setLayout(fullLayout)
screen = QDesktopWidget().screenGeometry()
widget.setGeometry(0, 100, screen.width(), screen.height()-130)
initialize()
widget.show()
app.exec_()