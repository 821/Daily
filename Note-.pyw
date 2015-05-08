import sys,re,os
from PyQt4.QtCore import *; from PyQt4.QtGui import *; from PyQt4.QtWebKit import *

# settings
listfile = 'E:/Note-/files.txt' # format: 字體	E:/Jekyll/_Notes/IT/Fonts.md
pandoc = '"D:/Program Files/Bulky/Pandoc/pandoc.exe"'
te = '"D:/Program Files/A/Everedit/Everedit.exe"'
cssjs = 'E:/Note-/style.css'
outfolder = 'E:/Note-/html/'

# frame
app = QApplication(sys.argv)
widget = QWidget()
widget.setWindowTitle('Note-')

# open the list
f = open(listfile, 'r+', encoding='utf-8')
filelist = f.read().splitlines()
getname = re.compile(u'^.+(?=\t)')
getpath = re.compile(u'(?<=\t).+$')
filedict = {}
namelist = []
for i in filelist:
	name = getname.search(i).group()
	path = getpath.search(i).group()
	filedict[name] = path
	namelist.append(name)

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
	else:
		html(itempath, 'html')

# viewing
webView = QWebView()

# list
listWidget = QListWidget()
listItem = []
for name in namelist:
	lItem = QListWidgetItem(name)
	lItem.setBackgroundColor(QColor('black'))
	lItem.setTextColor(QColor('white'))
	listItem.append(lItem)
for i in range(len(listItem)):
	listWidget.insertItem(i+1,listItem[i])
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
geButton = QPushButton('Generate')
geButton.clicked.connect(generate)

# edit button
edButton = QPushButton('Edit')
def edit():
	os.system(te + ' ' + filedict[getcurrent()])
edButton.clicked.connect(edit)

# list button
liButton = QPushButton('List')
def editlist():
	os.system(te + ' ' + listfile)
liButton.clicked.connect(editlist)

# layouts
hlayout1 = QHBoxLayout()
hlayout1.addWidget(listWidget)
hlayout1.addWidget(webView)

hlayout2 = QHBoxLayout()
hlayout2.addWidget(viButton)
hlayout2.addWidget(geButton)
hlayout2.addWidget(edButton)
hlayout2.addWidget(liButton)

vlayout = QVBoxLayout()
vlayout.addLayout(hlayout1)
vlayout.addLayout(hlayout2)

widget.setLayout(vlayout)
screen = QDesktopWidget().screenGeometry()
widget.setGeometry(0, 100, screen.width(), screen.height()-130)
listWidget.setFixedWidth(150)
widget.show()
app.exec_()