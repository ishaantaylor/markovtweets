import random

class MarkovWalk():
	def __init__(self, ngrams):
		self.ngrams = ngrams

	def generate(self, beginning_twogram, size):
		string = beginning_twogram[0] + " " + beginning_twogram[1]
		ngram = beginning_twogram
		for i in xrange(size):
			follow_word = self._generate(ngram) 
			ngram = tuple([ngram[1],follow_word])
			string += ' ' + follow_word

		string += '.\n'
		return string

	def _generate(self, gram):
		probabilities = self.ngrams[gram]
		seed = random.randint(0,1)
		words = probabilities.keys()

		for k,v in probabilities.iteritems():
			if (seed - v < 0):
				follow_word = k
				break
			seed -= v

		return follow_word