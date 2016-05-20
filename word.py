class Word():
	def __init__(self, word):
		self.word = word
		self.phone = []
		self.syns = []
		self.pos = ''

	def __str__(self):
		ret = ''
		ret += self.word + ': '
		ret += self.pos + ', '
		ret += ' '.join(self.phone) + ', ' 
		ret += '[' + ', '.join(self.syns[:3]) + '...]' 
		return ret