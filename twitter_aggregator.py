#twitter_aggregator.py
import tweepy
import json

#Gets the authorization to connect to the twitter API
def getAuthorizationToAPI():
	consumer_key = 'AeW8XmXn5SWRnJk3c1rYWD0sy'
	consumer_secret = '0b3E8SA7bRrgWIHdBrSdO9MQP7UHnJH2tdTP6LF2x7F98z8dQz'

	access_token = '930631159-KCELDfC4VS8ZrkvClufEqIOMTQlW1OYCoNEqPbhV'
	access_token_secret = 'HYaOdgCfduW7ey6knQEx2VACEKc0viYkc641p0LZX8A5P'

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	return auth


#Generic Class to listen to live tweets
class TweetListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        twitter_handle = decoded['user']['screen_name']
        tweet_text = decoded['text'].encode('ascii', 'ignore')
        print '@%s: %s' % (twitter_handle, tweet_text)
        print ''
        return True

    def on_error(self, status):
        print status


def streamTweetsFromLocation(location):
	auth = getAuthorizationToAPI()
	stream = tweepy.Stream(auth, TweetListener())
	stream.filter(locations=location)


def main():
	SanFrancisco = [-122.75,36.8,-121.75,37.8]
	streamTweetsFromLocation(SanFrancisco)



###set up

def search_for(query, api):
	results = api.search(q=query, lang='en', rpp=100)
	data = [r.text.encode('utf8') for r in results]

	for tweet_text in data:
	    print tweet_text


if __name__ == "__main__":
    main()