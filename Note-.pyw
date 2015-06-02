# settings
listfile = 'E:/Note-/files.txt' # format: 字體    E:/Jekyll/_Notes/IT/Fonts.md
pandoc = 'D:/Progra~1/Bulky/Pandoc/pandoc.exe'
te = 'D:/Progra~1/A/EmEditor/EmEditor.exe'
cssjs = 'E:/Note-/style.css'
outfolder = 'E:/Note-/html/' # will generate if not exist
upfolder = '/Note-/'
WinSCP = 'D:/Progra~1/C/WinSCP/winscp.com'
server = 'https://usernameoremail:password@dav.example.com/'
oauth2 = 'youroauth2'

import sys,re,os,dropbox
from PyQt4.QtGui import *; from PyQt4.QtWebKit import QWebView; from PyQt4.QtCore import Qt

# open the list
def initialize():
	listWidget.clear()
	global filedict
	add2list(1, 'All Files')
	add2list(2, 'Style')
	j = 2
	filedict = {'All Files': listfile, 'Style': cssjs}
	with open(listfile, 'r', encoding='utf-8') as f:
		filelist = f.read().splitlines()
	for i in filelist:
		name = re.sub(r'    .+$', '', i)
		path = re.sub(r'^.+    ', '', i)
		filedict[name] = path
		j += 1
		add2list(j, name)

# check existence and create
def foldercreate(path):
	folderexist = os.path.isdir(path)
	if folderexist == False:
		os.mkdir(path)

# add item to listWidget with format
def add2list(j, name):
	lItem = QListWidgetItem(name)
	lItem.setBackgroundColor(QColor('black'))
	lItem.setTextColor(QColor('white'))
	listWidget.insertItem(j, lItem)

# get filename from fullpath
def getname(fullpath):
	reget = re.compile(u'(?<=/)[^/]+$')
	return reget.search(fullpath).group()

# generate the output path
def outpath(inpath):
	return outfolder + getname(inpath) + '.html'

# get current text in list
def getCurrentListItem():
	return listWidget.currentItem().text()

# view button
def view():
	with open(outpath(filedict[getCurrentListItem()]), 'r', encoding='utf-8') as visit:
		tabWidget.setTabText(tabWidget.currentIndex(), getCurrentListItem())
		crtabwd = tabWidget.currentWidget()
		crtabwd.setHtml(visit.read())

# create and view in new tab button
def newtab():
	tabWidget.addNewTab()
	view()

# generate from input files and view output
def html(infile, informat):
	os.system(pandoc + ' ' + infile + ' -f ' + informat + ' -t html --highlight-style=pygments -H ' + cssjs + ' -s -o ' + outpath(infile))
def generate():
	itempath = filedict[getCurrentListItem()]
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
	view()

# edit selected item
def edit():
	os.system(te + ' ' + filedict[getCurrentListItem()])

# add item
def add():
	text, ok = QInputDialog.getText(widget, 'Add', 'Add')
	if ok:
		rectified = re.sub(r'\\', "/", text)
		with open(listfile, 'a+', encoding='utf-8') as f:
			f.write('\n' + rectified)
		refresh()

# backup to ftp or webdav
def backup():
	os.system(WinSCP + ' /command "open ' + server + '" "put ' + re.sub(r'\/', r'\\', filedict[getCurrentListItem()]) + ' ' + upfolder + '" "exit"')

# backup to dropbox
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
	founditems = listWidget.findItems(llineEdit.text(), Qt.MatchFlag(16) and Qt.MatchFlag(1))
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
app = QApplication(sys.argv)
widget = QWidget()
icon = QIcon(widget.style().standardIcon(QStyle.SP_CommandLink)) # generate icon
widget.setWindowIcon(icon)
widget.setWindowTitle('Note-')
tabWidget = TabWidget()
listWidget = QListWidget()
initialize()
foldercreate(outfolder)
llineEdit, blineEdit = QLineEdit(), QLineEdit()
hlayout1 = QHBoxLayout()
hlayout1.addWidget(listWidget)
hlayout1.addWidget(tabWidget)
hlayout2.addWidget(llineEdit, 0, 3)
hlayout2.addWidget(blineEdit, 0, 10)
for text, func, column in (("Reload List", initialize, 0),
					("Find in List", fil, 1),
					("Next Item", nextitem, 2),
					("View", view, 4),
					("New Tab", newtab, 5),
					("Regenerate", generate, 6),
					("Edit", edit, 7),
					("Add", add, 8),
					("Backup", backup, 9),
					("Find Next", findnext, 11)):
	button = QPushButton(text)
	button.clicked.connect(func)
	hlayout2.addWidget(button, 0, column)
vlayout = QVBoxLayout()
vlayout.addLayout(hlayout1)
vlayout.addLayout(hlayout2)
widget.setLayout(vlayout)
screen = QDesktopWidget().screenGeometry()
widget.setGeometry(0, 100, screen.width(), screen.height()-130)
listWidget.setFixedWidth(150)
widget.show()
app.exec_()