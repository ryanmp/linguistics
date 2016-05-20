
import string
from word import Word
from pprint import pprint

'''

okay, I've decided that this library is unnecessary and too slow for what I'd like to try to do...
instead i'm just going to include the source library (it's just a big text file list of words with associated data)
and then load this data into a python dictionary. 
this should greatly speed up the lookup speeds?







'''





d = {}

f = open('pronounce.txt')
print 'building phones'
for (idx, line) in enumerate(f):
	if idx > 126: # skip header stuff
		word = line.split()[0].lower()
		content = line.split()[1:]
		if word not in d:
			d[word] = Word(word)
		d[word].phone = content
f.close()

f = open('part_of_speech.txt', 'rU')
print 'building part(s) of speech'
for line in f:
	x = line.strip().split('\xd7')
	word = x[0].lower()
	content = x[1]
	if word not in d:
		d[word] = Word(word)
	d[word].pos = content
f.close()

f = open('thesaurus.txt', 'rU')
print 'building thesaurus entries'
for (idx, line) in enumerate(f):
	word = line.split(',')[0].lower()
	content = line.strip().split(',')[1:]
	if word not in d:
		d[word] = Word(word)
	d[word].syns = content
f.close()


def phone_stresses(word):
	ret = ''
	for sound in d[word].phone:
		num = ''.join(x for x in sound if x.isdigit())
		if len(num) > 0:
			ret += str(num)
	return ret

def count_phone_syllables(word):
	return len(phone_stresses(word))

def line_to_words(line):
	return [word.strip(string.punctuation).lower() for word in line.split()]

def line_to_stresses(line):
	stresses = []
	line = line_to_words(line)
	for word in line:
		stresses.append(phone_stresses(word))
	return stresses

f = open('Onthewaydown.txt')
txt = []
for line in f:
	l = line.rstrip()
	l = l.lower()
	l = l.replace(',','')
	l = l.decode('unicode_escape').encode('ascii','ignore')
	txt.append(l)

pprint(txt)

stresses = []
for line in txt:
	stresses.append(line_to_stresses(line))

pprint(stresses)





