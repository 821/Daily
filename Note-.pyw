import sys,re,os,dropbox
from PyQt4.QtCore import *; from PyQt4.QtGui import *; from PyQt4.QtWebKit import *

# settings
listfile = 'E:/Note-/files.txt' # format: 字體    E:/Jekyll/_Notes/IT/Fonts.md
pandoc = 'D:/Progra~1/Bulky/Pandoc/pandoc.exe'
te = 'D:/Progra~1/A/EmEditor/EmEditor.exe'
cssjs = 'E:/Note-/style.css'
outfolder = 'E:/Note-/html/'
upfolder = '/My%20Computers/lien/F:/Note-/'
WinSCP = 'D:/Progra~1/C/WinSCP/winscp.com'
server = 'https://usernameoremail:password@dav.example.com/'
oauth2 = ''

# frame
app = QApplication(sys.argv)
widget = QWidget()
widget.setWindowTitle('Note-')

# open the list
def initialize():
	global client, filedict, namelist
	client = dropbox.client.DropboxClient(oauth2)
	namelist = []
	filedict = {}
	f = open(listfile, 'r', encoding='utf-8')
	filelist = f.read().splitlines()
	f.close()
	getname = re.compile(u'^.+(?=    )')
	getpath = re.compile(u'(?<=    ).+$')
	for i in filelist:
		name = getname.search(i).group()
		path = getpath.search(i).group()
		filedict[name] = path
		namelist.append(name) # sequence of elements in filedict is strange
	return namelist

# make the folders
outfolderExist=os.path.isdir(outfolder)
if outfolderExist == False:
	os.mkdir(outfolder)

# generate the output path
def outpath(infile):
	getfilename = re.compile(u'(?<=/)[^/]+$')
	outfile = outfolder + getfilename.search(infile).group() + '.html'
	return outfile

# generate html
def html(infile, informat):
	os.system(pandoc + ' ' + infile + ' -f ' + informat + ' -t html --highlight-style=pygments -H ' + cssjs + ' -s -o ' + outpath(infile))
def generate():
	itempath = filedict[getcurrent()]
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

# load list in listWidget
def loadlist():
	initialize()
	listItem = []
	for name in namelist:
		lItem = QListWidgetItem(name)
		lItem.setBackgroundColor(QColor('black'))
		lItem.setTextColor(QColor('white'))
		listItem.append(lItem)
	for i in range(len(listItem)):
		listWidget.insertItem(i+1,listItem[i])

# refresh list
def refresh():
	namelist = []
	listWidget.clear()
	loadlist()

# viewing
webView = QWebView()

# list
listWidget = QListWidget()
loadlist()
# get current text in list
def getcurrent():
	return listWidget.currentItem().text()

# view button
viButton = QPushButton('View')
def view():
	viewfile = outpath(filedict[getcurrent()])
	visit = open(viewfile, 'r', encoding='utf-8')
	webView.setHtml(visit.read())
viButton.clicked.connect(view)

# generate button
geButton = QPushButton('Generate + View')
geButton.clicked.connect(generate)

# edit button
edButton = QPushButton('Edit')
def edit():
	os.system(te + ' ' + filedict[getcurrent()])
edButton.clicked.connect(edit)

# add button
adButton = QPushButton('Add')
def add():
	text, ok = QInputDialog.getText(widget, 'Add', 'Add')
	if ok:
		rectified = re.sub(r'\\', "/", text)
		f = open(listfile, 'a+', encoding='utf-8')
		f.write('\n' + rectified)
		f.close()
		refresh()
adButton.clicked.connect(add)

# list button
liButton = QPushButton('Edit List')
def editlist():
	os.system(te + ' ' + listfile)
liButton.clicked.connect(editlist)

# refresh button
f5Button = QPushButton('Refresh List')
def remove():
	listWidget.clear()
#f5Button.clicked.connect(remove)
f5Button.clicked.connect(refresh)

# style button
stButton = QPushButton('Style')
def editlist():
	os.system(te + ' ' + cssjs)
stButton.clicked.connect(editlist)

# backup button
baButton = QPushButton('Backup')
def backup():
	winpath = re.sub(r'\/', r'\\', filedict[getcurrent()])
	print(WinSCP + ' /command "open ' + server + '" "put ' + winpath + ' ' + upfolder + '" "exit"')
	os.system(WinSCP + ' /command "open ' + server + '" "put ' + winpath + ' ' + upfolder + '" "exit"')
baButton.clicked.connect(backup)

# dropbox button
dbButton = QPushButton('Dropbox')
def dropbox():
	fullpath = filedict[getcurrent()]
	dbpath = re.search(u'/[^/]+$', fullpath)
	f = open(fullpath, 'rb')
	response = client.put_file(dbpath.group(), f, overwrite=True)
dbButton.clicked.connect(dropbox)

# layouts
hlayout1 = QHBoxLayout()
hlayout1.addWidget(listWidget)
hlayout1.addWidget(webView)

hlayout2 = QHBoxLayout()
hlayout2.addWidget(viButton)
hlayout2.addWidget(geButton)
hlayout2.addWidget(edButton)
hlayout2.addWidget(adButton)
hlayout2.addWidget(liButton)
hlayout2.addWidget(f5Button)
hlayout2.addWidget(stButton)
hlayout2.addWidget(baButton)
hlayout2.addWidget(dbButton)

vlayout = QVBoxLayout()
vlayout.addLayout(hlayout1)
vlayout.addLayout(hlayout2)

widget.setLayout(vlayout)
screen = QDesktopWidget().screenGeometry()
widget.setGeometry(0, 100, screen.width(), screen.height()-130)
listWidget.setFixedWidth(150)
widget.show()
app.exec_()