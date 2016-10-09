import tweepy
import os.path

from auth import auth_twitter
from listener import TweetListener

def stream_tweets_from(location, markov, limit=5000, words=None):
	"""
	@param location 	longitude&latitude ex. [-122.75,36.8,-121.75,70.8]
	@param limit    	integer
	@param words 		array of words to track
	"""

	auth = auth_twitter()

	# start stream
	tweet_listener = TweetListener(markov)
	stream = tweepy.Stream(auth, tweet_listener)
	stream.filter(locations=location, track=words)
	
