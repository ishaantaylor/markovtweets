import tweepy
#Gets the authorization to connect to the twitter API
def auth_twitter():
	consumer_key = 'AeW8XmXn5SWRnJk3c1rYWD0sy'
	consumer_secret = '0b3E8SA7bRrgWIHdBrSdO9MQP7UHnJH2tdTP6LF2x7F98z8dQz'

	access_token = '930631159-KCELDfC4VS8ZrkvClufEqIOMTQlW1OYCoNEqPbhV'
	access_token_secret = 'HYaOdgCfduW7ey6knQEx2VACEKc0viYkc641p0LZX8A5P'

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	return auth
