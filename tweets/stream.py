import tweepy
import json
import sys
import os.path
import cPickle as pickle

from markov import Markov
from auth import auth_twitter
from listener import TweetListener

def stream_tweets_from(location, limit=5000, words=None):
	"""
	@param location 	longitude&latitude ex. [-122.75,36.8,-121.75,70.8]
	@param limit    	integer
	@param words 		array of words to track
	"""

	auth = auth_twitter()

	# load ngrams
	try:
		ngrams = pickle.load( open( "ngrams.p", "rb" ) )
	except IOError:
		ngrams = dict()

	# load beginning words
	try:
		beginnings = pickle.load( open( "beginnings.p", "rb" ) )
	except IOError:
		beginnings = []

	# create markov engine
	print ngrams
	print beginnings
	markov = Markov(ngrams, beginnings)

	# start stream
	try:
		tweet_listener = TweetListener(markov)
		stream = tweepy.Stream(auth, tweet_listener)
		stream.filter(locations=location, track=words)
	except KeyboardInterrupt:
		pickle.dump( markov.two_gram_follow_probability, open( "ngrams.p", "wb" ) )
		pickle.dump( markov.beginnings, open( "beginnings.p", "wb" ) )
