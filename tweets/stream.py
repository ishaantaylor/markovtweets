import tweepy
import json
import os.path
import cPickle as pickle

from auth import auth_twitter
from listener import TweetListener

def stream_tweets_from(location, limit=5000, words=None):
	"""
	@param location 	longitude&latitude ex. [-122.75,36.8,-121.75,70.8]
	@param limit    	integer
	@param words 		array of words to track
	"""

	auth = auth_twitter()

	try:
		ngrams = pickle.load( open( "ngrams.p", "rb" ) )
		print 'ngrams',
		print ngrams
	except IOError:
		ngrams = dict()

	try:
		tweet_listener = TweetListener(ngrams)
		stream = tweepy.Stream(auth, tweet_listener)
		stream.filter(locations=location, track=words)
	except KeyboardInterrupt:
		print tweet_listener.two_gram_follow_probability
		pickle.dump( tweet_listener.two_gram_follow_probability, open( "ngrams.p", "wb" ) )
