import tweepy
from auth import auth_twitter
from listener import TweetListener

def stream_tweets_from(location, limit=5000, words=None):
	"""
	@param location 	longitude&latitude ex. [-122.75,36.8,-121.75,70.8]
	@param limit    	integer
	@param words 		array of words to track
	"""

	auth = auth_twitter()
	stream = tweepy.Stream(auth, TweetListener())
	stream.filter(locations=location, track=words)
