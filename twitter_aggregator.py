#twitter_aggregator.py
import re
import json
from collections import defaultdict
from collections import Counter
import pprint
import requests
import time
import string
from words.moods import moods
from tweets.stream import stream_tweets_from

LOCATION = [-122.75,36.8,-121.75,70.8] # San Francisco
# CURRENTTIME

counts = {"pos": 0, "neg": 0, "neutral": 0}

pos = 0
neg = 0
neutral = 0
tweetCount = 0

counter = Counter()

# class SentimentCounter():
# 	def __init__(self):
		

def printSentiment(text):
	payload = {'text':text}
	url = 'http://text-processing.com/api/sentiment/'
	r = requests.post(url, data=payload)

	try:
		global counts
		json = r.json()
		counts[json['label']] = counts[json['label']] + 1

		total = counts['pos'] + counts['neg'] + counts['neutral']
		prints = 'Pos: %.2f | Neg: %.2f | Neutral: %.2f   || Total: %s' % (pos / float(total), neg / float(total), neutral / float(total), total)
		print prints
		f.write(str(prints + "\n"))
	except:
		print "Error"
		pass

#validate input for counter
def validate(words):
	return [ strip_punctuation( word.lower() ) for word in words if valid_word( word ) ]


#count hashtagged words
def count_hashtags(tweet):
	words = tweet.split()
	counter.update(validate(words))


def strip_punctuation(s):
	return ''.join(c for c in s if c not in string.punctuation)

def valid_hashtag(word):
	return word[0] == "@" and len(word) > 0

def valid_word(word):
	return not valid_hashtag(word) and word in moods


def current_time_formatted():
	return time.strftime("%Y%m%d-%H%M%S")

def main():
	# file that the data is written to
	stream_tweets_from(LOCATION)
	print(validate("angry ANGRY?!?!?!?... angry yea yea yea yea bad bad banal banal".split(' ')))

if __name__ == "__main__":
	main()
