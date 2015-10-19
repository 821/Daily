from bs4 import BeautifulSoup

infile = ''
outfile = ''

with open(infile, 'r', encoding = 'utf-8') as inputs, open(outfile, 'a', encoding = 'utf-8') as outfile:
	for line in inputs.read().splitlines():
		j = line.split('```')
		head = j[0]
		mean = j[1]
		soup = BeautifulSoup(mean, "html.parser", from_encoding = 'utf-8')
		#outfile.write(head + '```' + soup.prettify() + '\n</>\n')
		outfile.write(head + '```')
		divs = soup.find_all('div')
		for div in divs:
			die = 0
			for child in div.children:
				if child.name == 'div':
					die = 1
			if die == 0:
				outfile.write(str(div))
		outfile.write('\n')