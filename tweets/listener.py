import json
import tweepy
import time
import requests
import string

from collections import Counter
from words.moods import moods

# Generic Class to listen to live tweets
class TweetListener(tweepy.StreamListener):
    def __init__(self):
        self.counter = Counter()
        self.two_gram_count = Counter()
        self.two_gram_follow = dict()
        self.two_gram_follow_probability = dict()

        self.count = 0
        self.sentimentCounts = {"pos": 0, "neg": 0, "neutral": 0}
        self.moods = moods


    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

       	f = open("runs/" + self.current_time_formatted() + ".txt", 'a')	


        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        twitter_handle = decoded['user']['screen_name']
        tweet_text = decoded['text'].encode('ascii', 'ignore')
        self.count_hashtags(tweet_text)
        self.process_two_grams(tweet_text)
        
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


    # TODO: modify tweets to be as close as possible to a sentence (syntactically)
    def sentenceify_tweet(self, tweet_text):
        # parse out newlines, insert periods (?), ignore ngrams which include hashtags, @username, links
        return tweet_text.lower()
    

    # TODO: move functions below to wordutil.py as _
    # TODO: eventually modify this to process all ngrams from n = 2 .. m
    def process_two_grams(self, tweet_text):
        tweet_text = self.sentenceify_tweet(tweet_text)
        print tweet_text

        # TODO: abstract operation in util function
        hashtags = [ x for x in tweet_text.split(' ') if x.startswith('#') ]
        addresses = [ x for x in tweet_text.split(' ') if x.startswith('@') ]

        words = [ self.strip_punctuation(w) for w in tweet_text.split(' ') if w not in hashtags and w not in addresses and w ]

        print words

        # Do I need to count this?
        # self.two_gram_count.update([ tuple([words[i],words[i+1]]) \
        #     for i in xrange(len(words) - 1) \
        #     if self.ngram_contains_words(words[i],words[i+1]) \
        # ])

        for i in xrange(len(words) - 2):
            two_gram = tuple([words[i],words[i+1]])
            if not self.two_gram_follow.has_key(two_gram):
                self.two_gram_follow[two_gram] = []

            # self.two_gram_follow[two_gram] = self.two_gram_follow[two_gram].append(words[i+2])
            self.upsert_follow_probability_count(two_gram, words[i+2])

        print self.two_gram_follow_probability



    def upsert_follow_probability_count(self, n_gram, follow_word):
        """ self.two_gram_follow_probability example (to illustrate structure)
        {
            tuple1: {
                probabilities : {
                    word1: 0.4,
                    word2: 0.6
                },
                count : 3
            },
            tuple2: {
                probabilities : {
                    word4: 0.2,
                    word3: 0.3,
                    word5: 0.5
                },
                count : 8
            },
            ...
        }
        """
        # TODO: better verify what we're counting (ngram_contains_words)
        if not self.ngram_contains_words(n_gram):
            return None
        elif not self.two_gram_follow_probability.has_key(n_gram):
            # initialize tuple obj
            self.two_gram_follow_probability[n_gram] = dict()
            self.two_gram_follow_probability[n_gram]["count"] = 1
            self.two_gram_follow_probability[n_gram]["probabilities"] = dict()
            self.two_gram_follow_probability[n_gram]["probabilities"][follow_word] = 1
        else:
            probability_obj = self.two_gram_follow_probability[n_gram]
            self.two_gram_follow_probability[n_gram]["probabilities"] = self.new_probabilities(probability_obj["count"], probability_obj["probabilities"], follow_word)
            self.two_gram_follow_probability[n_gram]["count"] = probability_obj["count"] + 1


    # calculate probabilities_dict for current state + new_word
    def new_probabilities(self, count, probabilities_dict, new_word):
        new_count = count + 1

        # for each word, update probability with new_count 
        for k,v in probabilities_dict.iteritems():
            # is_new_word handles case new_word exists in probabilities_dict + makes vals float
            is_new_word = 1. if new_word == k else 0.
            probabilities_dict[k] = ((count * v) + is_new_word) / new_count

        # if word does not exist, initialize it
        if not probabilities_dict.has_key(new_word):
            probabilities_dict[new_word] = 1. / new_count

        return probabilities_dict

        

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


    # TODO: validate the 2gram is a viable word
    def ngram_contains_words(self, ngram):
        return True
        # if word1.startswith('http') or word2.startswith('http'):
            # return False
        # elif word1 == 'extendhere':
        #     return False
        # else:
        #     return True

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

