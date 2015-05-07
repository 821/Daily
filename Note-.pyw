import sys,re,os
from PyQt4.QtCore import *; from PyQt4.QtGui import *; from PyQt4.QtWebKit import *

# settings
filelist = 'E:/Note-/files.txt'
pandoc = '"D:/Program Files/Bulky/Pandoc/pandoc.exe"'
te = '"D:/Program Files/A/Everedit/Everedit.exe"'
cssjs = 'E:/Note-/style.css'
outfolder = 'E:/Note-/html/'

# open the list
f = open(filelist, 'r+', encoding='utf-8')
mylist = f.read().splitlines()

# make the folders
outfolderExist=os.path.isdir(outfolder)
if outfolderExist == False:
	os.mkdir(outfolder)

# generate the output path
def outpath(infile):
	filename = re.compile(u'(?<=/)[^/]+$')
	outfile = outfolder + filename.search(infile).group() + '.html'
	return outfile

# generate html
def html(infile, informat):
	os.system(pandoc + ' ' + infile + ' -f ' + informat + ' -t html --highlight-style=pygments -H ' + cssjs + ' -s -o ' + outpath(infile))
def generate():
	itemtext = listWidget.currentItem().text()
	if itemtext[-2:] == 'md' or itemtext[-2:] == 'xt':
		html(itemtext, 'markdown_github')
	elif itemtext[-2:] == 'le':
		html(itemtext, 'textile')
	else:
		html(itemtext, 'html')

# viewing
def view():
	viewfile = outpath(listWidget.currentItem().text())
	visit = open(viewfile, 'r', encoding='utf-8')
	webView.setHtml(visit.read())

# frame
app = QApplication(sys.argv)
widget = QWidget()
widget.setWindowTitle('筆記本')

# list
listWidget = QListWidget()
listItem = []
for item in mylist:
	lItem = QListWidgetItem(item)
	lItem.setBackgroundColor(QColor('black'))
	lItem.setTextColor(QColor('white'))
	listItem.append(lItem)
for i in range(len(listItem)):
	listWidget.insertItem(i+1,listItem[i])

# viewer
webView = QWebView()

# view button
viButton = QPushButton('View')
viButton.clicked.connect(view)

# generate button
geButton = QPushButton('Generate')
geButton.clicked.connect(generate)

# edit button
edButton = QPushButton('Edit')
def edit():
	itemtext = listWidget.currentItem().text()
	os.system(te + ' ' + itemtext)
edButton.clicked.connect(edit)

# list button
liButton = QPushButton('List')
def editlist():
	os.system(te + ' ' + filelist)
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
listWidget.setFixedWidth(300)
widget.show()
app.exec_()