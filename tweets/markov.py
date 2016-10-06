class Markov():
	def __init__(self, probabilities=dict(), beginnings=[]):
		self.two_gram_follow_probability = probabilities
		# self.two_gram_count = Counter()
		# self.two_gram_follow = dict()
		self.beginnings = beginnings


	def process_beginning(self, tweet_text):
		words = tweet_text.split()
		if len(words) > 3:
			self.beginnings.append(tuple([words[0], words[1]]))


	# TODO: move functions below to wordutil.py as _
	# TODO: eventually modify this construct to process all ngrams from n = 2 .. m
	def process_two_grams(self, words):
		# Do I need to count this?
		# self.two_gram_count.update([ tuple([words[i],words[i+1]]) \
		#     for i in xrange(len(words) - 1) \
		#     if self.ngram_contains_words(words[i],words[i+1]) \
		# ])

		for i in xrange(len(words) - 2):
			two_gram = tuple([words[i],words[i+1]])

			# if not self.two_gram_follow.has_key(two_gram):
			#     self.two_gram_follow[two_gram] = []
			# self.two_gram_follow[two_gram] = self.two_gram_follow[two_gram].append(words[i+2])

			self.upsert_follow_probability_count(two_gram, words[i+2])

		# print self.two_gram_follow_probability



	def upsert_follow_probability_count(self, n_gram, follow_word):
		""" self.two_gram_follow_probability example (to illustrate structure)
		{
		    tuple1: {
		        probabilities : {
		            word1: 0.4,
		            word2: 0.6
		        },
		        count : 10
		    },
		    tuple2: {
		        probabilities : {
		            word4: 0.2,
		            word3: 0.3,
		            word5: 0.5
		        },
		        count : 10
		    },
		    ...
		}
		"""
		if not self.two_gram_follow_probability.has_key(n_gram):
			# initialize tuple obj
			self.two_gram_follow_probability[n_gram] = dict()
			self.two_gram_follow_probability[n_gram]["count"] = 1
			self.two_gram_follow_probability[n_gram]["probabilities"] = dict()
			self.two_gram_follow_probability[n_gram]["probabilities"][follow_word] = 1
		else:
			probability_obj = self.two_gram_follow_probability[n_gram]
			self.two_gram_follow_probability[n_gram]["probabilities"] = self.new_probabilities(probability_obj["count"], probability_obj["probabilities"], follow_word)
			self.two_gram_follow_probability[n_gram]["count"] = probability_obj["count"] + 1


	# calculate probabilities_dict for current state + new_word
	def new_probabilities(self, count, probabilities_dict, new_word):
		new_count = count + 1

		# for each word, update probability with new_count 
		for k,v in probabilities_dict.iteritems():
			# is_new_word handles case new_word exists in probabilities_dict + makes vals float
			is_new_word = 1. if new_word == k else 0.
			probabilities_dict[k] = ((count * v) + is_new_word) / new_count

		# if word does not exist, initialize it
		if not probabilities_dict.has_key(new_word):
			probabilities_dict[new_word] = 1. / new_count

		return probabilities_dict
