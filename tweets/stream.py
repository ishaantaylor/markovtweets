import tweepy
from auth import auth_twitter
from listener import TweetListener

def stream_tweets_from(location):
	auth = auth_twitter()
	stream = tweepy.Stream(auth, TweetListener())
	stream.filter(locations=location)
