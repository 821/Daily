from PIL import Image
import os

maxwidth = 1920
maxheight = 4500
test = 'F:\\b\\'
src = 'F:\\bc\\'
to = 'F:\\d\\'
record = 'F:\\record.cmd'

def movepic(pic, test, maxwidth, maxheight):
	im = Image.open(test + pic, mode='r')
	if im.width > maxwidth or im.height > maxheight:
		rec.write('cp ' + src + pic + ' ' + to + pic + '\n')
	im.close()

with open(record, 'w') as rec:
	for pic in os.listdir(test):
		movepic(pic, test, maxwidth, maxheight)
