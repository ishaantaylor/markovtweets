import random

class MarkovWalk():
	def __init__(self, ngrams):
		self.ngrams = ngrams

	def generate(self, beginning_twogram, max_size):
		string = beginning_twogram[0] + " " + beginning_twogram[1]
		ngram = beginning_twogram
		for i in xrange(max_size):
			follow_word = self.next_word(ngram) 
			if follow_word == None:
				break
			ngram = tuple([ngram[1],follow_word])
			string += ' ' + follow_word

		string += '.\n'
		return string


	def next_word(self, gram):
		if not self.ngrams.has_key(gram):
			return None
		else: 
			probabilities = self.ngrams[gram]
			seed = random.randint(0,1)
			words = probabilities.keys()

			print gram
			print probabilities

			for k,v in probabilities.iteritems():
				if (seed - v < 0):
					follow_word = k
					break
				seed -= v

			return follow_word