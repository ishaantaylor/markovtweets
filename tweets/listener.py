import json
import tweepy
import time
import requests
import string
import random

from collections import Counter
from words.moods import moods

from markov import Markov
from MarkovWalk import MarkovWalk

# Generic Class to listen to live tweets
class TweetListener(tweepy.StreamListener):
    def __init__(self, markov):
        self.markov = markov
        self.count = 0
        self.sentimentCounts = {"pos": 0, "neg": 0, "neutral": 0}
        self.moods = moods


    def on_data(self, data):
        self.count += 1
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        twitter_handle = decoded['user']['screen_name']
        global tweet_text
        tweet_text = decoded['text'].encode('ascii', 'ignore')
        # print '@%s: %s' % (twitter_handle, tweet_text)
        # NOTE: updates mood counter
        # self.count_hashtags(tweet_text)

        self.process_tweet(tweet_text)
        
        # NOTE: only print out something every 5 tweets
        if self.count % 5 == 0:
            self.generate_tweet()
        return True


    # TODO: move this function to markov.py
    def generate_tweet(self):
        walker = MarkovWalk(self.markov.two_gram_follow_probability)
        generated_text = walker.generate(random.choice(self.markov.beginnings), 15)
        if len(generated_text.split()) > 2:
            print generated_text


    def on_error(self, status):
        print status


    def process_tweet(self, tweet_text):
        self.markov.process_two_grams(self.get_tweet_text(tweet_text))
        self.markov.process_beginning(tweet_text)


    def get_tweet_text(self, text):
        return self.get_words(text);


    def get_words(self, text):
        """
        Get words of tweet_text after sentenceify_tweet, removing hashtags and @ handles
        """
        
        text = self.sentenceify_tweet(text)
        
        # TODO: abstract operation in util function
        hashtags = [ x for x in tweet_text.split(' ') if x.startswith('#') ]
        addresses = [ x for x in tweet_text.split(' ') if x.startswith('@') ]
        return [ self.strip_punctuation(w) for w in tweet_text.split(' ') if w not in hashtags and w not in addresses and w ]


    # TODO: enhance sentencify tweet such that it modifies tweets to be as close as possible to a sentence (syntactically)
    def sentenceify_tweet(self, tweet_text):
        # parse out newlines, insert periods (?), ignore ngrams which include hashtags, @username, links
        return tweet_text.lower()
     

    # TODO: validate the ngram has viable words
    def ngram_contains_words(self, ngram):
        word1 = ngram[0]
        word2 = ngram[1]
        # extend here
        if word1.startswith('http') or word2.startswith('http'):
            return False
        elif  word1.lower().startswith("rt"):
            return False
        # elif word1 == 'extendhere':
        #     return False
        else:
            return True

    def current_time_formatted(self):
        return time.strftime("%Y%m%d-%H%M%S")

    #count hashtagged words
    def count_hashtags(self, tweet):
        words = tweet.split()
        self.counter.update(self.validate(words))

    #validate input for counter
    def validate(self, words):
        return [ self.strip_punctuation( word.lower() ) for word in words if self.valid_word( word ) ]


    def valid_word(self, word):
        return not self.valid_hashtag(word) and word in self.moods


    def strip_punctuation(self, s):
        # chris: this is faster
        return s.translate(string.maketrans("",""), string.punctuation)

    def valid_hashtag(self, word):
        return word[0] == "@" and len(word) > 0

