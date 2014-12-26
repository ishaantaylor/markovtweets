#twitter_aggregator.py
import tweepy

### set up twitter api
consumer_token = 'AeW8XmXn5SWRnJk3c1rYWD0sy'
consumer_secret = '0b3E8SA7bRrgWIHdBrSdO9MQP7UHnJH2tdTP6LF2x7F98z8dQz'

access_token = '930631159-KCELDfC4VS8ZrkvClufEqIOMTQlW1OYCoNEqPbhV'
access_token_secret = 'HYaOdgCfduW7ey6knQEx2VACEKc0viYkc641p0LZX8A5P'

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


###set up

def search_for(query, api):
	query = "#happy AND #sad"
	results = api.search(q=query, lang='en', rpp=100)
	data = [r.text.encode('utf8') for r in results]

	for tweet_text in data:
	    print tweet_text

def count_hashtags(results):
	



