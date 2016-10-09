import sys
# TODO: instead of pickle module for data serialization, use JSON or MessagePack
import cPickle as pickle
import os.path
import logging
from tweets.markov import Markov

from tweets.stream import stream_tweets_from


SAN_FRANCISCO = [-122.75,36.8,-121.75,70.8]
LIMIT = 50000
WORDS = ['technology']

def main():
	# set up logger
	root = logging.getLogger()
	root.setLevel(logging.DEBUG)

	ch = logging.StreamHandler(sys.stdout)
	ch.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	ch.setFormatter(formatter)
	root.addHandler(ch)
	

	# load ngrams
	try:
		ngrams = pickle.load( open( "ngrams.p", "rb" ) )
		logging.info("Loaded ngrams.p")
	except IOError:
		ngrams = dict()
		logging.warning("Failed to load ngrams.p.")

	# load beginning words
	try:
		beginnings = pickle.load( open( "beginnings.p", "rb" ) )
		logging.info("Loaded beginnings.p")
	except IOError:
		beginnings = []
		logging.warning("Failed to load beginnings.p.")


	# create markov engine
	MARKOV = Markov(ngrams, beginnings)

	try:
		stream_tweets_from(SAN_FRANCISCO, MARKOV, LIMIT, WORDS)
	except KeyboardInterrupt:
		# save ngram models and beginnings
		try:
			pickle.dump( MARKOV.two_gram_follow_probability, open( "ngrams.p", "wb" ) )
			pickle.dump( MARKOV.beginnings, open( "beginnings.p", "wb" ) )
			logging.info("Saved markov model data.")
		except e:
			print logging.error("Failed to save markov model data."),
			print sys.exc_info()[0]



if __name__ == "__main__":
	main()
