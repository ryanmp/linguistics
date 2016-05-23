#import string
import re

txt_file_path = 'moby.txt'

f = open(txt_file_path)
txt = ''

txt = ''.join(f.readlines())
txt = re.split(r"\n|\.",txt)

clean_txt = []
for line in txt:
	l = line.rstrip()
	l = l.lower()
	l = l.replace(',','')
	l = l.decode('unicode_escape').encode('ascii','ignore')
	words = re.findall('\w+', l)
	if len(words) > 0:
		clean_txt.append(words)





