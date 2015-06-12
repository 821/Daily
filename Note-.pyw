import sys,re,os,shutil,datetime
from PyQt4.QtGui import *; from PyQt4.QtWebKit import QWebView; from PyQt4.QtCore import Qt,QObject
from conf import * # import settings

# convinience functions
outpath = lambda inpath: outfolder + os.path.basename(inpath) + '.html'
crListItem = lambda: listWidget.currentItem().text()
crTabWidget = lambda: tabWidget.currentWidget()
def lastbackup():
	flist = []
	for i in os.listdir(localbackupfolder):
		if i[-3:] == 'zip':
			flist.append(i)
	return os.path.join(localbackupfolder, max(flist))
def alldo(func, list):
	for v in list:
		func(v)
# add item to listWidget with format
def add2list(name):
	lItem = QListWidgetItem(name)
	lItem.setBackgroundColor(QColor('black'))
	lItem.setTextColor(QColor('white'))
	listWidget.addItem(lItem)
# check existence and create
def foldercreate(path):
	folderexist = os.path.isdir(path)
	if folderexist == False:
		os.mkdir(path)
# create buttons with function and geometry
def buttoncreate(text, tooltip, func, column, key):
	button = QPushButton(text)
	button.clicked.connect(func)
	button.setToolTip(tooltip)
	buttonLayout.addWidget(button, 0, column)
	QShortcut(QKeySequence(key), widget, func)

# open the list
def initialize():
	listWidget.clear()
	global filedict
	alldo(add2list, ['All Files', 'Style'])
	filedict = {'All Files': listfile, 'Style': cssjs}
	with open(listfile, 'r', encoding='utf-8') as f:
		filelist = f.read().splitlines()
		for i in filelist:
			name = re.sub(r'    .+$', '', i)
			path = re.sub(r'^.+    ', '', i)
			filedict[name] = os.path.normpath(path)
			add2list(name)

# viewing related
def view():
	with open(outpath(filedict[crListItem()]), 'r', encoding='utf-8') as visit:
		tabWidget.setTabText(tabWidget.currentIndex(), crListItem())
		crTabWidget().setHtml(visit.read())
def newtab():
	tabWidget.addNewTab()
	view()

# generate from input files
html = lambda infile, informat: os.system(pandoc + ' ' + infile + ' -f ' + informat + ' -t html --highlight-style=pygments -H ' + cssjs + ' -s -o ' + outpath(infile))
def generate(itempath):
	if itempath[-2:] == 'md' or itempath[-3:] == 'txt':
		html(itempath, 'markdown_github')
	elif itempath[-7:] == 'textile':
		html(itempath, 'textile')
	elif itempath[-3:] == 'tex':
		html(itempath, 'latex')
	elif itempath[-3:] == 'rst':
		html(itempath, 'rst')
	elif itempath[-3:] == 'org':
		html(itempath, 'org')
	else:
		html(itempath, 'html')
def regenerate():
	generate(filedict[crListItem()])
	view()

# edit selected item and the item being viewed
edit = lambda path: os.system(te + ' ' + path)
def editview():
	tabtitle = tabWidget.tabText(tabWidget.currentIndex())
	edit(filedict[tabtitle])

# backup
zip = lambda path: os.system(szip + ' a ' + localbackupfolder + backuptime + '.zip -p' + password + ' ' + path)
unzip = lambda path: os.system(szip + ' x ' + lastbackup() + ' -o' + os.path.dirname(path) + ' ' + os.path.basename(path) + ' -p' + password + ' -y')
def zipall():
	global backuptime
	backuptime = datetime.datetime.now().strftime("%y%m%d%H%M%S")
	alldo(zip, filedict.values())
ftp = lambda path: os.system(WinSCP + ' /command "open ' + server + '" "put ' + path + ' ' + upfolder + '" "exit"')
def ftpall():
	zipall()
	ftp(lastbackup())
def dropbox():
	dbclient = dropbox.client.DropboxClient(oauth2)
	with open(filedict[crListItem()], 'rb') as f:
		response = dbclient.put_file('/' + os.path.basename(filedict[crListItem()]), f, overwrite=True)

# find next
def findnext():
	next = crTabWidget().findText(blineEdit.text())
	crTabWidget().focusNextChild(next)
# find in list
def fil():
	global founditems, foundindex, findtext
	if findtext != llineEdit.text():
		initialize()
		foundindex = 0
		founditems = listWidget.findItems(llineEdit.text(), Qt.MatchFlag(16) and Qt.MatchFlag(1)) # 1: partial search, 4:regex, 16: case insensitive
		for item in founditems:
			item.setBackgroundColor(QColor('blue'))
		listWidget.setCurrentItem(founditems[0])
		findtext = llineEdit.text()
	else:
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
		self.addNewTab()
	def closeTab(self, index):
		self.last_closed_doc = self.widget(index)
		self.removeTab(index)
	def addNewTab(self, title = "Untitled"):
		self.insertTab(0, QWebView(), title)
		self.setCurrentIndex(0)

# start here
findtext = 0
alldo(foldercreate, [outfolder, localbackupfolder])
app = QApplication(sys.argv)
widget = QWidget()
widget.setWindowTitle('Note-')
widget.setWindowIcon(QIcon(widget.style().standardIcon(QStyle.SP_DialogSaveButton)))
buttonLayout = QGridLayout()
rightHalf = QVBoxLayout()
fullLayout = QHBoxLayout()
tabWidget = TabWidget()
listWidget = QListWidget()
listWidget.setFixedWidth(150)
llineEdit, blineEdit = QLineEdit(), QLineEdit()
buttoncreate('List F1', 'Reload the list', initialize, 0, Qt.Key_F1)
buttoncreate('Find F2', 'Find the next item with the string', fil, 1, Qt.Key_F2)
buttonLayout.addWidget(llineEdit, 0, 3)
buttoncreate('View F3', 'View selected item', view, 4, Qt.Key_F3)
buttoncreate('Tab F4', 'View in a new tab', newtab, 5, Qt.Key_F4)
buttoncreate('Convert F5', 'Generate selected item to HTML', regenerate, 6, Qt.Key_F5)
buttoncreate('CA C+F5', 'Generate all items to HTML', lambda:alldo(generate, filedict.values()), 7, Qt.CTRL + Qt.Key_F5)
buttoncreate('Edit F6', 'Edit selected item', lambda: edit(filedict[crListItem()]), 8, Qt.Key_F6)
buttoncreate('ET F7', 'Edit item in current tab', editview, 9, Qt.Key_F7)
buttoncreate('FTP F8', 'Upload selected item to FTP/WebDAV', lambda: ftp(filedict[crListItem()]), 11, Qt.Key_F8)
buttoncreate('FTP All F9', 'Pack all items with password and upload to FTP/WebDAV', ftpall, 12, Qt.Key_F9)
buttoncreate('Dropbox F10', 'Upload selected item to Dropbox', dropbox, 13, Qt.Key_F10)
buttoncreate('Pack F11', 'Pack all items with password', zipall, 14, Qt.Key_F11)
buttoncreate('Restore C+F11', 'Restore selected item from the latest pack', lambda:unzip(filedict[crListItem()]), 15, Qt.CTRL + Qt.Key_F11)
buttonLayout.addWidget(blineEdit, 0, 16)
buttoncreate('Find Next F12', 'Find string in currently viewing item', findnext, 17, Qt.Key_F12)
rightHalf.addWidget(tabWidget)
rightHalf.addLayout(buttonLayout)
fullLayout.addWidget(listWidget)
fullLayout.addLayout(rightHalf)
widget.setLayout(fullLayout)
screen = QDesktopWidget().screenGeometry()
widget.setGeometry(0, 100, screen.width(), screen.height()-130)
initialize()
widget.show()
app.exec_()