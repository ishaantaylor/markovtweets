import json
import tweepy
import time
import requests
import string

from collections import Counter


#Generic Class to listen to live tweets
class TweetListener(tweepy.StreamListener):
    def __init__(self):
        self.counter = Counter()
        self.count = 0
        self.sentimentCounts = {"pos": 0, "neg": 0, "neutral": 0}
        self.moods = [
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
            'youthful', 'yearn'
            'zealous', 'zesty'
        ]


    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

       	f = open("runs/" + self.current_time_formatted() + ".txt", 'a')	


        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        twitter_handle = decoded['user']['screen_name']
        tweet_text = decoded['text'].encode('ascii', 'ignore')
        self.count_hashtags(tweet_text)
        
        print '@%s: %s' % (twitter_handle, tweet_text)
        f.write(str('@%s: %s' % (twitter_handle, tweet_text) + "\n"))

        # makes call to sentiment API
        # self.printSentiment(tweet_text)
        # f.write()

        print self.counter
        for k,v in  self.counter.most_common():
        	print("('{}':{})".format(k,v)),
        	f.write(str("('{}':{}) ".format(k,v)))

        print '\n'
        f.write(str('\n\n'))


        return True

    def on_error(self, status):
        print status

    def printSentiment(self, text):
        payload = {'text':text}
        url = 'http://text-processing.com/api/sentiment/'
        r = requests.post(url, data=payload)

        try:
            json = r.json()
            self.sentimentCounts[json['label']] = self.sentimentCounts[json['label']] + 1

            total = self.sentimentCounts['pos'] + self.sentimentCounts['neg'] + self.sentimentCounts['neutral']
            prints = 'Pos: %.2f | Neg: %.2f | Neutral: %.2f   || Total: %s' % (pos / float(total), neg / float(total), neutral / float(total), total)
            print prints
            f.write(str(prints + "\n"))
        except:
            print "Error"
            pass



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
        return ''.join(c for c in s if c not in string.punctuation)

    def valid_hashtag(self, word):
        return word[0] == "@" and len(word) > 0

