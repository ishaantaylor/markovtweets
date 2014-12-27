#twitter_aggregator.py
import tweepy
import json
from collections import defaultdict
from collections import Counter
import pprint

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
        count_hashtags(tweet_text)
        print '@%s: %s' % (twitter_handle, tweet_text)
        print counter
        return True

    def on_error(self, status):
        print status


def streamTweetsFromLocation(location):
	auth = getAuthorizationToAPI()
	stream = tweepy.Stream(auth, TweetListener())
	stream.filter(locations=location)




###set up datastore
d = defaultdict(int)
counter = Counter()

"""
def search_for(query, api):
	results = api.search(q=query, lang='en', rpp=100)
	data = [r.text.encode('utf8') for r in results]

	for tweet_text in data:
	    # print tweet_text
	    count_hashtags(tweet_text)

	print counter


# prepend hashtag
def pp_ht(array_of_words):
	for i in xrange(0, len(array_of_words)):
		array_of_words[i] = '#' + array_of_words[i];
	return array_of_words
"""

#count hashtagged words
def count_hashtags(tweet):
	words = tweet.split()

	#make words valid
	counter.update(validate(words))


"""
def isValid(word):
	return isHashtag(word)

def isHashtag(word):
	if (len(word) > 1):
		return word[0] == '#'
	return false
"""

#validate input for counter
def validate(words):
	things_to_strip = [".", ",", "?", ")", "(", ":", ";", "'", "'s", "!", "#", "$", "&"]
	for i in xrange(0, len(words)):
		temp = words[i]

		# remove all punctuation
		for j in xrange(0, len(things_to_strip)):
			# if punctuation exists
			if things_to_strip[j] in temp:

				# remove all occurances of each punctuation
				indices = findOccurences(temp, things_to_strip[j])
				for index in indices:
					newstr = temp[:index] + temp[index+1:]
					temp = newstr

		# remove  all @twitter_handles
		if len(temp) > 0 and temp[0] == "@":
			temp = ""

		# make word lowercase
		temp = makeLowercase(temp)

		# any other operations eg. remove punctuation

		words[i] = temp

	# remove unwanted words
	new_words = []
	moods = ['happy', 'sad', 'excited', 'angry', 'confused', 'love', 'hate', 'bored', 'tired', 'drunk']
	for word in words:
		if word != "" and word in moods:
			new_words.append(word)
	
	return new_words

#find occurences
def findOccurences(string, character):
    return [i for i, letter in enumerate(string) if letter == character]

def makeLowercase(word):
	return word.lower()


def main():
	SanFrancisco = [-122.75,36.8,-121.75,37.8]
	streamTweetsFromLocation(SanFrancisco)



if __name__ == "__main__":
	main()
