import re, random, itertools, operator

'''
usage: 			"txt1 = ling.Txt('onthewaydown.txt', d)" where d is a ling.Dict()
description: 	a class for importing textfiles, removing formatting, creating word arrays
				once a textfile -> Txt()...  then we can do the fun stuff with it
'''
class Txt():

	def __init__(self, path, dict):

		self.txt = []
		self.path = path

		f = open(path)
		raw_txt = ''

		raw_txt = ''.join(f.readlines())
		raw_txt = re.split(r"\n|\.",raw_txt)

		for line in raw_txt:
			l = line.rstrip()
			l = l.lower()
			l = l.replace(',','')
			l = l.decode('unicode_escape').encode('ascii','ignore')
			words = re.findall('\w+', l)
			if len(words) > 0:
				#self.txt.append(words)
				word_list = []
				for word in words:
					if word in dict.d:
						word_list.append(dict.d[word])
				self.txt.append(word_list)


		f.close()

	def __str__(self):
		ret = '---------------------------\n'
		ret += '----- ' + self.path + '\n'
		ret += '---------------------------\n'
		for line in self.txt:
			line_as_str = ' '.join([word.word for word in line])
			ret += line_as_str + '\n'
		ret += '---------------------------'
		return ret

	def GetAlliterations(self):
		first_phones = []
		for l in self.txt:
			for w in l:
				if len(w.phone) > 0:
					first_phones.append((w.word, w.phone[0]))
		alliterations = []
		groupings = [list(j) for i, j in itertools.groupby(first_phones, operator.itemgetter(1))]
		for group in groupings:
			if len(group) > 1:
				alliterations.append(group)
		alliterations.sort(key = len)
		alliterations.reverse()
		return alliterations



	'''
	usage: 			"print instance_name.ToString(['words', 'phones'])" where txt1 is a Txt()
	description: 	used to print a text passage along with other inline class attributes
	'''
	def ToString(self, params):
		ret = '---------------------------\n'
		ret += '----- ' + self.path + '\n'
		ret += '---------------------------\n'
		for line in self.txt:

			for param in params:

				if param == 'words':
					line_as_str = ' '.join([word.word for word in line])
				elif param == 'phones':
					line_as_str = ''
					for word in line:
						line_as_str += ' '.join(word.phone) + '   '
				elif param == 'poss':
					line_as_str = ' '.join([word.pos for word in line])
				elif param == 'syns':
					line_as_str = ''
					for word in line:
						syn = word.word
						if len(word.syns) > 0:
							sub_sample = [i for i in word.syns if len(i.split()) == 1]
							if len(sub_sample) > 1:
								syn = random.sample(sub_sample, 1)[0]
							else: 
								syn = random.sample(word.syns, 1)[0]
						line_as_str += syn + '   '
				else:
					line_as_str = 'unrecognized parameter' 

				ret += line_as_str + '\n'

			ret += '\n'

		ret += '---------------------------'
		return ret

	def GetStresses(self):
		ret = []
		for line in self.txt:
			line_stresses = []
			for word in line:
				stresses = word.GetStresses()
				line_stresses.append(stresses)
			ret.append(line_stresses)
		return ret

	def GetSyllables(self):
		ret = []
		for line in self.txt:
			line_syllables = []
			for word in line:
				syllables = word.GetSyllables()
				line_syllables.append(syllables)
			ret.append(line_syllables)
		return ret

	def GetWordsPerSentence(self):
		ret = []
		for line in self.txt:
			ret.append(len(line))
		return ret


class Word():

	def __init__(self, word):
		self.word = word
		self.phone = []
		self.syns = []
		self.pos = ''

	def __str__(self):
		ret = ''
		ret += self.word + ': '
		ret += '(' + self.pos + '), '
		ret += ' '.join(self.phone) + ', ' 
		ret += '[' + ', '.join(self.syns[:3]) + '...]' 
		return ret

	def GetStresses(self):
		ret = ''
		for sound in self.phone:
			num = ''.join(x for x in sound if x.isdigit())
			if len(num) > 0:
				ret += str(num)
		if len(ret) > 0:
			return ret
		return '9'

	def GetSyllables(self):
		return len(self.GetStresses())

	def ToString(self, param):
		if param == 'word':
			return self.word
		elif param == 'phone':
			return ' '.join(self.phone)
		elif param == 'pos':
			return self.pos
		elif param == 'syn':
			sub_sample = [i for i in self.syns if len(i.split()) == 1]
			if len(sub_sample) > 1:
				return random.sample(sub_sample, 1)
			else: 
				return random.sample(self.syns, 1)
		else:
			return ''

	def GetRhyme(self):
		rhyme_part = []
		for i in reversed(self.phone):
			rhyme_part.append(i)
			if bool(re.compile('\d').search(i)): #contains_digits
				break
		return rhyme_part[::-1]


class Dict():

	def __init__(self):
		self.d = {}

		f = open('pronounce.txt')
		print 'building phones'
		for (idx, line) in enumerate(f):
			if idx > 126: # skip header stuff
				word = line.split()[0].lower()
				content = line.split()[1:]
				if word not in self.d:
					self.d[word] = Word(word)
				self.d[word].phone = content
		f.close()

		f = open('part_of_speech.txt', 'rU')
		print 'building part(s) of speech'
		for line in f:
			x = line.strip().split('\xd7')
			word = x[0].lower()
			content = x[1]
			if word not in self.d:
				self.d[word] = Word(word)
			self.d[word].pos = content
		f.close()

		f = open('thesaurus.txt', 'rU')
		print 'building thesaurus entries'
		for (idx, line) in enumerate(f):
			word = line.split(',')[0].lower()
			content = line.strip().split(',')[1:]
			if word not in self.d:
				self.d[word] = Word(word)
			self.d[word].syns = content
		f.close()

	def GetRhymes(self, word):
		test = self.d[word].GetRhyme()
		rhyming_words = []
		for k, v in self.d.iteritems():
			r = v.GetRhyme()
			if r == test:
				rhyming_words.append(k)
		return rhyming_words


