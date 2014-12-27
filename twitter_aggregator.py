#twitter_aggregator.py
import tweepy
import json
from collections import defaultdict
from collections import Counter
import pprint
import requests

pos = 0
neg = 0
neutral = 0

#Gets the authorization to connect to the twitter API
def getAuthorizationToAPI():
	consumer_key = 'AeW8XmXn5SWRnJk3c1rYWD0sy'
	consumer_secret = '0b3E8SA7bRrgWIHdBrSdO9MQP7UHnJH2tdTP6LF2x7F98z8dQz'

	access_token = '930631159-KCELDfC4VS8ZrkvClufEqIOMTQlW1OYCoNEqPbhV'
	access_token_secret = 'HYaOdgCfduW7ey6knQEx2VACEKc0viYkc641p0LZX8A5P'

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	return auth


def printSentiment(text):
	payload = {'text':text}
	url = 'http://text-processing.com/api/sentiment/'
	r = requests.post(url, data=payload)

	try:
		json = r.json()
		if (json['label'] == 'pos'): 
			global pos 
			pos = pos + 1
		elif (json['label'] == 'neg'): 
			global neg
			neg = neg + 1
		elif (json['label'] == 'neutral'): 
			global neutral
			neutral = neutral + 1

		total = pos + neg + neutral
		print 'Pos: %.2f | Neg: %.2f | Neutral: %.2f   || Total: %s' % (pos / float(total), neg / float(total), neutral / float(total), total)
	except:
		pass


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
        printSentiment(tweet_text)
        print counter
        print ''
        
        return True

    def on_error(self, status):
        print status


def stream_tweets_from(location):
	auth = getAuthorizationToAPI()
	stream = tweepy.Stream(auth, TweetListener())
	stream.filter(locations=location)

def main():
	SanFrancisco = [-122.75,36.8,-121.75,70.8]
	stream_tweets_from(SanFrancisco)


###set up datastore
d = defaultdict(int)
counter = Counter()


#count hashtagged words
def count_hashtags(tweet):
	words = tweet.split()
	counter.update(validate(words))


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
	moods = [ #'love',

			'angry', 'aggravated', 'agitated', 'annoyed', 'anxious', 'appreciative', 'ashamed', 'awe', 'awful', 'amazed', 'amused', 'animosity', 'apprehensive', 'astonished', 'attracted', 'aroused', 'apathetic',
			'bitter', 'banal', 'blissful', 'bubbly', 'bittersweet', 'betrayed', 'bewildered', 'bored', 
			'callous', 'cozy', 'combative', 'conflicted', 'confused', 'content', 'curious', 'cautious', 'comfortable', 'concerned', 'contempt', 'cranky', 'cynical', 
			'depressed', 'disgusted', 'disturbed', 'driven', 'dynamic', 'discontented', 'devastated', 'disappointed', 'discouraged', 'disheartened', 'distracted', 'distresed', 'dejected', 'delighted', 'delirious',
			'elated', 'enraged', 'enthused', 'envious', 'excited', 'exhausted', 'enthusiastic', 'enchanted', 'emptiness', 'embarassed', 'ecstatic', 'eager',
			'fearful', 'frustrated', 'furious', 'foolish', 'flabbergasted', 'fascinated', 
			'gentle', 'grateful', 'greedy', 'gratified', 'gleeful', 'gloomy', ''
			'hate', 'hatred', 'honest', 'hopeful', 'hostile', 'happy',
			'ignored', 'impartial', 'impulsive', 'inquisitive', 'inspired', 'intolerant', 'irritated', 
			'jealous', 'joyful', 'jubilant', 'jaded', 

			'lonely', 'lovely', 'lustful', 'lust', 'loathe', 'loved',
			'mad', 'malicious', 'meek', 'motivated', 'merry', 'miserable',
			'nasty', 'naughty', 'negative', 'nervious', 'needy', 
			'obnoxious', 'obstinate', 'optimistic', 'ouraged', 'offeded', 'obsessed', 
			'painful', 'patient', 'perky', 'perturbed', 'pessimistic', 'pitiful', 'positive', 'proud', 'playful', 'pleased', 'pleasureful', 'puzzled', 'passionate',
			'quirky', 
			'rageful', 'raw', 'relaxed', 'relieved', 'repulsed', 'resentment', 'rude',
			'sad', 'satisfied', 'scornful', 'sensitive', 'sentimental', 'shameful', 'sorrow', 'spiteful', 'stubborn', 'surprised', 'shy', 'sheepish', 'sexy', 'sensitive', 'sensual', 'scared', 
			'tempted', 'tense', 'terrified', 'thinking', 'tired', 'troubled', 'thrilled', 'tranquil', 'trusting', 'tormented',
			'uncertain', 'unhappy', 'upset', 'uneasy', 'uncertain',
			'volatile', 'violent', 'vindictive', 'vociferous', 'vengeful', 'vicious', 
			'weary', 'worried', 'wrath', 'worn-out', 'warm'
			''
			'youthful', 'yearn'
			'zealous', 'zesty'
			]
	for word in words:
		if word != "" and word in moods:
			new_words.append(word)
	
	return new_words

# find occurences
# returns indices of character in string
def findOccurences(string, character):
    return [i for i, letter in enumerate(string) if letter == character]

def makeLowercase(word):
	return word.lower()


def main():
	SanFrancisco = [-122.75,36.8,-121.75,37.8]
	streamTweetsFromLocation(SanFrancisco)



if __name__ == "__main__":
	main()
